"""Endpoints de productos (RF04, RF05, RF06). Roles: ADMIN (consulta: todos)."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R400, JB_R404, JB_R409
# jb_requiere_roles: exige un rol; jb_usuario_actual: exige solo un token válido
from app.core.jb_security import jb_requiere_roles, jb_usuario_actual
# Esquemas de productos, receta y costo
from app.schemas.jb_producto_schema import (
    JbCostoProducto,
    JbProductoActualizar,
    JbProductoCrear,
    JbProductoRespuesta,
    JbRecetaDeProducto,
)
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de productos, con el nombre corto jb_servicio
from app.services import jb_producto_service as jb_servicio

# Router: rutas /productos, sección "Productos" de Swagger
jb_router = APIRouter(prefix="/productos", tags=["Productos"], responses=JB_PRIVADO)
# Seguridad para consultar: cualquier usuario con token
JB_TODOS = [Depends(jb_usuario_actual)]
# Seguridad para crear, modificar y eliminar: solo ADMIN
JB_ADMIN = [Depends(jb_requiere_roles("ADMIN"))]


# GET /api/v1/productos: lista todos
@jb_router.get("", response_model=list[JbProductoRespuesta], dependencies=JB_TODOS, summary="Listar productos")
def jb_listar_productos():
    """**Roles:** todos los usuarios autenticados."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar()


# GET /api/v1/productos/categoria/{id}: va antes de /{id_producto} porque es una ruta fija
@jb_router.get("/categoria/{id_categoria}", response_model=list[JbProductoRespuesta], dependencies=JB_TODOS,
               summary="Productos de una categoría", responses=JB_R404)
def jb_productos_por_categoria(id_categoria: int):
    """**Roles:** todos los usuarios autenticados."""
    # Pide los productos de la categoría al servicio
    return jb_servicio.jb_por_categoria(id_categoria)


# GET /api/v1/productos/{id}: consulta uno
@jb_router.get("/{id_producto}", response_model=JbProductoRespuesta, dependencies=JB_TODOS,
               summary="Consultar un producto", responses=JB_R404)
def jb_obtener_producto(id_producto: int):
    """**Roles:** todos los usuarios autenticados."""
    # Busca el producto (404 si no existe)
    return jb_servicio.jb_obtener(id_producto)


# GET /api/v1/productos/{id}/receta: ficha técnica del producto
@jb_router.get("/{id_producto}/receta", response_model=JbRecetaDeProducto, dependencies=JB_TODOS,
               summary="Receta (ficha técnica) de un producto", responses=JB_R404)
def jb_receta_producto(id_producto: int):
    """Insumos, cantidades y costo de cada línea de la receta (RF05). **Roles:** todos."""
    # Pide la receta al servicio
    return jb_servicio.jb_receta(id_producto)


# GET /api/v1/productos/{id}/costo: costo de producción y margen
@jb_router.get("/{id_producto}/costo", response_model=JbCostoProducto, dependencies=JB_TODOS,
               summary="Costo de producción y margen", responses=JB_R404)
def jb_costo_producto(id_producto: int):
    """Costo = suma de (cantidad x costo_unitario) de la receta. Margen = precio de venta - costo (RF06).

    **Roles:** todos los usuarios autenticados.
    """
    # Pide el cálculo al servicio
    return jb_servicio.jb_costo(id_producto)


# POST /api/v1/productos: crea uno (201, solo ADMIN)
@jb_router.post("", response_model=JbProductoRespuesta, status_code=status.HTTP_201_CREATED, dependencies=JB_ADMIN,
                summary="Crear producto", responses={**JB_R400, **JB_R409})
# El cuerpo se valida con JbProductoCrear
def jb_crear_producto(jb_datos: JbProductoCrear):
    """El precio debe ser mayor que 0 y la categoría debe existir y estar ACTIVA. El código no se repite.

    **Roles:** ADMIN.
    """
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_datos.model_dump())


# PUT /api/v1/productos/{id}: modifica uno (solo ADMIN)
@jb_router.put("/{id_producto}", response_model=JbProductoRespuesta, dependencies=JB_ADMIN,
               summary="Actualizar producto", responses={**JB_R400, **JB_R404, **JB_R409})
# Recibe el id de la URL y el cuerpo validado con JbProductoActualizar
def jb_actualizar_producto(id_producto: int, jb_datos: JbProductoActualizar):
    """**Roles:** ADMIN."""
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(id_producto, jb_datos.model_dump())


# DELETE /api/v1/productos/{id}: elimina o inactiva uno (solo ADMIN)
@jb_router.delete("/{id_producto}", response_model=JbResultadoEliminacion, dependencies=JB_ADMIN,
                  summary="Eliminar producto", responses=JB_R404)
def jb_eliminar_producto(id_producto: int):
    """RN04: si el producto aparece en pedidos pasa a INACTIVO; si no, se elimina con su receta.

    **Roles:** ADMIN.
    """
    # El servicio decide si es borrado lógico o físico
    return jb_servicio.jb_eliminar(id_producto)
