"""Reglas de negocio de compras (RF08) y RN02: cada compra suma al stock y actualiza el costo de los insumos."""
# datetime: fecha y hora
from datetime import datetime
# Decimal: números exactos para dinero y cantidades
from decimal import Decimal

# Session: sesión de trabajo con MySQL
from sqlalchemy.orm import Session

# Fechas en hora de Colombia y redondeos
from app.core.jb_utilidades import jb_ahora, jb_cantidad, jb_dinero, jb_hora_colombia
# Modelos de las tablas
from app.models.jb_modelos import JbCompra, JbDetalleCompra, JbInsumo, JbProveedor
# Consultas a insumos y proveedores
from app.repositories import jb_insumo_repository, jb_proveedor_repository
# Consultas a compras
from app.repositories import jb_compra_repository as jb_repositorio
# Errores comunes
from app.services.jb_comun import jb_conflicto, jb_dato_invalido, jb_no_encontrado


# Lista todas las compras
def jb_listar(jb_sesion: Session) -> list[JbCompra]:
    # Pide la lista al repositorio
    return jb_repositorio.jb_listar(jb_sesion)


# Busca una compra o responde 404
def jb_obtener(jb_sesion: Session, jb_id: int) -> JbCompra:
    # Busca por id
    jb_compra = jb_repositorio.jb_buscar(jb_sesion, jb_id)
    # Si no existe...
    if jb_compra is None:
        # ...responde 404
        raise jb_no_encontrado(f"La compra {jb_id}")
    # Devuelve la compra
    return jb_compra


# Comprueba que el proveedor exista y esté ACTIVO
def jb_validar_proveedor(jb_sesion: Session, jb_id_proveedor: int) -> JbProveedor:
    # Busca el proveedor
    jb_proveedor = jb_proveedor_repository.jb_buscar(jb_sesion, jb_id_proveedor)
    # Si no existe...
    if jb_proveedor is None:
        # ...responde 400 (equivale a fallar la llave foránea)
        raise jb_dato_invalido(f"El proveedor {jb_id_proveedor} no existe")
    # Si está INACTIVO...
    if jb_proveedor.estado != "ACTIVO":
        # ...responde 400
        raise jb_dato_invalido(f"El proveedor '{jb_proveedor.razon_social}' está INACTIVO: no se le pueden registrar compras")
    # Devuelve el proveedor
    return jb_proveedor


# Revisa la fecha de la compra
def jb_validar_fecha(jb_fecha: datetime | None) -> datetime:
    """Si no se envía fecha se usa la hora actual de Colombia. Una compra no puede estar en el futuro."""
    # Sin fecha: ahora
    if jb_fecha is None:
        # Devuelve la hora actual de Colombia
        return jb_ahora()
    # Pasa la fecha a hora de Colombia (por si llegó con otra zona horaria)
    jb_fecha = jb_hora_colombia(jb_fecha)
    # Si es posterior a este momento...
    if jb_fecha > jb_ahora():
        # ...responde 400
        raise jb_dato_invalido("La fecha de la compra no puede estar en el futuro")
    # Devuelve la fecha revisada
    return jb_fecha


# Busca y bloquea los insumos de una compra; todos deben existir
def jb_bloquear_insumos(jb_sesion: Session, jb_ids: list[int]) -> dict[int, JbInsumo]:
    # SELECT ... FOR UPDATE de los insumos: nadie más cambia su stock mientras esta compra no termine
    jb_insumos = jb_insumo_repository.jb_buscar_varios_para_actualizar(jb_sesion, jb_ids)
    # Ids que no se encontraron
    jb_faltantes = [str(jb_id) for jb_id in jb_ids if jb_id not in jb_insumos]
    # Si falta alguno...
    if jb_faltantes:
        # ...responde 400
        raise jb_dato_invalido(f"Estos insumos no existen: {', '.join(jb_faltantes)}")
    # Devuelve el diccionario {id_insumo: insumo}
    return jb_insumos


