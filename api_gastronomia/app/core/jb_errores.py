"""Traducción al español de los errores de FastAPI, Pydantic y MySQL."""
# HTTPStatus: tabla de Python con el nombre en inglés de cada código HTTP (404 -> "Not Found")
from http import HTTPStatus
# re: expresiones regulares, para sacar el nombre de la restricción del mensaje de MySQL
import re

# DBAPIError: error de SQLAlchemy que envuelve el error original de MySQL
from sqlalchemy.exc import DBAPIError

# Patrones (expresiones regulares) con los que los esquemas validan correos, teléfonos, documentos y NIT
from app.schemas.jb_tipos import (
    JB_PATRON_CORREO,  # patrón de los correos
    JB_PATRON_DOCUMENTO,  # patrón de los documentos de identidad
    JB_PATRON_NIT,  # patrón del NIT de los proveedores
    JB_PATRON_OBJECT_ID,  # patrón del id de MongoDB
    JB_PATRON_TELEFONO,  # patrón de los teléfonos
)

# Nombre en español de la parte de la petición donde está el error
JB_UBICACIONES = {
    "body": "cuerpo",  # el JSON que se envía en POST, PUT y PATCH
    "path": "ruta",  # un valor dentro de la URL, por ejemplo el 5 de /productos/5
    "query": "parámetro de consulta",  # lo que va después del ? en la URL, por ejemplo ?dias=7
    "header": "encabezado",  # los encabezados HTTP, por ejemplo Authorization
    "cookie": "cookie",  # las cookies del navegador (la API no las usa)
}

# Mensaje en español para cada tipo de error de validación de Pydantic.
# Lo que va entre llaves, por ejemplo {gt}, se reemplaza por el límite que no se cumplió.
# Las llaves dobles {{ }} se muestran como llaves normales { }.
JB_MENSAJES_VALIDACION = {
    "missing": "Es obligatorio",  # no se envió el campo
    "json_invalid": "El cuerpo no es un JSON válido: revise comas, comillas y llaves",  # JSON mal escrito
    "json_type": "El cuerpo debe ser un JSON",  # se envió otra cosa en vez de JSON
    "model_attributes_type": "Debe ser un objeto JSON {{ }}",  # se esperaba un objeto
    "dict_type": "Debe ser un objeto JSON {{ }}",  # se esperaba un objeto
    "model_type": "Debe ser un objeto JSON {{ }}",  # se esperaba un objeto
    "list_type": "Debe ser una lista [ ]",  # se esperaba una lista
    "string_type": "Debe ser un texto entre comillas",  # se envió un número u otro tipo
    "string_too_short": "Debe tener al menos {min_length} caracteres",  # texto muy corto
    "string_too_long": "Debe tener máximo {max_length} caracteres",  # texto muy largo
    "string_pattern_mismatch": "No tiene un formato válido",  # no cumple el patrón (si no hay uno más claro abajo)
    "int_type": "Debe ser un número entero",  # se esperaba un entero
    "int_parsing": "Debe ser un número entero",  # el texto no se puede convertir en entero
    "int_from_float": "Debe ser un número entero, sin decimales",  # llegó 1.5 donde va un entero
    "float_type": "Debe ser un número",  # se esperaba un número
    "float_parsing": "Debe ser un número",  # el texto no se puede convertir en número
    "decimal_type": "Debe ser un número",  # se esperaba un número decimal
    "decimal_parsing": "Debe ser un número",  # el texto no se puede convertir en decimal
    "decimal_max_places": "Debe tener máximo {decimal_places} decimales",  # demasiados decimales
    "decimal_max_digits": "Debe tener máximo {max_digits} dígitos",  # número demasiado largo
    "decimal_whole_digits": "Debe tener máximo {whole_digits} dígitos antes del punto",  # parte entera muy larga
    "finite_number": "Debe ser un número finito",  # se envió infinito o NaN
    "greater_than": "Debe ser mayor que {gt}",  # Field(gt=...)
    "greater_than_equal": "Debe ser mayor o igual a {ge}",  # Field(ge=...)
    "less_than": "Debe ser menor que {lt}",  # Field(lt=...)
    "less_than_equal": "Debe ser menor o igual a {le}",  # Field(le=...)
    "multiple_of": "Debe ser múltiplo de {multiple_of}",  # Field(multiple_of=...)
    "literal_error": "Debe ser uno de estos valores: {expected}",  # valor fuera de la lista permitida
    "enum": "Debe ser uno de estos valores: {expected}",  # valor fuera de la lista permitida
    "too_short": "Debe tener al menos {min_length} elementos",  # lista con muy pocos elementos
    "too_long": "Debe tener máximo {max_length} elementos",  # lista con demasiados elementos
    "bool_type": "Debe ser true o false",  # se esperaba un booleano
    "bool_parsing": "Debe ser true o false",  # el texto no se puede convertir en booleano
    "date_type": "Debe ser una fecha con el formato AAAA-MM-DD",  # se esperaba una fecha
    "date_parsing": "Debe ser una fecha válida con el formato AAAA-MM-DD",  # fecha mal escrita
    "date_from_datetime_parsing": "Debe ser una fecha válida con el formato AAAA-MM-DD",  # fecha mal escrita
    "date_from_datetime_inexact": "Debe ser solo una fecha, sin hora (AAAA-MM-DD)",  # llegó fecha con hora
    "datetime_type": "Debe ser una fecha y hora con el formato AAAA-MM-DDTHH:MM:SS",  # se esperaba fecha y hora
    "datetime_parsing": "Debe ser una fecha y hora válida con el formato AAAA-MM-DDTHH:MM:SS",  # mal escrita
    "datetime_from_date_parsing": "Debe ser una fecha y hora válida con el formato AAAA-MM-DDTHH:MM:SS",  # mal escrita
    "extra_forbidden": "Este campo no está permitido",  # se envió un campo que el esquema no acepta
    "value_error": "{error}",  # error de una validación propia: el mensaje ya está en español
    "assertion_error": "{error}",  # error de una validación propia: el mensaje ya está en español
}

