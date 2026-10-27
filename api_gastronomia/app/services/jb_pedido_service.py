"""Reglas de negocio de pedidos (RF10): RN01, RN03 y RN05."""
# defaultdict: diccionario que da un valor inicial a las claves nuevas (aquí, Decimal 0)
from collections import defaultdict
# Decimal: números exactos para dinero y cantidades
from decimal import Decimal

# Session: sesión de trabajo con MySQL
from sqlalchemy.orm import Session

# Hora actual de Colombia y redondeos
from app.core.jb_utilidades import jb_ahora, jb_cantidad, jb_dinero
# Modelos de las tablas
from app.models.jb_modelos import JbCliente, JbDetallePedido, JbPedido
# Consultas a clientes, insumos, productos y recetas
from app.repositories import jb_cliente_repository, jb_insumo_repository, jb_producto_repository, jb_receta_repository
# Consultas a pedidos
from app.repositories import jb_pedido_repository as jb_repositorio
# Errores comunes
from app.services.jb_comun import jb_conflicto, jb_dato_invalido, jb_no_encontrado

# Estados en los que un pedido ya no se puede modificar (RN05)
JB_ESTADOS_CERRADOS = ("ENTREGADO", "ANULADO")
# Estados a los que puede pasar un pedido desde cada estado
JB_TRANSICIONES = {
    # Un pedido nuevo se empieza a preparar o se anula
    "PENDIENTE": ("EN_PREPARACION", "ANULADO"),
    # Un pedido en preparación se entrega o se anula
    "EN_PREPARACION": ("ENTREGADO", "ANULADO"),
    # Estados finales: no pasan a ningún otro (RN05)
    "ENTREGADO": (),
    # Estados finales: no pasan a ningún otro (RN05)
    "ANULADO": (),
}


# Lista todos los pedidos
def jb_listar(jb_sesion: Session) -> list[JbPedido]:
    # Pide la lista al repositorio
    return jb_repositorio.jb_listar(jb_sesion)


# Busca un pedido o responde 404
def jb_obtener(jb_sesion: Session, jb_id: int) -> JbPedido:
    # Busca por id
    jb_pedido = jb_repositorio.jb_buscar(jb_sesion, jb_id)
    # Si no existe...
    if jb_pedido is None:
        # ...responde 404
        raise jb_no_encontrado(f"El pedido {jb_id}")
    # Devuelve el pedido
    return jb_pedido


# Pedidos que están en un estado (GET /pedidos/estado/{estado})
def jb_por_estado(jb_sesion: Session, jb_estado: str) -> list[JbPedido]:
    # Pide la consulta al repositorio
    return jb_repositorio.jb_por_estado(jb_sesion, jb_estado)


# Busca un pedido y lo bloquea para modificarlo, o responde 404
def jb_bloquear(jb_sesion: Session, jb_id: int) -> JbPedido:
    # SELECT ... FOR UPDATE: nadie más lo modifica mientras esta petición no termine
    jb_pedido = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_pedido is None:
        # ...responde 404
        raise jb_no_encontrado(f"El pedido {jb_id}")
    # Devuelve el pedido bloqueado
    return jb_pedido


# Comprueba que el pedido se pueda modificar (RN05)
def jb_validar_abierto(jb_pedido: JbPedido) -> None:
    """RN05: un pedido ENTREGADO o ANULADO no puede modificarse."""
    # Si el estado está en la lista de cerrados...
    if jb_pedido.estado in JB_ESTADOS_CERRADOS:
        # ...responde 409
        raise jb_conflicto(f"El pedido {jb_pedido.id_pedido} está {jb_pedido.estado} y no puede modificarse (RN05)")


# Comprueba que el cliente exista y esté ACTIVO
def jb_validar_cliente(jb_sesion: Session, jb_id_cliente: int) -> JbCliente:
    # Busca el cliente
    jb_cliente = jb_cliente_repository.jb_buscar(jb_sesion, jb_id_cliente)
    # Si no existe...
    if jb_cliente is None:
        # ...responde 400 (equivale a fallar la llave foránea)
        raise jb_dato_invalido(f"El cliente {jb_id_cliente} no existe")
    # Si está INACTIVO...
    if jb_cliente.estado != "ACTIVO":
        # ...responde 400
        raise jb_dato_invalido(f"El cliente {jb_id_cliente} está INACTIVO: no se le pueden registrar pedidos")
    # Devuelve el cliente
    return jb_cliente


