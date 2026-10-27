"""Reglas de negocio de categorías (RF03)."""
# Session: sesión de trabajo con MySQL
from sqlalchemy.orm import Session

# Modelo de la tabla categorias
from app.models.jb_modelos import JbCategoria
# Consultas a la tabla categorias
from app.repositories import jb_categoria_repository as jb_repositorio
# Errores y respuestas comunes
from app.services.jb_comun import jb_borrado_fisico, jb_borrado_logico, jb_no_encontrado


# Lista todas las categorías
def jb_listar(jb_sesion: Session) -> list[JbCategoria]:
    # Pide la lista al repositorio
    return jb_repositorio.jb_listar(jb_sesion)


# Busca una categoría o responde 404
def jb_obtener(jb_sesion: Session, jb_id: int) -> JbCategoria:
    # Busca por id
    jb_categoria = jb_repositorio.jb_buscar(jb_sesion, jb_id)
    # Si no existe...
    if jb_categoria is None:
        # ...responde 404
        raise jb_no_encontrado(f"La categoría {jb_id}")
    # Devuelve la categoría
    return jb_categoria


# Crea una categoría
def jb_crear(jb_sesion: Session, jb_datos: dict) -> JbCategoria:
    # Arma el objeto: nombre y descripción del cuerpo, estado ACTIVO
    jb_categoria = JbCategoria(**jb_datos, estado="ACTIVO")
    # Inserta; si el nombre ya existe la API responde 409
    jb_repositorio.jb_guardar(jb_sesion, jb_categoria)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve la categoría creada
    return jb_categoria


# Modifica una categoría
def jb_actualizar(jb_sesion: Session, jb_id: int, jb_datos: dict) -> JbCategoria:
    # Busca la categoría y la bloquea mientras se modifica
    jb_categoria = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_categoria is None:
        # ...responde 404
        raise jb_no_encontrado(f"La categoría {jb_id}")
    # Copia cada valor recibido al objeto
    for jb_campo, jb_valor in jb_datos.items():
        # Por ejemplo: jb_categoria.nombre = "Bebidas frías"
        setattr(jb_categoria, jb_campo, jb_valor)
    # Envía el cambio (409 si el nombre ya lo usa otra categoría)
    jb_repositorio.jb_guardar(jb_sesion, jb_categoria)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve la categoría modificada
    return jb_categoria


# Elimina una categoría o la deja INACTIVA
def jb_eliminar(jb_sesion: Session, jb_id: int) -> dict:
    """Si la categoría tiene productos queda INACTIVA (como RN04); si no, se borra."""
    # Busca la categoría y la bloquea
    jb_categoria = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_categoria is None:
        # ...responde 404
        raise jb_no_encontrado(f"La categoría {jb_id}")
    # Si tiene productos...
    if jb_repositorio.jb_tiene_productos(jb_sesion, jb_id):
        # ...borrado lógico
        jb_categoria.estado = "INACTIVO"
        # Confirma
        jb_sesion.commit()
        # Responde borrado lógico
        return jb_borrado_logico(f"La categoría {jb_id}")
    # Sin productos: se borra
    jb_repositorio.jb_borrar(jb_sesion, jb_categoria)
    # Confirma
    jb_sesion.commit()
    # Responde borrado físico
    return jb_borrado_fisico(f"La categoría {jb_id}")
