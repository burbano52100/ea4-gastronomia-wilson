"""Esquemas de calificaciones de los clientes (RF12), guardadas en bd_gastronomia_nosql."""
# datetime: fecha y hora
from datetime import datetime

# BaseModel: clase base; ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import BaseModel, ConfigDict, Field

# Base de los esquemas de entrada (quita espacios de los textos)
from app.schemas.jb_tipos import JbModeloEntrada


# Calificación de un producto, tal como la envía el cliente
class JbCalificacionProducto(JbModeloEntrada):
    # Producto que se califica
    id_producto: int
    # Calificación de 1 a 5 (ge = mayor o igual, le = menor o igual)
    calificacion: int = Field(ge=1, le=5)


# Datos para modificar una calificación
class JbCalificacionActualizar(JbModeloEntrada):
    # Calificación del servicio, de 1 a 5
    calificacion_servicio: int = Field(ge=1, le=5)
    # Comentario opcional, máximo 500 caracteres
    comentario: str | None = Field(default=None, max_length=500)
    # Lista de productos calificados, con al menos uno
    productos: list[JbCalificacionProducto] = Field(min_length=1)

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "calificacion_servicio": 4,
        "comentario": "Buena atención, el jugo estaba un poco dulce",
        "productos": [{"id_producto": 1, "calificacion": 5}, {"id_producto": 2, "calificacion": 3}],
    }]})


# Datos para crear una calificación: los mismos de actualizar más el pedido
class JbCalificacionCrear(JbCalificacionActualizar):
    # Pedido que se califica (debe estar ENTREGADO)
    id_pedido: int

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "id_pedido": 15,
        "calificacion_servicio": 5,
        "comentario": "Excelente atención y buen sabor",
        "productos": [{"id_producto": 1, "calificacion": 5}, {"id_producto": 2, "calificacion": 4}],
    }]})


# Producto calificado, como lo devuelve la API
class JbCalificacionProductoRespuesta(BaseModel):
    # Id del producto
    id_producto: int
    # Nombre del producto (lo agrega la API)
    nombre: str
    # Calificación de 1 a 5
    calificacion: int


# Calificación completa, como la devuelve la API
class JbCalificacionRespuesta(BaseModel):
    # Id de la calificación
    id_calificacion: int
    # Pedido calificado
    id_pedido: int
    # Cliente que calificó (lo toma la API del pedido)
    id_cliente: int
    # Fecha y hora de la calificación
    fecha: datetime
    # Calificación del servicio
    calificacion_servicio: int
    # Comentario, puede ser null
    comentario: str | None = None
    # Productos calificados
    productos: list[JbCalificacionProductoRespuesta]


# Una opinión sobre un producto, para el resumen de calificaciones del producto
class JbOpinionProducto(BaseModel):
    # Id de la calificación
    id_calificacion: int
    # Pedido calificado
    id_pedido: int
    # Cliente que calificó
    id_cliente: int
    # Fecha de la calificación
    fecha: datetime
    # Calificación que recibió el producto
    calificacion: int
    # Comentario general, puede ser null
    comentario: str | None = None


# Respuesta de GET /calificaciones/producto/{id}: promedio y opiniones de un producto
class JbResumenCalificaciones(BaseModel):
    # Id del producto
    id_producto: int
    # Nombre del producto
    producto: str
    # Promedio de calificaciones; null si nadie lo ha calificado
    promedio: float | None
    # Cuántas calificaciones tiene
    total_calificaciones: int
    # Lista de opiniones
    calificaciones: list[JbOpinionProducto]
