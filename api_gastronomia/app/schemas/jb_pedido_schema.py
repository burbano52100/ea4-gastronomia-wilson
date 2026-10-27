"""Esquemas de pedidos (RF10).

RN01: quien registra el pedido solo envía productos y cantidades. Precio, subtotal y total los calcula
la API, por eso esos campos no existen en JbPedidoCrear (si se envían, la API responde 422).
"""
# datetime: fecha y hora
from datetime import datetime
# Literal: solo permite ciertos valores fijos
from typing import Literal

# ConfigDict: configuración del esquema; Field: reglas de un campo; field_validator: validación propia de un campo
from pydantic import ConfigDict, Field, field_validator

# Tipos compartidos y la función que revisa repetidos
from app.schemas.jb_tipos import (
    JbCantidadPedido,  # cantidad pedida mayor que 0 con hasta 2 decimales
    JbModeloEntrada,  # base de los esquemas que reciben datos
    JbModeloRespuesta,  # base de las respuestas
    JbNumero,  # decimal que se responde como número
    jb_validar_sin_repetidos,  # revisa que no haya ids repetidos
)

# Tipos de pedido permitidos (ENUM de la tabla pedidos)
JbTipoPedido = Literal["MESA", "PARA_LLEVAR", "EVENTO"]
# Estados de pedido permitidos (ENUM de la tabla pedidos)
JbEstadoPedido = Literal["PENDIENTE", "EN_PREPARACION", "ENTREGADO", "ANULADO"]


# Un ítem del pedido, tal como se envía: solo producto y cantidad (RN01)
class JbItemPedido(JbModeloEntrada):
    # Producto pedido: debe existir y estar DISPONIBLE
    id_producto: int = Field(gt=0)
    # Cantidad: mayor que 0, hasta 2 decimales (por ejemplo, 1.5 libras)
    cantidad: JbCantidadPedido


# Datos para crear un pedido
class JbPedidoCrear(JbModeloEntrada):
    # Cliente que pide: debe existir y estar ACTIVO
    id_cliente: int = Field(gt=0)
    # Tipo de pedido
    tipo_pedido: JbTipoPedido
    # Observaciones opcionales, máximo 255 caracteres
    observaciones: str | None = Field(default=None, max_length=255)
    # Ítems: de 1 a 50, sin productos repetidos
    detalle: list[JbItemPedido] = Field(min_length=1, max_length=50)

    # Validación propia del campo detalle
    @field_validator("detalle")
    # Se ejecuta sobre la clase, no sobre un objeto
    @classmethod
    # Recibe la lista de ítems ya validados y la devuelve si no hay productos repetidos
    def jb_sin_productos_repetidos(cls, jb_detalle: list[JbItemPedido]) -> list[JbItemPedido]:
        # Un producto no puede aparecer dos veces en el mismo pedido
        return jb_validar_sin_repetidos(jb_detalle, "id_producto", "producto")

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "id_cliente": 1,  # ejemplo del campo id_cliente
        "tipo_pedido": "MESA",  # ejemplo del campo tipo_pedido
        "observaciones": "Sin cebolla",  # ejemplo del campo observaciones
        "detalle": [{"id_producto": 4, "cantidad": 1}, {"id_producto": 9, "cantidad": 2}],  # ejemplo del campo detalle
    }]})


# Datos para modificar un pedido (mismos campos: el detalle se reemplaza completo y se recalcula)
class JbPedidoActualizar(JbPedidoCrear):
    """Mismos campos que JbPedidoCrear. Solo funciona si el pedido no está ENTREGADO ni ANULADO (RN05)."""


# Datos para cambiar el estado de un pedido (PATCH /pedidos/{id}/estado)
class JbPedidoEstado(JbModeloEntrada):
    # Estado nuevo
    estado: JbEstadoPedido

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{"estado": "EN_PREPARACION"}]})


# Un ítem del pedido, como lo devuelve la API
class JbItemPedidoRespuesta(JbModeloRespuesta):
    # Id del ítem
    id_detalle: int
    # Id del producto
    id_producto: int
    # Nombre del producto (lo agrega la API)
    nombre_producto: str
    # Cantidad
    cantidad: JbNumero
    # Precio del producto al momento del pedido (lo pone la API, RN01)
    precio_unitario: JbNumero
    # cantidad x precio_unitario (lo calcula la API, RN01)
    subtotal: JbNumero


# Pedido completo, como lo devuelve la API
class JbPedidoRespuesta(JbModeloRespuesta):
    # Id del pedido
    id_pedido: int
    # Fecha y hora del pedido (hora de Colombia)
    fecha_pedido: datetime
    # Id del cliente
    id_cliente: int
    # Nombre completo del cliente (lo agrega la API)
    nombre_cliente: str
    # Usuario que lo registró (la API lo toma del token)
    id_usuario: int
    # Tipo de pedido
    tipo_pedido: JbTipoPedido
    # Estado actual
    estado: JbEstadoPedido
    # Observaciones (puede ser null)
    observaciones: str | None = None
    # Suma de los subtotales (RN01)
    total: JbNumero
    # Ítems del pedido
    detalle: list[JbItemPedidoRespuesta]


# ----- VENTA RAPIDA (usabilidad.md, paso B1): esquema JbVentaCrear -----
# Datos para vender un producto en un solo paso (POST /pedidos/venta)
class JbVentaCrear(JbModeloEntrada):
    # Cliente que compra: debe existir y estar ACTIVO
    id_cliente: int = Field(gt=0)
    # Producto que se vende: debe estar DISPONIBLE
    id_producto: int = Field(gt=0)
    # Cantidad mayor que 0, con máximo 2 decimales
    cantidad: JbCantidadPedido
    # Tipo de pedido; si no se envía queda PARA_LLEVAR
    tipo_pedido: JbTipoPedido = "PARA_LLEVAR"
    # Observaciones opcionales, máximo 255 caracteres
    observaciones: str | None = Field(default=None, max_length=255)

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "id_cliente": 1,  # ejemplo del campo id_cliente
        "id_producto": 9,  # ejemplo del campo id_producto
        "cantidad": 2,  # ejemplo del campo cantidad
    }]})
