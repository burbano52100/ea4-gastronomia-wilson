"""Endpoints de recetas o fichas técnicas (RF05). Roles: ADMIN, COCINERO."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R400, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Sesión de MySQL
from app.database.jb_conexion_mysql import JbSesion
# Esquemas de recetas
from app.schemas.jb_receta_schema import JbRecetaActualizar, JbRecetaCrear, JbRecetaRespuesta
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de recetas, con el nombre corto jb_servicio
from app.services import jb_receta_service as jb_servicio

# Router: rutas /recetas; TODOS sus endpoints exigen ADMIN o COCINERO
jb_router = APIRouter(
    # Prefijo de las rutas
    prefix="/recetas",
    # Sección de Swagger
    tags=["Recetas"],
    # Seguridad de todo el router
    dependencies=[Depends(jb_requiere_roles("ADMIN", "COCINERO"))],
    # Errores 401 y 403 en todos los endpoints
    responses=JB_PRIVADO,
)


# GET /api/v1/recetas: lista todas las líneas
@jb_router.get("", response_model=list[JbRecetaRespuesta], summary="Listar recetas")
# Recibe la sesión de MySQL
def jb_listar_recetas(jb_sesion: JbSesion):
    """Todas las líneas de receta, ordenadas por producto. **Roles:** ADMIN, COCINERO."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar(jb_sesion)


# GET /api/v1/recetas/{id}: consulta una línea
@jb_router.get("/{id_receta}", response_model=JbRecetaRespuesta, summary="Consultar una línea de receta", responses=JB_R404)
# Recibe el id_receta de la URL y la sesión de MySQL
def jb_obtener_receta(id_receta: int, jb_sesion: JbSesion):
    """**Roles:** ADMIN, COCINERO."""
    # Busca la línea (404 si no existe)
    return jb_servicio.jb_obtener(jb_sesion, id_receta)


# POST /api/v1/recetas: crea una línea (201)
@jb_router.post("", response_model=JbRecetaRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Agregar un insumo a una receta", responses={**JB_R400, **JB_R409})  # título en Swagger y errores que puede responder
# Recibe el cuerpo JSON ya validado y la sesión de MySQL
def jb_crear_receta(jb_datos: JbRecetaCrear, jb_sesion: JbSesion):
    """El producto debe existir y el insumo debe existir y estar ACTIVO. Un insumo aparece una sola vez
    en la receta de cada producto (409 si se repite).

    **Roles:** ADMIN, COCINERO.
    """
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_sesion, jb_datos.model_dump())


# PUT /api/v1/recetas/{id}: modifica una línea
@jb_router.put("/{id_receta}", response_model=JbRecetaRespuesta, summary="Actualizar una línea de receta",
               responses={**JB_R400, **JB_R404, **JB_R409})  # errores que puede responder
# Recibe el id_receta de la URL, el cuerpo JSON ya validado y la sesión de MySQL
def jb_actualizar_receta(id_receta: int, jb_datos: JbRecetaActualizar, jb_sesion: JbSesion):
    """**Roles:** ADMIN, COCINERO."""
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(jb_sesion, id_receta, jb_datos.model_dump())


# DELETE /api/v1/recetas/{id}: borra una línea
@jb_router.delete("/{id_receta}", response_model=JbResultadoEliminacion, summary="Eliminar una línea de receta",
                  responses=JB_R404)  # errores que puede responder
# Recibe el id_receta de la URL y la sesión de MySQL
def jb_eliminar_receta(id_receta: int, jb_sesion: JbSesion):
    """La receta es configuración, no un movimiento: se borra directamente. **Roles:** ADMIN, COCINERO."""
    # Pide el borrado al servicio
    return jb_servicio.jb_eliminar(jb_sesion, id_receta)
