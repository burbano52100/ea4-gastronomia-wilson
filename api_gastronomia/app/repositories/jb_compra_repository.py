"""Acceso a la colección compras. El detalle de cada compra va embebido en el mismo documento."""
# Clase con el CRUD genérico
from app.repositories.jb_base_repository import JbRepositorioBase


# Repositorio de compras: hereda el CRUD y agrega la consulta por proveedor
class JbCompraRepository(JbRepositorioBase):
    # Constructor
    def __init__(self):
        # Colección "compras"; el _id se responde como "id_compra"
        super().__init__("compras", "id_compra")

    # Historial de compras de un proveedor
    def jb_por_proveedor(self, jb_id_proveedor: int) -> list[dict]:
        # Filtra por proveedor y ordena de la más reciente a la más antigua (-1 = descendente)
        return self.jb_listar({"id_proveedor": jb_id_proveedor}, [("fecha_compra", -1)])


# Instancia única que usan los servicios
jb_compra_repository = JbCompraRepository()
