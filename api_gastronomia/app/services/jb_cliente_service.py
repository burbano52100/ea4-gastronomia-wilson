"""Reglas de negocio de clientes (RF09)."""
# Acceso a clientes
from app.repositories.jb_cliente_repository import jb_cliente_repository
# Acceso a pedidos (para el historial y para saber si el cliente tiene movimientos)
from app.repositories.jb_pedido_repository import jb_pedido_repository
# Respuestas y errores comunes
from app.services.jb_comun import jb_borrado_fisico, jb_borrado_logico, jb_no_encontrado


# Lista todos los clientes
def jb_listar() -> list[dict]:
    # Pide la lista al repositorio
    return jb_cliente_repository.jb_listar()


# Busca un cliente o responde 404
def jb_obtener(jb_id: int) -> dict:
    # Busca por id
    jb_cliente = jb_cliente_repository.jb_buscar_por_id(jb_id)
    # Si no existe...
    if jb_cliente is None:
        # ...responde 404
        raise jb_no_encontrado(f"El cliente {jb_id}")
    # Devuelve el cliente
    return jb_cliente


# Crea un cliente
def jb_crear(jb_datos: dict) -> dict:
    # Todo cliente nuevo empieza ACTIVO
    jb_datos["estado"] = "ACTIVO"
    # Lo inserta (si la identificación ya existe, la API responde 409)
    return jb_cliente_repository.jb_insertar(jb_datos)


# Modifica un cliente
def jb_actualizar(jb_id: int, jb_datos: dict) -> dict:
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # Guarda los cambios y devuelve el cliente actualizado
    return jb_cliente_repository.jb_actualizar(jb_id, jb_datos)


# Elimina un cliente
def jb_eliminar(jb_id: int) -> dict:
    """RN04: un cliente con pedidos no se borra, se marca INACTIVO."""
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # Si tiene algún pedido...
    if jb_pedido_repository.jb_existe({"id_cliente": jb_id}):
        # ...se marca INACTIVO
        jb_cliente_repository.jb_actualizar(jb_id, {"estado": "INACTIVO"})
        # Responde borrado lógico
        return jb_borrado_logico(f"El cliente {jb_id}")
    # Si no tiene pedidos, se borra de verdad
    jb_cliente_repository.jb_eliminar(jb_id)
    # Responde borrado físico
    return jb_borrado_fisico(f"El cliente {jb_id}")


# Historial de pedidos de un cliente
def jb_pedidos(jb_id: int) -> list[dict]:
    # Comprueba que el cliente exista (404 si no)
    jb_obtener(jb_id)
    # Devuelve sus pedidos
    return jb_pedido_repository.jb_por_cliente(jb_id)
