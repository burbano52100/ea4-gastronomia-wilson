"""Esquemas de pedidos (RF10).

RN01: el cliente solo envía productos y cantidades. Precio, subtotal y total los calcula la API,
por eso esos campos no existen en JbPedidoCrear.
"""
# datetime: fecha y hora
from datetime import datetime
# Literal: solo permite ciertos valores fijos
from typing import Literal

# BaseModel: clase base; ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import BaseModel, ConfigDict, Field

# JbModeloEntrada: base de los esquemas de entrada; JbNumero: decimal que se responde como número
from app.schemas.jb_tipos import JbModeloEntrada, JbNumero

# Tipos de pedido permitidos (ENUM del instructivo)
JbTipoPedido = Literal["MESA", "PARA_LLEVAR", "EVENTO"]
# Estados de pedido permitidos (ENUM del instructivo)
JbEstadoPedido = Literal["PENDIENTE", "EN_PREPARACION", "ENTREGADO", "ANULADO"]


# Un ítem del pedido, tal como se envía: solo producto y cantidad (RN01)
class JbItemPedido(JbModeloEntrada):
    # Producto pedido
    id_producto: int
    # Cantidad: entero mayor que 0 y máximo 1000 (gt = mayor que, le = menor o igual)
    cantidad: int = Field(gt=0, le=1000)


# Datos para crear o modificar un pedido
class JbPedidoCrear(JbModeloEntrada):
    # Cliente que pide
    id_cliente: int
    # Tipo de pedido, uno de la lista
    tipo_pedido: JbTipoPedido
    # Observaciones opcionales, máximo 255 caracteres
    observaciones: str | None = Field(default=None, max_length=255)
    # Lista de ítems, con al menos uno
    detalle: list[JbItemPedido] = Field(min_length=1)

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "id_cliente": 1,
        "tipo_pedido": "MESA",
        "observaciones": "Sin cebolla",
        "detalle": [{"id_producto": 1, "cantidad": 2}, {"id_producto": 2, "cantidad": 2}],
    }]})


# Datos para cambiar el estado de un pedido (PATCH /pedidos/{id}/estado)
class JbPedidoEstado(JbModeloEntrada):
    # Estado nuevo, uno de la lista
    estado: JbEstadoPedido

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{"estado": "EN_PREPARACION"}]})


# Un ítem del pedido, como lo devuelve la API
class JbItemPedidoRespuesta(BaseModel):
    # Producto
    id_producto: int
    # Cantidad
    cantidad: int
    # Precio del producto al momento del pedido (lo pone la API)
    precio_unitario: JbNumero
    # cantidad x precio_unitario (lo calcula la API, RN01)
    subtotal: JbNumero


# Pedido completo, como lo devuelve la API
class JbPedidoRespuesta(BaseModel):
    # Id del pedido
    id_pedido: int
    # Fecha y hora del pedido
    fecha_pedido: datetime
    # Cliente
    id_cliente: int
    # Usuario que lo registró (lo toma la API del token)
    id_usuario: int
    # Tipo de pedido
    tipo_pedido: JbTipoPedido
    # Estado actual
    estado: JbEstadoPedido
    # Observaciones, pueden ser null
    observaciones: str | None = None
    # Suma de los subtotales (la calcula la API, RN01)
    total: JbNumero
    # Ítems del pedido
    detalle: list[JbItemPedidoRespuesta]
