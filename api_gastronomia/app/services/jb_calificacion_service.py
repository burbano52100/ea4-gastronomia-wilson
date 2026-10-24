"""Reglas de negocio de calificaciones de los clientes (RF12, MongoDB bd_gastronomia_nosql)."""
# Fecha y hora actual de Colombia
from app.core.jb_utilidades import jb_ahora
# Acceso a calificaciones (base NoSQL)
from app.repositories.jb_calificacion_repository import jb_calificacion_repository
# Acceso a pedidos
from app.repositories.jb_pedido_repository import jb_pedido_repository
# Acceso a productos
from app.repositories.jb_producto_repository import jb_producto_repository
# Respuestas y errores comunes
from app.services.jb_comun import jb_borrado_fisico, jb_dato_invalido, jb_no_encontrado


# Lista todas las calificaciones
def jb_listar() -> list[dict]:
    # De la más reciente a la más antigua
    return jb_calificacion_repository.jb_listar(jb_orden=[("fecha", -1)])


# Busca una calificación o responde 404
def jb_obtener(jb_id: int) -> dict:
    # Busca por id
    jb_calificacion = jb_calificacion_repository.jb_buscar_por_id(jb_id)
    # Si no existe...
    if jb_calificacion is None:
        # ...responde 404
        raise jb_no_encontrado(f"La calificación {jb_id}")
    # Devuelve la calificación
    return jb_calificacion


# Valida los productos calificados y les agrega el nombre
def jb_preparar_productos(jb_pedido: dict, jb_productos: list[dict]) -> list[dict]:
    """Solo se califican productos que estén en el pedido; el nombre lo toma la API de la base de datos."""
    # Conjunto con los ids de los productos que tiene el pedido
    jb_en_pedido = {jb_item["id_producto"] for jb_item in jb_pedido["detalle"]}
    # Lista con los ids de los productos que se quieren calificar
    jb_ids = [jb_item["id_producto"] for jb_item in jb_productos]
    # Si la lista tiene más elementos que el conjunto (que no repite), hay un producto repetido
    if len(jb_ids) != len(set(jb_ids)):
        # Responde 400
        raise jb_dato_invalido("Un producto no puede calificarse dos veces en la misma calificación")
    # Aquí se guardan los productos ya preparados
    jb_resultado = []
    # Recorre cada producto calificado
    for jb_item in jb_productos:
        # Si el producto no está en el pedido...
        if jb_item["id_producto"] not in jb_en_pedido:
            # ...responde 400
            raise jb_dato_invalido(f"El producto {jb_item['id_producto']} no hace parte del pedido {jb_pedido['id_pedido']}")
        # Busca el producto para tomar su nombre
        jb_producto = jb_producto_repository.jb_buscar_por_id(jb_item["id_producto"])
        # Agrega el producto con el formato que se guarda en MongoDB
        jb_resultado.append({
            # Id del producto
            "id_producto": jb_item["id_producto"],
            # Nombre real; si el producto ya no existe, un nombre genérico
            "nombre": jb_producto["nombre"] if jb_producto else f"Producto {jb_item['id_producto']}",
            # Calificación enviada
            "calificacion": jb_item["calificacion"],
        })
    # Devuelve la lista preparada
    return jb_resultado


# Busca el pedido y comprueba que esté ENTREGADO
def jb_pedido_entregado(jb_id_pedido: int) -> dict:
    # Busca el pedido en la base principal
    jb_pedido = jb_pedido_repository.jb_buscar_por_id(jb_id_pedido)
    # Si no existe...
    if jb_pedido is None:
        # ...responde 400 (el id viene en el cuerpo, no en la URL)
        raise jb_dato_invalido(f"El pedido {jb_id_pedido} no existe")
    # Si no está ENTREGADO...
    if jb_pedido["estado"] != "ENTREGADO":
        # ...responde 400
        raise jb_dato_invalido(f"Solo se califican pedidos ENTREGADOS; el pedido {jb_id_pedido} está {jb_pedido['estado']}")
    # Devuelve el pedido
    return jb_pedido


# Registra una calificación nueva
def jb_crear(jb_datos: dict) -> dict:
    # Comprueba que el pedido exista y esté ENTREGADO
    jb_pedido = jb_pedido_entregado(jb_datos["id_pedido"])
    # Inserta la calificación; el índice único de id_pedido hace que un pedido calificado dos veces dé 409
    return jb_calificacion_repository.jb_insertar({
        # Pedido calificado
        "id_pedido": jb_datos["id_pedido"],
        # El cliente se toma del pedido (no lo envía quien califica)
        "id_cliente": jb_pedido["id_cliente"],
        # Fecha y hora actual
        "fecha": jb_ahora(),
        # Calificación del servicio
        "calificacion_servicio": jb_datos["calificacion_servicio"],
        # Comentario; get devuelve None si no se envió
        "comentario": jb_datos.get("comentario"),
        # Productos validados y con su nombre
        "productos": jb_preparar_productos(jb_pedido, jb_datos["productos"]),
    })


# Modifica una calificación
def jb_actualizar(jb_id: int, jb_datos: dict) -> dict:
    # Busca la calificación (404 si no existe)
    jb_calificacion = jb_obtener(jb_id)
    # Busca su pedido para validar los productos
    jb_pedido = jb_pedido_entregado(jb_calificacion["id_pedido"])
    # Guarda los cambios y devuelve la calificación actualizada
    return jb_calificacion_repository.jb_actualizar(jb_id, {
        # Calificación del servicio nueva
        "calificacion_servicio": jb_datos["calificacion_servicio"],
        # Comentario nuevo
        "comentario": jb_datos.get("comentario"),
        # Productos validados y con su nombre
        "productos": jb_preparar_productos(jb_pedido, jb_datos["productos"]),
    })


# Borra una calificación
def jb_eliminar(jb_id: int) -> dict:
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # La borra
    jb_calificacion_repository.jb_eliminar(jb_id)
    # Responde que se borró
    return jb_borrado_fisico(f"La calificación {jb_id}")


# Promedio y opiniones de un producto
def jb_resumen_producto(jb_id_producto: int) -> dict:
    # Busca el producto en la base principal
    jb_producto = jb_producto_repository.jb_buscar_por_id(jb_id_producto)
    # Si no existe...
    if jb_producto is None:
        # ...responde 404
        raise jb_no_encontrado(f"El producto {jb_id_producto}")
    # Calcula el resumen con la agregación de la base NoSQL
    jb_resumen = jb_calificacion_repository.jb_resumen_producto(jb_id_producto)
    # Arma la respuesta (forma de JbResumenCalificaciones)
    return {
        # Id del producto
        "id_producto": jb_id_producto,
        # Nombre del producto
        "producto": jb_producto["nombre"],
        # Promedio con 2 decimales; None si nadie lo ha calificado
        "promedio": round(jb_resumen["promedio"], 2) if jb_resumen else None,
        # Número de calificaciones; 0 si no hay
        "total_calificaciones": jb_resumen["total_calificaciones"] if jb_resumen else 0,
        # Lista de opiniones; vacía si no hay
        "calificaciones": jb_resumen["calificaciones"] if jb_resumen else [],
    }
