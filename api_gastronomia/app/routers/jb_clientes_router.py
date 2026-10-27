"""Endpoints de clientes (RF09). Roles: ADMIN, CAJERO."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Sesión de MySQL
from app.database.jb_conexion_mysql import JbSesion
# Esquemas de clientes
from app.schemas.jb_cliente_schema import JbClienteActualizar, JbClienteCrear, JbClienteRespuesta
# Esquema de los pedidos (para el historial)
from app.schemas.jb_pedido_schema import JbPedidoRespuesta
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de clientes, con el nombre corto jb_servicio
from app.services import jb_cliente_service as jb_servicio

# Router: rutas /clientes; TODOS sus endpoints exigen ADMIN o CAJERO
jb_router = APIRouter(
    # Prefijo de las rutas
    prefix="/clientes",
    # Sección de Swagger
    tags=["Clientes"],
    # Seguridad de todo el router
    dependencies=[Depends(jb_requiere_roles("ADMIN", "CAJERO"))],
    # Errores 401 y 403 en todos los endpoints
    responses=JB_PRIVADO,
)


# GET /api/v1/clientes: lista todos
@jb_router.get("", response_model=list[JbClienteRespuesta], summary="Listar clientes")
# Recibe la sesión de MySQL
def jb_listar_clientes(jb_sesion: JbSesion):
    """**Roles:** ADMIN, CAJERO."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar(jb_sesion)


# GET /api/v1/clientes/{id}: consulta uno
@jb_router.get("/{id_cliente}", response_model=JbClienteRespuesta, summary="Consultar un cliente", responses=JB_R404)
# Recibe el id_cliente de la URL y la sesión de MySQL
def jb_obtener_cliente(id_cliente: int, jb_sesion: JbSesion):
    """**Roles:** ADMIN, CAJERO."""
    # Busca el cliente (404 si no existe)
    return jb_servicio.jb_obtener(jb_sesion, id_cliente)


# GET /api/v1/clientes/{id}/pedidos: historial de pedidos
@jb_router.get("/{id_cliente}/pedidos", response_model=list[JbPedidoRespuesta],
               summary="Historial de pedidos de un cliente", responses=JB_R404)  # título en Swagger y errores que puede responder
# Recibe el id_cliente de la URL y la sesión de MySQL
def jb_pedidos_cliente(id_cliente: int, jb_sesion: JbSesion):
    """Pedidos del cliente con su detalle, del más reciente al más antiguo. **Roles:** ADMIN, CAJERO."""
    # Pide el historial al servicio (404 si el cliente no existe)
    return jb_servicio.jb_pedidos(jb_sesion, id_cliente)


# POST /api/v1/clientes: crea uno (201)
@jb_router.post("", response_model=JbClienteRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Crear cliente", responses=JB_R409)  # título en Swagger y errores que puede responder
# Recibe el cuerpo JSON ya validado y la sesión de MySQL
def jb_crear_cliente(jb_datos: JbClienteCrear, jb_sesion: JbSesion):
    """La identificación no se repite. **Roles:** ADMIN, CAJERO."""
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_sesion, jb_datos.model_dump())


# PUT /api/v1/clientes/{id}: modifica uno
@jb_router.put("/{id_cliente}", response_model=JbClienteRespuesta, summary="Actualizar cliente",
               responses={**JB_R404, **JB_R409})  # errores que puede responder
# Recibe el id_cliente de la URL, el cuerpo JSON ya validado y la sesión de MySQL
def jb_actualizar_cliente(id_cliente: int, jb_datos: JbClienteActualizar, jb_sesion: JbSesion):
    """**Roles:** ADMIN, CAJERO."""
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(jb_sesion, id_cliente, jb_datos.model_dump())


# DELETE /api/v1/clientes/{id}: elimina o inactiva uno
@jb_router.delete("/{id_cliente}", response_model=JbResultadoEliminacion, summary="Eliminar cliente", responses=JB_R404)
# Recibe el id_cliente de la URL y la sesión de MySQL
def jb_eliminar_cliente(id_cliente: int, jb_sesion: JbSesion):
    """RN04: si el cliente tiene pedidos pasa a INACTIVO; si no, se borra. **Roles:** ADMIN, CAJERO."""
    # El servicio decide si es borrado lógico o físico
    return jb_servicio.jb_eliminar(jb_sesion, id_cliente)
