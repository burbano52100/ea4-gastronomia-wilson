"""Endpoints de usuarios del sistema (RF02). Roles: ADMIN."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R400, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Esquemas de usuarios (lo que entra y lo que sale)
from app.schemas.jb_usuario_schema import JbUsuarioActualizar, JbUsuarioCrear, JbUsuarioRespuesta
# Servicio de usuarios, con el nombre corto jb_servicio
from app.services import jb_usuario_service as jb_servicio

# Dependencia "solo ADMIN"; se guarda en una variable para usarla también al eliminar (y saber quién elimina)
jb_solo_admin = jb_requiere_roles("ADMIN")
# Router: rutas /usuarios; TODOS sus endpoints exigen ADMIN
jb_router = APIRouter(prefix="/usuarios", tags=["Usuarios"], responses=JB_PRIVADO,
                      dependencies=[Depends(jb_solo_admin)])


# GET /api/v1/usuarios: lista todos (sin contraseña)
@jb_router.get("", response_model=list[JbUsuarioRespuesta], summary="Listar usuarios")
def jb_listar_usuarios():
    """Lista los usuarios. Nunca devuelve la contraseña (RN06). **Roles:** ADMIN."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar()


# GET /api/v1/usuarios/{id}: consulta uno
@jb_router.get("/{id_usuario}", response_model=JbUsuarioRespuesta, summary="Consultar un usuario", responses=JB_R404)
def jb_obtener_usuario(id_usuario: int):
    """**Roles:** ADMIN."""
    # Busca el usuario (404 si no existe)
    return jb_servicio.jb_obtener(id_usuario)


# POST /api/v1/usuarios: crea uno (201)
@jb_router.post("", response_model=JbUsuarioRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Crear usuario", responses=JB_R409)
# El cuerpo se valida con JbUsuarioCrear
def jb_crear_usuario(jb_datos: JbUsuarioCrear):
    """Crea un usuario con rol ADMIN, CAJERO o COCINERO. Correo e identificación no se repiten (409).

    **Roles:** ADMIN.
    """
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_datos.model_dump())


# PUT /api/v1/usuarios/{id}: modifica uno
@jb_router.put("/{id_usuario}", response_model=JbUsuarioRespuesta, summary="Actualizar usuario",
               responses={**JB_R404, **JB_R409})
# Recibe el id de la URL y el cuerpo validado con JbUsuarioActualizar
def jb_actualizar_usuario(id_usuario: int, jb_datos: JbUsuarioActualizar):
    """Si no envía `password`, se conserva la contraseña actual. **Roles:** ADMIN."""
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(id_usuario, jb_datos.model_dump())


# DELETE /api/v1/usuarios/{id}: elimina o inactiva uno
@jb_router.delete("/{id_usuario}", response_model=JbResultadoEliminacion, summary="Eliminar usuario",
                  responses={**JB_R400, **JB_R404})
# Recibe el id de la URL y el usuario del token (para no permitir que se elimine a sí mismo)
def jb_eliminar_usuario(id_usuario: int, jb_usuario: dict = Depends(jb_solo_admin)):
    """Si el usuario registró pedidos o compras pasa a INACTIVO (RN04); si no, se elimina.
    No se puede eliminar el usuario con el que se inició sesión. **Roles:** ADMIN.
    """
    # Pasa el id a eliminar y el id de quien está en sesión
    return jb_servicio.jb_eliminar(id_usuario, jb_usuario["id_usuario"])
