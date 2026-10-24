"""Reglas de negocio de compras de insumos (RF08, RN02).

RN02: al registrar una compra se suma la cantidad al stock_actual de cada insumo y se
actualiza su costo_unitario. Si la compra se modifica o se elimina, el inventario se ajusta.
"""
# defaultdict: diccionario que da un valor inicial a las claves nuevas (aquí, Decimal 0)
from collections import defaultdict
# Decimal: números exactos para cantidades y dinero
from decimal import Decimal

# Funciones de apoyo: hora actual, redondeo de cantidades y de dinero, y conversión a hora de Colombia
from app.core.jb_utilidades import jb_ahora, jb_cantidad, jb_dinero, jb_hora_colombia
# Acceso a compras
from app.repositories.jb_compra_repository import jb_compra_repository
# Acceso a insumos (inventario)
from app.repositories.jb_insumo_repository import jb_insumo_repository
# Acceso a proveedores
from app.repositories.jb_proveedor_repository import jb_proveedor_repository
# Respuestas y errores comunes
from app.services.jb_comun import jb_borrado_fisico, jb_conflicto, jb_dato_invalido, jb_no_encontrado


# Lista todas las compras
def jb_listar() -> list[dict]:
    # Pide la lista al repositorio
    return jb_compra_repository.jb_listar()


# Busca una compra o responde 404
def jb_obtener(jb_id: int) -> dict:
    # Busca por id
    jb_compra = jb_compra_repository.jb_buscar_por_id(jb_id)
    # Si no existe...
    if jb_compra is None:
        # ...responde 404
        raise jb_no_encontrado(f"La compra {jb_id}")
    # Devuelve la compra
    return jb_compra


# Comprueba que el proveedor exista y esté ACTIVO
def jb_validar_proveedor(jb_id_proveedor: int) -> None:
    # Busca el proveedor
    jb_proveedor = jb_proveedor_repository.jb_buscar_por_id(jb_id_proveedor)
    # Si no existe...
    if jb_proveedor is None:
        # ...responde 400 (equivale a fallar una llave foránea)
        raise jb_dato_invalido(f"El proveedor {jb_id_proveedor} no existe")
    # Si está INACTIVO...
    if jb_proveedor["estado"] != "ACTIVO":
        # ...responde 400
        raise jb_dato_invalido(f"El proveedor '{jb_proveedor['razon_social']}' está INACTIVO")


# Valida los ítems y calcula subtotales y total
def jb_preparar_detalle(jb_items: list[dict]) -> tuple[list[dict], Decimal]:
    """Valida los insumos y calcula subtotal = cantidad x costo_unitario y el total."""
    # Lista de ítems preparados y total que empieza en 0
    jb_detalle, jb_total = [], Decimal("0")
    # Recorre cada ítem enviado
    for jb_item in jb_items:
        # Busca el insumo
        jb_insumo = jb_insumo_repository.jb_buscar_por_id(jb_item["id_insumo"])
        # Si no existe...
        if jb_insumo is None:
            # ...responde 400
            raise jb_dato_invalido(f"El insumo {jb_item['id_insumo']} no existe")
        # Si está INACTIVO...
        if jb_insumo["estado"] != "ACTIVO":
            # ...responde 400
            raise jb_dato_invalido(f"El insumo '{jb_insumo['nombre']}' está INACTIVO")
        # Subtotal = cantidad x costo unitario, redondeado a 2 decimales
        jb_subtotal = jb_dinero(jb_item["cantidad"] * jb_item["costo_unitario"])
        # Agrega el ítem con el formato que se guarda en MongoDB
        jb_detalle.append({
            # Insumo comprado
            "id_insumo": jb_item["id_insumo"],
            # Cantidad con 3 decimales
            "cantidad": jb_cantidad(jb_item["cantidad"]),
            # Costo unitario con 2 decimales
            "costo_unitario": jb_dinero(jb_item["costo_unitario"]),
            # Subtotal calculado
            "subtotal": jb_subtotal,
        })
        # Suma el subtotal al total
        jb_total += jb_subtotal
    # Devuelve el detalle y el total redondeado
    return jb_detalle, jb_dinero(jb_total)


# Suma las cantidades de cada insumo del detalle (por si un insumo aparece en varias líneas)
def jb_cantidades_por_insumo(jb_detalle: list[dict]) -> dict[int, Decimal]:
    # Diccionario {id_insumo: cantidad}; cada insumo nuevo empieza en 0
    jb_cantidades = defaultdict(lambda: Decimal("0"))
    # Recorre cada línea
    for jb_item in jb_detalle:
        # Suma la cantidad de la línea a su insumo
        jb_cantidades[jb_item["id_insumo"]] += jb_item["cantidad"]
    # Devuelve las cantidades por insumo
    return jb_cantidades


# Revisa que restar inventario no deje ningún insumo en negativo
def jb_verificar_salidas(jb_cambios: dict[int, Decimal]) -> None:
    """Antes de restar inventario comprueba que ningún insumo quede con stock negativo."""
    # Lista de insumos que no alcanzan
    jb_faltantes = []
    # Recorre cada insumo y su cambio (positivo = sumar, negativo = restar)
    for jb_id_insumo, jb_cambio in jb_cambios.items():
        # Si el cambio suma (o no cambia), no hay riesgo
        if jb_cambio >= 0:
            # Pasa al siguiente insumo
            continue
        # Busca el insumo para ver su stock actual
        jb_insumo = jb_insumo_repository.jb_buscar_por_id(jb_id_insumo)
        # Si al restar quedaría negativo...
        if jb_insumo is not None and jb_insumo["stock_actual"] + jb_cambio < 0:
            # ...se anota en la lista de faltantes
            jb_faltantes.append(f"{jb_insumo['nombre']} (hay {jb_insumo['stock_actual']}, se deben retirar {-jb_cambio})")
    # Si hubo faltantes...
    if jb_faltantes:
        # ...responde 409 sin tocar el inventario
        raise jb_conflicto(
            # Mensaje con todos los faltantes separados por punto y coma
            "No se puede ajustar la compra porque parte de los insumos ya se consumió: " + "; ".join(jb_faltantes)
        )


