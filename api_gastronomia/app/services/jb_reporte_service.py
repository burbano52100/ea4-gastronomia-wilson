"""Reportes de ventas (RF11). Solo cuentan los pedidos ENTREGADOS."""
# date: solo fecha
from datetime import date
# Decimal: números exactos para dinero
from decimal import Decimal

# Funciones de apoyo: redondeo de dinero, fin del día e inicio del día
from app.core.jb_utilidades import jb_dinero, jb_fin_del_dia, jb_inicio_del_dia
# Módulo con las consultas de reportes
from app.repositories import jb_reporte_repository
# Error 400
from app.services.jb_comun import jb_dato_invalido


# Reporte de ventas entre dos fechas
def jb_ventas(jb_desde: date, jb_hasta: date) -> dict:
    # Si el rango está al revés...
    if jb_desde > jb_hasta:
        # ...responde 400
        raise jb_dato_invalido("La fecha 'desde' no puede ser mayor que 'hasta'")
    # Consulta desde el inicio del primer día hasta el final del último día
    jb_resultado = jb_reporte_repository.jb_ventas(jb_inicio_del_dia(jb_desde), jb_fin_del_dia(jb_hasta))
    # Total vendido; 0 si no hubo ventas
    jb_total = jb_resultado["total_vendido"] if jb_resultado else Decimal("0")
    # Número de pedidos; 0 si no hubo ventas
    jb_numero = jb_resultado["numero_pedidos"] if jb_resultado else 0
    # Arma la respuesta (forma de JbReporteVentas)
    return {
        # Fecha inicial
        "desde": jb_desde,
        # Fecha final
        "hasta": jb_hasta,
        # Número de pedidos
        "numero_pedidos": jb_numero,
        # Total vendido con 2 decimales
        "total_vendido": jb_dinero(jb_total),
        # Promedio por pedido; si no hubo pedidos, 0 (para no dividir por cero)
        "ticket_promedio": jb_dinero(jb_total / jb_numero) if jb_numero else Decimal("0.00"),
    }


# Ranking de productos más vendidos
def jb_productos_mas_vendidos(jb_limite: int) -> list[dict]:
    # Arma una lista agregando la posición (1, 2, 3...) a cada fila del ranking
    return [
        # La posición más todos los campos de la fila (** copia los campos del diccionario)
        {"posicion": jb_posicion, **jb_fila}
        # enumerate numera las filas empezando en 1
        for jb_posicion, jb_fila in enumerate(jb_reporte_repository.jb_productos_mas_vendidos(jb_limite), start=1)
    ]
