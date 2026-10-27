"""Reglas de negocio de recetas o fichas técnicas (RF05)."""
# Session: sesión de trabajo con MySQL
from sqlalchemy.orm import Session

# Modelos de las tablas
from app.models.jb_modelos import JbInsumo, JbProducto, JbReceta
# Consultas a insumos y productos
from app.repositories import jb_insumo_repository, jb_producto_repository
# Consultas a recetas
from app.repositories import jb_receta_repository as jb_repositorio
# Errores comunes
from app.services.jb_comun import jb_dato_invalido, jb_no_encontrado


# Lista todas las líneas de receta
def jb_listar(jb_sesion: Session) -> list[JbReceta]:
    # Pide la lista al repositorio
    return jb_repositorio.jb_listar(jb_sesion)


# Busca una línea de receta o responde 404
def jb_obtener(jb_sesion: Session, jb_id: int) -> JbReceta:
    # Busca por id
    jb_receta = jb_repositorio.jb_buscar(jb_sesion, jb_id)
    # Si no existe...
    if jb_receta is None:
        # ...responde 404
        raise jb_no_encontrado(f"La línea de receta {jb_id}")
    # Devuelve la línea
    return jb_receta


# Comprueba que el producto exista
def jb_validar_producto(jb_sesion: Session, jb_id_producto: int) -> JbProducto:
    # Busca el producto
    jb_producto = jb_producto_repository.jb_buscar(jb_sesion, jb_id_producto)
    # Si no existe...
    if jb_producto is None:
        # ...responde 400 (equivale a fallar la llave foránea)
        raise jb_dato_invalido(f"El producto {jb_id_producto} no existe")
    # Devuelve el producto
    return jb_producto


# Comprueba que el insumo exista y esté ACTIVO
def jb_validar_insumo(jb_sesion: Session, jb_id_insumo: int) -> JbInsumo:
    # Busca el insumo
    jb_insumo = jb_insumo_repository.jb_buscar(jb_sesion, jb_id_insumo)
    # Si no existe...
    if jb_insumo is None:
        # ...responde 400
        raise jb_dato_invalido(f"El insumo {jb_id_insumo} no existe")
    # Si está INACTIVO...
    if jb_insumo.estado != "ACTIVO":
        # ...responde 400
        raise jb_dato_invalido(f"El insumo '{jb_insumo.nombre}' está INACTIVO: no se puede usar en recetas")
    # Devuelve el insumo
    return jb_insumo


# Crea una línea de receta
def jb_crear(jb_sesion: Session, jb_datos: dict) -> JbReceta:
    # Arma el objeto con el producto, el insumo y la cantidad (400 si alguno no sirve)
    jb_receta = JbReceta(
        # Producto (debe existir)
        producto=jb_validar_producto(jb_sesion, jb_datos["id_producto"]),
        # Insumo (debe existir y estar ACTIVO)
        insumo=jb_validar_insumo(jb_sesion, jb_datos["id_insumo"]),
        # Cantidad por unidad de producto
        cantidad=jb_datos["cantidad"],
    )
    # Inserta; si el insumo ya está en la receta de ese producto la API responde 409
    jb_repositorio.jb_guardar(jb_sesion, jb_receta)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve la línea creada
    return jb_receta


# Modifica una línea de receta
def jb_actualizar(jb_sesion: Session, jb_id: int, jb_datos: dict) -> JbReceta:
    # Busca la línea y la bloquea mientras se modifica
    jb_receta = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_receta is None:
        # ...responde 404
        raise jb_no_encontrado(f"La línea de receta {jb_id}")
    # Si cambia el producto, el nuevo debe existir
    if jb_datos["id_producto"] != jb_receta.id_producto:
        # Asigna el nuevo producto
        jb_receta.producto = jb_validar_producto(jb_sesion, jb_datos["id_producto"])
    # Si cambia el insumo, el nuevo debe existir y estar ACTIVO
    if jb_datos["id_insumo"] != jb_receta.id_insumo:
        # Asigna el nuevo insumo
        jb_receta.insumo = jb_validar_insumo(jb_sesion, jb_datos["id_insumo"])
    # Cambia la cantidad
    jb_receta.cantidad = jb_datos["cantidad"]
    # Envía el cambio (409 si la pareja producto-insumo ya existe en otra línea)
    jb_repositorio.jb_guardar(jb_sesion, jb_receta)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve la línea modificada
    return jb_receta


# Elimina una línea de receta
def jb_eliminar(jb_sesion: Session, jb_id: int) -> dict:
    """La receta es configuración, no un movimiento: se borra directamente."""
    # Busca la línea y la bloquea
    jb_receta = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_receta is None:
        # ...responde 404
        raise jb_no_encontrado(f"La línea de receta {jb_id}")
    # La borra
    jb_repositorio.jb_borrar(jb_sesion, jb_receta)
    # Confirma
    jb_sesion.commit()
    # Responde borrado físico
    return {"mensaje": f"La línea de receta {jb_id} se eliminó", "tipo_borrado": "FISICO"}
