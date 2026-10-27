"""Endpoints de compras (RF08, RN02). Roles: solo ADMIN."""
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
# Esquemas de compras
from app.schemas.jb_compra_schema import JbCompraActualizar, JbCompraCrear, JbCompraRespuesta
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de compras, con el nombre corto jb_servicio
from app.services import jb_compra_service as jb_servicio

# Dependencia que solo deja pasar al rol ADMIN
jb_solo_admin = jb_requiere_roles("ADMIN")
# Router: rutas /compras, sección "Compras" de Swagger; TODOS sus endpoints exigen ADMIN
jb_router = APIRouter(prefix="/compras", tags=["Compras"], dependencies=[Depends(jb_solo_admin)], responses=JB_PRIVADO)


# GET /api/v1/compras: lista todas
@jb_router.get("", response_model=list[JbCompraRespuesta], summary="Listar compras")
# Recibe la sesión de MySQL
def jb_listar_compras(jb_sesion: JbSesion):
    """Compras con su detalle, de la más reciente a la más antigua. **Roles:** ADMIN."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar(jb_sesion)


# GET /api/v1/compras/{id}: consulta una
@jb_router.get("/{id_compra}", response_model=JbCompraRespuesta, summary="Consultar una compra", responses=JB_R404)
# Recibe el id_compra de la URL y la sesión de MySQL
def jb_obtener_compra(id_compra: int, jb_sesion: JbSesion):
    """**Roles:** ADMIN."""
    # Busca la compra (404 si no existe)
    return jb_servicio.jb_obtener(jb_sesion, id_compra)


# POST /api/v1/compras: registra una (201)
@jb_router.post("", response_model=JbCompraRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Registrar compra", responses={**JB_R400, **JB_R409})  # título en Swagger y errores que puede responder
# jb_usuario es el ADMIN que registra (la misma dependencia del router, no se ejecuta dos veces)
def jb_crear_compra(jb_datos: JbCompraCrear, jb_sesion: JbSesion, jb_usuario: Annotated[JbUsuario, Depends(jb_solo_admin)]):
    """Se envían solo insumo, cantidad y costo de cada ítem: subtotales y total los calcula la API.

    **RN02:** por cada insumo comprado sube su `stock_actual` y su `costo_unitario` pasa a ser el de esta compra.
    Todo se guarda en una sola transacción. El usuario que registra se toma del token.

    **Roles:** ADMIN.
    """
    # Pasa los datos y el id del usuario del token al servicio
    return jb_servicio.jb_crear(jb_sesion, jb_datos.model_dump(), jb_usuario.id_usuario)


# PUT /api/v1/compras/{id}: modifica los datos generales
@jb_router.put("/{id_compra}", response_model=JbCompraRespuesta, summary="Actualizar datos de una compra",
               responses={**JB_R400, **JB_R404, **JB_R409})  # errores que puede responder
# Recibe el id_compra de la URL, el cuerpo JSON ya validado y la sesión de MySQL
def jb_actualizar_compra(id_compra: int, jb_datos: JbCompraActualizar, jb_sesion: JbSesion):
    """Cambia factura, fecha y proveedor. El detalle no se cambia porque ya movió el inventario:
    si una compra quedó mal, se elimina y se registra de nuevo.

    **Roles:** ADMIN.
    """
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(jb_sesion, id_compra, jb_datos.model_dump())


# DELETE /api/v1/compras/{id}: elimina una y devuelve el inventario
@jb_router.delete("/{id_compra}", response_model=JbResultadoEliminacion, summary="Eliminar compra",
                  responses={**JB_R404, **JB_R409})  # errores que puede responder
# Recibe el id_compra de la URL y la sesión de MySQL
def jb_eliminar_compra(id_compra: int, jb_sesion: JbSesion):
    """Resta del stock lo que la compra había sumado. Si parte de lo comprado ya se usó (el stock
    quedaría negativo) responde 409 y no cambia nada.

    **Roles:** ADMIN.
    """
    # Pide el borrado al servicio
    return jb_servicio.jb_eliminar(jb_sesion, id_compra)
