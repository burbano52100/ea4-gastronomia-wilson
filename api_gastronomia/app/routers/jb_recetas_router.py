"""Endpoints de recetas o fichas técnicas (RF05). Roles: ADMIN, COCINERO."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R400, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Esquemas de recetas (lo que entra y lo que sale)
from app.schemas.jb_receta_schema import JbRecetaCrear, JbRecetaRespuesta
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de recetas, con el nombre corto jb_servicio
from app.services import jb_receta_service as jb_servicio

# Router: rutas /recetas; TODOS sus endpoints exigen ADMIN o COCINERO
jb_router = APIRouter(prefix="/recetas", tags=["Recetas"], responses=JB_PRIVADO,
                      dependencies=[Depends(jb_requiere_roles("ADMIN", "COCINERO"))])


# GET /api/v1/recetas: lista todas las líneas de receta
@jb_router.get("", response_model=list[JbRecetaRespuesta], summary="Listar líneas de receta")
def jb_listar_recetas():
    """Cada documento dice cuánto de un insumo lleva una unidad de un producto. **Roles:** ADMIN, COCINERO."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar()


# GET /api/v1/recetas/{id}: consulta una línea
@jb_router.get("/{id_receta}", response_model=JbRecetaRespuesta, summary="Consultar una línea de receta",
               responses=JB_R404)
def jb_obtener_receta(id_receta: int):
    """**Roles:** ADMIN, COCINERO."""
    # Busca la línea (404 si no existe)
    return jb_servicio.jb_obtener(id_receta)


# POST /api/v1/recetas: agrega un insumo a la receta de un producto (201)
@jb_router.post("", response_model=JbRecetaRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Agregar insumo a la receta de un producto", responses={**JB_R400, **JB_R409})
# El cuerpo se valida con JbRecetaCrear
def jb_crear_receta(jb_datos: JbRecetaCrear):
    """El producto y el insumo deben existir. Un insumo no se repite en la receta de un producto (409).

    **Roles:** ADMIN, COCINERO.
    """
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_datos.model_dump())


# PUT /api/v1/recetas/{id}: modifica una línea
@jb_router.put("/{id_receta}", response_model=JbRecetaRespuesta, summary="Actualizar línea de receta",
               responses={**JB_R400, **JB_R404, **JB_R409})
# Recibe el id de la URL y el cuerpo validado (usa el mismo esquema de crear)
def jb_actualizar_receta(id_receta: int, jb_datos: JbRecetaCrear):
    """**Roles:** ADMIN, COCINERO."""
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(id_receta, jb_datos.model_dump())


# DELETE /api/v1/recetas/{id}: borra una línea
@jb_router.delete("/{id_receta}", response_model=JbResultadoEliminacion, summary="Eliminar línea de receta",
                  responses=JB_R404)
def jb_eliminar_receta(id_receta: int):
    """**Roles:** ADMIN, COCINERO."""
    # Pide al servicio que la borre
    return jb_servicio.jb_eliminar(id_receta)
