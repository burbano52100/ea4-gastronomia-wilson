"""Endpoints de pedidos (RF10, RN01, RN03, RN05). Roles: ADMIN, CAJERO (cambio de estado: también COCINERO)."""
# Annotated: agrega información extra a un tipo
from typing import Annotated

# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R400, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Sesión de MySQL
from app.database.jb_conexion_mysql import JbSesion
# Modelo de la tabla usuarios
from app.models.jb_modelos import JbUsuario
# Esquemas de pedidos
from app.schemas.jb_pedido_schema import (
    JbEstadoPedido,  # estados permitidos de un pedido
    JbPedidoActualizar,  # datos para modificar
    JbPedidoCrear,  # datos para crear
    JbPedidoEstado,  # datos para cambiar el estado
    JbPedidoRespuesta,  # forma de la respuesta
    # ----- VENTA RAPIDA (usabilidad.md, paso B3): esquema de la venta -----
    JbVentaCrear,  # datos de la venta rápida
)
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de pedidos, con el nombre corto jb_servicio
from app.services import jb_pedido_service as jb_servicio

# Router: rutas /pedidos, sección "Pedidos" de Swagger
jb_router = APIRouter(prefix="/pedidos", tags=["Pedidos"], responses=JB_PRIVADO)
# Dependencia para el CRUD: ADMIN y CAJERO
jb_caja = jb_requiere_roles("ADMIN", "CAJERO")
# Dependencia para consultar por estado y cambiar el estado: también COCINERO (prepara y entrega)
jb_cocina = jb_requiere_roles("ADMIN", "CAJERO", "COCINERO")


