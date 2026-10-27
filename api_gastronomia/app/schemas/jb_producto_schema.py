"""Esquemas de productos (RF04), de su receta (RF05) y de su costo de producción (RF06)."""
# Literal: solo permite ciertos valores fijos
from typing import Literal

# BaseModel: clase base; ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import BaseModel, ConfigDict, Field

# Tipos compartidos
from app.schemas.jb_tipos import JbDineroPositivo, JbModeloEntrada, JbModeloRespuesta, JbNumero

# Estados de un producto (ENUM de la tabla productos)
JbEstadoProducto = Literal["DISPONIBLE", "AGOTADO", "INACTIVO"]


# Datos para crear un producto
class JbProductoCrear(JbModeloEntrada):
    # Código interno: de 2 a 20 caracteres
    codigo: str = Field(min_length=2, max_length=20)
    # Nombre: de 2 a 100 caracteres
    nombre: str = Field(min_length=2, max_length=100)
    # Descripción opcional
    descripcion: str | None = Field(default=None, max_length=1000)
    # Precio de venta mayor que 0, con máximo 2 decimales
    precio_venta: JbDineroPositivo
    # Porción, unidad, libra, vaso...
    unidad_venta: str = Field(min_length=2, max_length=20)
    # Categoría: debe existir y estar ACTIVA
    id_categoria: int = Field(gt=0)

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "codigo": "BEB-010",  # ejemplo del campo codigo
        "nombre": "Jugo de mora",  # ejemplo del campo nombre
        "descripcion": "Jugo natural de mora en agua",  # ejemplo del campo descripcion
        "precio_venta": 4500,  # ejemplo del campo precio_venta
        "unidad_venta": "vaso",  # ejemplo del campo unidad_venta
        "id_categoria": 2,  # ejemplo del campo id_categoria
    }]})


# Datos para modificar un producto: los de crear más el estado
class JbProductoActualizar(JbProductoCrear):
    # DISPONIBLE, AGOTADO o INACTIVO
    estado: JbEstadoProducto

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "codigo": "BEB-010",  # ejemplo del campo codigo
        "nombre": "Jugo de mora",  # ejemplo del campo nombre
        "descripcion": "Jugo natural de mora en agua",  # ejemplo del campo descripcion
        "precio_venta": 5000,  # ejemplo del campo precio_venta
        "unidad_venta": "vaso",  # ejemplo del campo unidad_venta
        "id_categoria": 2,  # ejemplo del campo id_categoria
        "estado": "DISPONIBLE",  # ejemplo del campo estado
    }]})


# Producto como lo devuelve la API
class JbProductoRespuesta(JbModeloRespuesta):
    # Id del producto
    id_producto: int
    # Código
    codigo: str
    # Nombre
    nombre: str
    # Descripción (puede ser null)
    descripcion: str | None = None
    # Precio de venta
    precio_venta: JbNumero
    # Unidad de venta
    unidad_venta: str
    # Id de la categoría
    id_categoria: int
    # Nombre de la categoría (lo agrega la API)
    nombre_categoria: str | None = None
    # Estado
    estado: JbEstadoProducto


# Una línea de la receta, con su costo
class JbLineaReceta(BaseModel):
    # Id de la línea de receta
    id_receta: int
    # Id del insumo
    id_insumo: int
    # Nombre del insumo
    insumo: str
    # Unidad de medida del insumo
    unidad_medida: str
    # Cantidad del insumo por unidad de producto
    cantidad: JbNumero
    # Costo actual del insumo por unidad de medida
    costo_unitario: JbNumero
    # cantidad x costo_unitario
    costo_linea: JbNumero


# Receta completa de un producto (GET /productos/{id}/receta)
class JbRecetaDeProducto(BaseModel):
    # Id del producto
    id_producto: int
    # Nombre del producto
    producto: str
    # Líneas de la receta (vacía si el producto no tiene receta)
    insumos: list[JbLineaReceta]


# Costo de producción y margen (GET /productos/{id}/costo)
class JbCostoProducto(BaseModel):
    # Id del producto
    id_producto: int
    # Nombre del producto
    producto: str
    # Precio de venta
    precio_venta: JbNumero
    # Suma de (cantidad x costo_unitario) de la receta
    costo_produccion: JbNumero
    # precio_venta - costo_produccion
    margen: JbNumero
    # margen / precio_venta x 100
    margen_porcentaje: JbNumero
    # Líneas de la receta con su costo
    detalle: list[JbLineaReceta]
