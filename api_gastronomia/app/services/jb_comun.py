"""Respuestas y errores que comparten todos los servicios."""
# HTTPException: error que FastAPI convierte en respuesta HTTP; status: nombres de los códigos
from fastapi import HTTPException, status


# Crea un error 404
def jb_no_encontrado(jb_texto: str) -> HTTPException:
    """404 para el recurso de la URL. Ejemplo: jb_no_encontrado('El producto 7')."""
    # El mensaje queda, por ejemplo, "El producto 7 no existe"
    return HTTPException(status.HTTP_404_NOT_FOUND, f"{jb_texto} no existe")


# Crea un error 400
def jb_dato_invalido(jb_mensaje: str) -> HTTPException:
    """400 cuando el cuerpo de la petición rompe una regla (por ejemplo, un id que no existe)."""
    # Error 400 con el mensaje recibido
    return HTTPException(status.HTTP_400_BAD_REQUEST, jb_mensaje)


# Crea un error 409 (conflicto con el estado actual de los datos)
def jb_conflicto(jb_mensaje: str) -> HTTPException:
    # Error 409 con el mensaje recibido
    return HTTPException(status.HTTP_409_CONFLICT, jb_mensaje)


# Respuesta de un DELETE que no borra sino que deja INACTIVO
def jb_borrado_logico(jb_texto: str) -> dict:
    """RN04: si tiene movimientos asociados no se borra, se marca INACTIVO."""
    # Diccionario con la forma de JbResultadoEliminacion
    return {
        # Explica por qué no se borró
        "mensaje": f"{jb_texto} tiene movimientos asociados: no se eliminó, su estado cambió a INACTIVO (RN04)",
        # Indica que fue un borrado lógico
        "tipo_borrado": "LOGICO",
    }


# Respuesta de un DELETE que sí borra el registro
def jb_borrado_fisico(jb_texto: str) -> dict:
    # Mensaje de confirmación y tipo de borrado FISICO
    return {"mensaje": f"{jb_texto} se eliminó porque no tenía movimientos asociados", "tipo_borrado": "FISICO"}
