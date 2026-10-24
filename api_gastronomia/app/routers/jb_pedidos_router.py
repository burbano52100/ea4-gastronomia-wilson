"""Endpoints de pedidos (RF10). Roles: ADMIN, CAJERO; el COCINERO consulta y cambia el estado."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R400, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Esquemas de pedidos (lo que entra y lo que sale) y la lista de estados
from app.schemas.jb_pedido_schema import JbEstadoPedido, JbPedidoCrear, JbPedidoEstado, JbPedidoRespuesta
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de pedidos, con el nombre corto jb_servicio
from app.services import jb_pedido_service as jb_servicio

# Router: rutas /pedidos; los roles se ponen en cada endpoint porque cambian
jb_router = APIRouter(prefix="/pedidos", tags=["Pedidos"], responses=JB_PRIVADO)
# Dependencia de ventas: ADMIN o CAJERO (crear, modificar y anular)
jb_ventas = jb_requiere_roles("ADMIN", "CAJERO")
# El cocinero necesita ver los pedidos para prepararlos y cambiarles el estado.
JB_CONSULTA = [Depends(jb_requiere_roles("ADMIN", "CAJERO", "COCINERO"))]


# GET /api/v1/pedidos: lista todos
@jb_router.get("", response_model=list[JbPedidoRespuesta], dependencies=JB_CONSULTA, summary="Listar pedidos")
def jb_listar_pedidos():
    """**Roles:** ADMIN, CAJERO, COCINERO."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar()


# GET /api/v1/pedidos/estado/{estado}: va antes de /{id_pedido}
@jb_router.get("/estado/{estado}", response_model=list[JbPedidoRespuesta], dependencies=JB_CONSULTA,
               summary="Pedidos filtrados por estado")
# estado se toma de la URL y solo acepta los valores de JbEstadoPedido (si no, 422)
def jb_pedidos_por_estado(estado: JbEstadoPedido):
    """Estados: PENDIENTE, EN_PREPARACION, ENTREGADO, ANULADO. **Roles:** ADMIN, CAJERO, COCINERO."""
    # Pide la consulta al servicio
    return jb_servicio.jb_por_estado(estado)


# GET /api/v1/pedidos/{id}: consulta uno
@jb_router.get("/{id_pedido}", response_model=JbPedidoRespuesta, dependencies=JB_CONSULTA,
               summary="Consultar un pedido", responses=JB_R404)
def jb_obtener_pedido(id_pedido: int):
    """**Roles:** ADMIN, CAJERO, COCINERO."""
    # Busca el pedido (404 si no existe)
    return jb_servicio.jb_obtener(id_pedido)


# POST /api/v1/pedidos: registra uno (201)
@jb_router.post("", response_model=JbPedidoRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Registrar pedido", responses=JB_R400)
# Recibe el cuerpo validado y el usuario del token (exige ADMIN o CAJERO)
def jb_crear_pedido(jb_datos: JbPedidoCrear, jb_usuario: dict = Depends(jb_ventas)):
    """Solo se envían productos y cantidades. **RN01:** la API toma el precio de cada producto,
    calcula `subtotal = cantidad * precio_unitario` y el total. El pedido inicia PENDIENTE.

    **Roles:** ADMIN, CAJERO.
    """
    # Pasa los datos y el id del usuario que registra al servicio
    return jb_servicio.jb_crear(jb_datos.model_dump(), jb_usuario["id_usuario"])


# PUT /api/v1/pedidos/{id}: modifica uno (ADMIN o CAJERO)
@jb_router.put("/{id_pedido}", response_model=JbPedidoRespuesta, dependencies=[Depends(jb_ventas)],
               summary="Actualizar pedido", responses={**JB_R400, **JB_R404, **JB_R409})
# Recibe el id de la URL y el cuerpo validado (usa el mismo esquema de crear)
def jb_actualizar_pedido(id_pedido: int, jb_datos: JbPedidoCrear):
    """Recalcula el detalle y el total (RN01). **RN05:** un pedido ENTREGADO o ANULADO responde 409.

    **Roles:** ADMIN, CAJERO.
    """
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(id_pedido, jb_datos.model_dump())


# PATCH /api/v1/pedidos/{id}/estado: cambia solo el estado (también el COCINERO)
@jb_router.patch("/{id_pedido}/estado", response_model=JbPedidoRespuesta,
                 dependencies=[Depends(jb_requiere_roles("ADMIN", "CAJERO", "COCINERO"))],
                 summary="Cambiar el estado del pedido", responses={**JB_R400, **JB_R404, **JB_R409})
# Recibe el id de la URL y el cuerpo {"estado": ...}
def jb_cambiar_estado_pedido(id_pedido: int, jb_datos: JbPedidoEstado):
    """**RN03:** al pasar a ENTREGADO se descuentan del inventario los insumos de la receta de cada
    producto; si no alcanza responde 409 y no descuenta nada.
    **RN05:** un pedido ENTREGADO o ANULADO ya no cambia (409).

    **Roles:** ADMIN, CAJERO, COCINERO.
    """
    # Pasa el id y el estado nuevo al servicio
    return jb_servicio.jb_cambiar_estado(id_pedido, jb_datos.estado)


# DELETE /api/v1/pedidos/{id}: no borra, ANULA el pedido (ADMIN o CAJERO)
@jb_router.delete("/{id_pedido}", response_model=JbResultadoEliminacion, dependencies=[Depends(jb_ventas)],
                  summary="Anular pedido", responses={**JB_R404, **JB_R409})
def jb_anular_pedido(id_pedido: int):
    """Los pedidos no se borran: quedan ANULADOS (borrado lógico). RN05 aplica si ya está cerrado.

    **Roles:** ADMIN, CAJERO.
    """
    # Pide al servicio que lo anule
    return jb_servicio.jb_eliminar(id_pedido)
