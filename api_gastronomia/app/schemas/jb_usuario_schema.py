"""Esquemas de usuarios del sistema (RF02). La contraseña nunca está en la respuesta (RN06)."""
# Annotated: agrega reglas a un tipo; Literal: solo permite ciertos valores fijos
from typing import Annotated, Literal

# Herramientas de Pydantic: validador propio, clase base, configuración y reglas de campo
from pydantic import AfterValidator, BaseModel, ConfigDict, Field

# Tipos compartidos: correo, documento, estado y base de entrada
from app.schemas.jb_tipos import JbCorreo, JbDocumento, JbEstado, JbModeloEntrada

# Roles permitidos (ENUM del instructivo)
JbRol = Literal["ADMIN", "CAJERO", "COCINERO"]


# Validación propia de la contraseña
def jb_validar_password(jb_valor: str) -> str:
    # bcrypt solo usa los primeros 72 bytes; una "ñ" o una tilde ocupan 2 bytes
    if len(jb_valor.encode("utf-8")) > 72:
        # Este mensaje sale tal cual en el error 422
        raise ValueError("La contraseña no puede superar 72 bytes (límite de bcrypt)")
    # Si está bien, se devuelve sin cambios
    return jb_valor


# Contraseña: de 6 a 72 caracteres y además la validación de bytes
JbPassword = Annotated[str, Field(min_length=6, max_length=72), AfterValidator(jb_validar_password)]


# Datos para crear un usuario
class JbUsuarioCrear(JbModeloEntrada):
    # Documento de identidad
    identificacion: JbDocumento
    # Nombres: de 2 a 80 caracteres
    nombres: str = Field(min_length=2, max_length=80)
    # Apellidos: de 2 a 80 caracteres
    apellidos: str = Field(min_length=2, max_length=80)
    # Correo, que será el usuario de acceso
    correo: JbCorreo
    # Contraseña en texto plano (la API la cifra antes de guardarla)
    password: JbPassword
    # Rol
    rol: JbRol

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "identificacion": "1075209999",
        "nombres": "Valeria",
        "apellidos": "Cuéllar Ríos",
        "correo": "valeria.cuellar@gastronomia.com",
        "password": "Clave123*",
        "rol": "CAJERO",
    }]})


# Datos para modificar un usuario (la contraseña es opcional)
class JbUsuarioActualizar(JbModeloEntrada):
    # Documento de identidad
    identificacion: JbDocumento
    # Nombres: de 2 a 80 caracteres
    nombres: str = Field(min_length=2, max_length=80)
    # Apellidos: de 2 a 80 caracteres
    apellidos: str = Field(min_length=2, max_length=80)
    # Correo
    correo: JbCorreo
    # Contraseña nueva; si no se envía, se conserva la anterior
    password: JbPassword | None = Field(default=None, description="Opcional: envíela solo si quiere cambiarla")
    # Rol
    rol: JbRol
    # Estado; si no se envía queda ACTIVO
    estado: JbEstado = "ACTIVO"

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "identificacion": "1075209999",
        "nombres": "Valeria",
        "apellidos": "Cuéllar Ríos",
        "correo": "valeria.cuellar@gastronomia.com",
        "rol": "COCINERO",
        "estado": "ACTIVO",
    }]})


# Usuario como lo devuelve la API: no tiene password (RN06)
class JbUsuarioRespuesta(BaseModel):
    # Id del usuario
    id_usuario: int
    # Documento
    identificacion: str
    # Nombres
    nombres: str
    # Apellidos
    apellidos: str
    # Correo
    correo: str
    # Rol
    rol: JbRol
    # ACTIVO o INACTIVO
    estado: JbEstado
