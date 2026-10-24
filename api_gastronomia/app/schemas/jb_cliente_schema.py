"""Esquemas de clientes (RF09)."""
# Literal: solo permite ciertos valores fijos
from typing import Literal

# BaseModel: clase base; ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import BaseModel, ConfigDict, Field

# Tipos compartidos: correo, documento, estado, base de entrada y teléfono
from app.schemas.jb_tipos import JbCorreo, JbDocumento, JbEstado, JbModeloEntrada, JbTelefono

# Tipos de cliente permitidos (ENUM del instructivo)
JbTipoCliente = Literal["APRENDIZ", "INSTRUCTOR", "FUNCIONARIO", "EXTERNO"]


# Datos para crear un cliente
class JbClienteCrear(JbModeloEntrada):
    # Documento de identidad (5 a 20 letras, números o guiones)
    identificacion: JbDocumento
    # Nombres: de 2 a 80 caracteres
    nombres: str = Field(min_length=2, max_length=80)
    # Apellidos: de 2 a 80 caracteres
    apellidos: str = Field(min_length=2, max_length=80)
    # Teléfono opcional
    telefono: JbTelefono | None = None
    # Correo opcional
    correo: JbCorreo | None = None
    # Tipo de cliente, obligatorio
    tipo_cliente: JbTipoCliente

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "identificacion": "1081555000",
        "nombres": "Santiago",
        "apellidos": "Perdomo Vargas",
        "telefono": "3104445566",
        "correo": "santiago.perdomo@soy.sena.edu.co",
        "tipo_cliente": "APRENDIZ",
    }]})


# Datos para modificar un cliente: los mismos de crear más el estado
class JbClienteActualizar(JbClienteCrear):
    # Estado; si no se envía queda ACTIVO
    estado: JbEstado = "ACTIVO"


# Cliente como lo devuelve la API
class JbClienteRespuesta(BaseModel):
    # Id del cliente
    id_cliente: int
    # Documento
    identificacion: str
    # Nombres
    nombres: str
    # Apellidos
    apellidos: str
    # Teléfono, puede ser null
    telefono: str | None = None
    # Correo, puede ser null
    correo: str | None = None
    # Tipo de cliente
    tipo_cliente: JbTipoCliente
    # ACTIVO o INACTIVO
    estado: JbEstado
