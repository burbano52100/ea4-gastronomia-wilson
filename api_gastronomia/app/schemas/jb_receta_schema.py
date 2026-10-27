"""Esquemas de recetas o fichas técnicas (RF05)."""
# ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import ConfigDict, Field

# Tipos compartidos
from app.schemas.jb_tipos import JbCantidad, JbModeloEntrada, JbModeloRespuesta, JbNumero


# Datos para crear una línea de receta: "este producto usa esta cantidad de este insumo"
class JbRecetaCrear(JbModeloEntrada):
    # Producto: debe existir
    id_producto: int = Field(gt=0)
    # Insumo: debe existir y estar ACTIVO
    id_insumo: int = Field(gt=0)
    # Cantidad por unidad de producto: mayor que 0, hasta 3 decimales
    cantidad: JbCantidad

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{"id_producto": 15, "id_insumo": 8, "cantidad": 0.030}]})


# Datos para modificar una línea de receta (los mismos campos)
class JbRecetaActualizar(JbRecetaCrear):
    """Mismos campos que JbRecetaCrear: un PUT reemplaza la línea completa."""


# Línea de receta como la devuelve la API
class JbRecetaRespuesta(JbModeloRespuesta):
    # Id de la línea
    id_receta: int
    # Id del producto
    id_producto: int
    # Nombre del producto (lo agrega la API)
    nombre_producto: str
    # Id del insumo
    id_insumo: int
    # Nombre del insumo (lo agrega la API)
    nombre_insumo: str
    # Unidad de medida del insumo
    unidad_medida: str
    # Cantidad por unidad de producto
    cantidad: JbNumero
