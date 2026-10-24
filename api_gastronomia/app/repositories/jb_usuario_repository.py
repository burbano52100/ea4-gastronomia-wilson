"""Acceso a la colección usuarios. El hash de la contraseña se oculta en todas las consultas (RN06)."""
# Clase con el CRUD genérico
from app.repositories.jb_base_repository import JbRepositorioBase


# Repositorio de usuarios: oculta la contraseña y agrega la búsqueda para el login
class JbUsuarioRepository(JbRepositorioBase):
    # Constructor
    def __init__(self):
        # Colección "usuarios", id "id_usuario"; el campo password nunca se devuelve
        super().__init__("usuarios", "id_usuario", jb_campos_ocultos=("password",))

    # Busca un usuario por correo, con su contraseña cifrada
    def jb_buscar_para_login(self, jb_correo: str) -> dict | None:
        """Única consulta que devuelve el hash de la contraseña: solo la usa el login."""
        # find_one sin proyección: trae todos los campos, incluido el hash
        return self.jb_coleccion.find_one({"correo": jb_correo})


# Instancia única que usan los servicios
jb_usuario_repository = JbUsuarioRepository()
