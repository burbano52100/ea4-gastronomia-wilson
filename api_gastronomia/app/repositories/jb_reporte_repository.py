"""Consultas de reportes con el framework de agregación de MongoDB.

$match = WHERE, $group = GROUP BY, $sort = ORDER BY, $limit = LIMIT, $lookup = JOIN.
"""
# datetime: fecha y hora
from datetime import datetime

# jb_db: la base principal
from app.database.jb_conexion_mongo import jb_db


# Reporte de ventas por rango de fechas (RF11)
def jb_ventas(jb_desde: datetime, jb_hasta: datetime) -> dict | None:
    """Total vendido y número de pedidos ENTREGADOS en un rango de fechas."""
    # aggregate ejecuta las etapas en orden sobre la colección pedidos
    jb_resultado = list(jb_db.pedidos.aggregate([
        # $match: solo pedidos ENTREGADOS con fecha entre desde y hasta (WHERE)
        {"$match": {"estado": "ENTREGADO", "fecha_pedido": {"$gte": jb_desde, "$lte": jb_hasta}}},
        # $group con _id None: un solo grupo con todos; suma los totales y cuenta los pedidos
        {"$group": {"_id": None, "total_vendido": {"$sum": "$total"}, "numero_pedidos": {"$sum": 1}}},
    ]))
    # Si hubo ventas devuelve el resultado; si no, None
    return jb_resultado[0] if jb_resultado else None


# Ranking de productos más vendidos (RF11)
def jb_productos_mas_vendidos(jb_limite: int) -> list[dict]:
    """Ranking de productos por cantidad vendida en pedidos ENTREGADOS."""
    # Ejecuta las etapas y devuelve la lista de resultados
    return list(jb_db.pedidos.aggregate([
        # $match: solo pedidos ENTREGADOS
        {"$match": {"estado": "ENTREGADO"}},
        # $unwind: un documento por cada ítem del detalle
        {"$unwind": "$detalle"},
        # $group: agrupa por producto (GROUP BY id_producto)
        {"$group": {
            # Clave del grupo: el id del producto
            "_id": "$detalle.id_producto",
            # Suma de unidades vendidas
            "cantidad_vendida": {"$sum": "$detalle.cantidad"},
            # Suma del dinero vendido
            "total_vendido": {"$sum": "$detalle.subtotal"},
            # En cuántos pedidos aparece
            "numero_pedidos": {"$sum": 1},
        }},
        # $sort: más unidades primero; si empatan, más dinero primero
        {"$sort": {"cantidad_vendida": -1, "total_vendido": -1}},
        # $limit: solo los primeros N
        {"$limit": jb_limite},
        # $lookup: trae el producto de la colección productos (JOIN) y lo deja en la lista "producto"
        {"$lookup": {"from": "productos", "localField": "_id", "foreignField": "_id", "as": "producto"}},
        # $project: elige y renombra los campos del resultado
        {"$project": {
            # 0 = no mostrar el _id
            "_id": 0,
            # El _id del grupo se muestra como id_producto
            "id_producto": "$_id",
            # Nombre del primer (y único) producto encontrado
            "nombre": {"$first": "$producto.nombre"},
            # 1 = mostrar el campo tal cual
            "cantidad_vendida": 1,
            # Mostrar el total vendido
            "total_vendido": 1,
            # Mostrar el número de pedidos
            "numero_pedidos": 1,
        }},
    ]))
