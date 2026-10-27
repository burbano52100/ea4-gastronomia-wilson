"""Consultas a la colección calificaciones de MongoDB (RF12)."""
# ObjectId: tipo del id que MongoDB pone a cada documento
from bson import ObjectId
# ReturnDocument: indica si find_one_and_update devuelve el documento antes o después del cambio
from pymongo import ReturnDocument

# Colección de calificaciones
from app.database.jb_conexion_mongo import jb_coleccion_calificaciones


# Lista todas las calificaciones, de la más reciente a la más antigua
def jb_listar() -> list[dict]:
    # db.calificaciones.find().sort({fecha: -1})
    return list(jb_coleccion_calificaciones().find().sort("fecha", -1))


# Busca una calificación por su id
def jb_buscar(jb_id: str) -> dict | None:
    # db.calificaciones.findOne({_id: ObjectId(id)}); None si no existe
    return jb_coleccion_calificaciones().find_one({"_id": ObjectId(jb_id)})


# Inserta una calificación nueva
def jb_insertar(jb_documento: dict) -> dict:
    """db.calificaciones.insertOne(documento). Si el pedido ya tenía calificación, MongoDB lanza
    DuplicateKeyError por el índice único uq_calificaciones_pedido."""
    # insert_one agrega el campo _id al mismo diccionario
    jb_coleccion_calificaciones().insert_one(jb_documento)
    # Devuelve el documento ya con su _id
    return jb_documento


# Cambia algunos campos de una calificación
def jb_actualizar(jb_id: str, jb_cambios: dict) -> dict | None:
    # db.calificaciones.findOneAndUpdate({_id}, {$set: cambios}) y devuelve el documento ya cambiado
    return jb_coleccion_calificaciones().find_one_and_update(
        # Documento a cambiar
        {"_id": ObjectId(jb_id)},
        # $set solo cambia los campos indicados
        {"$set": jb_cambios},
        # Devuelve el documento después del cambio
        return_document=ReturnDocument.AFTER,
    )


# Borra una calificación
def jb_eliminar(jb_id: str) -> bool:
    # db.calificaciones.deleteOne({_id}); True si borró un documento
    return jb_coleccion_calificaciones().delete_one({"_id": ObjectId(jb_id)}).deleted_count == 1


# Calificaciones que recibió un producto
def jb_por_producto(jb_id_producto: int) -> list[dict]:
    """Agregación: deja una fila por cada vez que el producto fue calificado, con su nota."""
    # Etapas de la agregación (se ejecutan en orden)
    jb_etapas = [
        # 1. Documentos donde aparece el producto (usa el índice idx_calificaciones_producto)
        {"$match": {"productos.id_producto": jb_id_producto}},
        # 2. Separa la lista productos: un documento por cada producto calificado
        {"$unwind": "$productos"},
        # 3. Se queda solo con el producto pedido
        {"$match": {"productos.id_producto": jb_id_producto}},
        # 4. Deja los campos que se responden; calificacion es la nota de ese producto
        {"$project": {
            "id_pedido": 1, "id_cliente": 1, "fecha": 1, "comentario": 1, "calificacion": "$productos.calificacion",  # 1 = incluir el campo
        }},
        # 5. De la más reciente a la más antigua
        {"$sort": {"fecha": -1}},
    ]
    # Ejecuta la agregación y devuelve la lista
    return list(jb_coleccion_calificaciones().aggregate(jb_etapas))


# Promedio y cantidad de calificaciones de un producto
def jb_resumen_producto(jb_id_producto: int) -> tuple[float | None, int]:
    """Agregación con $group: MongoDB calcula el promedio ($avg) y cuenta las calificaciones ($sum)."""
    # Etapas de la agregación
    jb_etapas = [
        # 1. Documentos donde aparece el producto
        {"$match": {"productos.id_producto": jb_id_producto}},
        # 2. Un documento por cada producto calificado
        {"$unwind": "$productos"},
        # 3. Solo el producto pedido
        {"$match": {"productos.id_producto": jb_id_producto}},
        # 4. Agrupa todo en un solo resultado con el promedio y la cantidad
        {"$group": {"_id": None, "promedio": {"$avg": "$productos.calificacion"}, "total": {"$sum": 1}}},
    ]
    # Ejecuta la agregación; si el producto no tiene calificaciones, no hay resultados
    jb_resultado = next(jb_coleccion_calificaciones().aggregate(jb_etapas), None)
    # Sin calificaciones: promedio None y total 0
    if jb_resultado is None:
        # Devuelve promedio None y cantidad 0
        return None, 0
    # Devuelve el promedio y la cantidad
    return jb_resultado["promedio"], jb_resultado["total"]
