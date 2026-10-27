"""Reglas de negocio de usuarios (RF02) y RN06 (contraseñas cifradas)."""
# Session: sesión de trabajo con MySQL
from sqlalchemy.orm import Session

# Cifrado de contraseñas con bcrypt
from app.core.jb_security import jb_cifrar_password
# Modelo de la tabla usuarios
from app.models.jb_modelos import JbUsuario
# Consultas a la tabla usuarios
from app.repositories import jb_usuario_repository as jb_repositorio
# Errores y respuestas comunes
from app.services.jb_comun import jb_borrado_fisico, jb_borrado_logico, jb_conflicto, jb_no_encontrado


# Lista todos los usuarios
def jb_listar(jb_sesion: Session) -> list[JbUsuario]:
    # Pide la lista al repositorio
    return jb_repositorio.jb_listar(jb_sesion)


# Busca un usuario o responde 404
def jb_obtener(jb_sesion: Session, jb_id: int) -> JbUsuario:
    # Busca por id
    jb_usuario = jb_repositorio.jb_buscar(jb_sesion, jb_id)
    # Si no existe...
    if jb_usuario is None:
        # ...responde 404
        raise jb_no_encontrado(f"El usuario {jb_id}")
    # Devuelve el usuario
    return jb_usuario


# Comprueba que quede al menos otro ADMIN activo
def jb_validar_otro_admin(jb_sesion: Session, jb_usuario: JbUsuario) -> None:
    """Sin ningún ADMIN activo nadie podría administrar el sistema: se impide."""
    # Solo importa si el usuario es hoy un ADMIN activo
    if jb_usuario.rol == "ADMIN" and jb_usuario.estado == "ACTIVO":
        # Si no hay ningún otro ADMIN activo...
        if jb_repositorio.jb_contar_otros_admins_activos(jb_sesion, jb_usuario.id_usuario) == 0:
            # ...responde 409
            raise jb_conflicto("Debe quedar al menos un usuario ADMIN activo")


# Crea un usuario (POST /usuarios y POST /auth/registro)
def jb_crear(jb_sesion: Session, jb_datos: dict) -> JbUsuario:
    # Arma el objeto con los datos recibidos
    jb_usuario = JbUsuario(
        # Documento
        identificacion=jb_datos["identificacion"],
        # Nombres
        nombres=jb_datos["nombres"],
        # Apellidos
        apellidos=jb_datos["apellidos"],
        # Correo (ya viene en minúsculas desde el esquema)
        correo=jb_datos["correo"],
        # RN06: se guarda el hash bcrypt, nunca el texto plano
        password=jb_cifrar_password(jb_datos["password"]),
        # Rol
        rol=jb_datos["rol"],
        # Todo usuario nuevo empieza ACTIVO
        estado="ACTIVO",
    )
    # Inserta; si el correo o el documento ya existen, MySQL responde 1062 y la API responde 409
    jb_repositorio.jb_guardar(jb_sesion, jb_usuario)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve el usuario creado
    return jb_usuario


# Modifica un usuario
def jb_actualizar(jb_sesion: Session, jb_id: int, jb_datos: dict) -> JbUsuario:
    # Busca el usuario y lo bloquea mientras se modifica
    jb_usuario = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_usuario is None:
        # ...responde 404
        raise jb_no_encontrado(f"El usuario {jb_id}")
    # Si deja de ser ADMIN o deja de estar ACTIVO, debe quedar otro ADMIN activo
    if jb_datos["rol"] != "ADMIN" or jb_datos["estado"] != "ACTIVO":
        # Revisa la regla
        jb_validar_otro_admin(jb_sesion, jb_usuario)
    # Recorre los campos que se pueden cambiar directamente
    for jb_campo in ("identificacion", "nombres", "apellidos", "correo", "rol", "estado"):
        # Copia el valor nuevo al objeto
        setattr(jb_usuario, jb_campo, jb_datos[jb_campo])
    # Si se envió una contraseña nueva...
    if jb_datos.get("password"):
        # ...se cifra y se guarda (RN06)
        jb_usuario.password = jb_cifrar_password(jb_datos["password"])
    # Envía el cambio (aquí salta el 409 si el correo o el documento ya los usa otro usuario)
    jb_repositorio.jb_guardar(jb_sesion, jb_usuario)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve el usuario modificado
    return jb_usuario


# Elimina un usuario o lo deja INACTIVO
def jb_eliminar(jb_sesion: Session, jb_id: int, jb_id_actual: int) -> dict:
    """Si el usuario ya registró pedidos o compras queda INACTIVO; si no, se borra."""
    # Nadie puede eliminarse a sí mismo
    if jb_id == jb_id_actual:
        # Responde 409
        raise jb_conflicto("No puede eliminar su propio usuario")
    # Busca el usuario y lo bloquea
    jb_usuario = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_usuario is None:
        # ...responde 404
        raise jb_no_encontrado(f"El usuario {jb_id}")
    # Debe quedar al menos otro ADMIN activo
    jb_validar_otro_admin(jb_sesion, jb_usuario)
    # Si tiene movimientos...
    if jb_repositorio.jb_tiene_movimientos(jb_sesion, jb_id):
        # ...borrado lógico: queda INACTIVO y ya no puede iniciar sesión
        jb_usuario.estado = "INACTIVO"
        # Confirma
        jb_sesion.commit()
        # Responde borrado lógico
        return jb_borrado_logico(f"El usuario {jb_id}")
    # Sin movimientos: se borra
    jb_repositorio.jb_borrar(jb_sesion, jb_usuario)
    # Confirma
    jb_sesion.commit()
    # Responde borrado físico
    return jb_borrado_fisico(f"El usuario {jb_id}")
