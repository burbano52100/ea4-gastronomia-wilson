"""Endpoints de calificaciones de los clientes (RF12, MongoDB bd_gastronomia_nosql). Roles: ADMIN, CAJERO."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R400, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Esquemas de calificaciones (lo que entra y lo que sale)
from app.schemas.jb_calificacion_schema import (
    JbCalificacionActualizar,
    JbCalificacionCrear,
    JbCalificacionRespuesta,
    JbResumenCalificaciones,
)
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de calificaciones, con el nombre corto jb_servicio
from app.services import jb_calificacion_service as jb_servicio

# Router: rutas /calificaciones, sección de Swagger, errores 401/403 y TODOS sus endpoints exigen ADMIN o CAJERO
jb_router = APIRouter(prefix="/calificaciones", tags=["Calificaciones (MongoDB NoSQL)"], responses=JB_PRIVADO,
                      dependencies=[Depends(jb_requiere_roles("ADMIN", "CAJERO"))])


# GET /api/v1/calificaciones: lista todas
@jb_router.get("", response_model=list[JbCalificacionRespuesta], summary="Listar calificaciones")
def jb_listar_calificaciones():
    """De la más reciente a la más antigua. **Roles:** ADMIN, CAJERO."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar()


# GET /api/v1/calificaciones/producto/{id}: va antes de /{id_calificacion} porque es una ruta más específica
@jb_router.get("/producto/{id_producto}", response_model=JbResumenCalificaciones,
               summary="Calificaciones y promedio de un producto", responses=JB_R404)
# id_producto se toma de la URL y FastAPI lo convierte en entero
def jb_calificaciones_producto(id_producto: int):
    """Calcula el promedio con una agregación de MongoDB ($unwind + $group + $avg). **Roles:** ADMIN, CAJERO."""
    # Pide el resumen al servicio
    return jb_servicio.jb_resumen_producto(id_producto)


# GET /api/v1/calificaciones/{id}: consulta una
@jb_router.get("/{id_calificacion}", response_model=JbCalificacionRespuesta, summary="Consultar una calificación",
               responses=JB_R404)
def jb_obtener_calificacion(id_calificacion: int):
    """**Roles:** ADMIN, CAJERO."""
    # Busca la calificación (404 si no existe)
    return jb_servicio.jb_obtener(id_calificacion)


# POST /api/v1/calificaciones: registra una (201)
@jb_router.post("", response_model=JbCalificacionRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Registrar calificación", responses={**JB_R400, **JB_R409})
# El cuerpo se valida con JbCalificacionCrear
def jb_crear_calificacion(jb_datos: JbCalificacionCrear):
    """Solo para pedidos ENTREGADOS y productos que estén en el pedido. Valores de 1 a 5.
    El cliente y el nombre de cada producto los toma la API. Un pedido se califica una sola vez (409).

    **Roles:** ADMIN, CAJERO.
    """
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_datos.model_dump())


# PUT /api/v1/calificaciones/{id}: modifica una
@jb_router.put("/{id_calificacion}", response_model=JbCalificacionRespuesta, summary="Actualizar calificación",
               responses={**JB_R400, **JB_R404})
# Recibe el id de la URL y el cuerpo validado con JbCalificacionActualizar
def jb_actualizar_calificacion(id_calificacion: int, jb_datos: JbCalificacionActualizar):
    """**Roles:** ADMIN, CAJERO."""
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(id_calificacion, jb_datos.model_dump())


# DELETE /api/v1/calificaciones/{id}: borra una
@jb_router.delete("/{id_calificacion}", response_model=JbResultadoEliminacion, summary="Eliminar calificación",
                  responses=JB_R404)
def jb_eliminar_calificacion(id_calificacion: int):
    """**Roles:** ADMIN, CAJERO."""
    # Pide al servicio que la borre
    return jb_servicio.jb_eliminar(id_calificacion)
