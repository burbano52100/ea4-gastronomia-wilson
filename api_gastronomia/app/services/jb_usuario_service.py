"""Reglas de negocio de usuarios (RF02, RN06)."""
# Función que cifra contraseñas con bcrypt
from app.core.jb_security import jb_cifrar_password
# Acceso a compras (para saber si el usuario registró compras)
from app.repositories.jb_compra_repository import jb_compra_repository
# Acceso a pedidos (para saber si el usuario registró pedidos)
from app.repositories.jb_pedido_repository import jb_pedido_repository
# Acceso a usuarios
from app.repositories.jb_usuario_repository import jb_usuario_repository
# Respuestas y errores comunes
from app.services.jb_comun import jb_borrado_fisico, jb_borrado_logico, jb_dato_invalido, jb_no_encontrado


# Lista todos los usuarios (sin contraseña)
def jb_listar() -> list[dict]:
    # Pide la lista al repositorio
    return jb_usuario_repository.jb_listar()


# Busca un usuario o responde 404
def jb_obtener(jb_id: int) -> dict:
    # Busca por id
    jb_usuario = jb_usuario_repository.jb_buscar_por_id(jb_id)
    # Si no existe...
    if jb_usuario is None:
        # ...responde 404
        raise jb_no_encontrado(f"El usuario {jb_id}")
    # Devuelve el usuario
    return jb_usuario


# Crea un usuario
def jb_crear(jb_datos: dict) -> dict:
    # RN06: cambia la contraseña escrita por su hash bcrypt
    jb_datos["password"] = jb_cifrar_password(jb_datos["password"])
    # Todo usuario nuevo empieza ACTIVO
    jb_datos["estado"] = "ACTIVO"
    # Lo inserta (si el correo o la identificación ya existen, la API responde 409)
    return jb_usuario_repository.jb_insertar(jb_datos)


# Modifica un usuario
def jb_actualizar(jb_id: int, jb_datos: dict) -> dict:
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # Si se envió una contraseña nueva...
    if jb_datos.get("password"):
        # ...se cifra antes de guardarla
        jb_datos["password"] = jb_cifrar_password(jb_datos["password"])
    # Si no se envió...
    else:
        # ...se quita del diccionario para no borrar la que ya tiene
        jb_datos.pop("password", None)
    # Guarda los cambios y devuelve el usuario actualizado
    return jb_usuario_repository.jb_actualizar(jb_id, jb_datos)


# Elimina un usuario
def jb_eliminar(jb_id: int, jb_id_usuario_sesion: int) -> dict:
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # Nadie puede eliminarse a sí mismo
    if jb_id == jb_id_usuario_sesion:
        # Responde 400
        raise jb_dato_invalido("No puede eliminar el usuario con el que inició sesión")
    # Tiene movimientos si registró algún pedido o alguna compra
    jb_tiene_movimientos = jb_pedido_repository.jb_existe({"id_usuario": jb_id}) or jb_compra_repository.jb_existe(
        # Busca compras registradas por este usuario
        {"id_usuario": jb_id}
    )
    # Si tiene movimientos...
    if jb_tiene_movimientos:
        # ...se marca INACTIVO
        jb_usuario_repository.jb_actualizar(jb_id, {"estado": "INACTIVO"})
        # Responde borrado lógico
        return jb_borrado_logico(f"El usuario {jb_id}")
    # Si no tiene movimientos, se borra de verdad
    jb_usuario_repository.jb_eliminar(jb_id)
    # Responde borrado físico
    return jb_borrado_fisico(f"El usuario {jb_id}")