# Arma los ítems del pedido con precios, subtotales y total (RN01)
def jb_armar_detalle(jb_sesion: Session, jb_items: list[dict]) -> tuple[list[JbDetallePedido], Decimal]:
    """RN01: el precio sale de la base de datos; subtotal = cantidad x precio_unitario; total = suma de subtotales."""
    # Busca todos los productos del pedido en una sola consulta
    jb_productos = jb_producto_repository.jb_buscar_varios(jb_sesion, [jb_item["id_producto"] for jb_item in jb_items])
    # Lista de ítems y total que empieza en 0
    jb_detalle, jb_total = [], Decimal("0")
    # Recorre cada ítem enviado
    for jb_item in jb_items:
        # Producto del ítem (None si no existe)
        jb_producto = jb_productos.get(jb_item["id_producto"])
        # Si no existe...
        if jb_producto is None:
            # ...responde 400
            raise jb_dato_invalido(f"El producto {jb_item['id_producto']} no existe")
        # Si no está DISPONIBLE (AGOTADO o INACTIVO)...
        if jb_producto.estado != "DISPONIBLE":
            # ...responde 400
            raise jb_dato_invalido(f"El producto '{jb_producto.nombre}' no se puede pedir: está {jb_producto.estado}")
        # Subtotal = cantidad x precio de venta guardado en la base, redondeado a 2 decimales
        jb_subtotal = jb_dinero(jb_item["cantidad"] * jb_producto.precio_venta)
        # Agrega el ítem
        jb_detalle.append(JbDetallePedido(
            # Producto
            producto=jb_producto,
            # Cantidad pedida
            cantidad=jb_item["cantidad"],
            # Precio tomado de la base en este momento: si después cambia, el pedido conserva este
            precio_unitario=jb_producto.precio_venta,
            # Subtotal calculado por la API
            subtotal=jb_subtotal,
        ))
        # Suma el subtotal al total
        jb_total += jb_subtotal
    # Devuelve los ítems y el total redondeado
    return jb_detalle, jb_dinero(jb_total)


# Registra un pedido nuevo
def jb_crear(jb_sesion: Session, jb_datos: dict, jb_id_usuario: int) -> JbPedido:
    # Comprueba el cliente (400 si no existe o está INACTIVO)
    jb_cliente = jb_validar_cliente(jb_sesion, jb_datos["id_cliente"])
    # Valida los productos y calcula subtotales y total (RN01)
    jb_detalle, jb_total = jb_armar_detalle(jb_sesion, jb_datos["detalle"])
    # Arma el pedido
    jb_pedido = JbPedido(
        # Fecha y hora actual de Colombia
        fecha_pedido=jb_ahora(),
        # Cliente
        cliente=jb_cliente,
        # Usuario que registra (viene del token)
        id_usuario=jb_id_usuario,
        # Tipo de pedido
        tipo_pedido=jb_datos["tipo_pedido"],
        # Todo pedido nuevo empieza PENDIENTE
        estado="PENDIENTE",
        # Total calculado (RN01)
        total=jb_total,
        # Observaciones; get devuelve None si no se enviaron
        observaciones=jb_datos.get("observaciones"),
        # Ítems del pedido
        detalle=jb_detalle,
    )
    # Inserta el pedido con sus ítems
    jb_repositorio.jb_guardar(jb_sesion, jb_pedido)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve el pedido registrado
    return jb_pedido


# Modifica un pedido (cliente, tipo, observaciones y detalle completo)
def jb_actualizar(jb_sesion: Session, jb_id: int, jb_datos: dict) -> JbPedido:
    # Busca el pedido y lo bloquea (404 si no existe)
    jb_pedido = jb_bloquear(jb_sesion, jb_id)
    # RN05: si está ENTREGADO o ANULADO responde 409
    jb_validar_abierto(jb_pedido)
    # Comprueba el cliente
    jb_cliente = jb_validar_cliente(jb_sesion, jb_datos["id_cliente"])
    # Valida los productos y vuelve a calcular subtotales y total (RN01)
    jb_detalle, jb_total = jb_armar_detalle(jb_sesion, jb_datos["detalle"])
    # Quita los ítems viejos (delete-orphan los borra de la tabla)
    jb_pedido.detalle.clear()
    # Envía el borrado antes de insertar los nuevos: la pareja pedido-producto es única
    jb_sesion.flush()
    # Agrega los ítems nuevos
    jb_pedido.detalle.extend(jb_detalle)
    # Cliente
    jb_pedido.cliente = jb_cliente
    # Tipo de pedido
    jb_pedido.tipo_pedido = jb_datos["tipo_pedido"]
    # Observaciones
    jb_pedido.observaciones = jb_datos.get("observaciones")
    # Total recalculado (RN01)
    jb_pedido.total = jb_total
    # Guarda los cambios
    jb_repositorio.jb_guardar(jb_sesion, jb_pedido)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve el pedido modificado
    return jb_pedido


# "Elimina" un pedido: en realidad lo anula
def jb_eliminar(jb_sesion: Session, jb_id: int) -> dict:
    """Un pedido no se borra porque es parte del historial de ventas: se ANULA. Si ya está cerrado aplica RN05."""
    # Busca el pedido y lo bloquea (404 si no existe)
    jb_pedido = jb_bloquear(jb_sesion, jb_id)
    # RN05: si ya está cerrado responde 409
    jb_validar_abierto(jb_pedido)
    # Cambia el estado a ANULADO
    jb_pedido.estado = "ANULADO"
    # Confirma la transacción
    jb_sesion.commit()
    # Responde borrado lógico
    return {"mensaje": f"El pedido {jb_id} quedó ANULADO: los pedidos no se borran", "tipo_borrado": "LOGICO"}


