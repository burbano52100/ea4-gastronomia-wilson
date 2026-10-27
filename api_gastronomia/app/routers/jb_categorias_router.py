"""Endpoints de categorías (RF03). Roles: ADMIN (consulta: todos)."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R404, JB_R409
# jb_requiere_roles: exige un rol; jb_usuario_actual: exige solo un token válido
from app.core.jb_security import jb_requiere_roles, jb_usuario_actual
# Sesión de MySQL
from app.database.jb_conexion_mysql import JbSesion
# Esquemas de categorías
from app.schemas.jb_categoria_schema import JbCategoriaActualizar, JbCategoriaCrear, JbCategoriaRespuesta
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de categorías, con el nombre corto jb_servicio
from app.services import jb_categoria_service as jb_servicio

# Router: rutas /categorias, sección "Categorías" de Swagger
jb_router = APIRouter(prefix="/categorias", tags=["Categorías"], responses=JB_PRIVADO)
# Seguridad para consultar: cualquier usuario con token
JB_TODOS = [Depends(jb_usuario_actual)]
# Seguridad para crear, modificar y eliminar: solo ADMIN
JB_ADMIN = [Depends(jb_requiere_roles("ADMIN"))]


# GET /api/v1/categorias: lista todas
@jb_router.get("", response_model=list[JbCategoriaRespuesta], dependencies=JB_TODOS, summary="Listar categorías")
# Recibe la sesión de MySQL
def jb_listar_categorias(jb_sesion: JbSesion):
    """**Roles:** todos los usuarios autenticados."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar(jb_sesion)


# GET /api/v1/categorias/{id}: consulta una
@jb_router.get("/{id_categoria}", response_model=JbCategoriaRespuesta, dependencies=JB_TODOS,
               summary="Consultar una categoría", responses=JB_R404)  # título en Swagger y errores que puede responder
# Recibe el id_categoria de la URL y la sesión de MySQL
def jb_obtener_categoria(id_categoria: int, jb_sesion: JbSesion):
    """**Roles:** todos los usuarios autenticados."""
    # Busca la categoría (404 si no existe)
    return jb_servicio.jb_obtener(jb_sesion, id_categoria)


# POST /api/v1/categorias: crea una (201, solo ADMIN)
@jb_router.post("", response_model=JbCategoriaRespuesta, status_code=status.HTTP_201_CREATED, dependencies=JB_ADMIN,
                summary="Crear categoría", responses=JB_R409)  # título en Swagger y errores que puede responder
# Recibe el cuerpo JSON ya validado y la sesión de MySQL
def jb_crear_categoria(jb_datos: JbCategoriaCrear, jb_sesion: JbSesion):
    """El nombre no se repite. **Roles:** ADMIN."""
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_sesion, jb_datos.model_dump())


# PUT /api/v1/categorias/{id}: modifica una (solo ADMIN)
@jb_router.put("/{id_categoria}", response_model=JbCategoriaRespuesta, dependencies=JB_ADMIN,
               summary="Actualizar categoría", responses={**JB_R404, **JB_R409})  # título en Swagger y errores que puede responder
# Recibe el id_categoria de la URL, el cuerpo JSON ya validado y la sesión de MySQL
def jb_actualizar_categoria(id_categoria: int, jb_datos: JbCategoriaActualizar, jb_sesion: JbSesion):
    """**Roles:** ADMIN."""
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(jb_sesion, id_categoria, jb_datos.model_dump())


# DELETE /api/v1/categorias/{id}: elimina o inactiva una (solo ADMIN)
@jb_router.delete("/{id_categoria}", response_model=JbResultadoEliminacion, dependencies=JB_ADMIN,
                  summary="Eliminar categoría", responses=JB_R404)  # título en Swagger y errores que puede responder
# Recibe el id_categoria de la URL y la sesión de MySQL
def jb_eliminar_categoria(id_categoria: int, jb_sesion: JbSesion):
    """Si la categoría tiene productos queda INACTIVA; si no, se borra. **Roles:** ADMIN."""
    # El servicio decide si es borrado lógico o físico
    return jb_servicio.jb_eliminar(jb_sesion, id_categoria)
