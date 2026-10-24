"""Conexión a MongoDB.

Se usan dos bases de datos, igual que en el instructivo:
- bd_gastronomia: la información estructurada (usuarios, productos, pedidos, compras...).
- bd_gastronomia_nosql: la información no estructurada (calificaciones de los clientes).
"""
# Decimal: el tipo de Python para números exactos (dinero y cantidades)
from decimal import Decimal

# Herramientas de pymongo para decir cómo convertir tipos de Python a tipos de MongoDB (BSON)
from bson.codec_options import CodecOptions, TypeCodec, TypeRegistry
# Decimal128: el tipo decimal exacto de MongoDB
from bson.decimal128 import Decimal128
# MongoClient: la conexión al servidor; ReturnDocument: indica si devolver el documento antes o después de cambiarlo
from pymongo import MongoClient, ReturnDocument

# Datos de conexión que vienen del .env
from app.core.jb_config import JB_MONGO_DB, JB_MONGO_DB_NOSQL, JB_MONGO_URI


# Clase que le enseña a pymongo a guardar y leer valores Decimal
class JbDecimalCodec(TypeCodec):
    """Guarda los Decimal de Python como Decimal128 (el equivalente de DECIMAL en SQL) y los lee de vuelta."""

    # Tipo de Python que se convierte
    python_type = Decimal
    # Tipo de MongoDB en el que se guarda
    bson_type = Decimal128

    # Se ejecuta al GUARDAR: Decimal de Python -> Decimal128 de MongoDB
    def transform_python(self, jb_valor):
        # Crea el Decimal128 con el mismo valor
        return Decimal128(jb_valor)

    # Se ejecuta al LEER: Decimal128 de MongoDB -> Decimal de Python
    def transform_bson(self, jb_valor):
        # to_decimal() devuelve el valor como Decimal de Python
        return jb_valor.to_decimal()


# Opciones de conexión que registran el convertidor de decimales
jb_opciones = CodecOptions(type_registry=TypeRegistry([JbDecimalCodec()]))
# Conexión al servidor de MongoDB; si en 5 segundos no responde, se produce un error
jb_cliente = MongoClient(JB_MONGO_URI, serverSelectionTimeoutMS=5000)
# Base principal (bd_gastronomia), usando el convertidor de decimales
jb_db = jb_cliente.get_database(JB_MONGO_DB, codec_options=jb_opciones)
# Base NoSQL (bd_gastronomia_nosql), usando el convertidor de decimales
jb_db_nosql = jb_cliente.get_database(JB_MONGO_DB_NOSQL, codec_options=jb_opciones)


# Función que entrega el siguiente número de id de una colección
def jb_siguiente_id(jb_coleccion: str, jb_base=jb_db) -> int:
    """Devuelve el siguiente id numérico (1, 2, 3...) de una colección, como un AUTO_INCREMENT."""
    # Busca el contador de la colección en "contadores", le suma 1 y lo devuelve, en una sola operación
    jb_contador = jb_base.contadores.find_one_and_update(
        # Cuál contador: el que tiene como _id el nombre de la colección
        {"_id": jb_coleccion},
        # Qué hacer: sumar 1 al campo "valor" ($inc = incrementar)
        {"$inc": {"valor": 1}},
        # Si el contador no existe todavía, lo crea (empieza en 1)
        upsert=True,
        # Devuelve el contador DESPUÉS de sumarle 1
        return_document=ReturnDocument.AFTER,
    )
    # Devuelve el número nuevo
    return jb_contador["valor"]