# Mensajes para cuando el límite es 1, para no decir "1 caracteres" o "1 elementos"
JB_MENSAJES_SINGULAR = {
    "string_too_short": "No puede estar vacío",  # min_length=1
    "string_too_long": "Debe tener máximo 1 carácter",  # max_length=1
    "too_short": "Debe tener al menos un elemento",  # lista con min_length=1
    "too_long": "Debe tener máximo un elemento",  # lista con max_length=1
    "decimal_max_places": "Debe tener máximo 1 decimal",  # decimal_places=1
    "decimal_max_digits": "Debe tener máximo 1 dígito",  # max_digits=1
}

# Mensajes más claros para los patrones conocidos, en vez de mostrar la expresión regular
JB_MENSAJES_PATRON = {
    JB_PATRON_CORREO: "Debe ser un correo válido, por ejemplo nombre@dominio.com",  # campo correo
    JB_PATRON_TELEFONO: "Debe ser un teléfono de 7 a 20 caracteres: números, espacios, +, ( ) y -",  # campo telefono
    JB_PATRON_DOCUMENTO: "Debe tener de 5 a 20 letras, números o guiones",  # campo identificacion
    JB_PATRON_NIT: "Debe tener de 5 a 20 números o guiones",  # campo nit de proveedores
    JB_PATRON_OBJECT_ID: "Debe ser un id de MongoDB: 24 caracteres entre 0-9 y a-f",  # id de una calificación
}

# Mensaje en español para los errores HTTP que FastAPI genera solo, con su texto en inglés
JB_MENSAJES_HTTP = {
    400: "Petición incorrecta",  # Bad Request
    401: "No autorizado: inicie sesión y envíe el token",  # Unauthorized
    403: "Acceso denegado",  # Forbidden
    404: "La ruta no existe: revise la dirección (todas empiezan por /api/v1)",  # Not Found
    405: "Método HTTP no permitido en esta ruta",  # Method Not Allowed
    500: "Error interno del servidor",  # Internal Server Error
}

# Claves del contexto de Pydantic que dicen "cuántos" (caracteres, elementos, decimales o dígitos)
JB_CLAVES_CANTIDAD = ("min_length", "max_length", "decimal_places", "max_digits")