# GET /api/v1/pedidos: lista todos
@jb_router.get("", response_model=list[JbPedidoRespuesta], dependencies=[Depends(jb_caja)], summary="Listar pedidos")
# Recibe la sesión de MySQL
def jb_listar_pedidos(jb_sesion: JbSesion):
    """Pedidos con su detalle, del más reciente al más antiguo. **Roles:** ADMIN, CAJERO."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar(jb_sesion)


# GET /api/v1/pedidos/estado/{estado}: va antes de /{id_pedido} porque es una ruta fija
@jb_router.get("/estado/{estado}", response_model=list[JbPedidoRespuesta], dependencies=[Depends(jb_cocina)],
               summary="Pedidos por estado")  # título en Swagger
# Recibe el estado de la URL y la sesión de MySQL
def jb_pedidos_por_estado(estado: JbEstadoPedido, jb_sesion: JbSesion):
    """Pedidos en un estado (PENDIENTE, EN_PREPARACION, ENTREGADO o ANULADO), del más antiguo al más reciente,
    que es el orden en que se atienden. Un estado distinto responde 422.

    **Roles:** ADMIN, CAJERO, COCINERO (el cocinero necesita ver los pedidos pendientes).
    """
    # Pide la consulta al servicio
    return jb_servicio.jb_por_estado(jb_sesion, estado)


# GET /api/v1/pedidos/{id}: consulta uno
@jb_router.get("/{id_pedido}", response_model=JbPedidoRespuesta, dependencies=[Depends(jb_caja)],
               summary="Consultar un pedido", responses=JB_R404)  # título en Swagger y errores que puede responder
# Recibe el id_pedido de la URL y la sesión de MySQL
def jb_obtener_pedido(id_pedido: int, jb_sesion: JbSesion):
    """**Roles:** ADMIN, CAJERO."""
    # Busca el pedido (404 si no existe)
    return jb_servicio.jb_obtener(jb_sesion, id_pedido)


# POST /api/v1/pedidos: registra uno (201)
@jb_router.post("", response_model=JbPedidoRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Registrar pedido", responses={**JB_R400, **JB_R409})  # título en Swagger y errores que puede responder
# jb_usuario es el ADMIN o CAJERO que registra el pedido
def jb_crear_pedido(jb_datos: JbPedidoCrear, jb_sesion: JbSesion, jb_usuario: Annotated[JbUsuario, Depends(jb_caja)]):
    """**RN01:** se envían solo productos y cantidades. La API toma el precio de venta de cada producto,
    calcula `subtotal = cantidad x precio_unitario` y el total. El pedido empieza PENDIENTE y el usuario
    que registra se toma del token. Los productos AGOTADO o INACTIVO no se pueden pedir.

    **Roles:** ADMIN, CAJERO.
    """
    # Pasa los datos y el id del usuario del token al servicio
    return jb_servicio.jb_crear(jb_sesion, jb_datos.model_dump(), jb_usuario.id_usuario)


# PUT /api/v1/pedidos/{id}: modifica uno
@jb_router.put("/{id_pedido}", response_model=JbPedidoRespuesta, dependencies=[Depends(jb_caja)],
               summary="Actualizar pedido", responses={**JB_R400, **JB_R404, **JB_R409})  # título en Swagger y errores que puede responder
# Recibe el id_pedido de la URL, el cuerpo JSON ya validado y la sesión de MySQL
def jb_actualizar_pedido(id_pedido: int, jb_datos: JbPedidoActualizar, jb_sesion: JbSesion):
    """Reemplaza el detalle y recalcula el total (RN01). **RN05:** un pedido ENTREGADO o ANULADO no se modifica (409).

    **Roles:** ADMIN, CAJERO.
    """
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(jb_sesion, id_pedido, jb_datos.model_dump())


# PATCH /api/v1/pedidos/{id}/estado: cambia el estado
@jb_router.patch("/{id_pedido}/estado", response_model=JbPedidoRespuesta, dependencies=[Depends(jb_cocina)],
                 summary="Cambiar el estado del pedido", responses={**JB_R404, **JB_R409})  # título en Swagger y errores que puede responder
# Recibe el id_pedido de la URL, el cuerpo JSON ya validado y la sesión de MySQL
def jb_cambiar_estado_pedido(id_pedido: int, jb_datos: JbPedidoEstado, jb_sesion: JbSesion):
    """Flujo: PENDIENTE -> EN_PREPARACION -> ENTREGADO; se puede ANULAR desde PENDIENTE o EN_PREPARACION.

    **RN03:** al pasar a ENTREGADO se descuentan del inventario los insumos de la receta de cada producto.
    Si no alcanzan responde 409 y no descuenta nada. **RN05:** un pedido ENTREGADO o ANULADO no cambia (409).

    **Roles:** ADMIN, CAJERO, COCINERO.
    """
    # Pasa el id y el estado nuevo al servicio
    return jb_servicio.jb_cambiar_estado(jb_sesion, id_pedido, jb_datos.estado)


# DELETE /api/v1/pedidos/{id}: anula uno
@jb_router.delete("/{id_pedido}", response_model=JbResultadoEliminacion, dependencies=[Depends(jb_caja)],
                  summary="Anular pedido", responses={**JB_R404, **JB_R409})  # título en Swagger y errores que puede responder
# Recibe el id_pedido de la URL y la sesión de MySQL
def jb_eliminar_pedido(id_pedido: int, jb_sesion: JbSesion):
    """Un pedido no se borra porque es parte del historial de ventas: queda ANULADO.
    **RN05:** si ya está ENTREGADO o ANULADO responde 409.

    **Roles:** ADMIN, CAJERO.
    """
    # Pide la anulación al servicio
    return jb_servicio.jb_eliminar(jb_sesion, id_pedido)


# ----- VENTA RAPIDA (usabilidad.md, paso B3): ruta POST /api/v1/pedidos/venta -----
# Dependencia para la venta rápida: solo ADMIN
jb_solo_admin = jb_requiere_roles("ADMIN")


# POST /api/v1/pedidos/venta: vende un producto en un solo paso (201, solo ADMIN)
@jb_router.post("/venta", response_model=JbPedidoRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Venta rápida de un producto", responses={**JB_R400, **JB_R409})  # título en Swagger y errores que puede responder
# jb_usuario es el ADMIN que hace la venta (sale del token)
def jb_venta_rapida(jb_datos: JbVentaCrear, jb_sesion: JbSesion, jb_usuario: Annotated[JbUsuario, Depends(jb_solo_admin)]):
    """Registra un pedido de un solo producto que queda ENTREGADO de una vez.
    **RN01:** el precio sale de la base de datos. **RN03:** descuenta del inventario los insumos de la receta;
    si no alcanzan responde 409 y no se guarda nada.

    **Roles:** ADMIN.
    """
    # Pasa los datos y el id del usuario del token al servicio
    return jb_servicio.jb_vender(jb_sesion, jb_datos.model_dump(), jb_usuario.id_usuario)
