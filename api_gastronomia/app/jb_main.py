"""Punto de entrada de la API.

Ejecutar (desde la carpeta api_gastronomia, con el entorno virtual activo):
    uvicorn app.jb_main:jb_app --reload
Documentación: http://localhost:8000/docs
"""
# logging: escribe mensajes de error en la terminal donde corre la API
import logging

# FastAPI: la aplicación; Request: la petición que llega a los manejadores de error
from fastapi import FastAPI, Request
# Error que FastAPI lanza cuando los datos no cumplen el esquema (422)
from fastapi.exceptions import RequestValidationError
# JSONResponse: respuesta JSON armada a mano; RedirectResponse: redirige a otra dirección
from fastapi.responses import JSONResponse, RedirectResponse
# Errores de MongoDB: sin conexión, dato repetido, permiso o autenticación, error general y error al escribir
from pymongo.errors import ConnectionFailure, DuplicateKeyError, OperationFailure, PyMongoError, WriteError
# Error de MySQL envuelto por SQLAlchemy (dato repetido, llave foránea, CHECK, sin conexión...)
from sqlalchemy.exc import DBAPIError
# Error HTTP base (lo usan FastAPI y Starlette para 401, 403, 404, 405...)
from starlette.exceptions import HTTPException as StarletteHTTPException

# Funciones que traducen al español los errores de FastAPI, Pydantic y MySQL
from app.core.jb_errores import jb_mensaje_http, jb_traducir_error, jb_traducir_error_mysql
# Un módulo por cada grupo de endpoints (cada uno tiene su jb_router)
from app.routers import (
    jb_auth_router,  # /auth: login, registro y perfil
    jb_calificaciones_router,  # /calificaciones (MongoDB)
    jb_categorias_router,  # /categorias
    jb_clientes_router,  # /clientes
    jb_compras_router,  # /compras
    jb_insumos_router,  # /insumos
    jb_pedidos_router,  # /pedidos
    jb_productos_router,  # /productos
    jb_proveedores_router,  # /proveedores
    jb_recetas_router,  # /recetas
    jb_reportes_router,  # /reportes
    jb_usuarios_router,  # /usuarios
)
# Forma de la respuesta 422 en español, para documentarla en Swagger
from app.schemas.jb_tipos import JbErrorValidacion

# Registrador de mensajes con el nombre de la API
jb_registro = logging.getLogger("api_gastronomia")

# Texto de presentación que aparece arriba en Swagger (acepta Markdown)
JB_DESCRIPCION = """
API REST de la **Unidad Productiva de Gastronomía** del Centro de Gestión y Desarrollo Sostenible
Surcolombiano (CGDSS). Gestiona productos, recetas, insumos, proveedores, compras, clientes y pedidos
en **MySQL** (bd_gastronomia), y las calificaciones de los clientes en **MongoDB** (bd_gastronomia_nosql).

### Cómo probarla aquí mismo
1. Abra **Autenticación > POST /api/v1/auth/login**, pulse *Try it out* y luego *Execute*.
2. Copie el valor de `access_token` de la respuesta.
3. Pulse el botón **Authorize** (arriba a la derecha), pegue el token y pulse *Authorize*.
4. Ya puede ejecutar cualquier endpoint según el rol del usuario.

Usuarios de prueba (script database/02): `burbano@gastronomia.com` / `Admin123*` (ADMIN),
`carlos.rojas@gastronomia.com` / `Cajero123*` (CAJERO) y `maria.cruz@gastronomia.com` / `Cocinero123*` (COCINERO).
"""

# Secciones de Swagger en el orden en que se muestran: "name" es el tag de cada router y "description" su texto
JB_ETIQUETAS = [
    {"name": "Autenticación", "description": "Inicio de sesión con JWT (RF01). /auth/login es el único endpoint público."},  # sección 1
    {"name": "Usuarios", "description": "Usuarios y roles ADMIN, CAJERO, COCINERO (RF02)."},  # sección 2
    {"name": "Categorías", "description": "Categorías de productos (RF03)."},  # sección 3
    {"name": "Productos", "description": "Productos, receta y costo de producción (RF04, RF05, RF06)."},  # sección 4
    {"name": "Insumos", "description": "Inventario, stock bajo y vencimientos (RF07)."},  # sección 5
    {"name": "Recetas", "description": "Fichas técnicas: insumos y cantidades por producto (RF05)."},  # sección 6
    {"name": "Proveedores", "description": "Proveedores y su historial de compras (RF08)."},  # sección 7
    {"name": "Compras", "description": "Compras de insumos; actualizan el inventario (RF08, RN02)."},  # sección 8
    {"name": "Clientes", "description": "Clientes por tipo y su historial de pedidos (RF09)."},  # sección 9
    {"name": "Pedidos", "description": "Pedidos y cambio de estado (RF10, RN01, RN03, RN05)."},  # sección 10
    {"name": "Reportes", "description": "Ventas por fechas y productos más vendidos (RF11)."},  # sección 11
    {"name": "Calificaciones (MongoDB)", "description": "Opiniones de los clientes sobre pedidos y productos (RF12)."},  # sección 12
]

