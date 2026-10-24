"""Reglas de negocio de proveedores (RF08)."""
# Acceso a compras (para el historial y para saber si el proveedor tiene movimientos)
from app.repositories.jb_compra_repository import jb_compra_repository
# Acceso a proveedores
from app.repositories.jb_proveedor_repository import jb_proveedor_repository
# Respuestas y errores comunes
from app.services.jb_comun import jb_borrado_fisico, jb_borrado_logico, jb_no_encontrado


# Lista todos los proveedores
def jb_listar() -> list[dict]:
    # Pide la lista al repositorio
    return jb_proveedor_repository.jb_listar()


# Busca un proveedor o responde 404
def jb_obtener(jb_id: int) -> dict:
    # Busca por id
    jb_proveedor = jb_proveedor_repository.jb_buscar_por_id(jb_id)
    # Si no existe...
    if jb_proveedor is None:
        # ...responde 404
        raise jb_no_encontrado(f"El proveedor {jb_id}")
    # Devuelve el proveedor
    return jb_proveedor


# Crea un proveedor
def jb_crear(jb_datos: dict) -> dict:
    # Todo proveedor nuevo empieza ACTIVO
    jb_datos["estado"] = "ACTIVO"
    # Lo inserta (si el NIT ya existe, la API responde 409)
    return jb_proveedor_repository.jb_insertar(jb_datos)


# Modifica un proveedor
def jb_actualizar(jb_id: int, jb_datos: dict) -> dict:
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # Guarda los cambios y devuelve el proveedor actualizado
    return jb_proveedor_repository.jb_actualizar(jb_id, jb_datos)


# Elimina un proveedor
def jb_eliminar(jb_id: int) -> dict:
    """RN04: un proveedor con compras registradas no se borra, se marca INACTIVO."""
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # Si tiene alguna compra...
    if jb_compra_repository.jb_existe({"id_proveedor": jb_id}):
        # ...se marca INACTIVO
        jb_proveedor_repository.jb_actualizar(jb_id, {"estado": "INACTIVO"})
        # Responde borrado lógico
        return jb_borrado_logico(f"El proveedor {jb_id}")
    # Si no tiene compras, se borra de verdad
    jb_proveedor_repository.jb_eliminar(jb_id)
    # Responde borrado físico
    return jb_borrado_fisico(f"El proveedor {jb_id}")


# Historial de compras de un proveedor
def jb_compras(jb_id: int) -> list[dict]:
    # Comprueba que el proveedor exista (404 si no)
    jb_obtener(jb_id)
    # Devuelve sus compras
    return jb_compra_repository.jb_por_proveedor(jb_id)
