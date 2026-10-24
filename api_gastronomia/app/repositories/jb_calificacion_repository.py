"""Acceso a la colección calificaciones, que vive en la base NoSQL (bd_gastronomia_nosql)."""
# jb_db_nosql: la base NoSQL
from app.database.jb_conexion_mongo import jb_db_nosql
# Clase con el CRUD genérico
from app.repositories.jb_base_repository import JbRepositorioBase


# Repositorio de calificaciones: hereda el CRUD y agrega el resumen por producto
class JbCalificacionRepository(JbRepositorioBase):
    # Constructor
    def __init__(self):
        # Colección "calificaciones", id "id_calificacion", en la base NoSQL
        super().__init__("calificaciones", "id_calificacion", jb_base=jb_db_nosql)

    # Calcula el promedio y la lista de calificaciones de un producto
    def jb_resumen_producto(self, jb_id_producto: int) -> dict | None:
        """Promedio y lista de calificaciones de un producto, calculados con una agregación."""
        # aggregate ejecuta una lista de etapas en orden; list() trae todos los resultados
        jb_resultado = list(self.jb_coleccion.aggregate([
            # $unwind: un documento por cada producto calificado (separa la lista "productos")
            {"$unwind": "$productos"},
            # $match: deja solo las filas del producto pedido (WHERE)
            {"$match": {"productos.id_producto": jb_id_producto}},
            # $sort: de la más reciente a la más antigua
            {"$sort": {"fecha": -1}},
            # $group: junta todas las filas en un solo resultado (GROUP BY)
            {"$group": {
                # Se agrupa por el id del producto
                "_id": "$productos.id_producto",
                # $avg: promedio de las calificaciones
                "promedio": {"$avg": "$productos.calificacion"},
                # $sum 1: cuenta cuántas calificaciones hay
                "total_calificaciones": {"$sum": 1},
                # $push: arma una lista con los datos de cada calificación
                "calificaciones": {"$push": {
                    # Id de la calificación
                    "id_calificacion": "$_id",
                    # Pedido calificado
                    "id_pedido": "$id_pedido",
                    # Cliente que calificó
                    "id_cliente": "$id_cliente",
                    # Fecha
                    "fecha": "$fecha",
                    # Calificación que recibió este producto
                    "calificacion": "$productos.calificacion",
                    # Comentario general
                    "comentario": "$comentario",
                }},
            }},
        ]))
        # Si hubo calificaciones devuelve el resumen; si no, None
        return jb_resultado[0] if jb_resultado else None


# Instancia única que usan los servicios
jb_calificacion_repository = JbCalificacionRepository()