# Crea la aplicación
jb_app = FastAPI(
    # Título que se ve en Swagger
    title="API Gastronomía CGDSS",
    # Versión de la API
    version="1.0.0",
    # Texto de presentación
    description=JB_DESCRIPCION,
    # Secciones y su orden
    openapi_tags=JB_ETIQUETAS,
)

# Registra los routers en este orden (es el orden de las secciones en Swagger)
for jb_modulo in (
    jb_auth_router,  # 1. Autenticación
    jb_usuarios_router,  # 2. Usuarios
    jb_categorias_router,  # 3. Categorías
    jb_productos_router,  # 4. Productos
    jb_insumos_router,  # 5. Insumos
    jb_recetas_router,  # 6. Recetas
    jb_proveedores_router,  # 7. Proveedores
    jb_compras_router,  # 8. Compras
    jb_clientes_router,  # 9. Clientes
    jb_pedidos_router,  # 10. Pedidos
    jb_reportes_router,  # 11. Reportes
    jb_calificaciones_router,  # 12. Calificaciones
):
    # Agrega las rutas del router con el prefijo /api/v1 (por ejemplo /api/v1/productos)
    jb_app.include_router(jb_modulo.jb_router, prefix="/api/v1")


# GET /: no aparece en Swagger (include_in_schema=False)
@jb_app.get("/", include_in_schema=False)
# Función que atiende la dirección raíz
def jb_inicio():
    # Quien abra http://localhost:8000 es enviado a la documentación
    return RedirectResponse(url="/docs")


# Arma la documentación de Swagger y cambia a español los textos que FastAPI pone en inglés
def jb_documentacion() -> dict:
    # Solo se arma la primera vez; después se reutiliza la que quedó guardada
    if jb_app.openapi_schema is None:
        # Genera la documentación normal de FastAPI (y la guarda en jb_app.openapi_schema)
        jb_esquema = FastAPI.openapi(jb_app)
        # Esquemas (formas de los datos) que aparecen al final de Swagger
        jb_componentes = jb_esquema["components"]["schemas"]
        # Quita el esquema en inglés del error 422
        jb_componentes.pop("HTTPValidationError", None)
        # Quita el esquema en inglés de cada error de validación
        jb_componentes.pop("ValidationError", None)
        # Genera el esquema del 422 en español; ref_template indica dónde quedan los esquemas internos
        jb_esquema_422 = JbErrorValidacion.model_json_schema(ref_template="#/components/schemas/{model}")
        # Agrega los esquemas internos (JbErrorCampo) a la documentación
        jb_componentes.update(jb_esquema_422.pop("$defs", {}))
        # Agrega el esquema del 422 en español
        jb_componentes["JbErrorValidacion"] = jb_esquema_422
        # Recorre cada ruta de la documentación
        for jb_ruta in jb_esquema["paths"].values():
            # Recorre cada método de la ruta (get, post, put...)
            for jb_operacion in jb_ruta.values():
                # Recorre cada código de respuesta documentado
                for jb_codigo, jb_respuesta in jb_operacion["responses"].items():
                    # Traduce la descripción de las respuestas correctas
                    if jb_respuesta.get("description") == "Successful Response":
                        # Texto en español
                        jb_respuesta["description"] = "Respuesta exitosa"
                    # En las respuestas 422...
                    if jb_codigo == "422":
                        # ...cambia la descripción por una en español
                        jb_respuesta["description"] = "Datos inválidos: el JSON o los parámetros no tienen el formato correcto"
                        # ...y apunta al esquema en español
                        jb_respuesta["content"] = {
                            "application/json": {"schema": {"$ref": "#/components/schemas/JbErrorValidacion"}}  # respuesta JSON con JbErrorValidacion
                        }
    # Devuelve la documentación ya traducida
    return jb_app.openapi_schema


# FastAPI usará esta función para generar /openapi.json (y por lo tanto Swagger)
jb_app.openapi = jb_documentacion


# Maneja los errores HTTP (401, 403, 404, 405, 409...): responde {"detalle": "..."} en español
@jb_app.exception_handler(StarletteHTTPException)
# Recibe la petición que falló y el error HTTP
async def jb_manejar_http(jb_peticion: Request, jb_error: StarletteHTTPException):
    # Traduce el mensaje si es uno de los textos en inglés de FastAPI ("Not Found", "Method Not Allowed"...)
    jb_detalle = jb_mensaje_http(jb_error.status_code, jb_error.detail, jb_error.headers)
    # Responde con el mismo código y los mismos encabezados (por ejemplo WWW-Authenticate o Allow)
    return JSONResponse(status_code=jb_error.status_code, content={"detalle": jb_detalle}, headers=jb_error.headers)


# Maneja los errores de validación (422): traduce cada error al español
@jb_app.exception_handler(RequestValidationError)
# Recibe la petición que falló y el error de validación
async def jb_manejar_validacion(jb_peticion: Request, jb_error: RequestValidationError):
    # Traduce cada uno de los errores encontrados
    jb_errores = [jb_traducir_error(jb_item) for jb_item in jb_error.errors()]
    # Responde 422 con un mensaje general y la lista de errores
    return JSONResponse(status_code=422, content={"detalle": "Los datos enviados no son válidos", "errores": jb_errores})