# Mensaje para cada restricción UNIQUE del script 01 cuando se intenta repetir un dato (error 1062 de MySQL)
JB_MENSAJES_UNICOS = {
    "uq_usuarios_identificacion": "Ya existe un usuario con esa identificación",  # usuarios.identificacion
    "uq_usuarios_correo": "Ya existe un usuario con ese correo",  # usuarios.correo
    "uq_categorias_nombre": "Ya existe una categoría con ese nombre",  # categorias.nombre
    "uq_productos_codigo": "Ya existe un producto con ese código",  # productos.codigo
    "uq_insumos_nombre": "Ya existe un insumo con ese nombre",  # insumos.nombre
    "uq_recetas_producto_insumo": "Ese insumo ya está en la receta de ese producto",  # recetas (producto, insumo)
    "uq_proveedores_nit": "Ya existe un proveedor con ese NIT",  # proveedores.nit
    "uq_compras_proveedor_factura": "Ese proveedor ya tiene una compra con ese número de factura",  # compras (proveedor, factura)
    "uq_detalle_compra_compra_insumo": "Un insumo no se puede repetir en la misma compra",  # detalle_compra (compra, insumo)
    "uq_clientes_identificacion": "Ya existe un cliente con esa identificación",  # clientes.identificacion
    "uq_detalle_pedido_pedido_producto": "Un producto no se puede repetir en el mismo pedido",  # detalle_pedido (pedido, producto)
}

# Mensaje para cada restricción CHECK del script 01 cuando un dato no la cumple (error 3819 de MySQL)
JB_MENSAJES_CHECK = {
    "ck_insumos_stock_actual": "El stock de un insumo no puede quedar negativo",  # insumos.stock_actual >= 0
    "ck_insumos_stock_minimo": "El stock mínimo no puede ser negativo",  # insumos.stock_minimo >= 0
    "ck_insumos_costo": "El costo de un insumo no puede ser negativo",  # insumos.costo_unitario >= 0
    "ck_productos_precio": "El precio de venta debe ser mayor que 0",  # productos.precio_venta > 0
    "ck_recetas_cantidad": "La cantidad de la receta debe ser mayor que 0",  # recetas.cantidad > 0
    "ck_compras_total": "El total de la compra no puede ser negativo",  # compras.total >= 0
    "ck_detalle_compra_cantidad": "La cantidad comprada debe ser mayor que 0",  # detalle_compra.cantidad > 0
    "ck_detalle_compra_costo": "El costo de compra no puede ser negativo",  # detalle_compra.costo_unitario >= 0
    "ck_detalle_compra_subtotal": "El subtotal de la compra no puede ser negativo",  # detalle_compra.subtotal >= 0
    "ck_pedidos_total": "El total del pedido no puede ser negativo",  # pedidos.total >= 0
    "ck_detalle_pedido_cantidad": "La cantidad pedida debe ser mayor que 0",  # detalle_pedido.cantidad > 0
    "ck_detalle_pedido_precio": "El precio del pedido debe ser mayor que 0",  # detalle_pedido.precio_unitario > 0
    "ck_detalle_pedido_subtotal": "El subtotal del pedido no puede ser negativo",  # detalle_pedido.subtotal >= 0
}

# Errores de MySQL que significan "no hay conexión" o "el usuario no puede entrar"
JB_ERRORES_CONEXION_MYSQL = (1044, 1045, 1049, 2003, 2005, 2006, 2013)


# Función que traduce dónde está un error de validación
def jb_ubicacion(jb_loc: tuple) -> tuple[str, str]:
    """Convierte la ubicación de Pydantic, por ejemplo ("body", "detalle", 0, "cantidad"),
    en ("cuerpo", "detalle[0].cantidad")."""
    # El primer elemento dice dónde está el error (body, path, query...): se traduce
    jb_donde = JB_UBICACIONES.get(jb_loc[0], str(jb_loc[0]))
    # Aquí se arma el nombre del campo, parte por parte
    jb_campo = ""
    # Se recorren las demás partes de la ubicación
    for jb_parte in jb_loc[1:]:
        # Un número es la posición dentro de una lista: se escribe entre corchetes, como detalle[0]
        if isinstance(jb_parte, int):
            # Agrega la posición entre corchetes
            jb_campo += f"[{jb_parte}]"
        # Un texto es el nombre de un campo: se separa con punto del anterior, como detalle[0].cantidad
        else:
            # Agrega el nombre del campo (con punto si ya había algo antes)
            jb_campo += f".{jb_parte}" if jb_campo else str(jb_parte)
    # Si no hay nombre de campo, el error es de todo el cuerpo (por ejemplo, no se envió nada)
    return jb_donde, jb_campo or "(todo el cuerpo)"


