"""Endpoints de proveedores (RF08). Roles: ADMIN."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Esquema de compra, para el historial de compras del proveedor
from app.schemas.jb_compra_schema import JbCompraRespuesta
# Esquemas de proveedores (lo que entra y lo que sale)
from app.schemas.jb_proveedor_schema import JbProveedorActualizar, JbProveedorCrear, JbProveedorRespuesta
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de proveedores, con el nombre corto jb_servicio
from app.services import jb_proveedor_service as jb_servicio

# Router: rutas /proveedores; TODOS sus endpoints exigen ADMIN
jb_router = APIRouter(prefix="/proveedores", tags=["Proveedores"], responses=JB_PRIVADO,
                      dependencies=[Depends(jb_requiere_roles("ADMIN"))])


# GET /api/v1/proveedores: lista todos
@jb_router.get("", response_model=list[JbProveedorRespuesta], summary="Listar proveedores")
def jb_listar_proveedores():
    """**Roles:** ADMIN."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar()


# GET /api/v1/proveedores/{id}: consulta uno
@jb_router.get("/{id_proveedor}", response_model=JbProveedorRespuesta, summary="Consultar un proveedor",
               responses=JB_R404)
def jb_obtener_proveedor(id_proveedor: int):
    """**Roles:** ADMIN."""
    # Busca el proveedor (404 si no existe)
    return jb_servicio.jb_obtener(id_proveedor)


# GET /api/v1/proveedores/{id}/compras: historial de compras del proveedor
@jb_router.get("/{id_proveedor}/compras", response_model=list[JbCompraRespuesta],
               summary="Historial de compras a un proveedor", responses=JB_R404)
def jb_compras_proveedor(id_proveedor: int):
    """Compras del proveedor, de la más reciente a la más antigua. **Roles:** ADMIN."""
    # Pide el historial al servicio
    return jb_servicio.jb_compras(id_proveedor)


# POST /api/v1/proveedores: crea uno (201)
@jb_router.post("", response_model=JbProveedorRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Crear proveedor", responses=JB_R409)
# El cuerpo se valida con JbProveedorCrear
def jb_crear_proveedor(jb_datos: JbProveedorCrear):
    """El NIT no se repite (409). **Roles:** ADMIN."""
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_datos.model_dump())


# PUT /api/v1/proveedores/{id}: modifica uno
@jb_router.put("/{id_proveedor}", response_model=JbProveedorRespuesta, summary="Actualizar proveedor",
               responses={**JB_R404, **JB_R409})
# Recibe el id de la URL y el cuerpo validado con JbProveedorActualizar
def jb_actualizar_proveedor(id_proveedor: int, jb_datos: JbProveedorActualizar):
    """**Roles:** ADMIN."""
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(id_proveedor, jb_datos.model_dump())


# DELETE /api/v1/proveedores/{id}: elimina o inactiva uno
@jb_router.delete("/{id_proveedor}", response_model=JbResultadoEliminacion, summary="Eliminar proveedor",
                  responses=JB_R404)
def jb_eliminar_proveedor(id_proveedor: int):
    """RN04: si el proveedor tiene compras pasa a INACTIVO; si no, se elimina. **Roles:** ADMIN."""
    # El servicio decide si es borrado lógico o físico
    return jb_servicio.jb_eliminar(id_proveedor)
