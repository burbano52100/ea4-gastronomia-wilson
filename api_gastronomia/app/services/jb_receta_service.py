"""Reglas de negocio de recetas o fichas técnicas (RF05)."""
# Acceso a insumos
from app.repositories.jb_insumo_repository import jb_insumo_repository
# Acceso a productos
from app.repositories.jb_producto_repository import jb_producto_repository
# Acceso a recetas
from app.repositories.jb_receta_repository import jb_receta_repository
# Respuestas y errores comunes
from app.services.jb_comun import jb_borrado_fisico, jb_dato_invalido, jb_no_encontrado


# Comprueba que el producto y el insumo de la receta existan (como las llaves foráneas)
def jb_validar_referencias(jb_datos: dict) -> None:
    # Si el producto no existe...
    if jb_producto_repository.jb_buscar_por_id(jb_datos["id_producto"]) is None:
        # ...responde 400
        raise jb_dato_invalido(f"El producto {jb_datos['id_producto']} no existe")
    # Busca el insumo
    jb_insumo = jb_insumo_repository.jb_buscar_por_id(jb_datos["id_insumo"])
    # Si no existe...
    if jb_insumo is None:
        # ...responde 400
        raise jb_dato_invalido(f"El insumo {jb_datos['id_insumo']} no existe")
    # Si está INACTIVO...
    if jb_insumo["estado"] != "ACTIVO":
        # ...responde 400
        raise jb_dato_invalido(f"El insumo '{jb_insumo['nombre']}' está INACTIVO")


# Lista todas las líneas de receta
def jb_listar() -> list[dict]:
    # Pide la lista al repositorio
    return jb_receta_repository.jb_listar()


# Busca una línea de receta o responde 404
def jb_obtener(jb_id: int) -> dict:
    # Busca por id
    jb_receta = jb_receta_repository.jb_buscar_por_id(jb_id)
    # Si no existe...
    if jb_receta is None:
        # ...responde 404
        raise jb_no_encontrado(f"La línea de receta {jb_id}")
    # Devuelve la línea
    return jb_receta


# Crea una línea de receta
def jb_crear(jb_datos: dict) -> dict:
    # Comprueba producto e insumo
    jb_validar_referencias(jb_datos)
    # La inserta; si ese producto ya tiene ese insumo, el índice único hace que la API responda 409
    return jb_receta_repository.jb_insertar(jb_datos)


# Modifica una línea de receta
def jb_actualizar(jb_id: int, jb_datos: dict) -> dict:
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # Comprueba producto e insumo
    jb_validar_referencias(jb_datos)
    # Guarda los cambios y devuelve la línea actualizada
    return jb_receta_repository.jb_actualizar(jb_id, jb_datos)


# Borra una línea de receta
def jb_eliminar(jb_id: int) -> dict:
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # La borra
    jb_receta_repository.jb_eliminar(jb_id)
    # Responde que se borró
    return jb_borrado_fisico(f"La línea de receta {jb_id}")