# Función que traduce un error de validación de Pydantic al español
def jb_traducir_error(jb_error: dict) -> dict:
    """Recibe un error de validación de Pydantic (en inglés) y devuelve
    {"ubicacion", "campo", "mensaje"} en español."""
    # Tipo de error, por ejemplo "missing" o "greater_than"
    jb_tipo = jb_error["type"]
    # Datos extra del error, por ejemplo {"gt": 0}; se copian para poder cambiarlos
    jb_contexto = dict(jb_error.get("ctx") or {})
    # Dónde está el error y en qué campo
    jb_donde, jb_campo = jb_ubicacion(jb_error["loc"])
    # En un JSON mal escrito, Pydantic da la posición del carácter, no un campo
    if jb_tipo == "json_invalid":
        # Se informa que el problema es todo el cuerpo
        jb_campo = "(todo el cuerpo)"
    # La lista de valores permitidos viene como "'A', 'B' or 'C'": se cambia "or" por "o"
    if "expected" in jb_contexto:
        # Reemplaza la palabra en inglés por la española
        jb_contexto["expected"] = str(jb_contexto["expected"]).replace(" or ", " o ")
    # El error de una validación propia es un objeto: se convierte en su texto
    if "error" in jb_contexto:
        # Queda solo el mensaje (que ya está en español)
        jb_contexto["error"] = str(jb_contexto["error"])
    # Se busca si el error trae una cantidad (mínimo o máximo de caracteres, elementos, decimales...)
    jb_cantidad = next((jb_contexto[jb_clave] for jb_clave in JB_CLAVES_CANTIDAD if jb_clave in jb_contexto), None)
    # Si la cantidad es 1, se usa el mensaje en singular
    if jb_cantidad == 1 and jb_tipo in JB_MENSAJES_SINGULAR:
        # Mensaje en singular, por ejemplo "No puede estar vacío"
        jb_mensaje = JB_MENSAJES_SINGULAR[jb_tipo]
    # Si es un patrón conocido (correo, teléfono...), se usa su mensaje claro
    elif jb_tipo == "string_pattern_mismatch" and jb_contexto.get("pattern") in JB_MENSAJES_PATRON:
        # Mensaje del patrón, por ejemplo "Debe ser un correo válido..."
        jb_mensaje = JB_MENSAJES_PATRON[jb_contexto["pattern"]]
    # En los demás casos se toma la plantilla del tipo de error
    else:
        # Si el tipo no está en la tabla, se usa un mensaje general
        jb_plantilla = JB_MENSAJES_VALIDACION.get(jb_tipo, "Valor no válido")
        # Se intenta reemplazar los {límites} de la plantilla con los datos del error
        try:
            # Por ejemplo "Debe ser mayor que {gt}" queda "Debe ser mayor que 0"
            jb_mensaje = jb_plantilla.format(**jb_contexto)
        # Si falta algún dato para la plantilla, se responde el mensaje general en vez de fallar
        except (KeyError, IndexError, ValueError):
            # Mensaje general
            jb_mensaje = "Valor no válido"
    # Resultado en español, con la misma forma para todos los errores
    return {"ubicacion": jb_donde, "campo": jb_campo, "mensaje": jb_mensaje}


