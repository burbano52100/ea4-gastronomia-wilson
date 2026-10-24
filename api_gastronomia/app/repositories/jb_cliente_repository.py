"""Acceso a la colección clientes."""
# Clase con el CRUD genérico
from app.repositories.jb_base_repository import JbRepositorioBase


# Repositorio de clientes: solo usa el CRUD heredado
class JbClienteRepository(JbRepositorioBase):
    # Constructor
    def __init__(self):
        # Colección "clientes"; el _id se responde como "id_cliente"
        super().__init__("clientes", "id_cliente")


# Instancia única que usan los servicios
jb_cliente_repository = JbClienteRepository()
