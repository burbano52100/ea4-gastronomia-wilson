"""Esquemas de calificaciones de los clientes (RF12), guardadas en MongoDB."""
# datetime: fecha y hora
from datetime import datetime
# Annotated: agrega reglas a un tipo
from typing import Annotated

# BaseModel: clase base; ConfigDict: configuración; Field: reglas; field_validator: validación propia de un campo
from pydantic import BaseModel, ConfigDict, Field, field_validator

# Tipos compartidos y la función que revisa repetidos
from app.schemas.jb_tipos import JbModeloEntrada, jb_validar_sin_repetidos

# Nota: número entero de 1 a 5 (el validador $jsonSchema de MongoDB exige lo mismo)
JbNota = Annotated[int, Field(ge=1, le=5)]


# Un producto calificado, tal como se envía (el nombre lo pone la API desde MySQL)
class JbProductoCalificado(JbModeloEntrada):
    # Producto: debe estar en el pedido
    id_producto: int = Field(gt=0)
    # Nota del producto
    calificacion: JbNota


# Datos para registrar una calificación
class JbCalificacionCrear(JbModeloEntrada):
    # Pedido calificado: debe existir en MySQL y estar ENTREGADO
    id_pedido: int = Field(gt=0)
    # Cliente: debe ser el que hizo el pedido
    id_cliente: int = Field(gt=0)
    # Nota del servicio
    calificacion_servicio: JbNota
    # Comentario opcional, máximo 500 caracteres
    comentario: str | None = Field(default=None, max_length=500)
    # Productos calificados: de 1 a 50, sin repetidos
    productos: list[JbProductoCalificado] = Field(min_length=1, max_length=50)

    # Validación propia del campo productos
    @field_validator("productos")
    # Se ejecuta sobre la clase, no sobre un objeto
    @classmethod
    # Recibe la lista de productos ya validados y la devuelve si no hay repetidos
    def jb_sin_productos_repetidos(cls, jb_productos: list[JbProductoCalificado]) -> list[JbProductoCalificado]:
        # Un producto se califica una sola vez en cada calificación
        return jb_validar_sin_repetidos(jb_productos, "id_producto", "producto")

    # Ejemplo que muestra Swagger al pulsar "Try it out" (el pedido 112 es ENTREGADO y aún no tiene calificación)
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "id_pedido": 112,  # ejemplo del campo id_pedido
        "id_cliente": 9,  # ejemplo del campo id_cliente
        "calificacion_servicio": 5,  # ejemplo del campo calificacion_servicio
        "comentario": "Excelente atención y buen sabor",  # ejemplo del campo comentario
        "productos": [{"id_producto": 11, "calificacion": 5}, {"id_producto": 10, "calificacion": 4}],  # ejemplo del campo productos
    }]})


# Datos para modificar una calificación (el pedido y el cliente no cambian)
class JbCalificacionActualizar(JbModeloEntrada):
    # Nota del servicio
    calificacion_servicio: JbNota
    # Comentario opcional
    comentario: str | None = Field(default=None, max_length=500)
    # Productos calificados: de 1 a 50, sin repetidos
    productos: list[JbProductoCalificado] = Field(min_length=1, max_length=50)

    # Validación propia del campo productos
    @field_validator("productos")
    # Se ejecuta sobre la clase, no sobre un objeto
    @classmethod
    # Recibe la lista de productos ya validados y la devuelve si no hay repetidos
    def jb_sin_productos_repetidos(cls, jb_productos: list[JbProductoCalificado]) -> list[JbProductoCalificado]:
        # Un producto se califica una sola vez en cada calificación
        return jb_validar_sin_repetidos(jb_productos, "id_producto", "producto")

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "calificacion_servicio": 4,  # ejemplo del campo calificacion_servicio
        "comentario": "Buen sabor, la espera fue un poco larga",  # ejemplo del campo comentario
        "productos": [{"id_producto": 11, "calificacion": 4}],  # ejemplo del campo productos
    }]})


# Un producto calificado, como lo devuelve la API
class JbProductoCalificadoRespuesta(BaseModel):
    # Id del producto
    id_producto: int
    # Nombre del producto (copiado de MySQL al registrar)
    nombre: str
    # Nota del producto
    calificacion: int


# Calificación completa, como la devuelve la API
class JbCalificacionRespuesta(BaseModel):
    # Id del documento en MongoDB (24 caracteres)
    id_calificacion: str
    # Pedido calificado
    id_pedido: int
    # Cliente
    id_cliente: int
    # Fecha y hora del registro (hora de Colombia)
    fecha: datetime
    # Nota del servicio
    calificacion_servicio: int
    # Comentario (puede ser null)
    comentario: str | None = None
    # Productos calificados
    productos: list[JbProductoCalificadoRespuesta]


# Una calificación de un producto (para GET /calificaciones/producto/{id})
class JbCalificacionDeProducto(BaseModel):
    # Id del documento en MongoDB
    id_calificacion: str
    # Pedido
    id_pedido: int
    # Cliente
    id_cliente: int
    # Fecha y hora
    fecha: datetime
    # Nota que recibió el producto en esa calificación
    calificacion: int
    # Comentario general (puede ser null)
    comentario: str | None = None


# Respuesta de GET /calificaciones/producto/{id}
class JbCalificacionesProducto(BaseModel):
    # Id del producto
    id_producto: int
    # Nombre del producto
    nombre: str
    # Cuántas calificaciones tiene
    total_calificaciones: int
    # Promedio de sus notas, con 2 decimales (null si no tiene calificaciones)
    promedio: float | None = None
    # Lista de calificaciones, de la más reciente a la más antigua
    calificaciones: list[JbCalificacionDeProducto]
