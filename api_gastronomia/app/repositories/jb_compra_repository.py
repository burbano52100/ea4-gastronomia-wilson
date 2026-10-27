"""Consultas a las tablas compras y detalle_compra."""
# select: arma un SELECT
from sqlalchemy import select
# Session: sesión de trabajo con la base de datos
from sqlalchemy.orm import Session

# Modelo de la tabla que se consulta (su detalle se carga con la relación)
from app.models.jb_modelos import JbCompra
# Funciones comunes de los repositorios
from app.repositories import jb_base_repository as jb_base


# Lista todas las compras, de la más reciente a la más antigua
def jb_listar(jb_sesion: Session) -> list[JbCompra]:
    # SELECT * FROM compras ORDER BY fecha_compra DESC
    return list(jb_sesion.scalars(select(JbCompra).order_by(JbCompra.fecha_compra.desc(), JbCompra.id_compra.desc())))


# Busca una compra por id
def jb_buscar(jb_sesion: Session, jb_id: int) -> JbCompra | None:
    # Usa la función común
    return jb_base.jb_buscar(jb_sesion, JbCompra, jb_id)


# Busca una compra por id y la bloquea para modificarla
def jb_buscar_para_actualizar(jb_sesion: Session, jb_id: int) -> JbCompra | None:
    # Usa la función común (SELECT ... FOR UPDATE)
    return jb_base.jb_buscar_para_actualizar(jb_sesion, JbCompra, jb_id)


# Historial de compras de un proveedor
def jb_por_proveedor(jb_sesion: Session, jb_id_proveedor: int) -> list[JbCompra]:
    # SELECT * FROM compras WHERE id_proveedor = :id ORDER BY fecha_compra DESC
    return list(jb_sesion.scalars(
        # Filtra por proveedor, de la más reciente a la más antigua
        select(JbCompra).where(JbCompra.id_proveedor == jb_id_proveedor)
        # ORDER BY fecha_compra DESC: las más recientes primero
        .order_by(JbCompra.fecha_compra.desc(), JbCompra.id_compra.desc())
    ))


# Guarda una compra nueva o modificada (con sus ítems)
def jb_guardar(jb_sesion: Session, jb_compra: JbCompra) -> JbCompra:
    # Usa la función común
    return jb_base.jb_guardar(jb_sesion, jb_compra)


# Borra una compra (sus ítems se borran en cascada)
def jb_borrar(jb_sesion: Session, jb_compra: JbCompra) -> None:
    # Usa la función común
    jb_base.jb_borrar(jb_sesion, jb_compra)
