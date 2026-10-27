"""Reglas de negocio de productos (RF04), su receta (RF05) y su costo de producción (RF06)."""
# Decimal: números exactos para dinero
from decimal import Decimal

# Session: sesión de trabajo con MySQL
from sqlalchemy.orm import Session

# Redondeo de dinero a 2 decimales
from app.core.jb_utilidades import jb_dinero
# Modelos de las tablas
from app.models.jb_modelos import JbCategoria, JbProducto
# Consultas a categorías y recetas
from app.repositories import jb_categoria_repository, jb_receta_repository
# Consultas a productos, con el nombre corto jb_repositorio
from app.repositories import jb_producto_repository as jb_repositorio
# Errores y respuestas comunes
from app.services.jb_comun import jb_borrado_fisico, jb_borrado_logico, jb_dato_invalido, jb_no_encontrado


# Lista todos los productos
def jb_listar(jb_sesion: Session) -> list[JbProducto]:
    # Pide la lista al repositorio
    return jb_repositorio.jb_listar(jb_sesion)


# Busca un producto o responde 404
def jb_obtener(jb_sesion: Session, jb_id: int) -> JbProducto:
    # Busca por id
    jb_producto = jb_repositorio.jb_buscar(jb_sesion, jb_id)
    # Si no existe...
    if jb_producto is None:
        # ...responde 404
        raise jb_no_encontrado(f"El producto {jb_id}")
    # Devuelve el producto
    return jb_producto


# Comprueba que la categoría exista y esté ACTIVA
def jb_validar_categoria(jb_sesion: Session, jb_id_categoria: int) -> JbCategoria:
    # Busca la categoría
    jb_categoria = jb_categoria_repository.jb_buscar(jb_sesion, jb_id_categoria)
    # Si no existe...
    if jb_categoria is None:
        # ...responde 400 (equivale a fallar la llave foránea)
        raise jb_dato_invalido(f"La categoría {jb_id_categoria} no existe")
    # Si está INACTIVA...
    if jb_categoria.estado != "ACTIVO":
        # ...responde 400
        raise jb_dato_invalido(f"La categoría '{jb_categoria.nombre}' está INACTIVA: no se le pueden asignar productos")
    # Devuelve la categoría
    return jb_categoria


# Productos de una categoría (GET /productos/categoria/{id})
def jb_por_categoria(jb_sesion: Session, jb_id_categoria: int) -> list[JbProducto]:
    # Si la categoría no existe...
    if jb_categoria_repository.jb_buscar(jb_sesion, jb_id_categoria) is None:
        # ...responde 404
        raise jb_no_encontrado(f"La categoría {jb_id_categoria}")
    # Pide los productos al repositorio
    return jb_repositorio.jb_por_categoria(jb_sesion, jb_id_categoria)


# Crea un producto
def jb_crear(jb_sesion: Session, jb_datos: dict) -> JbProducto:
    # Comprueba la categoría (400 si no existe o está INACTIVA)
    jb_categoria = jb_validar_categoria(jb_sesion, jb_datos["id_categoria"])
    # Arma el objeto con los datos recibidos; todo producto nuevo empieza DISPONIBLE
    jb_producto = JbProducto(**jb_datos, estado="DISPONIBLE", categoria=jb_categoria)
    # Inserta; si el código ya existe la API responde 409
    jb_repositorio.jb_guardar(jb_sesion, jb_producto)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve el producto creado
    return jb_producto


# Modifica un producto
def jb_actualizar(jb_sesion: Session, jb_id: int, jb_datos: dict) -> JbProducto:
    # Busca el producto y lo bloquea mientras se modifica
    jb_producto = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_producto is None:
        # ...responde 404
        raise jb_no_encontrado(f"El producto {jb_id}")
    # Si cambia de categoría, la nueva debe existir y estar ACTIVA
    if jb_datos["id_categoria"] != jb_producto.id_categoria:
        # Asigna la nueva categoría (SQLAlchemy actualiza id_categoria al guardar)
        jb_producto.categoria = jb_validar_categoria(jb_sesion, jb_datos["id_categoria"])
    # Recorre los demás campos
    for jb_campo in ("codigo", "nombre", "descripcion", "precio_venta", "unidad_venta", "estado"):
        # Copia el valor nuevo al objeto
        setattr(jb_producto, jb_campo, jb_datos[jb_campo])
    # Envía el cambio (409 si el código ya lo usa otro producto)
    jb_repositorio.jb_guardar(jb_sesion, jb_producto)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve el producto modificado
    return jb_producto


