"""Acceso a la colección pedidos. El detalle de cada pedido va embebido en el mismo documento."""
# Clase con el CRUD genérico
from app.repositories.jb_base_repository import JbRepositorioBase


# Repositorio de pedidos: hereda el CRUD y agrega consultas por estado y por cliente
class JbPedidoRepository(JbRepositorioBase):
    # Constructor
    def __init__(self):
        # Colección "pedidos"; el _id se responde como "id_pedido"
        super().__init__("pedidos", "id_pedido")

    # Pedidos que están en un estado
    def jb_por_estado(self, jb_estado: str) -> list[dict]:
        # Filtra por estado y ordena del más antiguo al más reciente (para atenderlos en orden)
        return self.jb_listar({"estado": jb_estado}, [("fecha_pedido", 1)])

    # Historial de pedidos de un cliente
    def jb_por_cliente(self, jb_id_cliente: int) -> list[dict]:
        # Filtra por cliente y ordena del más reciente al más antiguo
        return self.jb_listar({"id_cliente": jb_id_cliente}, [("fecha_pedido", -1)])

    # Cambia el estado de forma segura
    def jb_cambiar_estado_si(self, jb_id: int, jb_estado_actual: str, jb_estado_nuevo: str) -> bool:
        """Cambia el estado solo si el pedido sigue en el estado que se leyó (evita entregarlo dos veces)."""
        # Actualización condicional
        jb_resultado = self.jb_coleccion.update_one(
            # Condición: el pedido y que todavía tenga el estado que se leyó antes
            {"_id": jb_id, "estado": jb_estado_actual},
            # $set pone el estado nuevo
            {"$set": {"estado": jb_estado_nuevo}},
        )
        # True si se cambió; False si otro usuario lo cambió primero
        return jb_resultado.modified_count == 1


# Instancia única que usan los servicios
jb_pedido_repository = JbPedidoRepository()
