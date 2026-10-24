"""Reglas de negocio de productos (RF04), su receta (RF05) y su costo de producción (RF06)."""
# Decimal: números exactos para dinero
from decimal import Decimal

# Redondeo de dinero a 2 decimales
from app.core.jb_utilidades import jb_dinero
# Acceso a categorías
from app.repositories.jb_categoria_repository import jb_categoria_repository
# Acceso a insumos
from app.repositories.jb_insumo_repository import jb_insumo_repository
# Acceso a pedidos (para saber si un producto ya se vendió)
from app.repositories.jb_pedido_repository import jb_pedido_repository
# Acceso a productos
from app.repositories.jb_producto_repository import jb_producto_repository
# Acceso a recetas
from app.repositories.jb_receta_repository import jb_receta_repository
# Respuestas y errores comunes
from app.services.jb_comun import jb_borrado_fisico, jb_borrado_logico, jb_dato_invalido, jb_no_encontrado


# Lista todos los productos
def jb_listar() -> list[dict]:
    # Pide la lista al repositorio
    return jb_producto_repository.jb_listar()


# Busca un producto o responde 404
def jb_obtener(jb_id: int) -> dict:
    # Busca por id
    jb_producto = jb_producto_repository.jb_buscar_por_id(jb_id)
    # Si no existe...
    if jb_producto is None:
        # ...responde 404
        raise jb_no_encontrado(f"El producto {jb_id}")
    # Devuelve el producto
    return jb_producto


# Comprueba que la categoría exista y esté ACTIVA
def jb_validar_categoria(jb_id_categoria: int) -> None:
    # Busca la categoría
    jb_categoria = jb_categoria_repository.jb_buscar_por_id(jb_id_categoria)
    # Si no existe...
    if jb_categoria is None:
        # ...responde 400 (equivale a fallar una llave foránea)
        raise jb_dato_invalido(f"La categoría {jb_id_categoria} no existe")
    # Si está INACTIVA...
    if jb_categoria["estado"] != "ACTIVO":
        # ...responde 400
        raise jb_dato_invalido(f"La categoría '{jb_categoria['nombre']}' está INACTIVA")


# Crea un producto
def jb_crear(jb_datos: dict) -> dict:
    # Comprueba la categoría
    jb_validar_categoria(jb_datos["id_categoria"])
    # Todo producto nuevo empieza DISPONIBLE
    jb_datos["estado"] = "DISPONIBLE"
    # Lo inserta (si el código ya existe, la API responde 409)
    return jb_producto_repository.jb_insertar(jb_datos)


# Modifica un producto
def jb_actualizar(jb_id: int, jb_datos: dict) -> dict:
    # Busca el producto actual (404 si no existe)
    jb_producto = jb_obtener(jb_id)
    # Si se cambió la categoría...
    if jb_datos["id_categoria"] != jb_producto["id_categoria"]:
        # ...se comprueba la nueva
        jb_validar_categoria(jb_datos["id_categoria"])
    # Guarda los cambios y devuelve el producto actualizado
    return jb_producto_repository.jb_actualizar(jb_id, jb_datos)


# Elimina un producto
def jb_eliminar(jb_id: int) -> dict:
    """RN04: si el producto ya se vendió se marca INACTIVO; si no, se borra junto con su receta."""
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # Si aparece en el detalle de algún pedido...
    if jb_pedido_repository.jb_existe({"detalle.id_producto": jb_id}):
        # ...se marca INACTIVO
        jb_producto_repository.jb_actualizar(jb_id, {"estado": "INACTIVO"})
        # Responde borrado lógico
        return jb_borrado_logico(f"El producto {jb_id}")
    # Si nunca se vendió, primero se borra su receta
    jb_receta_repository.jb_eliminar_por_producto(jb_id)
    # Y luego el producto
    jb_producto_repository.jb_eliminar(jb_id)
    # Responde borrado físico
    return jb_borrado_fisico(f"El producto {jb_id}")


# Productos de una categoría
def jb_por_categoria(jb_id_categoria: int) -> list[dict]:
    # Si la categoría de la URL no existe...
    if jb_categoria_repository.jb_buscar_por_id(jb_id_categoria) is None:
        # ...responde 404
        raise jb_no_encontrado(f"La categoría {jb_id_categoria}")
    # Devuelve sus productos
    return jb_producto_repository.jb_por_categoria(jb_id_categoria)


# Receta de un producto con el costo de cada línea
def jb_receta(jb_id: int) -> dict:
    """RF05: insumos y cantidades de la receta, con el costo de cada línea."""
    # Busca el producto (404 si no existe)
    jb_producto = jb_obtener(jb_id)
    # Aquí se guardan las líneas de la receta
    jb_lineas = []
    # Recorre cada línea de la receta del producto
    for jb_linea in jb_receta_repository.jb_por_producto(jb_id):
        # Busca el insumo de esa línea
        jb_insumo = jb_insumo_repository.jb_buscar_por_id(jb_linea["id_insumo"])
        # Costo unitario actual del insumo; 0 si ya no existe
        jb_costo_unitario = jb_insumo["costo_unitario"] if jb_insumo else Decimal("0")
        # Agrega la línea con sus datos
        jb_lineas.append({
            # Id de la línea de receta
            "id_receta": jb_linea["id_receta"],
            # Id del insumo
            "id_insumo": jb_linea["id_insumo"],
            # Nombre del insumo
            "insumo": jb_insumo["nombre"] if jb_insumo else "(insumo eliminado)",
            # Unidad de medida
            "unidad_medida": jb_insumo["unidad_medida"] if jb_insumo else "",
            # Cantidad por unidad de producto
            "cantidad": jb_linea["cantidad"],
            # Costo unitario del insumo
            "costo_unitario": jb_costo_unitario,
            # Costo de la línea = cantidad x costo unitario
            "costo": jb_dinero(jb_linea["cantidad"] * jb_costo_unitario),
        })
    # Devuelve el producto con su lista de insumos
    return {"id_producto": jb_id, "producto": jb_producto["nombre"], "insumos": jb_lineas}


# Costo de producción y margen de un producto
def jb_costo(jb_id: int) -> dict:
    """RF06: costo de producción = suma de (cantidad x costo_unitario) y margen frente al precio de venta."""
    # Toma la receta con el costo de cada línea
    jb_detalle = jb_receta(jb_id)
    # Toma el producto para el precio de venta
    jb_producto = jb_obtener(jb_id)
    # Suma el costo de todas las líneas (empieza en 0 por si la receta está vacía)
    jb_costo_produccion = jb_dinero(sum((jb_linea["costo"] for jb_linea in jb_detalle["insumos"]), Decimal("0")))
    # Margen = precio de venta - costo de producción
    jb_margen = jb_dinero(jb_producto["precio_venta"] - jb_costo_produccion)
    # Arma la respuesta (forma de JbCostoProducto)
    return {
        # Id del producto
        "id_producto": jb_id,
        # Nombre del producto
        "producto": jb_producto["nombre"],
        # Precio de venta
        "precio_venta": jb_producto["precio_venta"],
        # Costo de producción
        "costo_produccion": jb_costo_produccion,
        # Margen en pesos
        "margen": jb_margen,
        # Margen en porcentaje = margen / precio x 100
        "margen_porcentaje": jb_dinero(jb_margen / jb_producto["precio_venta"] * 100),
    }