# Maneja los errores de MySQL: dato repetido (409), llave foránea, CHECK, sin conexión...
@jb_app.exception_handler(DBAPIError)
# Recibe la petición que falló y el error de MySQL
async def jb_manejar_error_mysql(jb_peticion: Request, jb_error: DBAPIError):
    # Traduce el error a (código HTTP, mensaje en español)
    jb_codigo, jb_mensaje = jb_traducir_error_mysql(jb_error)
    # Los errores 500 se anotan completos en la terminal para poder revisarlos
    if jb_codigo == 500:
        # Anota el error con su detalle técnico (el cliente no lo ve)
        jb_registro.exception("Error de MySQL")
    # Responde con el código y el mensaje traducidos
    return JSONResponse(status_code=jb_codigo, content={"detalle": jb_mensaje})


# Maneja los datos repetidos en un índice único de MongoDB: responde 409
@jb_app.exception_handler(DuplicateKeyError)
# Recibe la petición que falló y el error de dato repetido
async def jb_manejar_duplicado_mongo(jb_peticion: Request, jb_error: DuplicateKeyError):
    # Toma de MongoDB el nombre de los campos repetidos; si no viene, un texto general
    jb_campos = ", ".join((jb_error.details or {}).get("keyValue", {}).keys()) or "un campo único"
    # Responde 409 diciendo qué campo está repetido
    return JSONResponse(status_code=409, content={"detalle": f"Ya existe un registro con el mismo valor en: {jb_campos}"})


# Maneja los errores al escribir en MongoDB
@jb_app.exception_handler(WriteError)
# Recibe la petición que falló y el error de escritura
async def jb_manejar_error_escritura(jb_peticion: Request, jb_error: WriteError):
    # El código 121 significa que el documento no cumple el $jsonSchema de la colección
    if jb_error.code == 121:
        # Responde 400
        return JSONResponse(status_code=400, content={"detalle": "Los datos no cumplen la validación de MongoDB ($jsonSchema)"})
    # Cualquier otro error de escritura se anota en la terminal
    jb_registro.exception("Error de escritura en MongoDB")
    # Y se responde 500
    return JSONResponse(status_code=500, content={"detalle": "Error al guardar en MongoDB"})


# Maneja los errores de permisos o de usuario y contraseña de MongoDB
@jb_app.exception_handler(OperationFailure)
# Recibe la petición que falló y la operación rechazada
async def jb_manejar_operacion_mongo(jb_peticion: Request, jb_error: OperationFailure):
    # Anota el error completo en la terminal
    jb_registro.exception("Operación rechazada por MongoDB")
    # 13: sin permiso; 18: usuario o contraseña incorrectos
    if jb_error.code in (13, 18):
        # Responde 500 explicando qué revisar
        return JSONResponse(status_code=500, content={"detalle": "MongoDB rechazó el usuario de la API: revise MONGO_USUARIO y MONGO_PASSWORD del .env y el script 04"})
    # Cualquier otra operación rechazada
    return JSONResponse(status_code=500, content={"detalle": "Error interno de MongoDB"})


# Maneja la falta de conexión con MongoDB (servidor apagado)
@jb_app.exception_handler(ConnectionFailure)
# Recibe la petición que falló y el error de conexión
async def jb_manejar_sin_conexion_mongo(jb_peticion: Request, jb_error: ConnectionFailure):
    # Responde 500 explicando qué revisar
    return JSONResponse(
        # Código 500
        status_code=500,
        # Mensaje en español
        content={"detalle": "No hay conexión con MongoDB: revise que el contenedor esté encendido y los datos del .env"},
    )


# Maneja cualquier otro error de MongoDB
@jb_app.exception_handler(PyMongoError)
# Recibe la petición que falló y el error de MongoDB
async def jb_manejar_error_mongo(jb_peticion: Request, jb_error: PyMongoError):
    # Anota el error completo en la terminal
    jb_registro.exception("Error de MongoDB")
    # Responde 500 sin mostrar detalles internos
    return JSONResponse(status_code=500, content={"detalle": "Error interno de MongoDB"})


# Maneja cualquier error que no se haya previsto
@jb_app.exception_handler(Exception)
# Recibe la petición que falló y el error inesperado
async def jb_manejar_error_general(jb_peticion: Request, jb_error: Exception):
    # Anota el error completo en la terminal
    jb_registro.exception("Error no controlado")
    # Responde 500 sin mostrar detalles internos
    return JSONResponse(status_code=500, content={"detalle": "Error interno del servidor"})


# Este bloque solo se ejecuta si se corre el archivo directamente: python -m app.jb_main
if __name__ == "__main__":
    # Se importa aquí porque solo se necesita en este caso
    import uvicorn

    # Enciende la API en http://127.0.0.1:8000 con recarga automática
    uvicorn.run("app.jb_main:jb_app", host="127.0.0.1", port=8000, reload=True)
