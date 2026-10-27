"""Esquemas de proveedores (RF08)."""
# ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import ConfigDict, Field

# Tipos compartidos
from app.schemas.jb_tipos import JbCorreo, JbEstado, JbModeloEntrada, JbModeloRespuesta, JbNit, JbTelefono


# Datos para crear un proveedor
class JbProveedorCrear(JbModeloEntrada):
    # NIT o documento
    nit: JbNit
    # Nombre o razón social: de 2 a 120 caracteres
    razon_social: str = Field(min_length=2, max_length=120)
    # Teléfono (opcional)
    telefono: JbTelefono | None = None
    # Correo (opcional)
    correo: JbCorreo | None = None
    # Dirección (opcional)
    direccion: str | None = Field(default=None, max_length=150)

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "nit": "901555666-7",  # ejemplo del campo nit
        "razon_social": "Frutas del Macizo S.A.S.",  # ejemplo del campo razon_social
        "telefono": "3201112233",  # ejemplo del campo telefono
        "correo": "ventas@frutasdelmacizo.com",  # ejemplo del campo correo
        "direccion": "Carrera 7 # 4-10, Pitalito",  # ejemplo del campo direccion
    }]})


# Datos para modificar un proveedor: los de crear más el estado
class JbProveedorActualizar(JbProveedorCrear):
    # ACTIVO o INACTIVO
    estado: JbEstado

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "nit": "901555666-7",  # ejemplo del campo nit
        "razon_social": "Frutas del Macizo S.A.S.",  # ejemplo del campo razon_social
        "telefono": "3201112233",  # ejemplo del campo telefono
        "correo": "ventas@frutasdelmacizo.com",  # ejemplo del campo correo
        "direccion": "Carrera 7 # 4-10, Pitalito",  # ejemplo del campo direccion
        "estado": "ACTIVO",  # ejemplo del campo estado
    }]})


# Proveedor como lo devuelve la API
class JbProveedorRespuesta(JbModeloRespuesta):
    # Id del proveedor
    id_proveedor: int
    # NIT
    nit: str
    # Razón social
    razon_social: str
    # Teléfono (puede ser null)
    telefono: str | None = None
    # Correo (puede ser null)
    correo: str | None = None
    # Dirección (puede ser null)
    direccion: str | None = None
    # Estado
    estado: JbEstado
