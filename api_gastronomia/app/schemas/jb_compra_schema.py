"""Esquemas de compras (RF08). Subtotales y total los calcula la API, por eso no existen en JbCompraCrear."""
# datetime: fecha y hora
from datetime import datetime

# ConfigDict: configuración del esquema; Field: reglas de un campo; field_validator: validación propia de un campo
from pydantic import ConfigDict, Field, field_validator

# Tipos compartidos y la función que revisa repetidos
from app.schemas.jb_tipos import (
    JbCantidad,  # cantidad mayor que 0 con hasta 3 decimales
    JbDinero,  # dinero mayor o igual a 0
    JbModeloEntrada,  # base de los esquemas que reciben datos
    JbModeloRespuesta,  # base de las respuestas
    JbNumero,  # decimal que se responde como número
    jb_validar_sin_repetidos,  # revisa que no haya ids repetidos
)


# Un ítem de la compra, tal como se envía
class JbItemCompra(JbModeloEntrada):
    # Insumo comprado: debe existir y estar ACTIVO
    id_insumo: int = Field(gt=0)
    # Cantidad comprada: mayor que 0, hasta 3 decimales
    cantidad: JbCantidad
    # Costo por unidad en esta compra (RN02: pasa a ser el costo_unitario del insumo)
    costo_unitario: JbDinero


# Datos para registrar una compra
class JbCompraCrear(JbModeloEntrada):
    # Número de la factura del proveedor
    numero_factura: str = Field(min_length=1, max_length=30)
    # Fecha y hora de la compra (opcional: si no se envía, se usa la hora actual de Colombia)
    fecha_compra: datetime | None = None
    # Proveedor: debe existir y estar ACTIVO
    id_proveedor: int = Field(gt=0)
    # Ítems: de 1 a 50, sin insumos repetidos
    detalle: list[JbItemCompra] = Field(min_length=1, max_length=50)

    # Validación propia del campo detalle
    @field_validator("detalle")
    # Se ejecuta sobre la clase, no sobre un objeto
    @classmethod
    # Recibe la lista de ítems ya validados y la devuelve si no hay insumos repetidos
    def jb_sin_insumos_repetidos(cls, jb_detalle: list[JbItemCompra]) -> list[JbItemCompra]:
        # Un insumo no puede aparecer dos veces en la misma compra
        return jb_validar_sin_repetidos(jb_detalle, "id_insumo", "insumo")

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "numero_factura": "FAC-2001",  # ejemplo del campo numero_factura
        "id_proveedor": 6,  # ejemplo del campo id_proveedor
        "detalle": [  # ejemplo del campo detalle
            {"id_insumo": 5, "cantidad": 10, "costo_unitario": 3900},  # ejemplo de un elemento de la lista
            {"id_insumo": 11, "cantidad": 5.5, "costo_unitario": 7200},  # ejemplo de un elemento de la lista
        ],
    }]})


# Datos para modificar una compra: solo los datos generales (el detalle no cambia, ver README)
class JbCompraActualizar(JbModeloEntrada):
    # Número de la factura
    numero_factura: str = Field(min_length=1, max_length=30)
    # Fecha y hora de la compra
    fecha_compra: datetime
    # Proveedor
    id_proveedor: int = Field(gt=0)

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "numero_factura": "FAC-2001-A",  # ejemplo del campo numero_factura
        "fecha_compra": "2026-10-25T09:30:00",  # ejemplo del campo fecha_compra
        "id_proveedor": 6,  # ejemplo del campo id_proveedor
    }]})


# Un ítem de la compra, como lo devuelve la API
class JbItemCompraRespuesta(JbModeloRespuesta):
    # Id del ítem
    id_detalle_compra: int
    # Id del insumo
    id_insumo: int
    # Nombre del insumo (lo agrega la API)
    nombre_insumo: str
    # Cantidad comprada
    cantidad: JbNumero
    # Costo por unidad
    costo_unitario: JbNumero
    # cantidad x costo_unitario (lo calcula la API)
    subtotal: JbNumero


# Compra completa, como la devuelve la API
class JbCompraRespuesta(JbModeloRespuesta):
    # Id de la compra
    id_compra: int
    # Número de la factura
    numero_factura: str
    # Fecha y hora
    fecha_compra: datetime
    # Id del proveedor
    id_proveedor: int
    # Razón social del proveedor (la agrega la API)
    nombre_proveedor: str
    # Usuario que la registró (la API lo toma del token)
    id_usuario: int
    # Suma de los subtotales (la calcula la API)
    total: JbNumero
    # Ítems de la compra
    detalle: list[JbItemCompraRespuesta]
