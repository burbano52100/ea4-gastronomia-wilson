"""Configuración de la API leída desde el archivo .env (las claves nunca se escriben en el código)."""
# os: módulo de Python para leer las variables de entorno del sistema
import os

# load_dotenv: función que lee el archivo .env y carga sus valores como variables de entorno
from dotenv import load_dotenv

# Lee el archivo .env de la carpeta del proyecto (si una variable ya existe en el sistema, no la reemplaza)
load_dotenv()

# Dirección del servidor de MongoDB; si no está en el .env se usa la instalación local
JB_MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# Nombre de la base principal (usuarios, productos, pedidos...)
JB_MONGO_DB = os.getenv("MONGO_DB", "bd_gastronomia")
# Nombre de la base NoSQL (calificaciones)
JB_MONGO_DB_NOSQL = os.getenv("MONGO_DB_NOSQL", "bd_gastronomia_nosql")
# Nombre del usuario de MongoDB con privilegios mínimos que crea el script 03 (DCL)
JB_MONGO_API_USUARIO = os.getenv("MONGO_API_USUARIO", "jb_api_gastronomia")

# Clave secreta con la que se firman los tokens JWT; si no está en el .env queda vacía
JB_JWT_SECRET = os.getenv("JWT_SECRET", "")
# Algoritmo de firma del JWT: HS256 usa la misma clave para firmar y para verificar
JB_JWT_ALGORITMO = "HS256"
# Minutos que dura un token; se lee como texto y se convierte en número entero
JB_JWT_MINUTOS = int(os.getenv("JWT_MINUTOS", "60"))

# Si la clave secreta falta o es muy corta, los tokens serían inseguros: la API no arranca
if len(JB_JWT_SECRET) < 32:
    # Detiene la API mostrando en la terminal cómo solucionarlo
    raise RuntimeError(
        # Primera parte del mensaje: qué falta
        "Falta JWT_SECRET en el archivo .env (mínimo 32 caracteres). "
        # Segunda parte: cómo crear el .env
        "Copie .env.example como .env y genere una clave con: "
        # Tercera parte: el comando que genera una clave aleatoria de 64 caracteres
        'python -c "import secrets; print(secrets.token_hex(32))"'
    )
