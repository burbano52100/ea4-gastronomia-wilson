"""Endpoints de insumos del inventario (RF07). Roles: ADMIN, COCINERO."""
# APIRouter: agrupa endpoints; Depends: seguridad; Query: parámetros después del ?; status: códigos HTTP
from fastapi import APIRouter, Depends, Query, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Esquemas de insumos (lo que entra y lo que sale)
from app.schemas.jb_insumo_schema import JbInsumoActualizar, JbInsumoCrear, JbInsumoRespuesta
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de insumos, con el nombre corto jb_servicio
from app.services import jb_insumo_service as jb_servicio

# Router: rutas /insumos; TODOS sus endpoints exigen ADMIN o COCINERO
jb_router = APIRouter(prefix="/insumos", tags=["Insumos"], responses=JB_PRIVADO,
                      dependencies=[Depends(jb_requiere_roles("ADMIN", "COCINERO"))])


# GET /api/v1/insumos: lista todos
@jb_router.get("", response_model=list[JbInsumoRespuesta], summary="Listar insumos")
def jb_listar_insumos():
    """**Roles:** ADMIN, COCINERO."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar()


# Las rutas fijas (/stock-bajo, /por-vencer) van ANTES de /{id_insumo}; si no, FastAPI
# intentaría convertir "stock-bajo" en número y respondería 422.
@jb_router.get("/stock-bajo", response_model=list[JbInsumoRespuesta], summary="Insumos con stock bajo")
def jb_insumos_stock_bajo():
    """Insumos ACTIVOS con `stock_actual <= stock_minimo`. **Roles:** ADMIN, COCINERO."""
    # Pide la consulta al servicio
    return jb_servicio.jb_stock_bajo()


# GET /api/v1/insumos/por-vencer?dias=7
@jb_router.get("/por-vencer", response_model=list[JbInsumoRespuesta], summary="Insumos próximos a vencer")
# dias viene después del ?; si no se envía vale 7; debe estar entre 1 y 365
def jb_insumos_por_vencer(dias: int = Query(7, ge=1, le=365, description="Cantidad de días hacia adelante")):
    """Insumos que vencen entre hoy y dentro de `dias` días. **Roles:** ADMIN, COCINERO."""
    # Pide la consulta al servicio
    return jb_servicio.jb_por_vencer(dias)


# GET /api/v1/insumos/{id}: consulta uno
@jb_router.get("/{id_insumo}", response_model=JbInsumoRespuesta, summary="Consultar un insumo", responses=JB_R404)
def jb_obtener_insumo(id_insumo: int):
    """**Roles:** ADMIN, COCINERO."""
    # Busca el insumo (404 si no existe)
    return jb_servicio.jb_obtener(id_insumo)


# POST /api/v1/insumos: crea uno (201)
@jb_router.post("", response_model=JbInsumoRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Crear insumo", responses=JB_R409)
# El cuerpo se valida con JbInsumoCrear
def jb_crear_insumo(jb_datos: JbInsumoCrear):
    """El stock no puede ser negativo y el nombre no se repite. **Roles:** ADMIN, COCINERO."""
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_datos.model_dump())


# PUT /api/v1/insumos/{id}: modifica uno
@jb_router.put("/{id_insumo}", response_model=JbInsumoRespuesta, summary="Actualizar insumo",
               responses={**JB_R404, **JB_R409})
# Recibe el id de la URL y el cuerpo validado con JbInsumoActualizar
def jb_actualizar_insumo(id_insumo: int, jb_datos: JbInsumoActualizar):
    """**Roles:** ADMIN, COCINERO."""
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(id_insumo, jb_datos.model_dump())


# DELETE /api/v1/insumos/{id}: elimina o inactiva uno
@jb_router.delete("/{id_insumo}", response_model=JbResultadoEliminacion, summary="Eliminar insumo",
                  responses=JB_R404)
def jb_eliminar_insumo(id_insumo: int):
    """RN04: si el insumo está en recetas o compras pasa a INACTIVO; si no, se elimina.

    **Roles:** ADMIN, COCINERO.
    """
    # El servicio decide si es borrado lógico o físico
    return jb_servicio.jb_eliminar(id_insumo)
