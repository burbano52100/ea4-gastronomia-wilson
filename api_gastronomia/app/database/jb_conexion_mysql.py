"""Conexión a MySQL con SQLAlchemy, usando el usuario de la API con privilegios mínimos (nunca root)."""
# Iterator: tipo de una función que entrega valores con yield
from collections.abc import Iterator
# Annotated: agrega información extra a un tipo
from typing import Annotated

# Depends: le dice a FastAPI que ejecute una dependencia
from fastapi import Depends
# URL: arma la dirección de conexión; create_engine: crea el motor que maneja las conexiones
from sqlalchemy import URL, create_engine
# DeclarativeBase: base de los modelos; Session: sesión de trabajo; sessionmaker: fábrica de sesiones
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Datos de conexión leídos del .env
from app.core.jb_config import JB_MYSQL_BD, JB_MYSQL_HOST, JB_MYSQL_PASSWORD, JB_MYSQL_PORT, JB_MYSQL_USUARIO

# Dirección de conexión. URL.create se encarga de los caracteres especiales de la contraseña
jb_url_mysql = URL.create(
    # Motor MySQL con el conector PyMySQL
    drivername="mysql+pymysql",
    # Usuario de la API (del .env)
    username=JB_MYSQL_USUARIO,
    # Contraseña (del .env)
    password=JB_MYSQL_PASSWORD,
    # Servidor
    host=JB_MYSQL_HOST,
    # Puerto
    port=JB_MYSQL_PORT,
    # Base de datos
    database=JB_MYSQL_BD,
    # utf8mb4: tildes y eñes llegan bien
    query={"charset": "utf8mb4"},
)

# Motor: guarda un grupo de conexiones abiertas y las reutiliza
jb_motor = create_engine(
    # Dirección de conexión
    jb_url_mysql,
    # Antes de usar una conexión revisa que siga viva (por si MySQL se reinició)
    pool_pre_ping=True,
    # Renueva las conexiones cada hora
    pool_recycle=3600,
    # Opciones que se pasan a PyMySQL al abrir cada conexión
    connect_args={
        # Cada conexión trabaja en hora de Colombia (UTC-5): NOW() y CURDATE() dan la hora de Bogotá
        "init_command": "SET time_zone = '-05:00'",
        # Si MySQL no responde en 5 segundos, se da por apagado
        "connect_timeout": 5,
    },
)

# Fábrica de sesiones. expire_on_commit=False: los objetos se pueden seguir leyendo después de guardar
JbSesionLocal = sessionmaker(bind=jb_motor, expire_on_commit=False)


# Clase base de todos los modelos (cada modelo representa una tabla)
class JbBase(DeclarativeBase):
    """Base de los modelos de app/models/jb_modelos.py."""


# Dependencia que entrega una sesión por cada petición y la cierra al terminar
def jb_obtener_sesion() -> Iterator[Session]:
    """Cada petición trabaja con su propia sesión (transacción). Si algo falla, se deshace todo (rollback)."""
    # Abre una sesión nueva
    jb_sesion = JbSesionLocal()
    # Se intenta atender la petición con esta sesión
    try:
        # Entrega la sesión al endpoint y espera a que termine
        yield jb_sesion
    # Si el endpoint lanzó un error...
    except Exception:
        # ...se deshace lo que no se haya confirmado con commit
        jb_sesion.rollback()
        # Y el error sigue su camino hasta el manejador que responde al cliente
        raise
    # Pase lo que pase (con error o sin él)...
    finally:
        # ...la sesión se cierra y la conexión vuelve al grupo de conexiones
        jb_sesion.close()


# Atajo para pedir la sesión en un endpoint: jb_sesion: JbSesion
JbSesion = Annotated[Session, Depends(jb_obtener_sesion)]
