"""Consultas a la tabla proveedores."""
# Session: sesión de trabajo con la base de datos
from sqlalchemy.orm import Session

# Modelos de las tablas que se consultan
from app.models.jb_modelos import JbCompra, JbProveedor
# Funciones comunes de los repositorios
from app.repositories import jb_base_repository as jb_base


# Lista todos los proveedores ordenados por id
def jb_listar(jb_sesion: Session) -> list[JbProveedor]:
    # Usa la función común
    return jb_base.jb_listar(jb_sesion, JbProveedor, JbProveedor.id_proveedor)


# Busca un proveedor por id
def jb_buscar(jb_sesion: Session, jb_id: int) -> JbProveedor | None:
    # Usa la función común
    return jb_base.jb_buscar(jb_sesion, JbProveedor, jb_id)


# Busca un proveedor por id y lo bloquea para modificarlo
def jb_buscar_para_actualizar(jb_sesion: Session, jb_id: int) -> JbProveedor | None:
    # Usa la función común (SELECT ... FOR UPDATE)
    return jb_base.jb_buscar_para_actualizar(jb_sesion, JbProveedor, jb_id)


# Revisa si el proveedor tiene compras (RN04)
def jb_tiene_compras(jb_sesion: Session, jb_id: int) -> bool:
    # EXISTS (SELECT * FROM compras WHERE id_proveedor = :id)
    return jb_base.jb_existe(jb_sesion, JbCompra.id_proveedor == jb_id)


# Guarda un proveedor nuevo o modificado
def jb_guardar(jb_sesion: Session, jb_proveedor: JbProveedor) -> JbProveedor:
    # Usa la función común
    return jb_base.jb_guardar(jb_sesion, jb_proveedor)


# Borra un proveedor
def jb_borrar(jb_sesion: Session, jb_proveedor: JbProveedor) -> None:
    # Usa la función común
    jb_base.jb_borrar(jb_sesion, jb_proveedor)
