"""Esquemas de proveedores (RF08)."""
# BaseModel: clase base; ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import BaseModel, ConfigDict, Field

# Tipos compartidos: correo, estado, base de entrada y teléfono
from app.schemas.jb_tipos import JbCorreo, JbEstado, JbModeloEntrada, JbTelefono


# Datos para crear un proveedor
class JbProveedorCrear(JbModeloEntrada):
    # NIT: de 5 a 20 caracteres, solo números y guiones
    nit: str = Field(min_length=5, max_length=20, pattern=r"^[0-9-]+$")
    # Razón social: de 3 a 120 caracteres
    razon_social: str = Field(min_length=3, max_length=120)
    # Teléfono opcional
    telefono: JbTelefono | None = None
    # Correo opcional
    correo: JbCorreo | None = None
    # Dirección opcional, máximo 150 caracteres
    direccion: str | None = Field(default=None, max_length=150)

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "nit": "900555123-4",
        "razon_social": "Panificadora La Gaitana S.A.S.",
        "telefono": "3157778899",
        "correo": "pedidos@lagaitana.co",
        "direccion": "Calle 8 # 4-15, Neiva",
    }]})


# Datos para modificar un proveedor: los mismos de crear más el estado
class JbProveedorActualizar(JbProveedorCrear):
    # Estado; si no se envía queda ACTIVO
    estado: JbEstado = "ACTIVO"


# Proveedor como lo devuelve la API
class JbProveedorRespuesta(BaseModel):
    # Id del proveedor
    id_proveedor: int
    # NIT
    nit: str
    # Razón social
    razon_social: str
    # Teléfono, puede ser null
    telefono: str | None = None
    # Correo, puede ser null
    correo: str | None = None
    # Dirección, puede ser null
    direccion: str | None = None
    # ACTIVO o INACTIVO
    estado: JbEstado
