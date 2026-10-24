"""Acceso a la colección categorias."""
# Clase con el CRUD genérico
from app.repositories.jb_base_repository import JbRepositorioBase


# Repositorio de categorías: solo usa el CRUD heredado
class JbCategoriaRepository(JbRepositorioBase):
    # Constructor
    def __init__(self):
        # Colección "categorias"; el _id se responde como "id_categoria"
        super().__init__("categorias", "id_categoria")


# Instancia única que usan los servicios
jb_categoria_repository = JbCategoriaRepository()
