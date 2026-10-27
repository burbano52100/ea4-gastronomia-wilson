"""Endpoints de reportes (RF11). Roles: solo ADMIN."""
# date: solo fecha
from datetime import date
# Annotated: agrega información extra a un tipo
from typing import Annotated

# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); Query: parámetros después del ?
from fastapi import APIRouter, Depends, Query

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R400
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Sesión de MySQL
from app.database.jb_conexion_mysql import JbSesion
# Esquemas de los reportes
from app.schemas.jb_reporte_schema import JbProductoVendido, JbReporteVentas
# Servicio de reportes, con el nombre corto jb_servicio
from app.services import jb_reporte_service as jb_servicio

# Router: rutas /reportes; TODOS sus endpoints exigen ADMIN (información de ventas para decidir)
jb_router = APIRouter(
    # Prefijo de las rutas
    prefix="/reportes",
    # Sección de Swagger
    tags=["Reportes"],
    # Seguridad de todo el router
    dependencies=[Depends(jb_requiere_roles("ADMIN"))],
    # Errores 401 y 403 en todos los endpoints
    responses=JB_PRIVADO,
)


# GET /api/v1/reportes/ventas?desde=AAAA-MM-DD&hasta=AAAA-MM-DD
@jb_router.get("/ventas", response_model=JbReporteVentas, summary="Ventas por rango de fechas", responses=JB_R400)
# Recibe la sesión de MySQL, el parámetro desde de la consulta y el parámetro hasta de la consulta
def jb_reporte_ventas(
    # Sesión de MySQL
    jb_sesion: JbSesion,
    # Fecha inicial (obligatoria)
    desde: Annotated[date, Query(description="Fecha inicial, AAAA-MM-DD (incluida)")],
    # Fecha final (obligatoria)
    hasta: Annotated[date, Query(description="Fecha final, AAAA-MM-DD (incluida completa)")],
):
    """Total vendido y número de pedidos entre dos fechas. Solo cuentan los pedidos ENTREGADO (los anulados
    no son ventas). El día `hasta` se incluye completo. Si `desde` es posterior a `hasta` responde 400.

    **Roles:** ADMIN.
    """
    # Pide el reporte al servicio
    return jb_servicio.jb_ventas(jb_sesion, desde, hasta)


# GET /api/v1/reportes/productos-mas-vendidos?limite=10
@jb_router.get("/productos-mas-vendidos", response_model=list[JbProductoVendido], summary="Productos más vendidos")
# Recibe la sesión de MySQL y el parámetro limite de la consulta
def jb_productos_mas_vendidos(
    # Sesión de MySQL
    jb_sesion: JbSesion,
    # ?limite=N: entre 1 y 100; 10 si no se envía
    limite: Annotated[int, Query(ge=1, le=100, description="Cuántos productos mostrar")] = 10,
):
    """Ranking por unidades vendidas en pedidos ENTREGADO (si empatan, por dinero vendido).

    **Roles:** ADMIN.
    """
    # Pide el ranking al servicio
    return jb_servicio.jb_mas_vendidos(jb_sesion, limite)
