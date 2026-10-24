"""Endpoints de autenticación (RF01)."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R401, JB_R403, JB_R409
# jb_requiere_roles: exige un rol; jb_usuario_actual: exige solo un token válido
from app.core.jb_security import jb_requiere_roles, jb_usuario_actual
# Esquemas del login (lo que entra) y del token (lo que sale)
from app.schemas.jb_auth_schema import JbLogin, JbToken
# Esquemas de usuario para el registro y el perfil
from app.schemas.jb_usuario_schema import JbUsuarioCrear, JbUsuarioRespuesta
# Servicios con la lógica del login y de los usuarios
from app.services import jb_auth_service, jb_usuario_service

# Router de autenticación: todas sus rutas empiezan por /auth y salen en la sección "Autenticación"
jb_router = APIRouter(prefix="/auth", tags=["Autenticación"])


# POST /api/v1/auth/login. response_model: forma de la respuesta; summary: título en Swagger;
# responses: errores que se documentan. No tiene dependencias de seguridad: es el único endpoint público.
@jb_router.post("/login", response_model=JbToken, summary="Iniciar sesión (único endpoint público)",
                responses={**JB_R401, **JB_R403})
# Función que atiende la petición; FastAPI valida el cuerpo con JbLogin (si falla responde 422)
def jb_login(jb_datos: JbLogin):
    """Recibe correo y contraseña. Si son correctos devuelve un **token JWT** con el rol del usuario.

    Copie el `access_token` y péguelo en el botón **Authorize** (arriba a la derecha).
    """
    # Le pasa correo y contraseña al servicio, que devuelve el token
    return jb_auth_service.jb_iniciar_sesion(jb_datos.correo, jb_datos.password)


# POST /api/v1/auth/registro: responde 201 (creado); solo el ADMIN puede usarlo
@jb_router.post("/registro", response_model=JbUsuarioRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Registrar un usuario", responses={**JB_PRIVADO, **JB_R409},
                dependencies=[Depends(jb_requiere_roles("ADMIN"))])
# Recibe los datos del usuario validados con JbUsuarioCrear
def jb_registro(jb_datos: JbUsuarioCrear):
    """Crea un usuario con su rol. La contraseña se guarda cifrada con bcrypt (RN06).

    **Roles:** ADMIN.
    """
    # model_dump convierte el esquema en diccionario; el servicio cifra la contraseña y lo guarda
    return jb_usuario_service.jb_crear(jb_datos.model_dump())


# GET /api/v1/auth/perfil: cualquier usuario con token válido
@jb_router.get("/perfil", response_model=JbUsuarioRespuesta, summary="Datos del usuario autenticado",
               responses=JB_R401)
# Depends(jb_usuario_actual) lee el token y entrega {"id_usuario", "rol"} (401 si no hay token)
def jb_perfil(jb_usuario: dict = Depends(jb_usuario_actual)):
    """Devuelve los datos del dueño del token. **Roles:** todos."""
    # Busca y devuelve el usuario del token
    return jb_usuario_service.jb_obtener(jb_usuario["id_usuario"])
