"""Reglas de negocio de proveedores (RF08)."""
# Session: sesión de trabajo con MySQL
from sqlalchemy.orm import Session

# Modelos de las tablas
from app.models.jb_modelos import JbCompra, JbProveedor
# Consultas a compras
from app.repositories import jb_compra_repository
# Consultas a proveedores
from app.repositories import jb_proveedor_repository as jb_repositorio
# Errores y respuestas comunes
from app.services.jb_comun import jb_borrado_fisico, jb_borrado_logico, jb_no_encontrado


# Lista todos los proveedores
def jb_listar(jb_sesion: Session) -> list[JbProveedor]:
    # Pide la lista al repositorio
    return jb_repositorio.jb_listar(jb_sesion)


# Busca un proveedor o responde 404
def jb_obtener(jb_sesion: Session, jb_id: int) -> JbProveedor:
    # Busca por id
    jb_proveedor = jb_repositorio.jb_buscar(jb_sesion, jb_id)
    # Si no existe...
    if jb_proveedor is None:
        # ...responde 404
        raise jb_no_encontrado(f"El proveedor {jb_id}")
    # Devuelve el proveedor
    return jb_proveedor


# Crea un proveedor
def jb_crear(jb_sesion: Session, jb_datos: dict) -> JbProveedor:
    # Arma el objeto con los datos recibidos; todo proveedor nuevo empieza ACTIVO
    jb_proveedor = JbProveedor(**jb_datos, estado="ACTIVO")
    # Inserta; si el NIT ya existe la API responde 409
    jb_repositorio.jb_guardar(jb_sesion, jb_proveedor)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve el proveedor creado
    return jb_proveedor


# Modifica un proveedor
def jb_actualizar(jb_sesion: Session, jb_id: int, jb_datos: dict) -> JbProveedor:
    # Busca el proveedor y lo bloquea mientras se modifica
    jb_proveedor = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_proveedor is None:
        # ...responde 404
        raise jb_no_encontrado(f"El proveedor {jb_id}")
    # Copia cada valor recibido al objeto
    for jb_campo, jb_valor in jb_datos.items():
        # Por ejemplo: jb_proveedor.telefono = "3201112233"
        setattr(jb_proveedor, jb_campo, jb_valor)
    # Envía el cambio (409 si el NIT ya lo usa otro proveedor)
    jb_repositorio.jb_guardar(jb_sesion, jb_proveedor)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve el proveedor modificado
    return jb_proveedor


# Elimina un proveedor o lo deja INACTIVO (RN04)
def jb_eliminar(jb_sesion: Session, jb_id: int) -> dict:
    """RN04: si el proveedor tiene compras pasa a INACTIVO; si no, se borra."""
    # Busca el proveedor y lo bloquea
    jb_proveedor = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_proveedor is None:
        # ...responde 404
        raise jb_no_encontrado(f"El proveedor {jb_id}")
    # Si tiene compras...
    if jb_repositorio.jb_tiene_compras(jb_sesion, jb_id):
        # ...borrado lógico
        jb_proveedor.estado = "INACTIVO"
        # Confirma
        jb_sesion.commit()
        # Responde borrado lógico
        return jb_borrado_logico(f"El proveedor {jb_id}")
    # Sin compras: se borra
    jb_repositorio.jb_borrar(jb_sesion, jb_proveedor)
    # Confirma
    jb_sesion.commit()
    # Responde borrado físico
    return jb_borrado_fisico(f"El proveedor {jb_id}")


# Historial de compras de un proveedor (GET /proveedores/{id}/compras)
def jb_compras(jb_sesion: Session, jb_id: int) -> list[JbCompra]:
    # Comprueba que el proveedor exista (404 si no)
    jb_obtener(jb_sesion, jb_id)
    # Pide sus compras al repositorio
    return jb_compra_repository.jb_por_proveedor(jb_sesion, jb_id)
