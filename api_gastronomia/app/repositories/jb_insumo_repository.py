"""Consultas a la tabla insumos."""
# date: solo fecha
from datetime import date

# select: arma un SELECT
from sqlalchemy import select
# Session: sesión de trabajo con la base de datos
from sqlalchemy.orm import Session

# Modelos de las tablas que se consultan
from app.models.jb_modelos import JbDetalleCompra, JbInsumo, JbReceta
# Funciones comunes de los repositorios
from app.repositories import jb_base_repository as jb_base


# Lista todos los insumos ordenados por id
def jb_listar(jb_sesion: Session) -> list[JbInsumo]:
    # Usa la función común
    return jb_base.jb_listar(jb_sesion, JbInsumo, JbInsumo.id_insumo)


# Busca un insumo por id
def jb_buscar(jb_sesion: Session, jb_id: int) -> JbInsumo | None:
    # Usa la función común
    return jb_base.jb_buscar(jb_sesion, JbInsumo, jb_id)


# Busca un insumo por id y lo bloquea para modificarlo
def jb_buscar_para_actualizar(jb_sesion: Session, jb_id: int) -> JbInsumo | None:
    # Usa la función común (SELECT ... FOR UPDATE)
    return jb_base.jb_buscar_para_actualizar(jb_sesion, JbInsumo, jb_id)


# Busca y bloquea varios insumos (los de una compra o los que descuenta un pedido)
def jb_buscar_varios_para_actualizar(jb_sesion: Session, jb_ids: list[int]) -> dict[int, JbInsumo]:
    """SELECT ... FOR UPDATE ordenado por id: siempre se bloquean en el mismo orden, así dos operaciones
    al mismo tiempo no se quedan esperándose la una a la otra (bloqueo mutuo)."""
    # Arma la consulta: insumos cuyos id estén en la lista
    jb_consulta = (
        # SELECT * FROM insumos WHERE id_insumo IN (...)
        select(JbInsumo).where(JbInsumo.id_insumo.in_(jb_ids))
        # ORDER BY id_insumo
        .order_by(JbInsumo.id_insumo)
        # FOR UPDATE
        .with_for_update()
        # Trae los valores frescos de la base aunque el objeto ya estuviera en la sesión
        .execution_options(populate_existing=True)
    )
    # Devuelve un diccionario {id_insumo: insumo}
    return {jb_insumo.id_insumo: jb_insumo for jb_insumo in jb_sesion.scalars(jb_consulta)}


# Insumos activos con stock_actual menor o igual a stock_minimo (RF07)
def jb_stock_bajo(jb_sesion: Session) -> list[JbInsumo]:
    # SELECT * FROM insumos WHERE estado = 'ACTIVO' AND stock_actual <= stock_minimo ORDER BY nombre
    return list(jb_sesion.scalars(
        # Condiciones del filtro y orden por nombre
        select(JbInsumo).where(JbInsumo.estado == "ACTIVO", JbInsumo.stock_actual <= JbInsumo.stock_minimo)
        # ORDER BY nombre: en orden alfabético
        .order_by(JbInsumo.nombre)
    ))


# Insumos activos que vencen entre dos fechas (RF07)
def jb_por_vencer(jb_sesion: Session, jb_desde: date, jb_hasta: date) -> list[JbInsumo]:
    # SELECT * FROM insumos WHERE estado = 'ACTIVO' AND fecha_vencimiento BETWEEN :desde AND :hasta
    return list(jb_sesion.scalars(
        # Solo insumos activos
        select(JbInsumo).where(JbInsumo.estado == "ACTIVO", JbInsumo.fecha_vencimiento.between(jb_desde, jb_hasta))
        # Primero los que vencen antes
        .order_by(JbInsumo.fecha_vencimiento, JbInsumo.nombre)
    ))


# Revisa si el insumo tiene movimientos (RN04): aparece en compras o en recetas
def jb_tiene_movimientos(jb_sesion: Session, jb_id: int) -> bool:
    # Hay movimientos si aparece en algún detalle de compra o en alguna receta
    return jb_base.jb_existe(jb_sesion, JbDetalleCompra.id_insumo == jb_id) or jb_base.jb_existe(
        # Segunda condición: recetas que usan el insumo
        jb_sesion, JbReceta.id_insumo == jb_id
    )


# Guarda un insumo nuevo o modificado
def jb_guardar(jb_sesion: Session, jb_insumo: JbInsumo) -> JbInsumo:
    # Usa la función común
    return jb_base.jb_guardar(jb_sesion, jb_insumo)


# Borra un insumo
def jb_borrar(jb_sesion: Session, jb_insumo: JbInsumo) -> None:
    # Usa la función común
    jb_base.jb_borrar(jb_sesion, jb_insumo)
