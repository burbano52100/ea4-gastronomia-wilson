"""Reglas de negocio de insumos (RF07)."""
# timedelta: para sumar días a una fecha
from datetime import timedelta

# Funciones de fecha: hora actual, fin del día e inicio del día
from app.core.jb_utilidades import jb_ahora, jb_fin_del_dia, jb_inicio_del_dia
# Acceso a compras (para saber si el insumo se ha comprado)
from app.repositories.jb_compra_repository import jb_compra_repository
# Acceso a insumos
from app.repositories.jb_insumo_repository import jb_insumo_repository
# Acceso a recetas (para saber si el insumo se usa en alguna)
from app.repositories.jb_receta_repository import jb_receta_repository
# Respuestas y errores comunes
from app.services.jb_comun import jb_borrado_fisico, jb_borrado_logico, jb_no_encontrado


# Ajusta los datos antes de guardarlos
def jb_preparar(jb_datos: dict) -> dict:
    # MongoDB no guarda fechas sin hora: el vencimiento se guarda a las 00:00 de ese día.
    if jb_datos.get("fecha_vencimiento") is not None:
        # Convierte la fecha en fecha con hora 00:00:00
        jb_datos["fecha_vencimiento"] = jb_inicio_del_dia(jb_datos["fecha_vencimiento"])
    # Devuelve los datos listos
    return jb_datos


# Lista todos los insumos
def jb_listar() -> list[dict]:
    # Pide la lista al repositorio
    return jb_insumo_repository.jb_listar()


# Busca un insumo o responde 404
def jb_obtener(jb_id: int) -> dict:
    # Busca por id
    jb_insumo = jb_insumo_repository.jb_buscar_por_id(jb_id)
    # Si no existe...
    if jb_insumo is None:
        # ...responde 404
        raise jb_no_encontrado(f"El insumo {jb_id}")
    # Devuelve el insumo
    return jb_insumo


# Crea un insumo
def jb_crear(jb_datos: dict) -> dict:
    # Todo insumo nuevo empieza ACTIVO
    jb_datos["estado"] = "ACTIVO"
    # Ajusta la fecha y lo inserta
    return jb_insumo_repository.jb_insertar(jb_preparar(jb_datos))


# Modifica un insumo
def jb_actualizar(jb_id: int, jb_datos: dict) -> dict:
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # Ajusta la fecha, guarda los cambios y devuelve el insumo actualizado
    return jb_insumo_repository.jb_actualizar(jb_id, jb_preparar(jb_datos))


# Elimina un insumo
def jb_eliminar(jb_id: int) -> dict:
    """RN04: un insumo usado en recetas o compras no se borra, se marca INACTIVO."""
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # Tiene movimientos si aparece en alguna receta o en el detalle de alguna compra
    jb_tiene_movimientos = jb_receta_repository.jb_existe({"id_insumo": jb_id}) or jb_compra_repository.jb_existe(
        # Busca el insumo dentro de la lista "detalle" de las compras
        {"detalle.id_insumo": jb_id}
    )
    # Si tiene movimientos...
    if jb_tiene_movimientos:
        # ...se marca INACTIVO
        jb_insumo_repository.jb_actualizar(jb_id, {"estado": "INACTIVO"})
        # Responde borrado lógico
        return jb_borrado_logico(f"El insumo {jb_id}")
    # Si no tiene movimientos, se borra de verdad
    jb_insumo_repository.jb_eliminar(jb_id)
    # Responde borrado físico
    return jb_borrado_fisico(f"El insumo {jb_id}")


# Insumos con stock bajo
def jb_stock_bajo() -> list[dict]:
    # Pide la consulta al repositorio
    return jb_insumo_repository.jb_stock_bajo()


# Insumos que vencen en los próximos días
def jb_por_vencer(jb_dias: int) -> list[dict]:
    # Fecha de hoy en Colombia
    jb_hoy = jb_ahora().date()
    # Busca entre el inicio de hoy y el final del día hoy + N días
    return jb_insumo_repository.jb_por_vencer(
        # Desde hoy a las 00:00:00 hasta (hoy + días) a las 23:59:59
        jb_inicio_del_dia(jb_hoy), jb_fin_del_dia(jb_hoy + timedelta(days=jb_dias))
    )
