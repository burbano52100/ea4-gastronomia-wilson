"""Funciones de acceso a MySQL que comparten todos los repositorios."""
# exists: arma un EXISTS (...); select: arma un SELECT
from sqlalchemy import exists, select
# Session: sesión de trabajo con la base de datos
from sqlalchemy.orm import Session


# Trae todos los registros de una tabla
def jb_listar(jb_sesion: Session, jb_modelo, jb_orden) -> list:
    """SELECT * FROM tabla ORDER BY jb_orden."""
    # scalars devuelve objetos del modelo; list los junta en una lista
    return list(jb_sesion.scalars(select(jb_modelo).order_by(jb_orden)))


# Busca un registro por su llave primaria
def jb_buscar(jb_sesion: Session, jb_modelo, jb_id: int):
    """SELECT * FROM tabla WHERE id = jb_id. Devuelve None si no existe."""
    # get busca por llave primaria
    return jb_sesion.get(jb_modelo, jb_id)


# Busca un registro y lo bloquea hasta terminar la transacción
def jb_buscar_para_actualizar(jb_sesion: Session, jb_modelo, jb_id: int):
    """SELECT ... FOR UPDATE: mientras esta petición no termine, otra no puede modificar el mismo registro.
    Evita, por ejemplo, que dos usuarios entreguen el mismo pedido al mismo tiempo."""
    # with_for_update agrega FOR UPDATE; populate_existing trae los datos frescos de la base
    return jb_sesion.get(jb_modelo, jb_id, with_for_update=True, populate_existing=True)


# Pregunta si existe al menos un registro que cumpla una condición
def jb_existe(jb_sesion: Session, jb_condicion) -> bool:
    """SELECT EXISTS (SELECT * FROM tabla WHERE condición). Se usa para saber si hay movimientos (RN04)."""
    # scalar devuelve el único valor del resultado: True o False
    return bool(jb_sesion.scalar(select(exists().where(jb_condicion))))


# Agrega o actualiza un registro
def jb_guardar(jb_sesion: Session, jb_objeto):
    """INSERT o UPDATE. flush envía la instrucción a MySQL (sin confirmar todavía) para obtener el id."""
    # Agrega el objeto a la sesión
    jb_sesion.add(jb_objeto)
    # Envía el cambio a MySQL; aquí salta el error si un dato único se repite
    jb_sesion.flush()
    # Devuelve el objeto, ya con su id
    return jb_objeto


# Borra un registro
def jb_borrar(jb_sesion: Session, jb_objeto) -> None:
    """DELETE FROM tabla WHERE id = ... (sin confirmar todavía)."""
    # Marca el objeto para borrarlo
    jb_sesion.delete(jb_objeto)
    # Envía el DELETE a MySQL
    jb_sesion.flush()