# Registra una compra nueva
def jb_crear(jb_datos: dict, jb_id_usuario: int) -> dict:
    # Comprueba el proveedor
    jb_validar_proveedor(jb_datos["id_proveedor"])
    # Valida los insumos y calcula subtotales y total
    jb_detalle, jb_total = jb_preparar_detalle(jb_datos["detalle"])
    # Fecha enviada (puede no venir)
    jb_fecha = jb_datos.get("fecha_compra")
    # Inserta la compra
    jb_compra = jb_compra_repository.jb_insertar({
        # Número de factura
        "numero_factura": jb_datos["numero_factura"],
        # La fecha enviada pasada a hora de Colombia, o la hora actual si no se envió
        "fecha_compra": jb_hora_colombia(jb_fecha) if jb_fecha else jb_ahora(),
        # Proveedor
        "id_proveedor": jb_datos["id_proveedor"],
        # Usuario que registra (viene del token)
        "id_usuario": jb_id_usuario,
        # Total calculado
        "total": jb_total,
        # Detalle preparado
        "detalle": jb_detalle,
    })
    # RN02: por cada ítem, suma la cantidad al inventario y actualiza el costo unitario
    for jb_item in jb_detalle:
        # Entrada de inventario del insumo
        jb_insumo_repository.jb_registrar_entrada(jb_item["id_insumo"], jb_item["cantidad"], jb_item["costo_unitario"])
    # Devuelve la compra registrada
    return jb_compra


# Modifica una compra
def jb_actualizar(jb_id: int, jb_datos: dict) -> dict:
    """Reemplaza la compra completa y ajusta el inventario con la diferencia entre el detalle nuevo y el anterior."""
    # Busca la compra actual (404 si no existe)
    jb_compra = jb_obtener(jb_id)
    # Comprueba el proveedor
    jb_validar_proveedor(jb_datos["id_proveedor"])
    # Valida los insumos nuevos y calcula subtotales y total
    jb_detalle, jb_total = jb_preparar_detalle(jb_datos["detalle"])

    # Cantidades por insumo del detalle nuevo
    jb_nuevas = jb_cantidades_por_insumo(jb_detalle)
    # Cantidades por insumo del detalle anterior
    jb_anteriores = jb_cantidades_por_insumo(jb_compra["detalle"])
    # Diferencia por insumo (nuevo - anterior) para todos los insumos que aparecen en cualquiera de los dos
    jb_cambios = {jb_id_insumo: jb_nuevas[jb_id_insumo] - jb_anteriores[jb_id_insumo] for jb_id_insumo in {*jb_nuevas, *jb_anteriores}}
    # Si alguna diferencia resta más de lo que hay, responde 409
    jb_verificar_salidas(jb_cambios)

    # Fecha enviada (puede no venir)
    jb_fecha = jb_datos.get("fecha_compra")
    # Guarda la compra modificada
    jb_actualizada = jb_compra_repository.jb_actualizar(jb_id, {
        # Número de factura
        "numero_factura": jb_datos["numero_factura"],
        # La fecha enviada, o la que ya tenía la compra
        "fecha_compra": jb_hora_colombia(jb_fecha) if jb_fecha else jb_compra["fecha_compra"],
        # Proveedor
        "id_proveedor": jb_datos["id_proveedor"],
        # Total nuevo
        "total": jb_total,
        # Detalle nuevo
        "detalle": jb_detalle,
    })
    # Aplica al inventario cada diferencia
    for jb_id_insumo, jb_cambio in jb_cambios.items():
        # Solo si cambió algo
        if jb_cambio != 0:
            # Suma o resta la diferencia
            jb_insumo_repository.jb_cambiar_stock(jb_id_insumo, jb_cambio)
    # Actualiza el costo unitario de cada insumo con el de la compra
    for jb_item in jb_detalle:
        # Pone el costo unitario nuevo
        jb_insumo_repository.jb_actualizar_costo(jb_item["id_insumo"], jb_item["costo_unitario"])
    # Devuelve la compra actualizada
    return jb_actualizada


# Elimina una compra
def jb_eliminar(jb_id: int) -> dict:
    """Anula la compra: devuelve (resta) del inventario lo que esa compra había sumado."""
    # Busca la compra (404 si no existe)
    jb_compra = jb_obtener(jb_id)
    # Cambios negativos: lo que la compra había sumado ahora se resta
    jb_cambios = {jb_id_insumo: -jb_valor for jb_id_insumo, jb_valor in jb_cantidades_por_insumo(jb_compra["detalle"]).items()}
    # Si algún insumo ya se consumió y quedaría negativo, responde 409
    jb_verificar_salidas(jb_cambios)
    # Resta del inventario cada cantidad
    for jb_id_insumo, jb_cambio in jb_cambios.items():
        # Resta la cantidad (el cambio es negativo)
        jb_insumo_repository.jb_cambiar_stock(jb_id_insumo, jb_cambio)
    # Borra la compra
    jb_compra_repository.jb_eliminar(jb_id)
    # Responde que se borró
    return jb_borrado_fisico(f"La compra {jb_id} (se descontó del inventario lo que había ingresado)")
