"""03 - DCL: crea (o actualiza) el usuario de MongoDB que usa la API, con privilegios mínimos.

Equivale a 03_dcl_usuarios.sql (CREATE USER + GRANT). El usuario solo recibe el rol readWrite
sobre bd_gastronomia y bd_gastronomia_nosql: puede leer y escribir datos, pero no puede crear
usuarios, borrar bases de datos ni administrar el servidor (no es root).

Uso: python database/03_jb_dcl_usuarios.py
La contraseña se pide por teclado (o se toma de la variable MONGO_API_PASSWORD) para que no
quede escrita en el código ni en GitHub.
"""
# os: para leer variables de entorno
import os
# sys: para detener el script y modificar la ruta de búsqueda de módulos
import sys
# getpass: pide una contraseña por teclado sin mostrarla en pantalla
from getpass import getpass
# Path: manejo de rutas de archivos
from pathlib import Path

# Agrega la carpeta api_gastronomia a la ruta de Python para poder importar "app"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Nombre del usuario de MongoDB de la API (viene del .env)
from app.core.jb_config import JB_MONGO_API_USUARIO  # noqa: E402
# Las dos bases de datos
from app.database.jb_conexion_mongo import jb_db, jb_db_nosql  # noqa: E402


# Obtiene la contraseña del usuario de MongoDB
def jb_pedir_password() -> str:
    # Primero la busca en la variable de entorno MONGO_API_PASSWORD
    jb_password = os.getenv("MONGO_API_PASSWORD")
    # Si existe...
    if jb_password:
        # ...la usa
        return jb_password
    # Si no, la pide por teclado (no se ve lo que se escribe)
    jb_password = getpass(f"Contraseña para el usuario '{JB_MONGO_API_USUARIO}': ")
    # Si es muy corta o no coincide al repetirla...
    if len(jb_password) < 8 or jb_password != getpass("Repita la contraseña: "):
        # ...avisa
        print("Las contraseñas no coinciden o tienen menos de 8 caracteres.")
        # ...y detiene el script
        sys.exit(1)
    # Devuelve la contraseña
    return jb_password


# Función principal del script
def jb_main() -> None:
    # Permisos del usuario: solo leer y escribir en las dos bases de la API (privilegios mínimos, como GRANT)
    jb_roles = [
        # readWrite en la base principal
        {"role": "readWrite", "db": jb_db.name},
        # readWrite en la base NoSQL
        {"role": "readWrite", "db": jb_db_nosql.name},
    ]
    # Pide la contraseña
    jb_password = jb_pedir_password()
    # El usuario se define en bd_gastronomia: por eso la cadena de conexión usa authSource=bd_gastronomia.
    jb_existe = jb_db.command("usersInfo", JB_MONGO_API_USUARIO)["users"]
    # Si el usuario ya existe...
    if jb_existe:
        # ...le actualiza la contraseña y los permisos
        jb_db.command("updateUser", JB_MONGO_API_USUARIO, pwd=jb_password, roles=jb_roles)
        # Avisa
        print(f"Usuario '{JB_MONGO_API_USUARIO}' actualizado.")
    # Si no existe...
    else:
        # ...lo crea (equivale a CREATE USER + GRANT)
        jb_db.command("createUser", JB_MONGO_API_USUARIO, pwd=jb_password, roles=jb_roles)
        # Avisa
        print(f"Usuario '{JB_MONGO_API_USUARIO}' creado.")
    # Muestra los permisos que quedaron
    print("Privilegios: " + ", ".join(f"{jb_rol['role']} en {jb_rol['db']}" for jb_rol in jb_roles))
    # Muestra la cadena de conexión que se debe poner en el .env
    print("Cadena de conexión para el .env:")
    # <clave> se reemplaza por la contraseña elegida
    print(f"  MONGO_URI=mongodb://{JB_MONGO_API_USUARIO}:<clave>@localhost:27017/?authSource={jb_db.name}")


# Solo se ejecuta si se corre el archivo directamente
if __name__ == "__main__":
    # Llama a la función principal
    jb_main()
