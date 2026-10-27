"""Esquemas de autenticación (RF01)."""
# BaseModel: clase base; ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import BaseModel, ConfigDict, Field

# Tipos compartidos
from app.schemas.jb_tipos import JbCorreo, JbModeloEntrada
# Forma del usuario en las respuestas (sin contraseña)
from app.schemas.jb_usuario_schema import JbUsuarioRespuesta


# Datos que se envían para iniciar sesión (POST /auth/login)
class JbLogin(JbModeloEntrada):
    # Correo del usuario
    correo: JbCorreo
    # Contraseña tal como la escribe el usuario
    password: str = Field(min_length=1, max_length=72)

    # Ejemplo que muestra Swagger al pulsar "Try it out" (administrador de los datos de prueba)
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "correo": "burbano@gastronomia.com",  # ejemplo del campo correo
        "password": "Admin123*",  # ejemplo del campo password
    }]})


# Respuesta del login
class JbToken(BaseModel):
    # Token JWT que se envía en el encabezado Authorization: Bearer <token>
    access_token: str
    # Tipo de token (nombre estándar de OAuth 2)
    token_type: str = "bearer"
    # Minutos que dura el token
    expira_en_minutos: int
    # Datos del usuario que inició sesión
    usuario: JbUsuarioRespuesta
