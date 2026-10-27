"""Reglas de los reportes de ventas (RF11)."""
# date: solo fecha; timedelta: sumar días
from datetime import date, timedelta

# Session: sesión de trabajo con MySQL
from sqlalchemy.orm import Session

# Inicio del día y redondeo de dinero
from app.core.jb_utilidades import jb_dinero, jb_inicio_del_dia
# Consultas de los reportes
from app.repositories import jb_reporte_repository as jb_repositorio
# Error 400
from app.services.jb_comun import jb_dato_invalido


# Reporte de ventas por rango de fechas (GET /reportes/ventas)
def jb_ventas(jb_sesion: Session, jb_desde: date, jb_hasta: date) -> dict:
    """Cuenta solo pedidos ENTREGADO. El día "hasta" se incluye completo (hasta las 23:59:59)."""
    # Si el rango está al revés...
    if jb_desde > jb_hasta:
        # ...responde 400
        raise jb_dato_invalido("La fecha 'desde' no puede ser posterior a la fecha 'hasta'")
    # Desde las 00:00 del primer día hasta antes de las 00:00 del día siguiente al último
    jb_numero, jb_total = jb_repositorio.jb_ventas(
        # Inicio del rango
        jb_sesion, jb_inicio_del_dia(jb_desde),
        # Fin del rango (sin incluir)
        jb_inicio_del_dia(jb_hasta + timedelta(days=1)),
    )
    # Redondea el total
    jb_total = jb_dinero(jb_total)
    # Devuelve la forma de JbReporteVentas
    return {
        # Fecha inicial
        "desde": jb_desde,
        # Fecha final
        "hasta": jb_hasta,
        # Cantidad de pedidos entregados
        "numero_pedidos": jb_numero,
        # Total vendido
        "total_vendido": jb_total,
        # Promedio por pedido (0 si no hubo pedidos, para no dividir entre 0)
        "promedio_por_pedido": jb_dinero(jb_total / jb_numero) if jb_numero else jb_dinero(0),
    }


# Ranking de productos más vendidos (GET /reportes/productos-mas-vendidos)
def jb_mas_vendidos(jb_sesion: Session, jb_limite: int) -> list[dict]:
    # Pide el ranking al repositorio
    jb_filas = jb_repositorio.jb_mas_vendidos(jb_sesion, jb_limite)
    # Arma cada fila con su posición en el ranking (1, 2, 3...)
    return [
        # Forma de JbProductoVendido
        {
            # Puesto
            "posicion": jb_posicion,
            # Id del producto
            "id_producto": jb_fila.id_producto,
            # Nombre
            "nombre": jb_fila.nombre,
            # Unidades vendidas
            "cantidad_vendida": jb_fila.cantidad_vendida,
            # Dinero vendido
            "total_vendido": jb_fila.total_vendido,
        }
        # Recorre las filas numerándolas desde 1
        for jb_posicion, jb_fila in enumerate(jb_filas, start=1)
    ]
