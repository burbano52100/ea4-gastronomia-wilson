"""Reglas de negocio de clientes (RF09)."""
# Session: sesión de trabajo con MySQL
from sqlalchemy.orm import Session

# Modelos de las tablas
from app.models.jb_modelos import JbCliente, JbPedido
# Consultas a pedidos
from app.repositories import jb_pedido_repository
# Consultas a clientes
from app.repositories import jb_cliente_repository as jb_repositorio
# Errores y respuestas comunes
from app.services.jb_comun import jb_borrado_fisico, jb_borrado_logico, jb_no_encontrado


# Lista todos los clientes
def jb_listar(jb_sesion: Session) -> list[JbCliente]:
    # Pide la lista al repositorio
    return jb_repositorio.jb_listar(jb_sesion)


# Busca un cliente o responde 404
def jb_obtener(jb_sesion: Session, jb_id: int) -> JbCliente:
    # Busca por id
    jb_cliente = jb_repositorio.jb_buscar(jb_sesion, jb_id)
    # Si no existe...
    if jb_cliente is None:
        # ...responde 404
        raise jb_no_encontrado(f"El cliente {jb_id}")
    # Devuelve el cliente
    return jb_cliente


# Crea un cliente
def jb_crear(jb_sesion: Session, jb_datos: dict) -> JbCliente:
    # Arma el objeto con los datos recibidos; todo cliente nuevo empieza ACTIVO
    jb_cliente = JbCliente(**jb_datos, estado="ACTIVO")
    # Inserta; si el documento ya existe la API responde 409
    jb_repositorio.jb_guardar(jb_sesion, jb_cliente)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve el cliente creado
    return jb_cliente


# Modifica un cliente
def jb_actualizar(jb_sesion: Session, jb_id: int, jb_datos: dict) -> JbCliente:
    # Busca el cliente y lo bloquea mientras se modifica
    jb_cliente = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_cliente is None:
        # ...responde 404
        raise jb_no_encontrado(f"El cliente {jb_id}")
    # Copia cada valor recibido al objeto
    for jb_campo, jb_valor in jb_datos.items():
        # Por ejemplo: jb_cliente.tipo_cliente = "EXTERNO"
        setattr(jb_cliente, jb_campo, jb_valor)
    # Envía el cambio (409 si el documento ya lo usa otro cliente)
    jb_repositorio.jb_guardar(jb_sesion, jb_cliente)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve el cliente modificado
    return jb_cliente


# Elimina un cliente o lo deja INACTIVO (RN04)
def jb_eliminar(jb_sesion: Session, jb_id: int) -> dict:
    """RN04: si el cliente tiene pedidos pasa a INACTIVO; si no, se borra."""
    # Busca el cliente y lo bloquea
    jb_cliente = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_cliente is None:
        # ...responde 404
        raise jb_no_encontrado(f"El cliente {jb_id}")
    # Si tiene pedidos...
    if jb_repositorio.jb_tiene_pedidos(jb_sesion, jb_id):
        # ...borrado lógico
        jb_cliente.estado = "INACTIVO"
        # Confirma
        jb_sesion.commit()
        # Responde borrado lógico
        return jb_borrado_logico(f"El cliente {jb_id}")
    # Sin pedidos: se borra
    jb_repositorio.jb_borrar(jb_sesion, jb_cliente)
    # Confirma
    jb_sesion.commit()
    # Responde borrado físico
    return jb_borrado_fisico(f"El cliente {jb_id}")


# Historial de pedidos de un cliente (GET /clientes/{id}/pedidos)
def jb_pedidos(jb_sesion: Session, jb_id: int) -> list[JbPedido]:
    # Comprueba que el cliente exista (404 si no)
    jb_obtener(jb_sesion, jb_id)
    # Pide sus pedidos al repositorio
    return jb_pedido_repository.jb_por_cliente(jb_sesion, jb_id)
