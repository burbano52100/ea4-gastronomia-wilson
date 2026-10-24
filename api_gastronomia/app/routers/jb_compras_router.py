"""Endpoints de compras de insumos (RF08, RN02). Roles: ADMIN."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R400, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Esquemas de compras (lo que entra y lo que sale)
from app.schemas.jb_compra_schema import JbCompraCrear, JbCompraRespuesta
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de compras, con el nombre corto jb_servicio
from app.services import jb_compra_service as jb_servicio

# Dependencia "solo ADMIN"; se guarda en una variable para usarla también al crear (y saber quién registra)
jb_solo_admin = jb_requiere_roles("ADMIN")
# Router: rutas /compras; TODOS sus endpoints exigen ADMIN
jb_router = APIRouter(prefix="/compras", tags=["Compras"], responses=JB_PRIVADO,
                      dependencies=[Depends(jb_solo_admin)])


# GET /api/v1/compras: lista todas
@jb_router.get("", response_model=list[JbCompraRespuesta], summary="Listar compras")
def jb_listar_compras():
    """**Roles:** ADMIN."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar()


# GET /api/v1/compras/{id}: consulta una
@jb_router.get("/{id_compra}", response_model=JbCompraRespuesta, summary="Consultar una compra", responses=JB_R404)
def jb_obtener_compra(id_compra: int):
    """**Roles:** ADMIN."""
    # Busca la compra (404 si no existe)
    return jb_servicio.jb_obtener(id_compra)


# POST /api/v1/compras: registra una (201)
@jb_router.post("", response_model=JbCompraRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Registrar compra", responses={**JB_R400, **JB_R409})
# Recibe el cuerpo validado y el usuario del token (para guardar quién registró la compra)
def jb_crear_compra(jb_datos: JbCompraCrear, jb_usuario: dict = Depends(jb_solo_admin)):
    """La API calcula subtotales y total. **RN02:** suma la cantidad comprada al `stock_actual`
    de cada insumo y actualiza su `costo_unitario`. Una factura no se repite para el mismo proveedor (409).

    **Roles:** ADMIN.
    """
    # Pasa los datos y el id del usuario al servicio
    return jb_servicio.jb_crear(jb_datos.model_dump(), jb_usuario["id_usuario"])


# PUT /api/v1/compras/{id}: modifica una
@jb_router.put("/{id_compra}", response_model=JbCompraRespuesta, summary="Actualizar compra",
               responses={**JB_R400, **JB_R404, **JB_R409})
# Recibe el id de la URL y el cuerpo validado (usa el mismo esquema de crear)
def jb_actualizar_compra(id_compra: int, jb_datos: JbCompraCrear):
    """Reemplaza la compra y ajusta el inventario con la diferencia. Si la cantidad que se quita ya se
    consumió responde 409. **Roles:** ADMIN.
    """
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(id_compra, jb_datos.model_dump())


# DELETE /api/v1/compras/{id}: anula una y descuenta del inventario lo que había sumado
@jb_router.delete("/{id_compra}", response_model=JbResultadoEliminacion, summary="Eliminar (anular) compra",
                  responses={**JB_R404, **JB_R409})
def jb_eliminar_compra(id_compra: int):
    """Resta del inventario lo que la compra había sumado y la elimina. Si esos insumos ya se
    consumieron responde 409. **Roles:** ADMIN.
    """
    # Pide al servicio que la elimine
    return jb_servicio.jb_eliminar(id_compra)
