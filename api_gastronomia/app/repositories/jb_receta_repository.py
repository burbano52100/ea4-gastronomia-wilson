"""Acceso a la colección recetas (relación N:M entre productos e insumos)."""
# Clase con el CRUD genérico
from app.repositories.jb_base_repository import JbRepositorioBase


# Repositorio de recetas: hereda el CRUD y agrega consultas por producto
class JbRecetaRepository(JbRepositorioBase):
    # Constructor
    def __init__(self):
        # Colección "recetas"; el _id se responde como "id_receta"
        super().__init__("recetas", "id_receta")

    # Líneas de receta de un producto
    def jb_por_producto(self, jb_id_producto: int) -> list[dict]:
        # Filtra por producto
        return self.jb_listar({"id_producto": jb_id_producto})

    # Borra toda la receta de un producto
    def jb_eliminar_por_producto(self, jb_id_producto: int) -> None:
        # delete_many borra todos los documentos que cumplan el filtro
        self.jb_coleccion.delete_many({"id_producto": jb_id_producto})


# Instancia única que usan los servicios
jb_receta_repository = JbRecetaRepository()
