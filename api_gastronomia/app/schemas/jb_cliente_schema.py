"""Esquemas de clientes (RF09)."""
# Literal: solo permite ciertos valores fijos
from typing import Literal

# ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import ConfigDict, Field

# Tipos compartidos
from app.schemas.jb_tipos import JbCorreo, JbDocumento, JbEstado, JbModeloEntrada, JbModeloRespuesta, JbTelefono

# Tipos de cliente permitidos (ENUM de la tabla clientes)
JbTipoCliente = Literal["APRENDIZ", "INSTRUCTOR", "FUNCIONARIO", "EXTERNO"]


# Datos para crear un cliente
class JbClienteCrear(JbModeloEntrada):
    # Documento de identidad
    identificacion: JbDocumento
    # Nombres: de 2 a 80 caracteres
    nombres: str = Field(min_length=2, max_length=80)
    # Apellidos: de 2 a 80 caracteres
    apellidos: str = Field(min_length=2, max_length=80)
    # Teléfono (opcional)
    telefono: JbTelefono | None = None
    # Correo (opcional)
    correo: JbCorreo | None = None
    # Tipo de cliente
    tipo_cliente: JbTipoCliente

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "identificacion": "1075400099",  # ejemplo del campo identificacion
        "nombres": "Andrea",  # ejemplo del campo nombres
        "apellidos": "Trujillo Paz",  # ejemplo del campo apellidos
        "telefono": "3209998877",  # ejemplo del campo telefono
        "correo": "andrea.trujillo@soy.sena.edu.co",  # ejemplo del campo correo
        "tipo_cliente": "APRENDIZ",  # ejemplo del campo tipo_cliente
    }]})


# Datos para modificar un cliente: los de crear más el estado
class JbClienteActualizar(JbClienteCrear):
    # ACTIVO o INACTIVO
    estado: JbEstado

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "identificacion": "1075400099",  # ejemplo del campo identificacion
        "nombres": "Andrea",  # ejemplo del campo nombres
        "apellidos": "Trujillo Paz",  # ejemplo del campo apellidos
        "telefono": "3209998877",  # ejemplo del campo telefono
        "correo": "andrea.trujillo@soy.sena.edu.co",  # ejemplo del campo correo
        "tipo_cliente": "APRENDIZ",  # ejemplo del campo tipo_cliente
        "estado": "ACTIVO",  # ejemplo del campo estado
    }]})


# Cliente como lo devuelve la API
class JbClienteRespuesta(JbModeloRespuesta):
    # Id del cliente
    id_cliente: int
    # Documento
    identificacion: str
    # Nombres
    nombres: str
    # Apellidos
    apellidos: str
    # Teléfono (puede ser null)
    telefono: str | None = None
    # Correo (puede ser null)
    correo: str | None = None
    # Tipo de cliente
    tipo_cliente: JbTipoCliente
    # Estado
    estado: JbEstado
