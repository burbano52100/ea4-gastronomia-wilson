"""Endpoints de productos (RF04, RF05, RF06). Roles: ADMIN (consulta: todos)."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R400, JB_R404, JB_R409
# jb_requiere_roles: exige un rol; jb_usuario_actual: exige solo un token válido
from app.core.jb_security import jb_requiere_roles, jb_usuario_actual
# Sesión de MySQL
from app.database.jb_conexion_mysql import JbSesion
# Esquemas de productos, receta y costo
from app.schemas.jb_producto_schema import (
    JbCostoProducto,  # forma de la respuesta del costo
    JbProductoActualizar,  # datos para modificar
    JbProductoCrear,  # datos para crear
    JbProductoRespuesta,  # forma de la respuesta
    JbRecetaDeProducto,  # forma de la receta de un producto
)
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de productos, con el nombre corto jb_servicio
from app.services import jb_producto_service as jb_servicio

# Router: rutas /productos, sección "Productos" de Swagger
jb_router = APIRouter(prefix="/productos", tags=["Productos"], responses=JB_PRIVADO)
# Seguridad para consultar: cualquier usuario con token
JB_TODOS = [Depends(jb_usuario_actual)]
# Seguridad para crear, modificar, eliminar y ver costos: solo ADMIN
JB_ADMIN = [Depends(jb_requiere_roles("ADMIN"))]
# Seguridad para ver la receta: ADMIN y COCINERO (igual que el CRUD de recetas)
JB_COCINA = [Depends(jb_requiere_roles("ADMIN", "COCINERO"))]


# GET /api/v1/productos: lista todos
@jb_router.get("", response_model=list[JbProductoRespuesta], dependencies=JB_TODOS, summary="Listar productos")
# Recibe la sesión de MySQL
def jb_listar_productos(jb_sesion: JbSesion):
    """**Roles:** todos los usuarios autenticados."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar(jb_sesion)


# GET /api/v1/productos/categoria/{id}: va antes de /{id_producto} porque es una ruta fija
@jb_router.get("/categoria/{id_categoria}", response_model=list[JbProductoRespuesta], dependencies=JB_TODOS,
               summary="Productos de una categoría", responses=JB_R404)  # título en Swagger y errores que puede responder
# Recibe el id_categoria de la URL y la sesión de MySQL
def jb_productos_por_categoria(id_categoria: int, jb_sesion: JbSesion):
    """**Roles:** todos los usuarios autenticados."""
    # Pide los productos de la categoría al servicio (404 si la categoría no existe)
    return jb_servicio.jb_por_categoria(jb_sesion, id_categoria)


# GET /api/v1/productos/{id}: consulta uno
@jb_router.get("/{id_producto}", response_model=JbProductoRespuesta, dependencies=JB_TODOS,
               summary="Consultar un producto", responses=JB_R404)  # título en Swagger y errores que puede responder
# Recibe el id_producto de la URL y la sesión de MySQL
def jb_obtener_producto(id_producto: int, jb_sesion: JbSesion):
    """**Roles:** todos los usuarios autenticados."""
    # Busca el producto (404 si no existe)
    return jb_servicio.jb_obtener(jb_sesion, id_producto)


# GET /api/v1/productos/{id}/receta: ficha técnica del producto
@jb_router.get("/{id_producto}/receta", response_model=JbRecetaDeProducto, dependencies=JB_COCINA,
               summary="Receta (ficha técnica) de un producto", responses=JB_R404)  # título en Swagger y errores que puede responder
# Recibe el id_producto de la URL y la sesión de MySQL
def jb_receta_producto(id_producto: int, jb_sesion: JbSesion):
    """Insumos y cantidades de la receta, con el costo de cada línea (RF05). Lista vacía si no tiene receta.

    **Roles:** ADMIN, COCINERO.
    """
    # Pide la receta al servicio
    return jb_servicio.jb_receta(jb_sesion, id_producto)


# GET /api/v1/productos/{id}/costo: costo de producción y margen
@jb_router.get("/{id_producto}/costo", response_model=JbCostoProducto, dependencies=JB_ADMIN,
               summary="Costo de producción y margen", responses=JB_R404)  # título en Swagger y errores que puede responder
# Recibe el id_producto de la URL y la sesión de MySQL
def jb_costo_producto(id_producto: int, jb_sesion: JbSesion):
    """RF06: costo = suma de (cantidad x costo_unitario) de la receta. Margen = precio de venta - costo,
    también en porcentaje. Responde 404 si el producto no tiene receta.

    **Roles:** ADMIN (los costos son información sensible).
    """
    # Pide el cálculo al servicio
    return jb_servicio.jb_costo(jb_sesion, id_producto)


# POST /api/v1/productos: crea uno (201, solo ADMIN)
@jb_router.post("", response_model=JbProductoRespuesta, status_code=status.HTTP_201_CREATED, dependencies=JB_ADMIN,
                summary="Crear producto", responses={**JB_R400, **JB_R409})  # título en Swagger y errores que puede responder
# Recibe el cuerpo JSON ya validado y la sesión de MySQL
def jb_crear_producto(jb_datos: JbProductoCrear, jb_sesion: JbSesion):
    """El precio debe ser mayor que 0 y la categoría debe existir y estar ACTIVA. El código no se repite.

    **Roles:** ADMIN.
    """
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_sesion, jb_datos.model_dump())


# PUT /api/v1/productos/{id}: modifica uno (solo ADMIN)
@jb_router.put("/{id_producto}", response_model=JbProductoRespuesta, dependencies=JB_ADMIN,
               summary="Actualizar producto", responses={**JB_R400, **JB_R404, **JB_R409})  # título en Swagger y errores que puede responder
# Recibe el id_producto de la URL, el cuerpo JSON ya validado y la sesión de MySQL
def jb_actualizar_producto(id_producto: int, jb_datos: JbProductoActualizar, jb_sesion: JbSesion):
    """**Roles:** ADMIN."""
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(jb_sesion, id_producto, jb_datos.model_dump())


# DELETE /api/v1/productos/{id}: elimina o inactiva uno (solo ADMIN)
@jb_router.delete("/{id_producto}", response_model=JbResultadoEliminacion, dependencies=JB_ADMIN,
                  summary="Eliminar producto", responses=JB_R404)  # título en Swagger y errores que puede responder
# Recibe el id_producto de la URL y la sesión de MySQL
def jb_eliminar_producto(id_producto: int, jb_sesion: JbSesion):
    """RN04: si el producto aparece en pedidos o tiene receta pasa a INACTIVO; si no, se borra.

    **Roles:** ADMIN.
    """
    # El servicio decide si es borrado lógico o físico
    return jb_servicio.jb_eliminar(jb_sesion, id_producto)
