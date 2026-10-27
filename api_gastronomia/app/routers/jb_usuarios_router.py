"""Endpoints de usuarios (RF02). Roles: solo ADMIN."""
# Annotated: agrega información extra a un tipo
from typing import Annotated

# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Sesión de MySQL
from app.database.jb_conexion_mysql import JbSesion
# Modelo de la tabla usuarios
from app.models.jb_modelos import JbUsuario
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Esquemas de usuarios
from app.schemas.jb_usuario_schema import JbUsuarioActualizar, JbUsuarioCrear, JbUsuarioRespuesta
# Servicio de usuarios, con el nombre corto jb_servicio
from app.services import jb_usuario_service as jb_servicio

# Dependencia que solo deja pasar al rol ADMIN
jb_solo_admin = jb_requiere_roles("ADMIN")
# Router: rutas /usuarios, sección "Usuarios" de Swagger; TODOS sus endpoints exigen ADMIN
jb_router = APIRouter(prefix="/usuarios", tags=["Usuarios"], dependencies=[Depends(jb_solo_admin)], responses=JB_PRIVADO)


# GET /api/v1/usuarios: lista todos
@jb_router.get("", response_model=list[JbUsuarioRespuesta], summary="Listar usuarios")
# Recibe la sesión de MySQL
def jb_listar_usuarios(jb_sesion: JbSesion):
    """Lista los usuarios sin su contraseña (RN06). **Roles:** ADMIN."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar(jb_sesion)


# GET /api/v1/usuarios/{id}: consulta uno
@jb_router.get("/{id_usuario}", response_model=JbUsuarioRespuesta, summary="Consultar un usuario", responses=JB_R404)
# Recibe el id_usuario de la URL y la sesión de MySQL
def jb_obtener_usuario(id_usuario: int, jb_sesion: JbSesion):
    """**Roles:** ADMIN."""
    # Busca el usuario (404 si no existe)
    return jb_servicio.jb_obtener(jb_sesion, id_usuario)


# POST /api/v1/usuarios: crea uno (201)
@jb_router.post("", response_model=JbUsuarioRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Crear usuario", responses=JB_R409)  # título en Swagger y errores que puede responder
# Recibe el cuerpo JSON ya validado y la sesión de MySQL
def jb_crear_usuario(jb_datos: JbUsuarioCrear, jb_sesion: JbSesion):
    """La contraseña se guarda cifrada con bcrypt (RN06). El correo y la identificación no se repiten.

    **Roles:** ADMIN.
    """
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_sesion, jb_datos.model_dump())


# PUT /api/v1/usuarios/{id}: modifica uno
@jb_router.put("/{id_usuario}", response_model=JbUsuarioRespuesta, summary="Actualizar usuario",
               responses={**JB_R404, **JB_R409})  # errores que puede responder
# Recibe el id_usuario de la URL, el cuerpo JSON ya validado y la sesión de MySQL
def jb_actualizar_usuario(id_usuario: int, jb_datos: JbUsuarioActualizar, jb_sesion: JbSesion):
    """Si se envía `password` se cambia la contraseña; si no, se conserva. Debe quedar al menos un ADMIN activo.

    **Roles:** ADMIN.
    """
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(jb_sesion, id_usuario, jb_datos.model_dump())


# DELETE /api/v1/usuarios/{id}: elimina o inactiva uno
@jb_router.delete("/{id_usuario}", response_model=JbResultadoEliminacion, summary="Eliminar usuario",
                  responses={**JB_R404, **JB_R409})  # errores que puede responder
# jb_actual es el ADMIN que hace la petición (la misma dependencia del router, no se ejecuta dos veces)
def jb_eliminar_usuario(id_usuario: int, jb_sesion: JbSesion, jb_actual: Annotated[JbUsuario, Depends(jb_solo_admin)]):
    """Si el usuario ya registró pedidos o compras queda INACTIVO; si no, se borra.
    Nadie puede eliminarse a sí mismo y debe quedar al menos un ADMIN activo.

    **Roles:** ADMIN.
    """
    # El servicio decide si es borrado lógico o físico
    return jb_servicio.jb_eliminar(jb_sesion, id_usuario, jb_actual.id_usuario)
