"""Esquemas de productos (RF04), su receta (RF05) y su costo de producción (RF06)."""
# Literal: solo permite ciertos valores fijos
from typing import Literal

# BaseModel: clase base; ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import BaseModel, ConfigDict, Field

# Tipos compartidos: dinero mayor que 0, base de entrada y número para las respuestas
from app.schemas.jb_tipos import JbDineroPositivo, JbModeloEntrada, JbNumero

# Estados de producto permitidos (ENUM del instructivo)
JbEstadoProducto = Literal["DISPONIBLE", "AGOTADO", "INACTIVO"]


# Datos para crear un producto
class JbProductoCrear(JbModeloEntrada):
    # Código interno: de 1 a 20 caracteres
    codigo: str = Field(min_length=1, max_length=20)
    # Nombre: de 2 a 100 caracteres
    nombre: str = Field(min_length=2, max_length=100)
    # Descripción opcional sin límite de tamaño
    descripcion: str | None = None
    # Precio de venta mayor que 0, como CHECK (precio_venta > 0)
    precio_venta: JbDineroPositivo
    # Porción, unidad, vaso...: de 1 a 20 caracteres
    unidad_venta: str = Field(min_length=1, max_length=20)
    # Categoría del producto
    id_categoria: int

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "codigo": "PRD-100",
        "nombre": "Tamal huilense",
        "descripcion": "Tamal de arroz con pollo y cerdo",
        "precio_venta": 9000,
        "unidad_venta": "unidad",
        "id_categoria": 1,
    }]})


# Datos para modificar un producto: los mismos de crear más el estado
class JbProductoActualizar(JbProductoCrear):
    # Estado; si no se envía queda DISPONIBLE
    estado: JbEstadoProducto = "DISPONIBLE"

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "codigo": "PRD-100",
        "nombre": "Tamal huilense",
        "descripcion": "Tamal de arroz con pollo, cerdo y huevo",
        "precio_venta": 9500,
        "unidad_venta": "unidad",
        "id_categoria": 1,
        "estado": "DISPONIBLE",
    }]})


# Producto como lo devuelve la API
class JbProductoRespuesta(BaseModel):
    # Id del producto
    id_producto: int
    # Código interno
    codigo: str
    # Nombre
    nombre: str
    # Descripción, puede ser null
    descripcion: str | None = None
    # Precio de venta
    precio_venta: JbNumero
    # Unidad de venta
    unidad_venta: str
    # Categoría
    id_categoria: int
    # DISPONIBLE, AGOTADO o INACTIVO
    estado: JbEstadoProducto


# Una línea de la receta de un producto, con su costo
class JbLineaRecetaProducto(BaseModel):
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
    # Costo unitario actual del insumo
    costo_unitario: JbNumero
    # cantidad x costo_unitario
    costo: JbNumero


# Respuesta de GET /productos/{id}/receta
class JbRecetaDeProducto(BaseModel):
    # Id del producto
    id_producto: int
    # Nombre del producto
    producto: str
    # Insumos de la receta
    insumos: list[JbLineaRecetaProducto]


# Respuesta de GET /productos/{id}/costo (RF06)
class JbCostoProducto(BaseModel):
    # Id del producto
    id_producto: int
    # Nombre del producto
    producto: str
    # Precio de venta
    precio_venta: JbNumero
    # Suma de cantidad x costo_unitario de toda la receta
    costo_produccion: JbNumero
    # precio_venta - costo_produccion
    margen: JbNumero
    # Margen como porcentaje del precio de venta
    margen_porcentaje: JbNumero