# Calcula cuánto de cada insumo necesita el pedido
def jb_insumos_necesarios(jb_sesion: Session, jb_pedido: JbPedido) -> dict[int, Decimal]:
    """Suma, por insumo, la cantidad de la receta multiplicada por las unidades pedidas.
    Si dos productos usan el mismo insumo, se suman los dos antes de comparar con el stock."""
    # Cantidad pedida de cada producto: {id_producto: cantidad}
    jb_cantidades = {jb_item.id_producto: jb_item.cantidad for jb_item in jb_pedido.detalle}
    # Diccionario {id_insumo: cantidad}; cada insumo nuevo empieza en 0
    jb_necesarios = defaultdict(lambda: Decimal("0"))
    # Recorre las recetas de todos los productos del pedido
    for jb_linea in jb_receta_repository.jb_por_productos(jb_sesion, list(jb_cantidades)):
        # Suma: cantidad de la receta x unidades pedidas de ese producto
        jb_necesarios[jb_linea.id_insumo] += jb_linea.cantidad * jb_cantidades[jb_linea.id_producto]
    # Devuelve las cantidades redondeadas a 3 decimales
    return {jb_id_insumo: jb_cantidad(jb_valor) for jb_id_insumo, jb_valor in jb_necesarios.items()}


# Descuenta del inventario los insumos del pedido (RN03)
def jb_descontar_inventario(jb_sesion: Session, jb_pedido: JbPedido) -> None:
    """RN03: descuenta los insumos de la receta. Si no alcanza el inventario responde 409
    y la transacción se deshace: no se descuenta nada y el pedido no cambia de estado."""
    # Cuánto se necesita de cada insumo
    jb_necesarios = jb_insumos_necesarios(jb_sesion, jb_pedido)
    # Si ningún producto tiene receta, no hay nada que descontar
    if not jb_necesarios:
        # Termina sin cambiar el inventario
        return
    # Busca y bloquea los insumos (SELECT ... FOR UPDATE)
    jb_insumos = jb_insumo_repository.jb_buscar_varios_para_actualizar(jb_sesion, list(jb_necesarios))
    # 1) Verificar TODO antes de descontar NADA
    jb_faltantes = []
    # Recorre cada insumo necesario
    for jb_id_insumo, jb_requerido in jb_necesarios.items():
        # Insumo bloqueado
        jb_insumo = jb_insumos[jb_id_insumo]
        # Si no alcanza...
        if jb_insumo.stock_actual < jb_requerido:
            # ...se anota cuánto se necesita y cuánto hay
            jb_faltantes.append(
                # Por ejemplo: "Tomate: se necesitan 0.300 kg y hay 0.100"
                f"{jb_insumo.nombre}: se necesitan {jb_requerido} {jb_insumo.unidad_medida} y hay {jb_insumo.stock_actual}"
            )
    # Si faltó algún insumo...
    if jb_faltantes:
        # ...responde 409; la sesión hace rollback y no queda nada a medias
        raise jb_conflicto("Inventario insuficiente para entregar el pedido (RN03). " + "; ".join(jb_faltantes))
    # 2) Descontar: todo alcanza
    for jb_id_insumo, jb_requerido in jb_necesarios.items():
        # Resta la cantidad necesaria del stock
        jb_insumos[jb_id_insumo].stock_actual = jb_cantidad(jb_insumos[jb_id_insumo].stock_actual - jb_requerido)


# Cambia el estado de un pedido (PATCH /pedidos/{id}/estado)
def jb_cambiar_estado(jb_sesion: Session, jb_id: int, jb_estado_nuevo: str) -> JbPedido:
    # Busca el pedido y lo bloquea: evita que dos usuarios lo entreguen al mismo tiempo
    jb_pedido = jb_bloquear(jb_sesion, jb_id)
    # RN05: si ya está ENTREGADO o ANULADO responde 409
    jb_validar_abierto(jb_pedido)
    # Estados a los que puede pasar desde el actual
    jb_permitidos = JB_TRANSICIONES[jb_pedido.estado]
    # Si el estado pedido no es uno de esos...
    if jb_estado_nuevo not in jb_permitidos:
        # ...responde 409 explicando a cuáles sí puede pasar
        raise jb_conflicto(f"Un pedido {jb_pedido.estado} solo puede pasar a {' o '.join(jb_permitidos)}")
    # Si se entrega, se descuenta el inventario (RN03)
    if jb_estado_nuevo == "ENTREGADO":
        # Descuenta los insumos (409 si no alcanzan)
        jb_descontar_inventario(jb_sesion, jb_pedido)
    # Cambia el estado
    jb_pedido.estado = jb_estado_nuevo
    # Confirma todo junto: estado e inventario
    jb_sesion.commit()
    # Devuelve el pedido actualizado
    return jb_pedido
