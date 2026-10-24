"""Esquemas de insumos del inventario (RF07)."""
# date: solo fecha (sin hora)
from datetime import date
# Literal: solo permite ciertos valores fijos
from typing import Literal

# BaseModel: clase base; ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import BaseModel, ConfigDict, Field

# Tipos compartidos: dinero, estado, base de entrada, número para respuestas y stock
from app.schemas.jb_tipos import JbDinero, JbEstado, JbModeloEntrada, JbNumero, JbStock

# Unidades de medida permitidas (ENUM del instructivo)
JbUnidadMedida = Literal["g", "kg", "ml", "l", "lb", "unidad"]


# Datos para crear un insumo
class JbInsumoCrear(JbModeloEntrada):
    # Nombre: de 2 a 100 caracteres
    nombre: str = Field(min_length=2, max_length=100)
    # Unidad de medida, una de la lista
    unidad_medida: JbUnidadMedida
    # Existencias actuales, mayor o igual a 0
    stock_actual: JbStock
    # Nivel mínimo de alerta, mayor o igual a 0
    stock_minimo: JbStock
    # Costo por unidad de medida, mayor o igual a 0
    costo_unitario: JbDinero
    # Fecha de vencimiento opcional
    fecha_vencimiento: date | None = None

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "nombre": "Maíz blanco",
        "unidad_medida": "kg",
        "stock_actual": 20,
        "stock_minimo": 5,
        "costo_unitario": 3000,
        "fecha_vencimiento": "2027-03-31",
    }]})


# Datos para modificar un insumo: los mismos de crear más el estado
class JbInsumoActualizar(JbInsumoCrear):
    # Estado; si no se envía queda ACTIVO
    estado: JbEstado = "ACTIVO"

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "nombre": "Maíz blanco",
        "unidad_medida": "kg",
        "stock_actual": 18.5,
        "stock_minimo": 6,
        "costo_unitario": 3100,
        "fecha_vencimiento": "2027-03-31",
        "estado": "ACTIVO",
    }]})


# Insumo como lo devuelve la API
class JbInsumoRespuesta(BaseModel):
    # Id del insumo
    id_insumo: int
    # Nombre
    nombre: str
    # Unidad de medida
    unidad_medida: JbUnidadMedida
    # Existencias actuales
    stock_actual: JbNumero
    # Nivel mínimo de alerta
    stock_minimo: JbNumero
    # Costo por unidad de medida
    costo_unitario: JbNumero
    # Fecha de vencimiento, puede ser null
    fecha_vencimiento: date | None = None
    # ACTIVO o INACTIVO
    estado: JbEstado