# Elimina un producto o lo deja INACTIVO (RN04)
def jb_eliminar(jb_sesion: Session, jb_id: int) -> dict:
    """RN04: si el producto aparece en pedidos o tiene receta pasa a INACTIVO; si no, se borra."""
    # Busca el producto y lo bloquea
    jb_producto = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_producto is None:
        # ...responde 404
        raise jb_no_encontrado(f"El producto {jb_id}")
    # Si tiene movimientos...
    if jb_repositorio.jb_tiene_movimientos(jb_sesion, jb_id):
        # ...borrado lógico
        jb_producto.estado = "INACTIVO"
        # Confirma
        jb_sesion.commit()
        # Responde borrado lógico
        return jb_borrado_logico(f"El producto {jb_id}")
    # Sin movimientos: se borra
    jb_repositorio.jb_borrar(jb_sesion, jb_producto)
    # Confirma
    jb_sesion.commit()
    # Responde borrado físico
    return jb_borrado_fisico(f"El producto {jb_id}")


# Arma las líneas de la receta de un producto, cada una con su costo
def jb_lineas_receta(jb_sesion: Session, jb_id_producto: int) -> list[dict]:
    # Aquí se juntan las líneas
    jb_lineas = []
    # Recorre cada línea de la receta del producto
    for jb_receta in jb_receta_repository.jb_por_producto(jb_sesion, jb_id_producto):
        # Insumo de la línea
        jb_insumo = jb_receta.insumo
        # Agrega la línea con la forma de JbLineaReceta
        jb_lineas.append({
            # Id de la línea
            "id_receta": jb_receta.id_receta,
            # Id del insumo
            "id_insumo": jb_insumo.id_insumo,
            # Nombre del insumo
            "insumo": jb_insumo.nombre,
            # Unidad de medida
            "unidad_medida": jb_insumo.unidad_medida,
            # Cantidad por unidad de producto
            "cantidad": jb_receta.cantidad,
            # Costo actual del insumo
            "costo_unitario": jb_insumo.costo_unitario,
            # cantidad x costo_unitario, redondeado a 2 decimales
            "costo_linea": jb_dinero(jb_receta.cantidad * jb_insumo.costo_unitario),
        })
    # Devuelve las líneas
    return jb_lineas


# Receta de un producto (GET /productos/{id}/receta)
def jb_receta(jb_sesion: Session, jb_id: int) -> dict:
    # Busca el producto (404 si no existe)
    jb_producto = jb_obtener(jb_sesion, jb_id)
    # Devuelve la forma de JbRecetaDeProducto (lista vacía si no tiene receta)
    return {"id_producto": jb_id, "producto": jb_producto.nombre, "insumos": jb_lineas_receta(jb_sesion, jb_id)}


# Costo de producción y margen (GET /productos/{id}/costo)
def jb_costo(jb_sesion: Session, jb_id: int) -> dict:
    """RF06: costo = suma de (cantidad x costo_unitario) de la receta. Margen = precio de venta - costo."""
    # Busca el producto (404 si no existe)
    jb_producto = jb_obtener(jb_sesion, jb_id)
    # Líneas de la receta con su costo
    jb_lineas = jb_lineas_receta(jb_sesion, jb_id)
    # Sin receta no hay costo que calcular
    if not jb_lineas:
        # Responde 404
        raise jb_no_encontrado(f"La receta del producto {jb_id}")
    # Suma el costo de todas las líneas
    jb_costo_total = jb_dinero(sum((jb_linea["costo_linea"] for jb_linea in jb_lineas), Decimal("0")))
    # Margen en dinero
    jb_margen = jb_dinero(jb_producto.precio_venta - jb_costo_total)
    # Devuelve la forma de JbCostoProducto
    return {
        # Id del producto
        "id_producto": jb_id,
        # Nombre del producto
        "producto": jb_producto.nombre,
        # Precio de venta
        "precio_venta": jb_producto.precio_venta,
        # Costo de producción
        "costo_produccion": jb_costo_total,
        # Margen en dinero
        "margen": jb_margen,
        # Margen en porcentaje sobre el precio de venta
        "margen_porcentaje": jb_dinero(jb_margen / jb_producto.precio_venta * 100),
        # Detalle de la receta
        "detalle": jb_lineas,
    }
