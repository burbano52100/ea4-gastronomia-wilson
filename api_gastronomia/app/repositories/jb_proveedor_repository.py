"""Acceso a la colección proveedores."""
# Clase con el CRUD genérico
from app.repositories.jb_base_repository import JbRepositorioBase


# Repositorio de proveedores: solo usa el CRUD heredado
class JbProveedorRepository(JbRepositorioBase):
    # Constructor
    def __init__(self):
        # Colección "proveedores"; el _id se responde como "id_proveedor"
        super().__init__("proveedores", "id_proveedor")


# Instancia única que usan los servicios
jb_proveedor_repository = JbProveedorRepository()
