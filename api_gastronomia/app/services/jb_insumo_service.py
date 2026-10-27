"""Reglas de negocio de insumos (RF07)."""
# timedelta: sumar días a una fecha
from datetime import timedelta

# Session: sesión de trabajo con MySQL
from sqlalchemy.orm import Session

# Fecha de hoy en Colombia
from app.core.jb_utilidades import jb_hoy
# Modelo de la tabla insumos
from app.models.jb_modelos import JbInsumo
# Consultas a la tabla insumos
from app.repositories import jb_insumo_repository as jb_repositorio
# Errores y respuestas comunes
from app.services.jb_comun import jb_borrado_fisico, jb_borrado_logico, jb_no_encontrado


# Lista todos los insumos
def jb_listar(jb_sesion: Session) -> list[JbInsumo]:
    # Pide la lista al repositorio
    return jb_repositorio.jb_listar(jb_sesion)


# Busca un insumo o responde 404
def jb_obtener(jb_sesion: Session, jb_id: int) -> JbInsumo:
    # Busca por id
    jb_insumo = jb_repositorio.jb_buscar(jb_sesion, jb_id)
    # Si no existe...
    if jb_insumo is None:
        # ...responde 404
        raise jb_no_encontrado(f"El insumo {jb_id}")
    # Devuelve el insumo
    return jb_insumo


# Crea un insumo
def jb_crear(jb_sesion: Session, jb_datos: dict) -> JbInsumo:
    # Arma el objeto con los datos recibidos; todo insumo nuevo empieza ACTIVO
    jb_insumo = JbInsumo(**jb_datos, estado="ACTIVO")
    # Inserta; si el nombre ya existe la API responde 409
    jb_repositorio.jb_guardar(jb_sesion, jb_insumo)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve el insumo creado
    return jb_insumo


# Modifica un insumo (sirve también para ajustar el inventario a mano)
def jb_actualizar(jb_sesion: Session, jb_id: int, jb_datos: dict) -> JbInsumo:
    # Busca el insumo y lo bloquea mientras se modifica
    jb_insumo = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_insumo is None:
        # ...responde 404
        raise jb_no_encontrado(f"El insumo {jb_id}")
    # Copia cada valor recibido al objeto
    for jb_campo, jb_valor in jb_datos.items():
        # Por ejemplo: jb_insumo.stock_actual = 8
        setattr(jb_insumo, jb_campo, jb_valor)
    # Envía el cambio (409 si el nombre ya lo usa otro insumo)
    jb_repositorio.jb_guardar(jb_sesion, jb_insumo)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve el insumo modificado
    return jb_insumo


# Elimina un insumo o lo deja INACTIVO (RN04)
def jb_eliminar(jb_sesion: Session, jb_id: int) -> dict:
    """RN04: si el insumo aparece en compras o en recetas pasa a INACTIVO; si no, se borra."""
    # Busca el insumo y lo bloquea
    jb_insumo = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_insumo is None:
        # ...responde 404
        raise jb_no_encontrado(f"El insumo {jb_id}")
    # Si tiene movimientos...
    if jb_repositorio.jb_tiene_movimientos(jb_sesion, jb_id):
        # ...borrado lógico
        jb_insumo.estado = "INACTIVO"
        # Confirma
        jb_sesion.commit()
        # Responde borrado lógico
        return jb_borrado_logico(f"El insumo {jb_id}")
    # Sin movimientos: se borra
    jb_repositorio.jb_borrar(jb_sesion, jb_insumo)
    # Confirma
    jb_sesion.commit()
    # Responde borrado físico
    return jb_borrado_fisico(f"El insumo {jb_id}")


# Insumos con stock bajo (GET /insumos/stock-bajo)
def jb_stock_bajo(jb_sesion: Session) -> list[JbInsumo]:
    # Pide la consulta al repositorio (stock_actual <= stock_minimo)
    return jb_repositorio.jb_stock_bajo(jb_sesion)


# Insumos por vencer (GET /insumos/por-vencer?dias=N)
def jb_por_vencer(jb_sesion: Session, jb_dias: int) -> list[JbInsumo]:
    """Insumos cuya fecha de vencimiento está entre hoy y hoy + N días (ambos incluidos)."""
    # Fecha de hoy en Colombia
    jb_fecha_hoy = jb_hoy()
    # Pide la consulta al repositorio con el rango de fechas
    return jb_repositorio.jb_por_vencer(jb_sesion, jb_fecha_hoy, jb_fecha_hoy + timedelta(days=jb_dias))
