"""Reglas de negocio de categorías (RF03)."""
# Acceso a categorías
from app.repositories.jb_categoria_repository import jb_categoria_repository
# Acceso a productos (para saber si una categoría tiene productos)
from app.repositories.jb_producto_repository import jb_producto_repository
# Respuestas y errores comunes
from app.services.jb_comun import jb_borrado_fisico, jb_borrado_logico, jb_no_encontrado


# Lista todas las categorías
def jb_listar() -> list[dict]:
    # Pide la lista al repositorio
    return jb_categoria_repository.jb_listar()


# Busca una categoría o responde 404
def jb_obtener(jb_id: int) -> dict:
    # Busca por id
    jb_categoria = jb_categoria_repository.jb_buscar_por_id(jb_id)
    # Si no existe...
    if jb_categoria is None:
        # ...responde 404
        raise jb_no_encontrado(f"La categoría {jb_id}")
    # Devuelve la categoría
    return jb_categoria


# Crea una categoría
def jb_crear(jb_datos: dict) -> dict:
    # Toda categoría nueva empieza ACTIVA
    jb_datos["estado"] = "ACTIVO"
    # La inserta (si el nombre ya existe, MongoDB lanza error y la API responde 409)
    return jb_categoria_repository.jb_insertar(jb_datos)


# Modifica una categoría
def jb_actualizar(jb_id: int, jb_datos: dict) -> dict:
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # Guarda los cambios y devuelve la categoría actualizada
    return jb_categoria_repository.jb_actualizar(jb_id, jb_datos)


# Elimina una categoría
def jb_eliminar(jb_id: int) -> dict:
    """Una categoría con productos no se borra: pasa a INACTIVO (mismo criterio de RN04)."""
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # Si hay algún producto de esta categoría...
    if jb_producto_repository.jb_existe({"id_categoria": jb_id}):
        # ...se marca INACTIVA en vez de borrarla
        jb_categoria_repository.jb_actualizar(jb_id, {"estado": "INACTIVO"})
        # Responde borrado lógico
        return jb_borrado_logico(f"La categoría {jb_id}")
    # Si no tiene productos, se borra de verdad
    jb_categoria_repository.jb_eliminar(jb_id)
    # Responde borrado físico
    return jb_borrado_fisico(f"La categoría {jb_id}")
