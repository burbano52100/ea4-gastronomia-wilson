"""Respuestas de error documentadas en Swagger. Se reutilizan en todos los routers."""
# JbError: forma del JSON de error {"detalle": "..."} que se muestra en Swagger
from app.schemas.jb_tipos import JbError

# Cada diccionario dice a Swagger: "este endpoint puede responder este código, con esta forma y esta descripción"
# 400: el dato rompe una regla de negocio
JB_R400 = {400: {"model": JbError, "description": "Los datos no cumplen una regla de negocio"}}
# 401: no se envió el token o no sirve
JB_R401 = {401: {"model": JbError, "description": "Token ausente, inválido o expirado"}}
# 403: el usuario no tiene el rol necesario
JB_R403 = {403: {"model": JbError, "description": "El rol del usuario no tiene permiso"}}
# 404: lo que se pide en la URL no existe
JB_R404 = {404: {"model": JbError, "description": "El recurso solicitado no existe"}}
# 409: choca con otro dato o con el estado actual
JB_R409 = {409: {"model": JbError, "description": "Conflicto: dato duplicado, inventario insuficiente o pedido cerrado"}}

# Los endpoints privados pueden responder 401 y 403: se juntan los dos diccionarios en uno
JB_PRIVADO = {**JB_R401, **JB_R403}
