"""Esquemas de insumos (RF07)."""
# date: solo fecha
from datetime import date
# Decimal: números exactos
from decimal import Decimal
# Literal: solo permite ciertos valores fijos
from typing import Literal

# ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import ConfigDict, Field

# Tipos compartidos
from app.schemas.jb_tipos import JbDinero, JbEstado, JbModeloEntrada, JbModeloRespuesta, JbNumero, JbStock

# Unidades de medida permitidas (ENUM de la tabla insumos)
JbUnidadMedida = Literal["g", "kg", "ml", "l", "lb", "unidad"]


# Datos para crear un insumo
class JbInsumoCrear(JbModeloEntrada):
    # Nombre: de 2 a 100 caracteres
    nombre: str = Field(min_length=2, max_length=100)
    # Unidad de medida
    unidad_medida: JbUnidadMedida
    # Existencias iniciales (0 si no se envía)
    stock_actual: JbStock = Decimal("0")
    # Stock mínimo de alerta (0 si no se envía)
    stock_minimo: JbStock = Decimal("0")
    # Costo por unidad de medida (0 si no se envía; lo actualizan las compras, RN02)
    costo_unitario: JbDinero = Decimal("0")
    # Fecha de vencimiento del lote actual (opcional)
    fecha_vencimiento: date | None = None

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "nombre": "Mora",  # ejemplo del campo nombre
        "unidad_medida": "kg",  # ejemplo del campo unidad_medida
        "stock_actual": 5,  # ejemplo del campo stock_actual
        "stock_minimo": 2,  # ejemplo del campo stock_minimo
        "costo_unitario": 6000,  # ejemplo del campo costo_unitario
        "fecha_vencimiento": "2026-11-10",  # ejemplo del campo fecha_vencimiento
    }]})


# Datos para modificar un insumo. Todo es obligatorio: un PUT reemplaza el registro completo
class JbInsumoActualizar(JbModeloEntrada):
    # Nombre
    nombre: str = Field(min_length=2, max_length=100)
    # Unidad de medida
    unidad_medida: JbUnidadMedida
    # Existencias (ajuste manual de inventario)
    stock_actual: JbStock
    # Stock mínimo
    stock_minimo: JbStock
    # Costo por unidad de medida
    costo_unitario: JbDinero
    # Fecha de vencimiento (null si no tiene)
    fecha_vencimiento: date | None
    # ACTIVO o INACTIVO
    estado: JbEstado

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "nombre": "Mora",  # ejemplo del campo nombre
        "unidad_medida": "kg",  # ejemplo del campo unidad_medida
        "stock_actual": 8,  # ejemplo del campo stock_actual
        "stock_minimo": 2,  # ejemplo del campo stock_minimo
        "costo_unitario": 6000,  # ejemplo del campo costo_unitario
        "fecha_vencimiento": "2026-11-15",  # ejemplo del campo fecha_vencimiento
        "estado": "ACTIVO",  # ejemplo del campo estado
    }]})


# Insumo como lo devuelve la API
class JbInsumoRespuesta(JbModeloRespuesta):
    # Id del insumo
    id_insumo: int
    # Nombre
    nombre: str
    # Unidad de medida
    unidad_medida: JbUnidadMedida
    # Existencias
    stock_actual: JbNumero
    # Stock mínimo
    stock_minimo: JbNumero
    # Costo por unidad de medida
    costo_unitario: JbNumero
    # Fecha de vencimiento (puede ser null)
    fecha_vencimiento: date | None = None
    # Estado
    estado: JbEstado


# Insumo con stock bajo: agrega cuánto falta para llegar al mínimo
class JbInsumoStockBajo(JbInsumoRespuesta):
    # stock_minimo - stock_actual
    faltante: JbNumero


# Insumo por vencer: agrega los días que le quedan
class JbInsumoPorVencer(JbInsumoRespuesta):
    # Días que faltan para la fecha de vencimiento (0 = vence hoy)
    dias_restantes: int
