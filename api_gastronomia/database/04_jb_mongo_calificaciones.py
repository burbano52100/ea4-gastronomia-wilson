"""04 - MongoDB NoSQL: colección calificaciones en bd_gastronomia_nosql.

Equivale a 04_mongo_calificaciones.js: crea la colección con validación $jsonSchema, sus índices
y guarda el documento de ejemplo que trae el instructivo.

El ejemplo del instructivo habla del pedido 125, el cliente 18 y los productos 4 y 9, que no
existen en bd_gastronomia porque el instructivo no da sus datos. MongoDB no tiene llaves
foráneas, así que el documento se guarda igual y sirve para ver su estructura en Compass.

Uso: python database/04_jb_mongo_calificaciones.py [--reiniciar]
"""
# sys: para leer los argumentos (--reiniciar) y modificar la ruta de búsqueda de módulos
import sys
# datetime: fecha y hora
from datetime import datetime
# Path: manejo de rutas de archivos
from pathlib import Path

# Agrega la carpeta api_gastronomia a la ruta de Python para poder importar "app" y "database"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# La base NoSQL, donde se crean las calificaciones
from app.database.jb_conexion_mongo import jb_db_nosql  # noqa: E402
# Definición de la colección calificaciones: validación $jsonSchema e índices
from app.models.jb_modelos import JB_MODELOS_NOSQL  # noqa: E402
# Funciones que ajustan contadores, crean colecciones y respaldan la base
from database.jb_utilidades_bd import jb_ajustar_contadores, jb_crear_colecciones, jb_preparar_base  # noqa: E402

# Documento de ejemplo del instructivo (sección "Colección en MongoDB"), con _id 1
JB_CALIFICACION_INSTRUCTIVO = {
    # Id numérico
    "_id": 1,
    # Pedido calificado
    "id_pedido": 125,
    # Cliente que calificó
    "id_cliente": 18,
    # Fecha y hora: "2026-10-20T12:30:00"
    "fecha": datetime(2026, 10, 20, 12, 30),
    # Calificación del servicio, de 1 a 5
    "calificacion_servicio": 5,
    # Comentario
    "comentario": "Excelente atención y buen sabor",
    # Calificación de cada producto del pedido
    "productos": [
        # Primer producto calificado
        {"id_producto": 4, "nombre": "Almuerzo ejecutivo", "calificacion": 5},
        # Segundo producto calificado
        {"id_producto": 9, "nombre": "Jugo de lulo", "calificacion": 4},
    ],
}


# Función principal del script
def jb_main() -> None:
    # Mensaje de inicio con el nombre de la base NoSQL
    print(f"NoSQL: creando la colección calificaciones en '{jb_db_nosql.name}'")
    # Si la base ya tiene colecciones: se detiene, o las respalda y borra si se escribió --reiniciar
    jb_preparar_base(jb_db_nosql, "--reiniciar" in sys.argv)
    # Crea la colección calificaciones con su validación e índices
    jb_crear_colecciones(jb_db_nosql, JB_MODELOS_NOSQL)
    # Guarda el documento de ejemplo del instructivo (la validación $jsonSchema lo revisa)
    jb_db_nosql.calificaciones.insert_one(JB_CALIFICACION_INSTRUCTIVO)
    # Deja el contador de calificaciones en el último id (la siguiente será la 2)
    jb_ajustar_contadores(jb_db_nosql, ["calificaciones"])
    # Muestra cuántas calificaciones quedaron
    print(f"  [OK] calificaciones: {jb_db_nosql.calificaciones.count_documents({})} documento (el ejemplo del instructivo)")
    # Mensaje final
    print("Script NoSQL terminado.")


# Solo se ejecuta si se corre el archivo directamente
if __name__ == "__main__":
    # Llama a la función principal
    jb_main()
