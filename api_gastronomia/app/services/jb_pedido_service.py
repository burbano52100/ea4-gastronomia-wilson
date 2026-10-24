"""Reglas de negocio de pedidos (RF10): RN01, RN03 y RN05."""
# defaultdict: diccionario que da un valor inicial a las claves nuevas (aquí, Decimal 0)
from collections import defaultdict
# Decimal: números exactos para cantidades y dinero
from decimal import Decimal

# Funciones de apoyo: hora actual, redondeo de cantidades y de dinero
from app.core.jb_utilidades import jb_ahora, jb_cantidad, jb_dinero
# Acceso a clientes
from app.repositories.jb_cliente_repository import jb_cliente_repository
# Acceso a insumos (inventario)
from app.repositories.jb_insumo_repository import jb_insumo_repository
# Acceso a pedidos
from app.repositories.jb_pedido_repository import jb_pedido_repository
# Acceso a productos
from app.repositories.jb_producto_repository import jb_producto_repository
# Acceso a recetas
from app.repositories.jb_receta_repository import jb_receta_repository
# Errores comunes
from app.services.jb_comun import jb_conflicto, jb_dato_invalido, jb_no_encontrado

# Estados en los que un pedido ya no se puede modificar (RN05)
JB_ESTADOS_CERRADOS = ("ENTREGADO", "ANULADO")


# Lista todos los pedidos
def jb_listar() -> list[dict]:
    # Pide la lista al repositorio
    return jb_pedido_repository.jb_listar()


# Busca un pedido o responde 404
def jb_obtener(jb_id: int) -> dict:
    # Busca por id
    jb_pedido = jb_pedido_repository.jb_buscar_por_id(jb_id)
    # Si no existe...
    if jb_pedido is None:
        # ...responde 404
        raise jb_no_encontrado(f"El pedido {jb_id}")
    # Devuelve el pedido
    return jb_pedido


# Pedidos que están en un estado
def jb_por_estado(jb_estado: str) -> list[dict]:
    # Pide la consulta al repositorio
    return jb_pedido_repository.jb_por_estado(jb_estado)


# Comprueba que el pedido se pueda modificar
def jb_validar_abierto(jb_pedido: dict) -> None:
    """RN05: un pedido ENTREGADO o ANULADO no puede modificarse."""
    # Si el estado está en la lista de cerrados...
    if jb_pedido["estado"] in JB_ESTADOS_CERRADOS:
        # ...responde 409
        raise jb_conflicto(f"El pedido {jb_pedido['id_pedido']} está {jb_pedido['estado']} y no puede modificarse (RN05)")


# Comprueba que el cliente exista y esté ACTIVO
def jb_validar_cliente(jb_id_cliente: int) -> None:
    # Busca el cliente
    jb_cliente = jb_cliente_repository.jb_buscar_por_id(jb_id_cliente)
    # Si no existe...
    if jb_cliente is None:
        # ...responde 400 (equivale a fallar una llave foránea)
        raise jb_dato_invalido(f"El cliente {jb_id_cliente} no existe")
    # Si está INACTIVO...
    if jb_cliente["estado"] != "ACTIVO":
        # ...responde 400
        raise jb_dato_invalido(f"El cliente {jb_id_cliente} está INACTIVO")


# Valida los productos y calcula precios, subtotales y total (RN01)
def jb_preparar_detalle(jb_items: list[dict]) -> tuple[list[dict], Decimal]:
    """RN01: el precio sale de la base de datos; subtotal = cantidad x precio_unitario; total = suma."""
    # Lista de ítems preparados y total que empieza en 0
    jb_detalle, jb_total = [], Decimal("0")
    # Recorre cada ítem enviado
    for jb_item in jb_items:
        # Busca el producto
        jb_producto = jb_producto_repository.jb_buscar_por_id(jb_item["id_producto"])
        # Si no existe...
        if jb_producto is None:
            # ...responde 400
            raise jb_dato_invalido(f"El producto {jb_item['id_producto']} no existe")
        # Si no está DISPONIBLE (AGOTADO o INACTIVO)...
        if jb_producto["estado"] != "DISPONIBLE":
            # ...responde 400
            raise jb_dato_invalido(f"El producto '{jb_producto['nombre']}' no está disponible ({jb_producto['estado']})")
        # Subtotal = cantidad x precio de venta guardado en la base, redondeado a 2 decimales
        jb_subtotal = jb_dinero(jb_item["cantidad"] * jb_producto["precio_venta"])
        # Agrega el ítem con el formato que se guarda en MongoDB
        jb_detalle.append({
            # Producto
            "id_producto": jb_item["id_producto"],
            # Cantidad pedida
            "cantidad": jb_item["cantidad"],
            # Precio tomado de la base (el cliente no lo envía)
            "precio_unitario": jb_producto["precio_venta"],
            # Subtotal calculado
            "subtotal": jb_subtotal,
        })
        # Suma el subtotal al total
        jb_total += jb_subtotal
    # Devuelve el detalle y el total redondeado
    return jb_detalle, jb_dinero(jb_total)


