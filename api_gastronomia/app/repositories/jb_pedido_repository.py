"""Consultas a las tablas pedidos y detalle_pedido."""
# select: arma un SELECT
from sqlalchemy import select
# Session: sesión de trabajo con la base de datos
from sqlalchemy.orm import Session

# Modelo de la tabla que se consulta (su detalle se carga con la relación)
from app.models.jb_modelos import JbPedido
# Funciones comunes de los repositorios
from app.repositories import jb_base_repository as jb_base


# Lista todos los pedidos, del más reciente al más antiguo
def jb_listar(jb_sesion: Session) -> list[JbPedido]:
    # SELECT * FROM pedidos ORDER BY fecha_pedido DESC
    return list(jb_sesion.scalars(select(JbPedido).order_by(JbPedido.fecha_pedido.desc(), JbPedido.id_pedido.desc())))


# Busca un pedido por id
def jb_buscar(jb_sesion: Session, jb_id: int) -> JbPedido | None:
    # Usa la función común
    return jb_base.jb_buscar(jb_sesion, JbPedido, jb_id)


# Busca un pedido por id y lo bloquea para modificarlo
def jb_buscar_para_actualizar(jb_sesion: Session, jb_id: int) -> JbPedido | None:
    # Usa la función común (SELECT ... FOR UPDATE): así nadie más lo entrega o anula al mismo tiempo
    return jb_base.jb_buscar_para_actualizar(jb_sesion, JbPedido, jb_id)


# Pedidos que están en un estado
def jb_por_estado(jb_sesion: Session, jb_estado: str) -> list[JbPedido]:
    # SELECT * FROM pedidos WHERE estado = :estado ORDER BY fecha_pedido
    return list(jb_sesion.scalars(
        # Filtra por estado; los más antiguos primero (es el orden en que se atienden)
        select(JbPedido).where(JbPedido.estado == jb_estado).order_by(JbPedido.fecha_pedido, JbPedido.id_pedido)
    ))


# Historial de pedidos de un cliente
def jb_por_cliente(jb_sesion: Session, jb_id_cliente: int) -> list[JbPedido]:
    # SELECT * FROM pedidos WHERE id_cliente = :id ORDER BY fecha_pedido DESC
    return list(jb_sesion.scalars(
        # Filtra por cliente, del más reciente al más antiguo
        select(JbPedido).where(JbPedido.id_cliente == jb_id_cliente)
        # ORDER BY fecha_pedido DESC: los más recientes primero
        .order_by(JbPedido.fecha_pedido.desc(), JbPedido.id_pedido.desc())
    ))


# Guarda un pedido nuevo o modificado (con sus ítems)
def jb_guardar(jb_sesion: Session, jb_pedido: JbPedido) -> JbPedido:
    # Usa la función común
    return jb_base.jb_guardar(jb_sesion, jb_pedido)
