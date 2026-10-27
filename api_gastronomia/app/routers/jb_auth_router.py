"""Endpoints de autenticación (RF01). /auth/login es el único endpoint público de la API."""
# Annotated: agrega información extra a un tipo
from typing import Annotated

# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R401, JB_R409
# jb_requiere_roles: exige un rol; jb_usuario_actual: exige solo un token válido
from app.core.jb_security import jb_requiere_roles, jb_usuario_actual
# Sesión de MySQL
from app.database.jb_conexion_mysql import JbSesion
# Modelo de la tabla usuarios
from app.models.jb_modelos import JbUsuario
# Esquemas del login y del token
from app.schemas.jb_auth_schema import JbLogin, JbToken
# Esquemas de usuarios
from app.schemas.jb_usuario_schema import JbUsuarioCrear, JbUsuarioRespuesta
# Servicios de autenticación y de usuarios
from app.services import jb_auth_service, jb_usuario_service

# Router: rutas /auth, sección "Autenticación" de Swagger
jb_router = APIRouter(prefix="/auth", tags=["Autenticación"])
# Dependencia que solo deja pasar al rol ADMIN
jb_solo_admin = jb_requiere_roles("ADMIN")


# POST /api/v1/auth/login: único endpoint público
@jb_router.post("/login", response_model=JbToken, summary="Iniciar sesión", responses=JB_R401)
# El cuerpo se valida con JbLogin; la sesión de MySQL la entrega FastAPI
def jb_login(jb_datos: JbLogin, jb_sesion: JbSesion):
    """Recibe correo y contraseña y devuelve un token JWT que lleva el rol del usuario (RF01).

    Copie el `access_token` y péguelo en el botón **Authorize** de Swagger (o en el encabezado
    `Authorization: Bearer <token>` de Thunder Client). **Es el único endpoint público.**
    """
    # Pide al servicio que verifique las credenciales y cree el token
    return jb_auth_service.jb_iniciar_sesion(jb_sesion, jb_datos.correo, jb_datos.password)


# POST /api/v1/auth/registro: crea un usuario (solo ADMIN)
@jb_router.post(
    # Ruta
    "/registro",
    # Forma de la respuesta (sin contraseña)
    response_model=JbUsuarioRespuesta,
    # 201: se creó un registro
    status_code=status.HTTP_201_CREATED,
    # Solo ADMIN
    dependencies=[Depends(jb_solo_admin)],
    # Título en Swagger
    summary="Registrar un usuario",
    # Errores posibles
    responses={**JB_PRIVADO, **JB_R409},
)
# Recibe el cuerpo JSON ya validado y la sesión de MySQL
def jb_registro(jb_datos: JbUsuarioCrear, jb_sesion: JbSesion):
    """Registra un usuario con su rol. La contraseña se guarda cifrada con bcrypt (RN06).

    **Roles:** ADMIN.
    """
    # Usa el mismo servicio que POST /usuarios
    return jb_usuario_service.jb_crear(jb_sesion, jb_datos.model_dump())


# GET /api/v1/auth/perfil: datos del usuario del token
@jb_router.get("/perfil", response_model=JbUsuarioRespuesta, summary="Mi perfil", responses=JB_R401)
# FastAPI entrega el usuario que obtuvo jb_usuario_actual a partir del token
def jb_perfil(jb_usuario: Annotated[JbUsuario, Depends(jb_usuario_actual)]):
    """Devuelve los datos del usuario autenticado (nunca la contraseña).

    **Roles:** cualquier usuario con token.
    """
    # El usuario ya viene validado por la dependencia
    return jb_usuario
