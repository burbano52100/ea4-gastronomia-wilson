"""Consultas a la tabla recetas."""
# select: arma un SELECT
from sqlalchemy import select
# Session: sesión de trabajo con la base de datos
from sqlalchemy.orm import Session

# Modelo de la tabla que se consulta
from app.models.jb_modelos import JbReceta
# Funciones comunes de los repositorios
from app.repositories import jb_base_repository as jb_base


# Lista todas las líneas de receta ordenadas por producto
def jb_listar(jb_sesion: Session) -> list[JbReceta]:
    # SELECT * FROM recetas ORDER BY id_producto, id_receta
    return list(jb_sesion.scalars(select(JbReceta).order_by(JbReceta.id_producto, JbReceta.id_receta)))


# Busca una línea de receta por id
def jb_buscar(jb_sesion: Session, jb_id: int) -> JbReceta | None:
    # Usa la función común
    return jb_base.jb_buscar(jb_sesion, JbReceta, jb_id)


# Busca una línea de receta por id y la bloquea para modificarla
def jb_buscar_para_actualizar(jb_sesion: Session, jb_id: int) -> JbReceta | None:
    # Usa la función común (SELECT ... FOR UPDATE)
    return jb_base.jb_buscar_para_actualizar(jb_sesion, JbReceta, jb_id)


# Receta de un producto
def jb_por_producto(jb_sesion: Session, jb_id_producto: int) -> list[JbReceta]:
    # SELECT * FROM recetas WHERE id_producto = :id ORDER BY id_receta
    return list(jb_sesion.scalars(
        # Filtra por producto y ordena por id
        select(JbReceta).where(JbReceta.id_producto == jb_id_producto).order_by(JbReceta.id_receta)
    ))


# Recetas de varios productos a la vez (los de un pedido, para RN03)
def jb_por_productos(jb_sesion: Session, jb_ids_productos: list[int]) -> list[JbReceta]:
    # SELECT * FROM recetas WHERE id_producto IN (...)
    return list(jb_sesion.scalars(select(JbReceta).where(JbReceta.id_producto.in_(jb_ids_productos))))


# Guarda una línea de receta nueva o modificada
def jb_guardar(jb_sesion: Session, jb_receta: JbReceta) -> JbReceta:
    # Usa la función común
    return jb_base.jb_guardar(jb_sesion, jb_receta)


# Borra una línea de receta
def jb_borrar(jb_sesion: Session, jb_receta: JbReceta) -> None:
    # Usa la función común
    jb_base.jb_borrar(jb_sesion, jb_receta)
