"""Consultas de los reportes de ventas (RF11). Solo cuentan los pedidos ENTREGADO."""
# datetime: fecha y hora
from datetime import datetime
# Decimal: números exactos
from decimal import Decimal

# func: funciones de SQL como COUNT y SUM; select: arma un SELECT
from sqlalchemy import func, select
# Session: sesión de trabajo con la base de datos
from sqlalchemy.orm import Session

# Modelos de las tablas que se consultan
from app.models.jb_modelos import JbDetallePedido, JbPedido, JbProducto


# Número de pedidos y total vendido entre dos momentos
def jb_ventas(jb_sesion: Session, jb_inicio: datetime, jb_fin: datetime) -> tuple[int, Decimal]:
    """SELECT COUNT(*), SUM(total) FROM pedidos
    WHERE estado = 'ENTREGADO' AND fecha_pedido >= :inicio AND fecha_pedido < :fin"""
    # Arma la consulta
    jb_consulta = select(
        # Cantidad de pedidos
        func.count(JbPedido.id_pedido),
        # Suma de los totales; COALESCE pone 0 si no hay pedidos (SUM daría NULL)
        func.coalesce(func.sum(JbPedido.total), 0),
    ).where(  # WHERE: las condiciones van abajo
        # Solo pedidos entregados (los anulados no son ventas)
        JbPedido.estado == "ENTREGADO",
        # Desde el inicio del rango (incluido)
        JbPedido.fecha_pedido >= jb_inicio,
        # Hasta antes del fin del rango
        JbPedido.fecha_pedido < jb_fin,
    )
    # Ejecuta la consulta y toma la única fila del resultado
    jb_numero, jb_total = jb_sesion.execute(jb_consulta).one()
    # Devuelve los dos valores
    return int(jb_numero), Decimal(jb_total)


# Ranking de productos más vendidos
def jb_mas_vendidos(jb_sesion: Session, jb_limite: int) -> list:
    """SELECT producto, SUM(cantidad), SUM(subtotal) ... GROUP BY producto ORDER BY SUM(cantidad) DESC LIMIT :limite"""
    # Suma de las cantidades vendidas, con nombre para usarla en el orden
    jb_cantidad = func.sum(JbDetallePedido.cantidad).label("cantidad_vendida")
    # Suma de los subtotales vendidos
    jb_total = func.sum(JbDetallePedido.subtotal).label("total_vendido")
    # Arma la consulta
    jb_consulta = (
        # Columnas del resultado
        select(JbProducto.id_producto, JbProducto.nombre, jb_cantidad, jb_total)
        # Une productos con detalle_pedido
        .join(JbDetallePedido, JbDetallePedido.id_producto == JbProducto.id_producto)
        # Une detalle_pedido con pedidos, para filtrar por estado
        .join(JbPedido, JbPedido.id_pedido == JbDetallePedido.id_pedido)
        # Solo pedidos entregados
        .where(JbPedido.estado == "ENTREGADO")
        # Agrupa por producto
        .group_by(JbProducto.id_producto, JbProducto.nombre)
        # Primero el que más unidades vendió; si empatan, el que más dinero dejó
        .order_by(jb_cantidad.desc(), jb_total.desc(), JbProducto.id_producto)
        # Solo los primeros jb_limite
        .limit(jb_limite)
    )
    # Ejecuta la consulta y devuelve todas las filas
    return list(jb_sesion.execute(jb_consulta).all())