# Registra un pedido nuevo
def jb_crear(jb_datos: dict, jb_id_usuario: int) -> dict:
    # Comprueba el cliente
    jb_validar_cliente(jb_datos["id_cliente"])
    # Valida los productos y calcula subtotales y total (RN01)
    jb_detalle, jb_total = jb_preparar_detalle(jb_datos["detalle"])
    # Inserta el pedido y lo devuelve
    return jb_pedido_repository.jb_insertar({
        # Fecha y hora actual de Colombia
        "fecha_pedido": jb_ahora(),
        # Cliente
        "id_cliente": jb_datos["id_cliente"],
        # Usuario que registra (viene del token)
        "id_usuario": jb_id_usuario,
        # Tipo de pedido
        "tipo_pedido": jb_datos["tipo_pedido"],
        # Todo pedido nuevo empieza PENDIENTE
        "estado": "PENDIENTE",
        # Observaciones; get devuelve None si no se enviaron
        "observaciones": jb_datos.get("observaciones"),
        # Total calculado (RN01)
        "total": jb_total,
        # Detalle con precios y subtotales
        "detalle": jb_detalle,
    })


# Modifica un pedido
def jb_actualizar(jb_id: int, jb_datos: dict) -> dict:
    # Busca el pedido (404 si no existe)
    jb_pedido = jb_obtener(jb_id)
    # RN05: si está ENTREGADO o ANULADO responde 409
    jb_validar_abierto(jb_pedido)
    # Comprueba el cliente
    jb_validar_cliente(jb_datos["id_cliente"])
    # Valida los productos y vuelve a calcular subtotales y total (RN01)
    jb_detalle, jb_total = jb_preparar_detalle(jb_datos["detalle"])
    # Guarda los cambios y devuelve el pedido actualizado
    return jb_pedido_repository.jb_actualizar(jb_id, {
        # Cliente
        "id_cliente": jb_datos["id_cliente"],
        # Tipo de pedido
        "tipo_pedido": jb_datos["tipo_pedido"],
        # Observaciones
        "observaciones": jb_datos.get("observaciones"),
        # Total recalculado (RN01)
        "total": jb_total,
        # Detalle nuevo
        "detalle": jb_detalle,
    })


# "Elimina" un pedido: en realidad lo anula
def jb_eliminar(jb_id: int) -> dict:
    """Un pedido no se borra (es un movimiento de venta): se ANULA. Si ya está cerrado aplica RN05."""
    # Busca el pedido (404 si no existe)
    jb_pedido = jb_obtener(jb_id)
    # RN05: si ya está cerrado responde 409
    jb_validar_abierto(jb_pedido)
    # Cambia el estado a ANULADO
    jb_pedido_repository.jb_actualizar(jb_id, {"estado": "ANULADO"})
    # Responde borrado lógico
    return {"mensaje": f"El pedido {jb_id} quedó ANULADO (los pedidos no se borran)", "tipo_borrado": "LOGICO"}


# Calcula cuánto de cada insumo necesita el pedido
def jb_insumos_necesarios(jb_pedido: dict) -> dict[int, Decimal]:
    """Suma, por insumo, la cantidad de la receta multiplicada por las unidades pedidas."""
    # Diccionario {id_insumo: cantidad}; cada insumo nuevo empieza en 0
    jb_necesarios = defaultdict(lambda: Decimal("0"))
    # Recorre cada producto del pedido
    for jb_item in jb_pedido["detalle"]:
        # Recorre cada línea de la receta de ese producto
        for jb_linea in jb_receta_repository.jb_por_producto(jb_item["id_producto"]):
            # Suma: cantidad de la receta x unidades pedidas
            jb_necesarios[jb_linea["id_insumo"]] += jb_linea["cantidad"] * jb_item["cantidad"]
    # Devuelve las cantidades redondeadas a 3 decimales
    return {jb_id_insumo: jb_cantidad(jb_valor) for jb_id_insumo, jb_valor in jb_necesarios.items()}


