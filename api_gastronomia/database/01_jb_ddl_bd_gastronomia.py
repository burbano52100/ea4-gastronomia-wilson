"""01 - DDL de bd_gastronomia: crea las colecciones con su validación $jsonSchema y sus índices.

Equivale al script 01_ddl_bd_gastronomia.sql del instructivo, adaptado a MongoDB.

Uso (desde la carpeta api_gastronomia, con el entorno virtual activo):
    python database/01_jb_ddl_bd_gastronomia.py              -> base nueva
    python database/01_jb_ddl_bd_gastronomia.py --reiniciar  -> respalda la base actual y la vuelve a crear
"""
# sys: para leer los argumentos (--reiniciar) y modificar la ruta de búsqueda de módulos
import sys
# Path: manejo de rutas de archivos
from pathlib import Path

# Agrega la carpeta api_gastronomia a la ruta de Python para poder importar "app" y "database"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# La base principal; noqa: E402 le dice al revisor de estilo que este import va aquí a propósito
from app.database.jb_conexion_mongo import jb_db  # noqa: E402
# Definición de las colecciones: validación $jsonSchema e índices
from app.models.jb_modelos import JB_MODELOS  # noqa: E402
# Funciones que respaldan la base y crean las colecciones
from database.jb_utilidades_bd import jb_crear_colecciones, jb_preparar_base  # noqa: E402


# Función principal del script
def jb_main() -> None:
    # Mensaje de inicio con el nombre de la base
    print(f"DDL: creando colecciones en '{jb_db.name}'")
    # Si la base ya tiene colecciones: se detiene, o las respalda y borra si se escribió --reiniciar
    jb_preparar_base(jb_db, "--reiniciar" in sys.argv)
    # Crea las colecciones con su validación e índices
    jb_crear_colecciones(jb_db, JB_MODELOS)
    # Mensaje final
    print("DDL terminado.")


# Solo se ejecuta si se corre el archivo directamente
if __name__ == "__main__":
    # Llama a la función principal
    jb_main()
