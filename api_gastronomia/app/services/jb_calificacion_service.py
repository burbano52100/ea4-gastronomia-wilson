"""Reglas de negocio de las calificaciones de los clientes (RF12).

Las calificaciones se guardan en MongoDB, pero se comprueban contra MySQL: el pedido debe existir
y estar ENTREGADO, el cliente debe ser el que hizo el pedido y los productos deben estar en el pedido.
MongoDB no tiene llaves foráneas, por eso estas reglas las revisa la API.
"""
# datetime: fecha y hora
from datetime import datetime

# DuplicateKeyError: error de MongoDB cuando se repite un valor de un índice único
from pymongo.errors import DuplicateKeyError
# Session: sesión de trabajo con MySQL
from sqlalchemy.orm import Session

# Zona horaria de Colombia y conversión de fechas
from app.core.jb_utilidades import JB_ZONA_BOGOTA, jb_hora_colombia
# Consultas a la colección calificaciones (MongoDB)
from app.repositories import jb_calificacion_repository as jb_repositorio
# Consultas a pedidos y productos (MySQL)
from app.repositories import jb_pedido_repository, jb_producto_repository
# Errores comunes
from app.services.jb_comun import jb_conflicto, jb_dato_invalido, jb_no_encontrado


# Convierte un documento de MongoDB en la forma de JbCalificacionRespuesta
def jb_a_respuesta(jb_documento: dict) -> dict:
    # Arma el diccionario de respuesta
    return {
        # El _id de MongoDB se responde como texto de 24 caracteres
        "id_calificacion": str(jb_documento["_id"]),
        # Pedido
        "id_pedido": jb_documento["id_pedido"],
        # Cliente
        "id_cliente": jb_documento["id_cliente"],
        # Fecha en hora de Colombia, sin zona horaria (igual que las fechas de MySQL)
        "fecha": jb_hora_colombia(jb_documento["fecha"]),
        # Nota del servicio
        "calificacion_servicio": jb_documento["calificacion_servicio"],
        # Comentario; get devuelve None si no tiene
        "comentario": jb_documento.get("comentario"),
        # Productos calificados
        "productos": jb_documento["productos"],
    }


# Lista todas las calificaciones
def jb_listar() -> list[dict]:
    # Pide la lista al repositorio y convierte cada documento
    return [jb_a_respuesta(jb_documento) for jb_documento in jb_repositorio.jb_listar()]


# Busca una calificación o responde 404
def jb_obtener(jb_id: str) -> dict:
    # Busca por id
    jb_documento = jb_repositorio.jb_buscar(jb_id)
    # Si no existe...
    if jb_documento is None:
        # ...responde 404
        raise jb_no_encontrado(f"La calificación {jb_id}")
    # Devuelve la calificación
    return jb_a_respuesta(jb_documento)


# Comprueba el pedido en MySQL y arma la lista de productos con su nombre
def jb_validar_contra_mysql(jb_sesion: Session, jb_id_pedido: int, jb_id_cliente: int | None, jb_productos: list[dict]) -> list[dict]:
    # Busca el pedido en MySQL
    jb_pedido = jb_pedido_repository.jb_buscar(jb_sesion, jb_id_pedido)
    # Si no existe...
    if jb_pedido is None:
        # ...responde 400
        raise jb_dato_invalido(f"El pedido {jb_id_pedido} no existe")
    # Solo se califican pedidos entregados
    if jb_pedido.estado != "ENTREGADO":
        # Responde 409 (choca con el estado actual del pedido)
        raise jb_conflicto(f"Solo se califican pedidos ENTREGADO: el pedido {jb_id_pedido} está {jb_pedido.estado}")
    # Si se indicó cliente, debe ser el del pedido
    if jb_id_cliente is not None and jb_id_cliente != jb_pedido.id_cliente:
        # Responde 400
        raise jb_dato_invalido(f"El cliente {jb_id_cliente} no hizo el pedido {jb_id_pedido}")
    # Nombre de cada producto del pedido: {id_producto: nombre}
    jb_nombres = {jb_item.id_producto: jb_item.nombre_producto for jb_item in jb_pedido.detalle}
    # Aquí se arma la lista que se guarda en MongoDB
    jb_resultado = []
    # Recorre cada producto calificado
    for jb_producto in jb_productos:
        # Si el producto no está en el pedido...
        if jb_producto["id_producto"] not in jb_nombres:
            # ...responde 400
            raise jb_dato_invalido(f"El producto {jb_producto['id_producto']} no está en el pedido {jb_id_pedido}")
        # Agrega el producto con su nombre tomado de MySQL
        jb_resultado.append({
            # Id del producto
            "id_producto": jb_producto["id_producto"],
            # Nombre copiado de MySQL (como en el ejemplo del instructivo)
            "nombre": jb_nombres[jb_producto["id_producto"]],
            # Nota
            "calificacion": jb_producto["calificacion"],
        })
    # Devuelve la lista
    return jb_resultado


