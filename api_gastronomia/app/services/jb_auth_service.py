"""Inicio de sesión (RF01)."""
# HTTPException: error HTTP; status: nombres de los códigos
from fastapi import HTTPException, status

# Minutos que dura el token
from app.core.jb_config import JB_JWT_MINUTOS
# Funciones para crear el token y comparar la contraseña con su hash
from app.core.jb_security import jb_crear_token, jb_verificar_password
# Acceso a la colección usuarios
from app.repositories.jb_usuario_repository import jb_usuario_repository


# Revisa correo y contraseña y, si están bien, entrega el token
def jb_iniciar_sesion(jb_correo: str, jb_password: str) -> dict:
    # Busca el usuario por correo (en minúsculas, como se guardan) incluyendo su hash
    jb_usuario = jb_usuario_repository.jb_buscar_para_login(jb_correo.lower())
    # El mismo mensaje para correo inexistente o clave errada: así no se revela qué correos existen.
    if jb_usuario is None or not jb_verificar_password(jb_password, jb_usuario["password"]):
        # Responde 401
        raise HTTPException(
            # Código 401 Unauthorized
            status.HTTP_401_UNAUTHORIZED,
            # Mensaje del error
            "Correo o contraseña incorrectos",
            # Indica que se usa autenticación Bearer
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Un usuario INACTIVO no puede entrar aunque la contraseña sea correcta
    if jb_usuario["estado"] != "ACTIVO":
        # Responde 403
        raise HTTPException(status.HTTP_403_FORBIDDEN, "El usuario está INACTIVO; comuníquese con el administrador")
    # Respuesta del login (forma de JbToken)
    return {
        # Token firmado con el id y el rol del usuario
        "access_token": jb_crear_token(jb_usuario["_id"], jb_usuario["rol"]),
        # Tipo de token estándar
        "token_type": "bearer",
        # Cuánto dura el token
        "expira_en_minutos": JB_JWT_MINUTOS,
        # Id del usuario
        "id_usuario": jb_usuario["_id"],
        # Nombre completo: nombres + espacio + apellidos
        "nombre": f"{jb_usuario['nombres']} {jb_usuario['apellidos']}",
        # Rol del usuario
        "rol": jb_usuario["rol"],
    }
