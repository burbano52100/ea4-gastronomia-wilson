"""Endpoints de reportes de ventas (RF11). Roles: ADMIN."""
# date: solo fecha
from datetime import date

# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); Query: parámetros después del ?
from fastapi import APIRouter, Depends, Query

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R400
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Esquemas de las respuestas de los reportes
from app.schemas.jb_reporte_schema import JbProductoVendido, JbReporteVentas
# Servicio de reportes, con el nombre corto jb_servicio
from app.services import jb_reporte_service as jb_servicio

# Router: rutas /reportes; TODOS sus endpoints exigen ADMIN
jb_router = APIRouter(prefix="/reportes", tags=["Reportes"], responses=JB_PRIVADO,
                      dependencies=[Depends(jb_requiere_roles("ADMIN"))])


# GET /api/v1/reportes/ventas?desde=AAAA-MM-DD&hasta=AAAA-MM-DD
@jb_router.get("/ventas", response_model=JbReporteVentas, summary="Ventas por rango de fechas", responses=JB_R400)
def jb_reporte_ventas(
    # desde: fecha obligatoria después del ?; description y examples son la ayuda de Swagger
    desde: date = Query(description="Fecha inicial (AAAA-MM-DD)", examples=["2026-10-01"]),
    # hasta: fecha obligatoria después del ?
    hasta: date = Query(description="Fecha final (AAAA-MM-DD)", examples=["2026-10-31"]),
):
    """Total vendido, número de pedidos y ticket promedio de los pedidos ENTREGADOS en el rango.

    **Roles:** ADMIN.
    """
    # Pide el reporte al servicio
    return jb_servicio.jb_ventas(desde, hasta)


# GET /api/v1/reportes/productos-mas-vendidos?limite=10
@jb_router.get("/productos-mas-vendidos", response_model=list[JbProductoVendido],
               summary="Ranking de productos más vendidos")
# limite viene después del ?; si no se envía vale 10; debe estar entre 1 y 100
def jb_reporte_mas_vendidos(limite: int = Query(10, ge=1, le=100, description="Cuántos productos mostrar")):
    """Productos ordenados por cantidad vendida en pedidos ENTREGADOS. **Roles:** ADMIN."""
    # Pide el ranking al servicio
    return jb_servicio.jb_productos_mas_vendidos(limite)