# Registra una calificación
def jb_crear(jb_sesion: Session, jb_datos: dict) -> dict:
    # Comprueba contra MySQL y arma los productos con su nombre
    jb_productos = jb_validar_contra_mysql(jb_sesion, jb_datos["id_pedido"], jb_datos["id_cliente"], jb_datos["productos"])
    # Arma el documento con la forma del ejemplo del instructivo
    jb_documento = {
        # Pedido
        "id_pedido": jb_datos["id_pedido"],
        # Cliente
        "id_cliente": jb_datos["id_cliente"],
        # Fecha y hora actual con zona horaria (MongoDB la guarda en UTC)
        "fecha": datetime.now(JB_ZONA_BOGOTA),
        # Nota del servicio
        "calificacion_servicio": jb_datos["calificacion_servicio"],
        # Comentario
        "comentario": jb_datos.get("comentario"),
        # Productos calificados
        "productos": jb_productos,
    }
    # Se intenta insertar
    try:
        # Inserta el documento (MongoDB revisa además su validador $jsonSchema)
        jb_repositorio.jb_insertar(jb_documento)
    # El índice único no deja calificar dos veces el mismo pedido
    except DuplicateKeyError:
        # Responde 409
        raise jb_conflicto(f"El pedido {jb_datos['id_pedido']} ya tiene una calificación: modifíquela con PUT")
    # Devuelve la calificación registrada
    return jb_a_respuesta(jb_documento)


# Modifica una calificación (nota, comentario y productos)
def jb_actualizar(jb_sesion: Session, jb_id: str, jb_datos: dict) -> dict:
    # Busca la calificación (404 si no existe)
    jb_documento = jb_repositorio.jb_buscar(jb_id)
    # Si no existe...
    if jb_documento is None:
        # ...responde 404
        raise jb_no_encontrado(f"La calificación {jb_id}")
    # Comprueba los productos contra el pedido de la calificación (el cliente no cambia)
    jb_productos = jb_validar_contra_mysql(jb_sesion, jb_documento["id_pedido"], None, jb_datos["productos"])
    # Cambia solo estos campos
    jb_nuevo = jb_repositorio.jb_actualizar(jb_id, {
        # Nota del servicio
        "calificacion_servicio": jb_datos["calificacion_servicio"],
        # Comentario
        "comentario": jb_datos.get("comentario"),
        # Productos
        "productos": jb_productos,
    })
    # Si alguien la borró justo antes...
    if jb_nuevo is None:
        # ...responde 404
        raise jb_no_encontrado(f"La calificación {jb_id}")
    # Devuelve la calificación modificada
    return jb_a_respuesta(jb_nuevo)


# Elimina una calificación
def jb_eliminar(jb_id: str) -> dict:
    # Si no se borró ningún documento...
    if not jb_repositorio.jb_eliminar(jb_id):
        # ...responde 404
        raise jb_no_encontrado(f"La calificación {jb_id}")
    # Responde borrado físico
    return {"mensaje": f"La calificación {jb_id} se eliminó", "tipo_borrado": "FISICO"}


# Calificaciones y promedio de un producto (GET /calificaciones/producto/{id})
def jb_por_producto(jb_sesion: Session, jb_id_producto: int) -> dict:
    # Busca el producto en MySQL
    jb_producto = jb_producto_repository.jb_buscar(jb_sesion, jb_id_producto)
    # Si no existe...
    if jb_producto is None:
        # ...responde 404
        raise jb_no_encontrado(f"El producto {jb_id_producto}")
    # MongoDB calcula el promedio y la cantidad
    jb_promedio, jb_total = jb_repositorio.jb_resumen_producto(jb_id_producto)
    # Lista de calificaciones del producto
    jb_calificaciones = [
        # Forma de JbCalificacionDeProducto
        {
            # Id del documento
            "id_calificacion": str(jb_documento["_id"]),
            # Pedido
            "id_pedido": jb_documento["id_pedido"],
            # Cliente
            "id_cliente": jb_documento["id_cliente"],
            # Fecha en hora de Colombia
            "fecha": jb_hora_colombia(jb_documento["fecha"]),
            # Nota del producto en esa calificación
            "calificacion": jb_documento["calificacion"],
            # Comentario general
            "comentario": jb_documento.get("comentario"),
        }
        # Recorre los documentos que devolvió la agregación
        for jb_documento in jb_repositorio.jb_por_producto(jb_id_producto)
    ]
    # Devuelve la forma de JbCalificacionesProducto
    return {
        # Id del producto
        "id_producto": jb_id_producto,
        # Nombre del producto
        "nombre": jb_producto.nombre,
        # Cantidad de calificaciones
        "total_calificaciones": jb_total,
        # Promedio con 2 decimales (None si no tiene calificaciones)
        "promedio": round(jb_promedio, 2) if jb_promedio is not None else None,
        # Lista de calificaciones
        "calificaciones": jb_calificaciones,
    }
