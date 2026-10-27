"""Esquemas de categorías (RF03)."""
# ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import ConfigDict, Field

# Tipos compartidos
from app.schemas.jb_tipos import JbEstado, JbModeloEntrada, JbModeloRespuesta


# Datos para crear una categoría
class JbCategoriaCrear(JbModeloEntrada):
    # Nombre: de 2 a 60 caracteres
    nombre: str = Field(min_length=2, max_length=60)
    # Descripción opcional: máximo 200 caracteres
    descripcion: str | None = Field(default=None, max_length=200)

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "nombre": "Bebidas frías",  # ejemplo del campo nombre
        "descripcion": "Jugos, limonadas y malteadas",  # ejemplo del campo descripcion
    }]})


# Datos para modificar una categoría: los de crear más el estado
class JbCategoriaActualizar(JbCategoriaCrear):
    # ACTIVO o INACTIVO
    estado: JbEstado

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "nombre": "Bebidas frías",  # ejemplo del campo nombre
        "descripcion": "Jugos, limonadas y malteadas",  # ejemplo del campo descripcion
        "estado": "ACTIVO",  # ejemplo del campo estado
    }]})


# Categoría como la devuelve la API
class JbCategoriaRespuesta(JbModeloRespuesta):
    # Id de la categoría
    id_categoria: int
    # Nombre
    nombre: str
    # Descripción (puede ser null)
    descripcion: str | None = None
    # Estado
    estado: JbEstado