# Registra una compra (RN02)
def jb_crear(jb_sesion: Session, jb_datos: dict, jb_id_usuario: int) -> JbCompra:
    """La API calcula subtotales y total. RN02: suma la cantidad al stock de cada insumo y
    deja como costo_unitario el de esta compra. Todo en una sola transacción: o se guarda todo o nada."""
    # Comprueba el proveedor (400 si no existe o está INACTIVO)
    jb_proveedor = jb_validar_proveedor(jb_sesion, jb_datos["id_proveedor"])
    # Fecha de la compra (ahora si no se envió)
    jb_fecha = jb_validar_fecha(jb_datos.get("fecha_compra"))
    # Busca y bloquea los insumos comprados
    jb_insumos = jb_bloquear_insumos(jb_sesion, [jb_item["id_insumo"] for jb_item in jb_datos["detalle"]])
    # Nombres de los insumos INACTIVOS
    jb_inactivos = [jb_insumo.nombre for jb_insumo in jb_insumos.values() if jb_insumo.estado != "ACTIVO"]
    # Si hay alguno...
    if jb_inactivos:
        # ...responde 400
        raise jb_dato_invalido(f"Estos insumos están INACTIVOS y no se pueden comprar: {', '.join(jb_inactivos)}")
    # Arma la compra; el usuario que registra viene del token
    jb_compra = JbCompra(
        # Número de factura
        numero_factura=jb_datos["numero_factura"],
        # Fecha y hora
        fecha_compra=jb_fecha,
        # Proveedor
        proveedor=jb_proveedor,
        # Usuario que registra
        id_usuario=jb_id_usuario,
    )
    # El total empieza en 0
    jb_total = Decimal("0")
    # Recorre cada ítem enviado
    for jb_item in jb_datos["detalle"]:
        # Insumo del ítem
        jb_insumo = jb_insumos[jb_item["id_insumo"]]
        # Subtotal = cantidad x costo_unitario, redondeado a 2 decimales
        jb_subtotal = jb_dinero(jb_item["cantidad"] * jb_item["costo_unitario"])
        # Agrega el ítem a la compra
        jb_compra.detalle.append(JbDetalleCompra(
            # Insumo comprado
            insumo=jb_insumo,
            # Cantidad
            cantidad=jb_item["cantidad"],
            # Costo por unidad
            costo_unitario=jb_item["costo_unitario"],
            # Subtotal calculado por la API
            subtotal=jb_subtotal,
        ))
        # Suma el subtotal al total
        jb_total += jb_subtotal
        # RN02: el stock sube con lo comprado
        jb_insumo.stock_actual = jb_cantidad(jb_insumo.stock_actual + jb_item["cantidad"])
        # RN02: el costo del insumo pasa a ser el de esta compra (la más reciente)
        jb_insumo.costo_unitario = jb_item["costo_unitario"]
    # Total de la compra
    jb_compra.total = jb_dinero(jb_total)
    # Inserta la compra con sus ítems y guarda los cambios de los insumos (409 si la factura se repite)
    jb_repositorio.jb_guardar(jb_sesion, jb_compra)
    # Confirma todo junto
    jb_sesion.commit()
    # Devuelve la compra registrada
    return jb_compra


# Modifica los datos generales de una compra
def jb_actualizar(jb_sesion: Session, jb_id: int, jb_datos: dict) -> JbCompra:
    """Solo cambia factura, fecha y proveedor. El detalle no se cambia porque ya movió el inventario (RN02):
    si una compra quedó mal, se elimina y se registra de nuevo."""
    # Busca la compra y la bloquea
    jb_compra = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_compra is None:
        # ...responde 404
        raise jb_no_encontrado(f"La compra {jb_id}")
    # Si cambia de proveedor, el nuevo debe existir y estar ACTIVO
    if jb_datos["id_proveedor"] != jb_compra.id_proveedor:
        # Asigna el nuevo proveedor
        jb_compra.proveedor = jb_validar_proveedor(jb_sesion, jb_datos["id_proveedor"])
    # Cambia el número de factura
    jb_compra.numero_factura = jb_datos["numero_factura"]
    # Cambia la fecha (no puede estar en el futuro)
    jb_compra.fecha_compra = jb_validar_fecha(jb_datos["fecha_compra"])
    # Envía el cambio (409 si ese proveedor ya tiene otra compra con esa factura)
    jb_repositorio.jb_guardar(jb_sesion, jb_compra)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve la compra modificada
    return jb_compra


# Elimina una compra y devuelve el inventario
def jb_eliminar(jb_sesion: Session, jb_id: int) -> dict:
    """Resta del stock lo que la compra había sumado. Si parte de lo comprado ya se usó
    (el stock quedaría negativo), responde 409 y no cambia nada."""
    # Busca la compra y la bloquea
    jb_compra = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_compra is None:
        # ...responde 404
        raise jb_no_encontrado(f"La compra {jb_id}")
    # Busca y bloquea los insumos de la compra
    jb_insumos = jb_bloquear_insumos(jb_sesion, [jb_item.id_insumo for jb_item in jb_compra.detalle])
    # Aquí se anotan los insumos que quedarían negativos
    jb_faltantes = []
    # Recorre cada ítem de la compra
    for jb_item in jb_compra.detalle:
        # Insumo del ítem
        jb_insumo = jb_insumos[jb_item.id_insumo]
        # Si hoy hay menos de lo que se compró...
        if jb_insumo.stock_actual < jb_item.cantidad:
            # ...se anota el problema
            jb_faltantes.append(f"{jb_insumo.nombre}: la compra sumó {jb_item.cantidad} y hoy hay {jb_insumo.stock_actual}")
    # Si algún stock quedaría negativo...
    if jb_faltantes:
        # ...responde 409 sin cambiar nada
        raise jb_conflicto("No se puede eliminar la compra: parte de lo comprado ya se usó. " + "; ".join(jb_faltantes))
    # Recorre de nuevo los ítems
    for jb_item in jb_compra.detalle:
        # Resta del stock lo que la compra había sumado
        jb_insumos[jb_item.id_insumo].stock_actual = jb_cantidad(jb_insumos[jb_item.id_insumo].stock_actual - jb_item.cantidad)
    # Borra la compra (sus ítems se borran en cascada)
    jb_repositorio.jb_borrar(jb_sesion, jb_compra)
    # Confirma todo junto
    jb_sesion.commit()
    # Responde borrado físico
    return {"mensaje": f"La compra {jb_id} se eliminó y su cantidad se restó del inventario", "tipo_borrado": "FISICO"}
