"""Esquemas de usuarios (RF02). La contraseña entra, pero nunca sale en una respuesta (RN06)."""
# Annotated: agrega reglas a un tipo; Literal: solo permite ciertos valores fijos
from typing import Annotated, Literal

# AfterValidator: validación propia después de las reglas de Field; ConfigDict: configuración; Field: reglas
from pydantic import AfterValidator, ConfigDict, Field

# Tipos compartidos
from app.schemas.jb_tipos import JbCorreo, JbDocumento, JbEstado, JbModeloEntrada, JbModeloRespuesta

# Roles permitidos (ENUM de la tabla usuarios)
JbRol = Literal["ADMIN", "CAJERO", "COCINERO"]


# Validación propia de las contraseñas nuevas
def jb_validar_password(jb_valor: str) -> str:
    """Una contraseña nueva debe tener al menos una letra y un número, y máximo 72 bytes (límite de bcrypt)."""
    # bcrypt solo usa los primeros 72 bytes; una tilde ocupa 2 bytes, por eso se cuentan bytes y no letras
    if len(jb_valor.encode("utf-8")) > 72:
        # El esquema responde 422 con este mensaje
        raise ValueError("Debe tener máximo 72 bytes (bcrypt no usa más)")
    # Revisa que tenga al menos una letra
    if not any(jb_caracter.isalpha() for jb_caracter in jb_valor):
        # El esquema responde 422 con este mensaje
        raise ValueError("Debe tener al menos una letra")
    # Revisa que tenga al menos un número
    if not any(jb_caracter.isdigit() for jb_caracter in jb_valor):
        # El esquema responde 422 con este mensaje
        raise ValueError("Debe tener al menos un número")
    # Si cumple todo, se devuelve igual
    return jb_valor


# Contraseña nueva: de 8 a 72 caracteres, con letra y número
JbPassword = Annotated[str, Field(min_length=8, max_length=72), AfterValidator(jb_validar_password)]


# Datos para crear un usuario (POST /usuarios y POST /auth/registro)
class JbUsuarioCrear(JbModeloEntrada):
    # Documento de identidad
    identificacion: JbDocumento
    # Nombres: de 2 a 80 caracteres
    nombres: str = Field(min_length=2, max_length=80)
    # Apellidos: de 2 a 80 caracteres
    apellidos: str = Field(min_length=2, max_length=80)
    # Correo para iniciar sesión
    correo: JbCorreo
    # Contraseña en texto plano: la API la cifra con bcrypt antes de guardarla (RN06)
    password: JbPassword
    # Rol del usuario
    rol: JbRol

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "identificacion": "1075999001",  # ejemplo del campo identificacion
        "nombres": "Luisa Fernanda",  # ejemplo del campo nombres
        "apellidos": "Ortega Ruiz",  # ejemplo del campo apellidos
        "correo": "luisa.ortega@gastronomia.com",  # ejemplo del campo correo
        "password": "Cajera2026",  # ejemplo del campo password
        "rol": "CAJERO",  # ejemplo del campo rol
    }]})


# Datos para modificar un usuario (PUT /usuarios/{id})
class JbUsuarioActualizar(JbModeloEntrada):
    # Documento de identidad
    identificacion: JbDocumento
    # Nombres
    nombres: str = Field(min_length=2, max_length=80)
    # Apellidos
    apellidos: str = Field(min_length=2, max_length=80)
    # Correo
    correo: JbCorreo
    # Rol
    rol: JbRol
    # ACTIVO o INACTIVO
    estado: JbEstado
    # Contraseña nueva (opcional): si no se envía, se conserva la actual
    password: JbPassword | None = None

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "identificacion": "1075999001",  # ejemplo del campo identificacion
        "nombres": "Luisa Fernanda",  # ejemplo del campo nombres
        "apellidos": "Ortega Ruiz",  # ejemplo del campo apellidos
        "correo": "luisa.ortega@gastronomia.com",  # ejemplo del campo correo
        "rol": "CAJERO",  # ejemplo del campo rol
        "estado": "ACTIVO",  # ejemplo del campo estado
    }]})


# Usuario como lo devuelve la API: sin el campo password (RN06)
class JbUsuarioRespuesta(JbModeloRespuesta):
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
    # Estado
    estado: JbEstado
