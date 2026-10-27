"""Reglas de la autenticación (RF01)."""
# Session: sesión de trabajo con MySQL
from sqlalchemy.orm import Session

# Minutos que dura el token
from app.core.jb_config import JB_JWT_MINUTOS
# Funciones de seguridad: crear token, verificar contraseña y error 401
from app.core.jb_security import jb_crear_token, jb_no_autorizado, jb_verificar_password
# Consultas a la tabla usuarios
from app.repositories import jb_usuario_repository


# Inicia sesión y genera el token
def jb_iniciar_sesion(jb_sesion: Session, jb_correo: str, jb_password: str) -> dict:
    """RF01: si el correo y la contraseña son correctos y el usuario está ACTIVO, devuelve un token con su rol."""
    # Busca el usuario por correo
    jb_usuario = jb_usuario_repository.jb_buscar_por_correo(jb_sesion, jb_correo)
    # Si no existe o la contraseña no coincide con el hash guardado...
    if jb_usuario is None or not jb_verificar_password(jb_password, jb_usuario.password):
        # ...responde 401 sin decir cuál de los dos falló (así no se puede adivinar qué correos existen)
        raise jb_no_autorizado("Correo o contraseña incorrectos")
    # Un usuario INACTIVO no puede iniciar sesión
    if jb_usuario.estado != "ACTIVO":
        # Responde 401
        raise jb_no_autorizado("El usuario está INACTIVO: no puede iniciar sesión")
    # Devuelve la forma de JbToken
    return {
        # Token firmado con el id y el rol del usuario
        "access_token": jb_crear_token(jb_usuario.id_usuario, jb_usuario.rol),
        # Tipo de token
        "token_type": "bearer",
        # Minutos que dura
        "expira_en_minutos": JB_JWT_MINUTOS,
        # Datos del usuario (el esquema de respuesta no incluye la contraseña)
        "usuario": jb_usuario,
    }
