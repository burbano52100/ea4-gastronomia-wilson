"""Endpoints de categorías (RF03). Roles: ADMIN (consulta: todos)."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R404, JB_R409
# jb_requiere_roles: exige un rol; jb_usuario_actual: exige solo un token válido
from app.core.jb_security import jb_requiere_roles, jb_usuario_actual
# Esquemas de categorías: Crear y Actualizar (lo que entra) y Respuesta (lo que sale)
from app.schemas.jb_categoria_schema import JbCategoriaActualizar, JbCategoriaCrear, JbCategoriaRespuesta
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de categorías, con el nombre corto jb_servicio
from app.services import jb_categoria_service as jb_servicio

# Router: rutas /categorias, sección "Categorías" de Swagger, y todos pueden responder 401/403
jb_router = APIRouter(prefix="/categorias", tags=["Categorías"], responses=JB_PRIVADO)
# Seguridad para consultar: cualquier usuario con token
JB_TODOS = [Depends(jb_usuario_actual)]
# Seguridad para crear, modificar y eliminar: solo ADMIN
JB_ADMIN = [Depends(jb_requiere_roles("ADMIN"))]


# GET /api/v1/categorias. response_model: la respuesta es una lista de JbCategoriaRespuesta;
# dependencies: quién puede usarlo; summary: título del endpoint en Swagger
@jb_router.get("", response_model=list[JbCategoriaRespuesta], dependencies=JB_TODOS, summary="Listar categorías")
# Función que atiende la petición
def jb_listar_categorias():
    """**Roles:** todos los usuarios autenticados."""
    # Pide la lista al servicio; FastAPI la convierte en JSON
    return jb_servicio.jb_listar()


# GET /api/v1/categorias/{id}: responses documenta que puede responder 404
@jb_router.get("/{id_categoria}", response_model=JbCategoriaRespuesta, dependencies=JB_TODOS,
               summary="Consultar una categoría", responses=JB_R404)
# id_categoria se toma de la URL; si no es un número, FastAPI responde 422
def jb_obtener_categoria(id_categoria: int):
    """**Roles:** todos los usuarios autenticados."""
    # Busca la categoría (404 si no existe)
    return jb_servicio.jb_obtener(id_categoria)


# POST /api/v1/categorias: status_code 201 significa "creado"
@jb_router.post("", response_model=JbCategoriaRespuesta, status_code=status.HTTP_201_CREATED, dependencies=JB_ADMIN,
                summary="Crear categoría", responses=JB_R409)
# FastAPI valida el cuerpo JSON con JbCategoriaCrear (si falla responde 422)
def jb_crear_categoria(jb_datos: JbCategoriaCrear):
    """El nombre no se puede repetir (409). **Roles:** ADMIN."""
    # model_dump convierte el esquema en diccionario para el servicio
    return jb_servicio.jb_crear(jb_datos.model_dump())


# PUT /api/v1/categorias/{id}: modifica una categoría
@jb_router.put("/{id_categoria}", response_model=JbCategoriaRespuesta, dependencies=JB_ADMIN,
               summary="Actualizar categoría", responses={**JB_R404, **JB_R409})
# Recibe el id de la URL y el cuerpo validado con JbCategoriaActualizar
def jb_actualizar_categoria(id_categoria: int, jb_datos: JbCategoriaActualizar):
    """**Roles:** ADMIN."""
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(id_categoria, jb_datos.model_dump())


# DELETE /api/v1/categorias/{id}: elimina o inactiva una categoría
@jb_router.delete("/{id_categoria}", response_model=JbResultadoEliminacion, dependencies=JB_ADMIN,
                  summary="Eliminar categoría", responses=JB_R404)
def jb_eliminar_categoria(id_categoria: int):
    """Si la categoría tiene productos pasa a INACTIVO; si no, se elimina. **Roles:** ADMIN."""
    # El servicio decide si es borrado lógico o físico
    return jb_servicio.jb_eliminar(id_categoria)