# Descuenta del inventario los insumos del pedido (RN03)
def jb_descontar_inventario(jb_pedido: dict) -> None:
    """RN03: descuenta los insumos de la receta. Si no alcanza el inventario responde 409 y no descuenta nada."""
    # Cuánto se necesita de cada insumo
    jb_necesarios = jb_insumos_necesarios(jb_pedido)

    # 1) Verificar TODO antes de descontar NADA
    jb_faltantes = []
    # Recorre cada insumo necesario
    for jb_id_insumo, jb_requerido in jb_necesarios.items():
        # Busca el insumo
        jb_insumo = jb_insumo_repository.jb_buscar_por_id(jb_id_insumo)
        # Stock disponible; 0 si el insumo ya no existe
        jb_disponible = jb_insumo["stock_actual"] if jb_insumo else Decimal("0")
        # Si no alcanza...
        if jb_disponible < jb_requerido:
            # Nombre del insumo para el mensaje
            jb_nombre = jb_insumo["nombre"] if jb_insumo else f"insumo {jb_id_insumo}"
            # Se anota cuánto se necesita y cuánto hay
            jb_faltantes.append(f"{jb_nombre}: se necesitan {jb_requerido}, hay {jb_disponible}")
    # Si faltó algún insumo...
    if jb_faltantes:
        # ...responde 409 sin haber descontado nada
        raise jb_conflicto("Inventario insuficiente para entregar el pedido (RN03): " + "; ".join(jb_faltantes))

    # 2) Descontar. Cada resta es condicional: si otro usuario consumió el insumo entre
    #    la verificación y la resta, se devuelve lo ya descontado (MongoDB local no usa transacciones).
    jb_descontados = []
    # Recorre cada insumo necesario
    for jb_id_insumo, jb_requerido in jb_necesarios.items():
        # Intenta restar; si no alcanzó (otro usuario lo gastó justo antes)...
        if not jb_insumo_repository.jb_descontar_si_alcanza(jb_id_insumo, jb_requerido):
            # ...devuelve al inventario todo lo que ya había descontado
            for jb_id_devolver, jb_cantidad_devolver in jb_descontados:
                # Suma de nuevo la cantidad
                jb_insumo_repository.jb_cambiar_stock(jb_id_devolver, jb_cantidad_devolver)
            # Y responde 409
            raise jb_conflicto("El inventario cambió mientras se entregaba el pedido; intente de nuevo (RN03)")
        # Si se pudo restar, se anota por si hay que devolverlo
        jb_descontados.append((jb_id_insumo, jb_requerido))


# Cambia el estado de un pedido (PATCH /pedidos/{id}/estado)
def jb_cambiar_estado(jb_id: int, jb_estado_nuevo: str) -> dict:
    # Busca el pedido (404 si no existe)
    jb_pedido = jb_obtener(jb_id)
    # RN05: si ya está cerrado responde 409
    jb_validar_abierto(jb_pedido)
    # Estado que tiene ahora
    jb_estado_actual = jb_pedido["estado"]
    # Si se pide el mismo estado que ya tiene...
    if jb_estado_nuevo == jb_estado_actual:
        # ...responde 400
        raise jb_dato_invalido(f"El pedido {jb_id} ya está en estado {jb_estado_actual}")

    # Se cambia el estado solo si nadie más lo cambió (evita entregar y descontar dos veces).
    if not jb_pedido_repository.jb_cambiar_estado_si(jb_id, jb_estado_actual, jb_estado_nuevo):
        # Si otro usuario lo cambió primero, responde 409
        raise jb_conflicto("Otro usuario modificó el pedido al mismo tiempo; consúltelo de nuevo")
    # Si el estado nuevo es ENTREGADO, hay que descontar el inventario (RN03)
    if jb_estado_nuevo == "ENTREGADO":
        # Se intenta descontar
        try:
            # Descuenta los insumos de la receta
            jb_descontar_inventario(jb_pedido)
        # Si falla (por ejemplo, no hay inventario)...
        except Exception:
            # ...se devuelve el pedido a su estado anterior
            jb_pedido_repository.jb_cambiar_estado_si(jb_id, jb_estado_nuevo, jb_estado_actual)
            # Y se deja pasar el mismo error (el 409)
            raise
    # Devuelve el pedido actualizado
    return jb_obtener(jb_id)