# Función que traduce los mensajes HTTP que FastAPI escribe en inglés
def jb_mensaje_http(jb_codigo: int, jb_detalle, jb_encabezados: dict | None) -> str:
    """Traduce los textos en inglés que FastAPI pone solo ("Not Found", "Method Not Allowed"...).
    Los mensajes propios de la API ya están en español y se devuelven igual."""
    # Si el mensaje no es el texto estándar en inglés de ese código, es propio de la API: no se toca
    if jb_detalle != HTTPStatus(jb_codigo).phrase:
        # Devuelve el mensaje tal cual
        return jb_detalle
    # Se busca el mensaje en español del código; si no está, se usa uno general
    jb_mensaje = JB_MENSAJES_HTTP.get(jb_codigo, "Error en la petición")
    # En un 405, el encabezado Allow dice qué métodos sí acepta la ruta: se agregan al mensaje
    if jb_codigo == 405 and jb_encabezados and "Allow" in jb_encabezados:
        # Agrega los métodos permitidos al final del mensaje
        jb_mensaje += f". Métodos permitidos: {jb_encabezados['Allow']}"
    # Mensaje final en español
    return jb_mensaje


# Función que traduce los errores de MySQL al español con su código HTTP
def jb_traducir_error_mysql(jb_error: DBAPIError) -> tuple[int, str]:
    """Convierte un error de MySQL en (código HTTP, mensaje en español).
    Es la última barrera: los servicios revisan casi todo antes, pero la base de datos manda."""
    # Error original que lanzó PyMySQL; sus argumentos son (número de error, texto en inglés)
    jb_argumentos = getattr(jb_error.orig, "args", ())
    # Número del error de MySQL, por ejemplo 1062
    jb_numero = jb_argumentos[0] if jb_argumentos else None
    # Texto del error de MySQL, en inglés
    jb_texto = str(jb_argumentos[1]) if len(jb_argumentos) > 1 else ""
    # 1062: dato repetido en un campo UNIQUE
    if jb_numero == 1062:
        # El texto termina en "for key 'tabla.nombre_restriccion'": se saca el nombre de la restricción
        jb_coincidencia = re.search(r"for key '(?:[^.']+\.)?([^']+)'", jb_texto)
        # Nombre de la restricción, o vacío si no se encontró
        jb_restriccion = jb_coincidencia.group(1) if jb_coincidencia else ""
        # Responde 409 con el mensaje de esa restricción, o uno general
        return 409, JB_MENSAJES_UNICOS.get(jb_restriccion, "Ya existe un registro con ese mismo dato")
    # 1451: se intenta borrar un registro del que dependen otros (llave foránea)
    if jb_numero == 1451:
        # Responde 409
        return 409, "No se puede eliminar: otros registros dependen de este"
    # 1452: se envió un id que no existe en la tabla relacionada (llave foránea)
    if jb_numero == 1452:
        # Responde 400
        return 400, "Uno de los id enviados no existe en la base de datos"
    # 3819: no se cumple una restricción CHECK
    if jb_numero == 3819:
        # El texto dice "Check constraint 'nombre' is violated": se saca el nombre
        jb_coincidencia = re.search(r"constraint '([^']+)'", jb_texto)
        # Nombre de la restricción, o vacío si no se encontró
        jb_restriccion = jb_coincidencia.group(1) if jb_coincidencia else ""
        # Responde 400 con el mensaje de esa restricción, o uno general
        return 400, JB_MENSAJES_CHECK.get(jb_restriccion, "Un dato no cumple las reglas de la base de datos")
    # 1406: un texto es más largo que la columna
    if jb_numero == 1406:
        # Responde 400
        return 400, "Un texto supera el largo permitido por la base de datos"
    # 1264 y 1690: un número no cabe en la columna (por ejemplo, un stock gigante)
    if jb_numero in (1264, 1690):
        # Responde 400
        return 400, "Un número supera el valor máximo permitido por la base de datos"
    # 1205 y 1213: otra operación tenía bloqueados los mismos datos
    if jb_numero in (1205, 1213):
        # Responde 409 pidiendo repetir la operación
        return 409, "Otra operación estaba usando los mismos datos: intente de nuevo"
    # 1142: el usuario de la API no tiene permiso para esa instrucción
    if jb_numero == 1142:
        # Responde 500 (es un problema de configuración, no del cliente)
        return 500, "El usuario de la API no tiene permiso para esa operación en MySQL"
    # Errores de conexión o de usuario y contraseña
    if jb_numero in JB_ERRORES_CONEXION_MYSQL:
        # Responde 500 explicando qué revisar
        return 500, "No hay conexión con MySQL: revise que el servidor esté encendido y los datos del .env"
    # Cualquier otro error de MySQL
    return 500, "Error interno de la base de datos"
