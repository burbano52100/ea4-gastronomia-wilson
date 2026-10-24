"""Esquemas de recetas o fichas técnicas (RF05): qué insumos y cuánto lleva cada producto."""
# BaseModel: clase base; ConfigDict: configuración del esquema
from pydantic import BaseModel, ConfigDict

# Tipos compartidos: cantidad, base de entrada y número para las respuestas
from app.schemas.jb_tipos import JbCantidad, JbModeloEntrada, JbNumero


# Datos para crear o modificar una línea de receta
class JbRecetaCrear(JbModeloEntrada):
    # Producto al que pertenece la receta
    id_producto: int
    # Insumo que usa
    id_insumo: int
    # Cantidad del insumo por unidad de producto, mayor que 0 con hasta 3 decimales
    cantidad: JbCantidad

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [
        {"id_producto": 3, "id_insumo": 5, "cantidad": 0.010}
    ]})


# Línea de receta como la devuelve la API
class JbRecetaRespuesta(BaseModel):
    # Id de la línea de receta
    id_receta: int
    # Producto
    id_producto: int
    # Insumo
    id_insumo: int
    # Cantidad
    cantidad: JbNumero
