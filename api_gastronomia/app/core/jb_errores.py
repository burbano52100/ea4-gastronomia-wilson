"""Traducción al español de los errores que FastAPI y Pydantic generan en inglés."""
# HTTPStatus: tabla de Python con el nombre en inglés de cada código HTTP (404 -> "Not Found")
from http import HTTPStatus

# Patrones (expresiones regulares) con los que los esquemas validan correos, teléfonos y documentos
from app.schemas.jb_tipos import JB_PATRON_CORREO, JB_PATRON_DOCUMENTO, JB_PATRON_TELEFONO

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
    JB_PATRON_DOCUMENTO: "Solo puede tener letras, números y guiones",  # campo identificacion
    r"^[0-9-]+$": "Solo puede tener números y guiones",  # campo nit de proveedores
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
            jb_campo += f"[{jb_parte}]"
        # Un texto es el nombre de un campo: se separa con punto del anterior, como detalle[0].cantidad
        else:
            jb_campo += f".{jb_parte}" if jb_campo else str(jb_parte)
    # Si no hay nombre de campo, el error es de todo el cuerpo (por ejemplo, no se envió nada)
    return jb_donde, jb_campo or "(todo el cuerpo)"


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
        jb_campo = "(todo el cuerpo)"
    # La lista de valores permitidos viene como "'A', 'B' or 'C'": se cambia "or" por "o"
    if "expected" in jb_contexto:
        jb_contexto["expected"] = str(jb_contexto["expected"]).replace(" or ", " o ")
    # El error de una validación propia es un objeto: se convierte en su texto
    if "error" in jb_contexto:
        jb_contexto["error"] = str(jb_contexto["error"])
    # Se busca si el error trae una cantidad (mínimo o máximo de caracteres, elementos, decimales...)
    jb_cantidad = next((jb_contexto[jb_clave] for jb_clave in JB_CLAVES_CANTIDAD if jb_clave in jb_contexto), None)
    # Si la cantidad es 1, se usa el mensaje en singular
    if jb_cantidad == 1 and jb_tipo in JB_MENSAJES_SINGULAR:
        jb_mensaje = JB_MENSAJES_SINGULAR[jb_tipo]
    # Si es un patrón conocido (correo, teléfono...), se usa su mensaje claro
    elif jb_tipo == "string_pattern_mismatch" and jb_contexto.get("pattern") in JB_MENSAJES_PATRON:
        jb_mensaje = JB_MENSAJES_PATRON[jb_contexto["pattern"]]
    # En los demás casos se toma la plantilla del tipo de error
    else:
        # Si el tipo no está en la tabla, se usa un mensaje general
        jb_plantilla = JB_MENSAJES_VALIDACION.get(jb_tipo, "Valor no válido")
        # Se intenta reemplazar los {límites} de la plantilla con los datos del error
        try:
            jb_mensaje = jb_plantilla.format(**jb_contexto)
        # Si falta algún dato para la plantilla, se responde el mensaje general en vez de fallar
        except (KeyError, IndexError, ValueError):
            jb_mensaje = "Valor no válido"
    # Resultado en español, con la misma forma para todos los errores
    return {"ubicacion": jb_donde, "campo": jb_campo, "mensaje": jb_mensaje}


def jb_mensaje_http(jb_codigo: int, jb_detalle, jb_encabezados: dict | None) -> str:
    """Traduce los textos en inglés que FastAPI pone solo ("Not Found", "Method Not Allowed"...).
    Los mensajes propios de la API ya están en español y se devuelven igual."""
    # Si el mensaje no es el texto estándar en inglés de ese código, es propio de la API: no se toca
    if jb_detalle != HTTPStatus(jb_codigo).phrase:
        return jb_detalle
    # Se busca el mensaje en español del código; si no está, se usa uno general
    jb_mensaje = JB_MENSAJES_HTTP.get(jb_codigo, "Error en la petición")
    # En un 405, el encabezado Allow dice qué métodos sí acepta la ruta: se agregan al mensaje
    if jb_codigo == 405 and jb_encabezados and "Allow" in jb_encabezados:
        jb_mensaje += f". Métodos permitidos: {jb_encabezados['Allow']}"
    # Mensaje final en español
    return jb_mensaje
