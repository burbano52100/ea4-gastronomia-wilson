"""Endpoints de clientes (RF09). Roles: ADMIN, CAJERO."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Esquemas de clientes (lo que entra y lo que sale)
from app.schemas.jb_cliente_schema import JbClienteActualizar, JbClienteCrear, JbClienteRespuesta
# Esquema de pedido, para el historial de pedidos del cliente
from app.schemas.jb_pedido_schema import JbPedidoRespuesta
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de clientes, con el nombre corto jb_servicio
from app.services import jb_cliente_service as jb_servicio

# Router: rutas /clientes; TODOS sus endpoints exigen ADMIN o CAJERO
jb_router = APIRouter(prefix="/clientes", tags=["Clientes"], responses=JB_PRIVADO,
                      dependencies=[Depends(jb_requiere_roles("ADMIN", "CAJERO"))])


# GET /api/v1/clientes: lista todos
@jb_router.get("", response_model=list[JbClienteRespuesta], summary="Listar clientes")
def jb_listar_clientes():
    """**Roles:** ADMIN, CAJERO."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar()


# GET /api/v1/clientes/{id}: consulta uno
@jb_router.get("/{id_cliente}", response_model=JbClienteRespuesta, summary="Consultar un cliente", responses=JB_R404)
def jb_obtener_cliente(id_cliente: int):
    """**Roles:** ADMIN, CAJERO."""
    # Busca el cliente (404 si no existe)
    return jb_servicio.jb_obtener(id_cliente)


# GET /api/v1/clientes/{id}/pedidos: historial de pedidos del cliente
@jb_router.get("/{id_cliente}/pedidos", response_model=list[JbPedidoRespuesta],
               summary="Historial de pedidos de un cliente", responses=JB_R404)
def jb_pedidos_cliente(id_cliente: int):
    """Pedidos del cliente, del más reciente al más antiguo. **Roles:** ADMIN, CAJERO."""
    # Pide el historial al servicio
    return jb_servicio.jb_pedidos(id_cliente)


# POST /api/v1/clientes: crea uno (201)
@jb_router.post("", response_model=JbClienteRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Crear cliente", responses=JB_R409)
# El cuerpo se valida con JbClienteCrear
def jb_crear_cliente(jb_datos: JbClienteCrear):
    """Tipo de cliente: APRENDIZ, INSTRUCTOR, FUNCIONARIO o EXTERNO. La identificación no se repite.

    **Roles:** ADMIN, CAJERO.
    """
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_datos.model_dump())


# PUT /api/v1/clientes/{id}: modifica uno
@jb_router.put("/{id_cliente}", response_model=JbClienteRespuesta, summary="Actualizar cliente",
               responses={**JB_R404, **JB_R409})
# Recibe el id de la URL y el cuerpo validado con JbClienteActualizar
def jb_actualizar_cliente(id_cliente: int, jb_datos: JbClienteActualizar):
    """**Roles:** ADMIN, CAJERO."""
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(id_cliente, jb_datos.model_dump())


# DELETE /api/v1/clientes/{id}: elimina o inactiva uno
@jb_router.delete("/{id_cliente}", response_model=JbResultadoEliminacion, summary="Eliminar cliente",
                  responses=JB_R404)
def jb_eliminar_cliente(id_cliente: int):
    """RN04: si el cliente tiene pedidos pasa a INACTIVO; si no, se elimina. **Roles:** ADMIN, CAJERO."""
    # El servicio decide si es borrado lógico o físico
    return jb_servicio.jb_eliminar(id_cliente)
