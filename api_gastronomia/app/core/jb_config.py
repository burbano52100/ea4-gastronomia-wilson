"""Configuración de la API leída desde el archivo .env (las claves nunca se escriben en el código)."""
# os: módulo de Python para leer las variables de entorno del sistema
import os

# load_dotenv: función que lee el archivo .env y carga sus valores como variables de entorno
from dotenv import load_dotenv

# Lee el archivo .env de la carpeta del proyecto (si una variable ya existe en el sistema, no la reemplaza)
load_dotenv()


# Función que lee una variable que no puede faltar
def jb_variable_obligatoria(jb_nombre: str) -> str:
    """Devuelve el valor de la variable; si falta o está vacía, la API no arranca y explica qué hacer."""
    # Lee la variable; si no existe queda como texto vacío
    jb_valor = os.getenv(jb_nombre, "")
    # Si está vacía...
    if not jb_valor:
        # ...detiene la API con un mensaje claro en la terminal
        raise RuntimeError(f"Falta la variable {jb_nombre} en el archivo .env: copie .env.example como .env y complételo")
    # Devuelve el valor leído
    return jb_valor


# ----- MySQL: base de datos principal (bd_gastronomia) -----
# Servidor donde está MySQL
JB_MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
# Puerto de MySQL; se lee como texto y se convierte en número entero
JB_MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
# Usuario de la API con privilegios mínimos (lo crea database/03_jb_dcl_usuarios.sql); nunca root
JB_MYSQL_USUARIO = jb_variable_obligatoria("MYSQL_USUARIO")
# Contraseña de ese usuario
JB_MYSQL_PASSWORD = jb_variable_obligatoria("MYSQL_PASSWORD")
# Nombre de la base de datos
JB_MYSQL_BD = os.getenv("MYSQL_BD", "bd_gastronomia")

# ----- MongoDB: calificaciones (bd_gastronomia_nosql) -----
# Servidor donde está MongoDB
JB_MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
# Puerto de MongoDB (27018 para no chocar con un MongoDB instalado en Windows)
JB_MONGO_PORT = int(os.getenv("MONGO_PORT", "27018"))
# Usuario de la API con permiso solo sobre la colección calificaciones (lo crea el script 04)
JB_MONGO_USUARIO = jb_variable_obligatoria("MONGO_USUARIO")
# Contraseña de ese usuario
JB_MONGO_PASSWORD = jb_variable_obligatoria("MONGO_PASSWORD")
# Nombre de la base de datos (el usuario de la API está creado dentro de ella)
JB_MONGO_BD = os.getenv("MONGO_BD", "bd_gastronomia_nosql")

# ----- JWT: tokens de sesión -----
# Clave secreta con la que se firman los tokens
JB_JWT_SECRET = os.getenv("JWT_SECRET", "")
# Algoritmo de firma: HS256 usa la misma clave para firmar y para verificar
JB_JWT_ALGORITMO = os.getenv("JWT_ALGORITMO", "HS256")
# Minutos que dura un token antes de vencer
JB_JWT_MINUTOS = int(os.getenv("JWT_MINUTOS", "60"))

# Si la clave secreta falta o es muy corta, los tokens serían inseguros: la API no arranca
if len(JB_JWT_SECRET) < 32:
    # Detiene la API mostrando en la terminal cómo solucionarlo
    raise RuntimeError(
        # Primera parte del mensaje: qué falta
        "Falta JWT_SECRET en el archivo .env (mínimo 32 caracteres). "
        # Segunda parte: el comando que genera una clave aleatoria de 64 caracteres
        'Genere una con: python -c "import secrets; print(secrets.token_hex(32))"'
    )

# Solo se aceptan algoritmos HMAC; así nadie puede configurar uno inseguro como "none"
if JB_JWT_ALGORITMO not in ("HS256", "HS384", "HS512"):
    # Detiene la API explicando qué valores sirven
    raise RuntimeError("JWT_ALGORITMO en el .env debe ser HS256, HS384 o HS512")
