"""Consultas a la tabla categorias."""
# Session: sesión de trabajo con la base de datos
from sqlalchemy.orm import Session

# Modelos de las tablas que se consultan
from app.models.jb_modelos import JbCategoria, JbProducto
# Funciones comunes de los repositorios
from app.repositories import jb_base_repository as jb_base


# Lista todas las categorías ordenadas por id
def jb_listar(jb_sesion: Session) -> list[JbCategoria]:
    # Usa la función común
    return jb_base.jb_listar(jb_sesion, JbCategoria, JbCategoria.id_categoria)


# Busca una categoría por id
def jb_buscar(jb_sesion: Session, jb_id: int) -> JbCategoria | None:
    # Usa la función común
    return jb_base.jb_buscar(jb_sesion, JbCategoria, jb_id)


# Busca una categoría por id y la bloquea para modificarla
def jb_buscar_para_actualizar(jb_sesion: Session, jb_id: int) -> JbCategoria | None:
    # Usa la función común (SELECT ... FOR UPDATE)
    return jb_base.jb_buscar_para_actualizar(jb_sesion, JbCategoria, jb_id)


# Revisa si la categoría tiene productos
def jb_tiene_productos(jb_sesion: Session, jb_id: int) -> bool:
    # EXISTS (SELECT * FROM productos WHERE id_categoria = :id)
    return jb_base.jb_existe(jb_sesion, JbProducto.id_categoria == jb_id)


# Guarda una categoría nueva o modificada
def jb_guardar(jb_sesion: Session, jb_categoria: JbCategoria) -> JbCategoria:
    # Usa la función común
    return jb_base.jb_guardar(jb_sesion, jb_categoria)


# Borra una categoría
def jb_borrar(jb_sesion: Session, jb_categoria: JbCategoria) -> None:
    # Usa la función común
    jb_base.jb_borrar(jb_sesion, jb_categoria)
