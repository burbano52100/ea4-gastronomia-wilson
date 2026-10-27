"""Conexión a MongoDB con PyMongo (colección calificaciones), con el usuario de la API (nunca root)."""
# MongoClient: cliente que se conecta al servidor de MongoDB
from pymongo import MongoClient
# Collection: tipo de una colección de MongoDB
from pymongo.collection import Collection

# Datos de conexión leídos del .env
from app.core.jb_config import JB_MONGO_BD, JB_MONGO_HOST, JB_MONGO_PASSWORD, JB_MONGO_PORT, JB_MONGO_USUARIO
# Zona horaria de Colombia
from app.core.jb_utilidades import JB_ZONA_BOGOTA

# Cliente de MongoDB. No se conecta todavía: lo hace en la primera consulta
jb_cliente_mongo = MongoClient(
    # Servidor
    host=JB_MONGO_HOST,
    # Puerto
    port=JB_MONGO_PORT,
    # Usuario de la API (del .env)
    username=JB_MONGO_USUARIO,
    # Contraseña (del .env); se pasa aparte, así no hay problemas con caracteres especiales
    password=JB_MONGO_PASSWORD,
    # Base donde está creado el usuario (el script 04 lo crea en bd_gastronomia_nosql)
    authSource=JB_MONGO_BD,
    # Si MongoDB no responde en 3 segundos, se da por apagado
    serverSelectionTimeoutMS=3000,
    # Las fechas se leen con zona horaria...
    tz_aware=True,
    # ...y se entregan en hora de Colombia (MongoDB las guarda en UTC)
    tzinfo=JB_ZONA_BOGOTA,
)

# Base de datos de las calificaciones
jb_bd_mongo = jb_cliente_mongo[JB_MONGO_BD]


# Función que devuelve la colección de calificaciones
def jb_coleccion_calificaciones() -> Collection:
    # La colección la crea el script 04 con su validador $jsonSchema
    return jb_bd_mongo["calificaciones"]
