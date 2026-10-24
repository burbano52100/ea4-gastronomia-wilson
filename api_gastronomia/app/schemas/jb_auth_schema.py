"""Esquemas de autenticación."""
# BaseModel: clase base de Pydantic; Field: agrega reglas y ejemplos a un campo
from pydantic import BaseModel, Field

# Base de los esquemas de entrada (quita espacios de los textos)
from app.schemas.jb_tipos import JbModeloEntrada


# Datos que se envían para iniciar sesión
class JbLogin(JbModeloEntrada):
    # Correo del usuario, máximo 120 caracteres; examples es el valor que muestra Swagger (el del admin de JB_ADMIN)
    correo: str = Field(max_length=120, examples=["burbano@gastronomia.com"])
    # Contraseña, máximo 72 caracteres (límite de bcrypt); el ejemplo es la del admin de JB_ADMIN
    password: str = Field(max_length=72, examples=["Admin123*"])


# Respuesta del login
class JbToken(BaseModel):
    # El token JWT (nombre estándar de OAuth 2)
    access_token: str
    # Tipo de token: siempre "bearer" (nombre y valor estándar de OAuth 2)
    token_type: str = "bearer"
    # Cuántos minutos dura el token
    expira_en_minutos: int
    # Id del usuario que inició sesión
    id_usuario: int
    # Nombre completo del usuario
    nombre: str
    # Rol del usuario: ADMIN, CAJERO o COCINERO
    rol: str
