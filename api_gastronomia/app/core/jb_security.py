"""Seguridad: cifrado de contraseñas con bcrypt, tokens JWT y validación de roles."""
# datetime: fecha y hora; timedelta: sumar minutos; timezone: la hora del token se maneja en UTC
from datetime import datetime, timedelta, timezone

# bcrypt: librería que cifra las contraseñas (RN06)
import bcrypt
# jwt (PyJWT): librería que crea y verifica los tokens JWT
import jwt
# Depends: inyecta dependencias; HTTPException: error HTTP; status: nombres de los códigos (401, 403...)
from fastapi import Depends, HTTPException, status
# HTTPBearer: lee el encabezado "Authorization: Bearer <token>"; HTTPAuthorizationCredentials: lo que se leyó
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Clave secreta, algoritmo y duración del token (vienen del .env)
from app.core.jb_config import JB_JWT_ALGORITMO, JB_JWT_MINUTOS, JB_JWT_SECRET

# Lector del token; además crea el botón "Authorize" de Swagger
jb_esquema_bearer = HTTPBearer(
    # Si falta el token no responde solo: la API decide y responde 401 con un mensaje en español
    auto_error=False,
    # Nombre del esquema de seguridad que aparece en la ventana "Authorize" de Swagger
    scheme_name="TokenJWT",
    # Texto de ayuda de esa ventana
    description="Pegue aquí el access_token que devuelve POST /api/v1/auth/login",
)


# Función que cifra una contraseña antes de guardarla
def jb_cifrar_password(jb_password: str) -> str:
    """RN06: la contraseña se guarda como hash bcrypt, nunca en texto plano."""
    # encode pasa el texto a bytes; gensalt crea una "sal" aleatoria; hashpw calcula el hash; decode lo vuelve texto
    return bcrypt.hashpw(jb_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


# Función que revisa si una contraseña escrita corresponde al hash guardado
def jb_verificar_password(jb_password: str, jb_hash: str) -> bool:
    """bcrypt no se descifra: se calcula el hash de lo escrito y se compara con el guardado."""
    # Se intenta la comparación
    try:
        # checkpw devuelve True si la contraseña coincide con el hash
        return bcrypt.checkpw(jb_password.encode("utf-8"), jb_hash.encode("utf-8"))
    # Si el hash guardado está dañado, bcrypt lanza ValueError
    except ValueError:
        # En ese caso se toma como contraseña incorrecta
        return False


# Función que crea el token JWT al iniciar sesión
def jb_crear_token(jb_id_usuario: int, jb_rol: str) -> str:
    # Momento actual en UTC (el estándar JWT usa UTC)
    jb_momento = datetime.now(timezone.utc)
    # Datos que van dentro del token (payload)
    jb_payload = {
        # sub (subject): el id del usuario, como texto
        "sub": str(jb_id_usuario),
        # rol del usuario, para revisar permisos sin consultar la base
        "rol": jb_rol,
        # iat (issued at): cuándo se creó el token
        "iat": jb_momento,
        # exp (expiration): cuándo vence el token
        "exp": jb_momento + timedelta(minutes=JB_JWT_MINUTOS),
    }
    # Firma el payload con la clave secreta y devuelve el token como texto
    return jwt.encode(jb_payload, JB_JWT_SECRET, algorithm=JB_JWT_ALGORITMO)


# Función que arma un error 401 con el mensaje indicado
def jb_no_autorizado(jb_mensaje: str) -> HTTPException:
    # El encabezado WWW-Authenticate le dice al cliente que debe enviar un token Bearer
    return HTTPException(status.HTTP_401_UNAUTHORIZED, jb_mensaje, headers={"WWW-Authenticate": "Bearer"})


# Dependencia que obtiene el usuario del token; la usan todos los endpoints privados
def jb_usuario_actual(
    # FastAPI lee el encabezado Authorization con jb_esquema_bearer; si no viene, queda en None
    jb_credenciales: HTTPAuthorizationCredentials | None = Depends(jb_esquema_bearer),
) -> dict:
    """Dependencia de todos los endpoints privados: sin un token válido responde 401."""
    # Sin token: 401
    if jb_credenciales is None:
        # Corta la petición con el mensaje de qué falta
        raise jb_no_autorizado("Token requerido: envíe el encabezado Authorization: Bearer <token>")
    # Se intenta leer y verificar el token
    try:
        # decode comprueba la firma y la fecha de vencimiento, y devuelve el payload
        jb_payload = jwt.decode(
            # El token que envió el cliente
            jb_credenciales.credentials,
            # La misma clave con la que se firmó
            JB_JWT_SECRET,
            # Solo se acepta el algoritmo configurado
            algorithms=[JB_JWT_ALGORITMO],
            # El token debe traer obligatoriamente exp y sub
            options={"require": ["exp", "sub"]},
        )
    # El token ya venció
    except jwt.ExpiredSignatureError:
        # 401 explicando que hay que volver a iniciar sesión
        raise jb_no_autorizado("El token expiró: inicie sesión de nuevo")
    # El token está mal formado, la firma no coincide o le faltan datos
    except jwt.InvalidTokenError:
        # 401 por token inválido
        raise jb_no_autorizado("Token inválido")
    # Un token sin rol no sirve para revisar permisos
    if jb_payload.get("rol") is None:
        # 401 por token incompleto
        raise jb_no_autorizado("Token inválido: no contiene el rol")
    # Devuelve el id (convertido a número) y el rol del usuario
    return {"id_usuario": int(jb_payload["sub"]), "rol": jb_payload["rol"]}


# Función que crea una dependencia de permisos para los roles que se le pasen
def jb_requiere_roles(*jb_roles: str):
    """Crea una dependencia que solo deja pasar a los roles indicados; si no, responde 403."""

    # Dependencia interna: primero obtiene el usuario del token (401 si no hay) y luego revisa su rol
    def jb_verificar_rol(jb_usuario: dict = Depends(jb_usuario_actual)) -> dict:
        # Si el rol del usuario no está en la lista de roles permitidos...
        if jb_usuario["rol"] not in jb_roles:
            # ...responde 403
            raise HTTPException(
                # Código 403 Forbidden
                status.HTTP_403_FORBIDDEN,
                # Mensaje con los roles que sí pueden, por ejemplo "requiere el rol ADMIN o CAJERO"
                f"Acceso denegado: esta acción requiere el rol {' o '.join(jb_roles)}",
            )
        # Si tiene permiso, entrega el usuario al endpoint
        return jb_usuario

    # Devuelve la dependencia ya configurada con los roles
    return jb_verificar_rol
