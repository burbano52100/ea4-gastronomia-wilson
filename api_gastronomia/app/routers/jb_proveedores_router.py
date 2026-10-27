"""Endpoints de proveedores (RF08). Roles: solo ADMIN."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Sesión de MySQL
from app.database.jb_conexion_mysql import JbSesion
# Esquema de las compras (para el historial)
from app.schemas.jb_compra_schema import JbCompraRespuesta
# Esquemas de proveedores
from app.schemas.jb_proveedor_schema import JbProveedorActualizar, JbProveedorCrear, JbProveedorRespuesta
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de proveedores, con el nombre corto jb_servicio
from app.services import jb_proveedor_service as jb_servicio

# Router: rutas /proveedores, sección "Proveedores" de Swagger; TODOS sus endpoints exigen ADMIN
jb_router = APIRouter(
    # Prefijo de las rutas
    prefix="/proveedores",
    # Sección de Swagger
    tags=["Proveedores"],
    # Seguridad de todo el router
    dependencies=[Depends(jb_requiere_roles("ADMIN"))],
    # Errores 401 y 403 en todos los endpoints
    responses=JB_PRIVADO,
)


# GET /api/v1/proveedores: lista todos
@jb_router.get("", response_model=list[JbProveedorRespuesta], summary="Listar proveedores")
# Recibe la sesión de MySQL
def jb_listar_proveedores(jb_sesion: JbSesion):
    """**Roles:** ADMIN."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar(jb_sesion)


# GET /api/v1/proveedores/{id}: consulta uno
@jb_router.get("/{id_proveedor}", response_model=JbProveedorRespuesta, summary="Consultar un proveedor", responses=JB_R404)
# Recibe el id_proveedor de la URL y la sesión de MySQL
def jb_obtener_proveedor(id_proveedor: int, jb_sesion: JbSesion):
    """**Roles:** ADMIN."""
    # Busca el proveedor (404 si no existe)
    return jb_servicio.jb_obtener(jb_sesion, id_proveedor)


# GET /api/v1/proveedores/{id}/compras: historial de compras
@jb_router.get("/{id_proveedor}/compras", response_model=list[JbCompraRespuesta],
               summary="Historial de compras a un proveedor", responses=JB_R404)  # título en Swagger y errores que puede responder
# Recibe el id_proveedor de la URL y la sesión de MySQL
def jb_compras_proveedor(id_proveedor: int, jb_sesion: JbSesion):
    """Compras del proveedor con su detalle, de la más reciente a la más antigua. **Roles:** ADMIN."""
    # Pide el historial al servicio (404 si el proveedor no existe)
    return jb_servicio.jb_compras(jb_sesion, id_proveedor)


# POST /api/v1/proveedores: crea uno (201)
@jb_router.post("", response_model=JbProveedorRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Crear proveedor", responses=JB_R409)  # título en Swagger y errores que puede responder
# Recibe el cuerpo JSON ya validado y la sesión de MySQL
def jb_crear_proveedor(jb_datos: JbProveedorCrear, jb_sesion: JbSesion):
    """El NIT no se repite. **Roles:** ADMIN."""
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_sesion, jb_datos.model_dump())


# PUT /api/v1/proveedores/{id}: modifica uno
@jb_router.put("/{id_proveedor}", response_model=JbProveedorRespuesta, summary="Actualizar proveedor",
               responses={**JB_R404, **JB_R409})  # errores que puede responder
# Recibe el id_proveedor de la URL, el cuerpo JSON ya validado y la sesión de MySQL
def jb_actualizar_proveedor(id_proveedor: int, jb_datos: JbProveedorActualizar, jb_sesion: JbSesion):
    """**Roles:** ADMIN."""
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(jb_sesion, id_proveedor, jb_datos.model_dump())


# DELETE /api/v1/proveedores/{id}: elimina o inactiva uno
@jb_router.delete("/{id_proveedor}", response_model=JbResultadoEliminacion, summary="Eliminar proveedor",
                  responses=JB_R404)  # errores que puede responder
# Recibe el id_proveedor de la URL y la sesión de MySQL
def jb_eliminar_proveedor(id_proveedor: int, jb_sesion: JbSesion):
    """RN04: si el proveedor tiene compras pasa a INACTIVO; si no, se borra. **Roles:** ADMIN."""
    # El servicio decide si es borrado lógico o físico
    return jb_servicio.jb_eliminar(jb_sesion, id_proveedor)
