"""Consultas a la tabla usuarios."""
# func: funciones de SQL como COUNT; select: arma un SELECT
from sqlalchemy import func, select
# Session: sesión de trabajo con la base de datos
from sqlalchemy.orm import Session

# Modelos de las tablas que se consultan
from app.models.jb_modelos import JbCompra, JbPedido, JbUsuario
# Funciones comunes de los repositorios
from app.repositories import jb_base_repository as jb_base


# Lista todos los usuarios ordenados por id
def jb_listar(jb_sesion: Session) -> list[JbUsuario]:
    # Usa la función común
    return jb_base.jb_listar(jb_sesion, JbUsuario, JbUsuario.id_usuario)


# Busca un usuario por id
def jb_buscar(jb_sesion: Session, jb_id: int) -> JbUsuario | None:
    # Usa la función común
    return jb_base.jb_buscar(jb_sesion, JbUsuario, jb_id)


# Busca un usuario por id y lo bloquea para modificarlo
def jb_buscar_para_actualizar(jb_sesion: Session, jb_id: int) -> JbUsuario | None:
    # Usa la función común (SELECT ... FOR UPDATE)
    return jb_base.jb_buscar_para_actualizar(jb_sesion, JbUsuario, jb_id)


# Busca un usuario por su correo (para el login)
def jb_buscar_por_correo(jb_sesion: Session, jb_correo: str) -> JbUsuario | None:
    # SELECT * FROM usuarios WHERE correo = :correo
    return jb_sesion.scalar(select(JbUsuario).where(JbUsuario.correo == jb_correo))


# Cuenta los administradores activos sin contar uno (el que se va a cambiar o eliminar)
def jb_contar_otros_admins_activos(jb_sesion: Session, jb_id_excluido: int) -> int:
    # SELECT COUNT(*) FROM usuarios WHERE rol = 'ADMIN' AND estado = 'ACTIVO' AND id_usuario <> :id
    return jb_sesion.scalar(
        # COUNT(*) sobre la tabla usuarios
        select(func.count()).select_from(JbUsuario).where(
            # Solo administradores
            JbUsuario.rol == "ADMIN",
            # Solo activos
            JbUsuario.estado == "ACTIVO",
            # Sin contar el usuario indicado
            JbUsuario.id_usuario != jb_id_excluido,
        )
    )


# Revisa si el usuario ya registró pedidos o compras
def jb_tiene_movimientos(jb_sesion: Session, jb_id: int) -> bool:
    # Hay movimientos si existe un pedido o una compra registrados por este usuario
    return jb_base.jb_existe(jb_sesion, JbPedido.id_usuario == jb_id) or jb_base.jb_existe(
        # Segunda condición: compras del usuario
        jb_sesion, JbCompra.id_usuario == jb_id
    )


# Guarda un usuario nuevo o modificado
def jb_guardar(jb_sesion: Session, jb_usuario: JbUsuario) -> JbUsuario:
    # Usa la función común
    return jb_base.jb_guardar(jb_sesion, jb_usuario)


# Borra un usuario
def jb_borrar(jb_sesion: Session, jb_usuario: JbUsuario) -> None:
    # Usa la función común
    jb_base.jb_borrar(jb_sesion, jb_usuario)

