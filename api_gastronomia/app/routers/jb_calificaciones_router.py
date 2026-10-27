"""Endpoints de calificaciones de los clientes (RF12), guardadas en MongoDB. Roles: ADMIN, CAJERO."""
# Annotated: agrega información extra a un tipo
from typing import Annotated

# APIRouter: agrupa endpoints; Depends: dependencias; Path: parámetros de la URL; status: códigos HTTP
from fastapi import APIRouter, Depends, Path, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R400, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Sesión de MySQL (para comprobar pedidos y productos)
from app.database.jb_conexion_mysql import JbSesion
# Esquemas de calificaciones
from app.schemas.jb_calificacion_schema import (
    JbCalificacionActualizar,  # datos para modificar
    JbCalificacionCrear,  # datos para crear
    JbCalificacionesProducto,  # forma de las calificaciones de un producto
    JbCalificacionRespuesta,  # forma de la respuesta
)
# Patrón del id de MongoDB y esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JB_PATRON_OBJECT_ID, JbResultadoEliminacion
# Servicio de calificaciones, con el nombre corto jb_servicio
from app.services import jb_calificacion_service as jb_servicio

# Id de una calificación en la URL: 24 caracteres hexadecimales (si no, responde 422)
JbIdCalificacion = Annotated[str, Path(pattern=JB_PATRON_OBJECT_ID, description="Id de MongoDB (24 caracteres)")]

# Router: rutas /calificaciones; TODOS sus endpoints exigen ADMIN o CAJERO
jb_router = APIRouter(
    # Prefijo de las rutas
    prefix="/calificaciones",
    # Sección de Swagger
    tags=["Calificaciones (MongoDB)"],
    # Seguridad de todo el router
    dependencies=[Depends(jb_requiere_roles("ADMIN", "CAJERO"))],
    # Errores 401 y 403 en todos los endpoints
    responses=JB_PRIVADO,
)


# GET /api/v1/calificaciones: lista todas
@jb_router.get("", response_model=list[JbCalificacionRespuesta], summary="Listar calificaciones")
# No recibe datos: responde la lista completa
def jb_listar_calificaciones():
    """Calificaciones de la más reciente a la más antigua. **Roles:** ADMIN, CAJERO."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar()


# GET /api/v1/calificaciones/producto/{id}: va antes de /{id_calificacion} porque es una ruta fija
@jb_router.get("/producto/{id_producto}", response_model=JbCalificacionesProducto,
               summary="Calificaciones y promedio de un producto", responses=JB_R404)  # título en Swagger y errores que puede responder
# Recibe el id_producto de la URL y la sesión de MySQL
def jb_calificaciones_producto(id_producto: int, jb_sesion: JbSesion):
    """Calificaciones que recibió el producto y su promedio, calculado por MongoDB con una agregación
    (`$unwind` + `$group` con `$avg`). 404 si el producto no existe en MySQL.

    **Roles:** ADMIN, CAJERO.
    """
    # Pide la consulta al servicio
    return jb_servicio.jb_por_producto(jb_sesion, id_producto)


# GET /api/v1/calificaciones/{id}: consulta una
@jb_router.get("/{id_calificacion}", response_model=JbCalificacionRespuesta, summary="Consultar una calificación",
               responses=JB_R404)  # errores que puede responder
# Recibe el id_calificacion de la URL
def jb_obtener_calificacion(id_calificacion: JbIdCalificacion):
    """**Roles:** ADMIN, CAJERO."""
    # Busca la calificación (404 si no existe)
    return jb_servicio.jb_obtener(id_calificacion)


# POST /api/v1/calificaciones: registra una (201)
@jb_router.post("", response_model=JbCalificacionRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Registrar calificación", responses={**JB_R400, **JB_R409})  # título en Swagger y errores que puede responder
# Recibe el cuerpo JSON ya validado y la sesión de MySQL
def jb_crear_calificacion(jb_datos: JbCalificacionCrear, jb_sesion: JbSesion):
    """El pedido debe existir en MySQL y estar ENTREGADO (409 si no), el cliente debe ser el que hizo el pedido
    y los productos deben estar en ese pedido (400 si no). Un pedido se califica una sola vez (409).
    Las notas son enteros de 1 a 5. El nombre de cada producto lo copia la API desde MySQL.

    **Roles:** ADMIN, CAJERO.
    """
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_sesion, jb_datos.model_dump())


# PUT /api/v1/calificaciones/{id}: modifica una
@jb_router.put("/{id_calificacion}", response_model=JbCalificacionRespuesta, summary="Actualizar calificación",
               responses={**JB_R400, **JB_R404})  # errores que puede responder
# Recibe el id_calificacion de la URL, el cuerpo JSON ya validado y la sesión de MySQL
def jb_actualizar_calificacion(id_calificacion: JbIdCalificacion, jb_datos: JbCalificacionActualizar, jb_sesion: JbSesion):
    """Cambia la nota del servicio, el comentario y los productos calificados (el pedido y el cliente no cambian).

    **Roles:** ADMIN, CAJERO.
    """
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(jb_sesion, id_calificacion, jb_datos.model_dump())


# DELETE /api/v1/calificaciones/{id}: borra una
@jb_router.delete("/{id_calificacion}", response_model=JbResultadoEliminacion, summary="Eliminar calificación",
                  responses=JB_R404)  # errores que puede responder
# Recibe el id_calificacion de la URL
def jb_eliminar_calificacion(id_calificacion: JbIdCalificacion):
    """**Roles:** ADMIN, CAJERO."""
    # Pide el borrado al servicio
    return jb_servicio.jb_eliminar(id_calificacion)
