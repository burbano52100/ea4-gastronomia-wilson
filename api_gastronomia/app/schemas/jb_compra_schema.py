"""Esquemas de compras de insumos a proveedores (RF08). Subtotales y total los calcula la API."""
# datetime: fecha y hora
from datetime import datetime

# BaseModel: clase base; ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import BaseModel, ConfigDict, Field

# Tipos compartidos: cantidad, dinero mayor que 0, base de entrada y número para las respuestas
from app.schemas.jb_tipos import JbCantidad, JbDineroPositivo, JbModeloEntrada, JbNumero


# Un ítem de la compra, tal como se envía
class JbItemCompra(JbModeloEntrada):
    # Insumo comprado
    id_insumo: int
    # Cantidad comprada, mayor que 0 con hasta 3 decimales
    cantidad: JbCantidad
    # Costo por unidad, mayor que 0 con hasta 2 decimales
    costo_unitario: JbDineroPositivo


# Datos para registrar una compra (no lleva subtotales ni total: los calcula la API)
class JbCompraCrear(JbModeloEntrada):
    # Número de la factura del proveedor: de 1 a 30 caracteres
    numero_factura: str = Field(min_length=1, max_length=30)
    # Proveedor de la compra
    id_proveedor: int
    # Fecha opcional; description es el texto de ayuda que muestra Swagger
    fecha_compra: datetime | None = Field(default=None, description="Si no se envía se usa la fecha y hora actual")
    # Lista de ítems, con al menos uno
    detalle: list[JbItemCompra] = Field(min_length=1)

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "numero_factura": "FV-2050",
        "id_proveedor": 1,
        "detalle": [
            {"id_insumo": 1, "cantidad": 10, "costo_unitario": 4300},
            {"id_insumo": 5, "cantidad": 5, "costo_unitario": 3900},
        ],
    }]})


# Un ítem de la compra, como lo devuelve la API
class JbItemCompraRespuesta(BaseModel):
    # Insumo comprado
    id_insumo: int
    # Cantidad comprada
    cantidad: JbNumero
    # Costo por unidad
    costo_unitario: JbNumero
    # cantidad x costo_unitario (lo calcula la API)
    subtotal: JbNumero


# Compra completa, como la devuelve la API
class JbCompraRespuesta(BaseModel):
    # Id de la compra
    id_compra: int
    # Número de factura
    numero_factura: str
    # Fecha y hora de la compra
    fecha_compra: datetime
    # Proveedor
    id_proveedor: int
    # Usuario que la registró (lo toma la API del token)
    id_usuario: int
    # Suma de los subtotales (la calcula la API)
    total: JbNumero
    # Ítems de la compra
    detalle: list[JbItemCompraRespuesta]
