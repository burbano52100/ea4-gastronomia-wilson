"""Tipos y modelos compartidos por todos los esquemas."""
# Decimal: números exactos para dinero y cantidades
from decimal import Decimal
# Annotated: agrega reglas a un tipo; Literal: solo permite ciertos valores fijos
from typing import Annotated, Literal

# Herramientas de Pydantic para validar y convertir datos
from pydantic import AfterValidator, BaseModel, ConfigDict, Field, PlainSerializer

# Expresión regular de un correo: texto, @, texto, punto, texto (sin espacios)
JB_PATRON_CORREO = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
# Expresión regular de un teléfono: de 7 a 20 caracteres entre números, +, ( ), espacios y guiones
JB_PATRON_TELEFONO = r"^[0-9+()\s-]{7,20}$"
# Expresión regular de un documento: de 5 a 20 letras, números o guiones
JB_PATRON_DOCUMENTO = r"^[0-9A-Za-z-]{5,20}$"


# Función que pasa un texto a minúsculas (se usa para los correos)
def jb_minusculas(jb_valor: str) -> str:
    # Devuelve el texto en minúsculas, así "Ana@Correo.com" y "ana@correo.com" son el mismo correo
    return jb_valor.lower()


# Los Decimal se responden como número en el JSON (Pydantic por defecto los enviaría como texto).
JbNumero = Annotated[Decimal, PlainSerializer(float, return_type=float, when_used="json")]

# Tipos para los datos que ENTRAN a la API (equivalen a DECIMAL(p,s) + CHECK en SQL).
# Dinero mayor que 0, máximo 10 dígitos y 2 decimales (por ejemplo, un precio)
JbDineroPositivo = Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=2)]
# Dinero mayor o igual a 0, máximo 10 dígitos y 2 decimales (por ejemplo, un costo)
JbDinero = Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=2)]
# Cantidad mayor que 0 con hasta 3 decimales (por ejemplo, 0.250 kg)
JbCantidad = Annotated[Decimal, Field(gt=0, max_digits=10, decimal_places=3)]
# Existencias mayores o iguales a 0 con hasta 3 decimales
JbStock = Annotated[Decimal, Field(ge=0, max_digits=10, decimal_places=3)]

# Correo: máximo 120 caracteres, con formato de correo, y se guarda en minúsculas
JbCorreo = Annotated[str, Field(max_length=120, pattern=JB_PATRON_CORREO), AfterValidator(jb_minusculas)]
# Teléfono: máximo 20 caracteres con el patrón de teléfono
JbTelefono = Annotated[str, Field(max_length=20, pattern=JB_PATRON_TELEFONO)]
# Documento: de 5 a 20 caracteres con el patrón de documento
JbDocumento = Annotated[str, Field(min_length=5, max_length=20, pattern=JB_PATRON_DOCUMENTO)]

# Estado: solo ACTIVO o INACTIVO
JbEstado = Literal["ACTIVO", "INACTIVO"]


# Clase base de los esquemas que reciben datos (Crear y Actualizar)
class JbModeloEntrada(BaseModel):
    """Base de los esquemas que reciben datos: quita espacios al inicio y al final de los textos."""

    # str_strip_whitespace: convierte "  Ana  " en "Ana" antes de validar
    model_config = ConfigDict(str_strip_whitespace=True)


# Forma de las respuestas de error: {"detalle": "mensaje"}
class JbError(BaseModel):
    # Mensaje del error
    detalle: str


# Forma de cada error de un 422: dónde está, qué campo y qué pasó
class JbErrorCampo(BaseModel):
    # Parte de la petición: cuerpo, ruta, parámetro de consulta...
    ubicacion: str
    # Nombre del campo con el error, por ejemplo detalle[0].cantidad
    campo: str
    # Explicación del error en español
    mensaje: str


# Forma de la respuesta 422 (datos inválidos)
class JbErrorValidacion(BaseModel):
    # Mensaje general
    detalle: str
    # Lista con cada error encontrado
    errores: list[JbErrorCampo]

    # Ejemplo que muestra Swagger para la respuesta 422
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "detalle": "Los datos enviados no son válidos",
        "errores": [{"ubicacion": "cuerpo", "campo": "precio_venta", "mensaje": "Debe ser mayor que 0"}],
    }]})


# Forma de la respuesta de los DELETE
class JbResultadoEliminacion(BaseModel):
    # Mensaje de lo que pasó
    mensaje: str
    # FISICO: se borró de la base; LOGICO: quedó INACTIVO o ANULADO (RN04)
    tipo_borrado: Literal["FISICO", "LOGICO"]
