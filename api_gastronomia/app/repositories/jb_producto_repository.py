"""Consultas a la tabla productos."""
# select: arma un SELECT
from sqlalchemy import select
# Session: sesión de trabajo con la base de datos
from sqlalchemy.orm import Session

# Modelos de las tablas que se consultan
from app.models.jb_modelos import JbDetallePedido, JbProducto, JbReceta
# Funciones comunes de los repositorios
from app.repositories import jb_base_repository as jb_base


# Lista todos los productos ordenados por id
def jb_listar(jb_sesion: Session) -> list[JbProducto]:
    # Usa la función común
    return jb_base.jb_listar(jb_sesion, JbProducto, JbProducto.id_producto)


# Busca un producto por id
def jb_buscar(jb_sesion: Session, jb_id: int) -> JbProducto | None:
    # Usa la función común
    return jb_base.jb_buscar(jb_sesion, JbProducto, jb_id)


# Busca un producto por id y lo bloquea para modificarlo
def jb_buscar_para_actualizar(jb_sesion: Session, jb_id: int) -> JbProducto | None:
    # Usa la función común (SELECT ... FOR UPDATE)
    return jb_base.jb_buscar_para_actualizar(jb_sesion, JbProducto, jb_id)


# Busca varios productos de una vez (los de un pedido)
def jb_buscar_varios(jb_sesion: Session, jb_ids: list[int]) -> dict[int, JbProducto]:
    # SELECT * FROM productos WHERE id_producto IN (...)
    jb_productos = jb_sesion.scalars(select(JbProducto).where(JbProducto.id_producto.in_(jb_ids)))
    # Devuelve un diccionario {id_producto: producto} para buscarlos rápido
    return {jb_producto.id_producto: jb_producto for jb_producto in jb_productos}


# Productos de una categoría
def jb_por_categoria(jb_sesion: Session, jb_id_categoria: int) -> list[JbProducto]:
    # SELECT * FROM productos WHERE id_categoria = :id ORDER BY id_producto
    return list(jb_sesion.scalars(
        # Filtra por la categoría y ordena por id
        select(JbProducto).where(JbProducto.id_categoria == jb_id_categoria).order_by(JbProducto.id_producto)
    ))


# Revisa si el producto tiene movimientos (RN04): aparece en pedidos o tiene receta
def jb_tiene_movimientos(jb_sesion: Session, jb_id: int) -> bool:
    # Hay movimientos si aparece en algún detalle de pedido o en alguna receta
    return jb_base.jb_existe(jb_sesion, JbDetallePedido.id_producto == jb_id) or jb_base.jb_existe(
        # Segunda condición: recetas del producto
        jb_sesion, JbReceta.id_producto == jb_id
    )


# Guarda un producto nuevo o modificado
def jb_guardar(jb_sesion: Session, jb_producto: JbProducto) -> JbProducto:
    # Usa la función común
    return jb_base.jb_guardar(jb_sesion, jb_producto)


# Borra un producto
def jb_borrar(jb_sesion: Session, jb_producto: JbProducto) -> None:
    # Usa la función común
    jb_base.jb_borrar(jb_sesion, jb_producto)
