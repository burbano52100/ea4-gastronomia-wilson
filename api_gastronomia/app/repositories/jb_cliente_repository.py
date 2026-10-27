"""Consultas a la tabla clientes."""
# Session: sesión de trabajo con la base de datos
from sqlalchemy.orm import Session

# Modelos de las tablas que se consultan
from app.models.jb_modelos import JbCliente, JbPedido
# Funciones comunes de los repositorios
from app.repositories import jb_base_repository as jb_base


# Lista todos los clientes ordenados por id
def jb_listar(jb_sesion: Session) -> list[JbCliente]:
    # Usa la función común
    return jb_base.jb_listar(jb_sesion, JbCliente, JbCliente.id_cliente)


# Busca un cliente por id
def jb_buscar(jb_sesion: Session, jb_id: int) -> JbCliente | None:
    # Usa la función común
    return jb_base.jb_buscar(jb_sesion, JbCliente, jb_id)


# Busca un cliente por id y lo bloquea para modificarlo
def jb_buscar_para_actualizar(jb_sesion: Session, jb_id: int) -> JbCliente | None:
    # Usa la función común (SELECT ... FOR UPDATE)
    return jb_base.jb_buscar_para_actualizar(jb_sesion, JbCliente, jb_id)


# Revisa si el cliente tiene pedidos (RN04)
def jb_tiene_pedidos(jb_sesion: Session, jb_id: int) -> bool:
    # EXISTS (SELECT * FROM pedidos WHERE id_cliente = :id)
    return jb_base.jb_existe(jb_sesion, JbPedido.id_cliente == jb_id)


# Guarda un cliente nuevo o modificado
def jb_guardar(jb_sesion: Session, jb_cliente: JbCliente) -> JbCliente:
    # Usa la función común
    return jb_base.jb_guardar(jb_sesion, jb_cliente)


# Borra un cliente
def jb_borrar(jb_sesion: Session, jb_cliente: JbCliente) -> None:
    # Usa la función común
    jb_base.jb_borrar(jb_sesion, jb_cliente)
