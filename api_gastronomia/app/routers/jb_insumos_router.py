"""Endpoints de insumos (RF07). Roles: ADMIN, COCINERO."""
# Annotated: agrega información extra a un tipo
from typing import Annotated

# APIRouter: agrupa endpoints; Depends: dependencias; Query: parámetros después del ?; status: códigos HTTP
from fastapi import APIRouter, Depends, Query, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Sesión de MySQL
from app.database.jb_conexion_mysql import JbSesion
# Esquemas de insumos
from app.schemas.jb_insumo_schema import (
    JbInsumoActualizar,  # datos para modificar
    JbInsumoCrear,  # datos para crear
    JbInsumoPorVencer,  # forma de un insumo por vencer
    JbInsumoRespuesta,  # forma de la respuesta
    JbInsumoStockBajo,  # forma de un insumo con stock bajo
)
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de insumos, con el nombre corto jb_servicio
from app.services import jb_insumo_service as jb_servicio

# Router: rutas /insumos; TODOS sus endpoints exigen ADMIN o COCINERO
jb_router = APIRouter(
    # Prefijo de las rutas
    prefix="/insumos",
    # Sección de Swagger
    tags=["Insumos"],
    # Seguridad de todo el router
    dependencies=[Depends(jb_requiere_roles("ADMIN", "COCINERO"))],
    # Errores 401 y 403 en todos los endpoints
    responses=JB_PRIVADO,
)


# GET /api/v1/insumos/stock-bajo: va ANTES de /{id_insumo}; si no, FastAPI tomaría "stock-bajo" como un id
@jb_router.get("/stock-bajo", response_model=list[JbInsumoStockBajo], summary="Insumos con stock bajo")
# Recibe la sesión de MySQL
def jb_insumos_stock_bajo(jb_sesion: JbSesion):
    """Insumos ACTIVOS con `stock_actual` menor o igual a `stock_minimo`, con lo que falta (RF07).

    **Roles:** ADMIN, COCINERO.
    """
    # Pide la consulta al servicio
    return jb_servicio.jb_stock_bajo(jb_sesion)


# GET /api/v1/insumos/por-vencer?dias=7: también va antes de /{id_insumo}
@jb_router.get("/por-vencer", response_model=list[JbInsumoPorVencer], summary="Insumos próximos a vencer")
# Recibe la sesión de MySQL y el parámetro dias de la consulta
def jb_insumos_por_vencer(
    # Sesión de MySQL
    jb_sesion: JbSesion,
    # ?dias=N: entre 0 y 365; 7 si no se envía
    dias: Annotated[int, Query(ge=0, le=365, description="Cantidad de días hacia adelante (0 = vencen hoy)")] = 7,
):
    """Insumos ACTIVOS que vencen entre hoy y hoy + `dias` (ambos incluidos), con los días que les quedan (RF07).

    **Roles:** ADMIN, COCINERO.
    """
    # Pide la consulta al servicio
    return jb_servicio.jb_por_vencer(jb_sesion, dias)


# GET /api/v1/insumos: lista todos
@jb_router.get("", response_model=list[JbInsumoRespuesta], summary="Listar insumos")
# Recibe la sesión de MySQL
def jb_listar_insumos(jb_sesion: JbSesion):
    """**Roles:** ADMIN, COCINERO."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar(jb_sesion)


# GET /api/v1/insumos/{id}: consulta uno
@jb_router.get("/{id_insumo}", response_model=JbInsumoRespuesta, summary="Consultar un insumo", responses=JB_R404)
# Recibe el id_insumo de la URL y la sesión de MySQL
def jb_obtener_insumo(id_insumo: int, jb_sesion: JbSesion):
    """**Roles:** ADMIN, COCINERO."""
    # Busca el insumo (404 si no existe)
    return jb_servicio.jb_obtener(jb_sesion, id_insumo)


# POST /api/v1/insumos: crea uno (201)
@jb_router.post("", response_model=JbInsumoRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Crear insumo", responses=JB_R409)  # título en Swagger y errores que puede responder
# Recibe el cuerpo JSON ya validado y la sesión de MySQL
def jb_crear_insumo(jb_datos: JbInsumoCrear, jb_sesion: JbSesion):
    """El nombre no se repite. El stock y el costo no pueden ser negativos. **Roles:** ADMIN, COCINERO."""
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_sesion, jb_datos.model_dump())


# PUT /api/v1/insumos/{id}: modifica uno
@jb_router.put("/{id_insumo}", response_model=JbInsumoRespuesta, summary="Actualizar insumo",
               responses={**JB_R404, **JB_R409})  # errores que puede responder
# Recibe el id_insumo de la URL, el cuerpo JSON ya validado y la sesión de MySQL
def jb_actualizar_insumo(id_insumo: int, jb_datos: JbInsumoActualizar, jb_sesion: JbSesion):
    """Sirve también para ajustar el inventario a mano (por ejemplo, después de un conteo).

    **Roles:** ADMIN, COCINERO.
    """
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(jb_sesion, id_insumo, jb_datos.model_dump())


# DELETE /api/v1/insumos/{id}: elimina o inactiva uno
@jb_router.delete("/{id_insumo}", response_model=JbResultadoEliminacion, summary="Eliminar insumo", responses=JB_R404)
# Recibe el id_insumo de la URL y la sesión de MySQL
def jb_eliminar_insumo(id_insumo: int, jb_sesion: JbSesion):
    """RN04: si el insumo aparece en compras o recetas pasa a INACTIVO; si no, se borra.

    **Roles:** ADMIN, COCINERO.
    """
    # El servicio decide si es borrado lógico o físico
    return jb_servicio.jb_eliminar(jb_sesion, id_insumo)
