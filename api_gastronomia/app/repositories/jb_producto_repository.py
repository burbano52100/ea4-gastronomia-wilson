"""Acceso a la colección productos."""
# Clase con el CRUD genérico
from app.repositories.jb_base_repository import JbRepositorioBase


# Repositorio de productos: hereda el CRUD y agrega la consulta por categoría
class JbProductoRepository(JbRepositorioBase):
    # Constructor
    def __init__(self):
        # Colección "productos"; el _id se responde como "id_producto"
        super().__init__("productos", "id_producto")

    # Productos de una categoría
    def jb_por_categoria(self, jb_id_categoria: int) -> list[dict]:
        # Filtra por categoría
        return self.jb_listar({"id_categoria": jb_id_categoria})


# Instancia única que usan los servicios
jb_producto_repository = JbProductoRepository()
