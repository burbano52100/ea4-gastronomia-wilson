"""Esquemas de categorías de productos (RF03)."""
# BaseModel: clase base; ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import BaseModel, ConfigDict, Field

# JbEstado: ACTIVO o INACTIVO; JbModeloEntrada: base de los esquemas de entrada
from app.schemas.jb_tipos import JbEstado, JbModeloEntrada


# Datos para crear una categoría
class JbCategoriaCrear(JbModeloEntrada):
    # Nombre: de 2 a 60 caracteres
    nombre: str = Field(min_length=2, max_length=60)
    # Descripción opcional, máximo 200 caracteres
    descripcion: str | None = Field(default=None, max_length=200)

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [
        {"nombre": "Comida típica", "descripcion": "Platos tradicionales del Huila"}
    ]})


# Datos para modificar una categoría: los mismos de crear más el estado
class JbCategoriaActualizar(JbCategoriaCrear):
    # Estado; si no se envía queda ACTIVO
    estado: JbEstado = "ACTIVO"

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [
        {"nombre": "Comida típica", "descripcion": "Platos tradicionales del Huila y el Tolima", "estado": "ACTIVO"}
    ]})


# Categoría como la devuelve la API
class JbCategoriaRespuesta(BaseModel):
    # Id de la categoría
    id_categoria: int
    # Nombre
    nombre: str
    # Descripción, puede ser null
    descripcion: str | None = None
    # ACTIVO o INACTIVO
    estado: JbEstado
