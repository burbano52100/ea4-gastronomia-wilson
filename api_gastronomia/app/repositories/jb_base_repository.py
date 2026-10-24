"""Repositorio base: las operaciones del CRUD que se repiten en todas las colecciones.

Cada repositorio hereda de JbRepositorioBase y agrega sus consultas propias.
"""
# jb_db: la base principal; jb_siguiente_id: entrega el próximo id numérico (AUTO_INCREMENT)
from app.database.jb_conexion_mongo import jb_db, jb_siguiente_id


# Clase con el CRUD genérico; los demás repositorios heredan de ella
class JbRepositorioBase:
    # Constructor: recibe la colección, el nombre del id, la base y los campos que nunca se devuelven
    def __init__(self, jb_nombre_coleccion: str, jb_campo_id: str, jb_base=jb_db, jb_campos_ocultos: tuple = ()):
        # Nombre de la colección, por ejemplo "productos"
        self.jb_nombre = jb_nombre_coleccion
        # Nombre con el que se responde el _id, por ejemplo "id_producto"
        self.jb_campo_id = jb_campo_id
        # Base de datos donde está la colección (la principal o la NoSQL)
        self.jb_base = jb_base
        # Objeto de pymongo para trabajar con la colección
        self.jb_coleccion = jb_base[jb_nombre_coleccion]
        # Campos que se esconden, por ejemplo ("password",)
        self.jb_campos_ocultos = jb_campos_ocultos
        # Proyección de MongoDB: {"password": 0} significa "no traer ese campo"; None trae todo
        self.jb_proyeccion = {jb_campo: 0 for jb_campo in jb_campos_ocultos} or None

    # Prepara un documento para la respuesta
    def jb_formatear(self, jb_documento: dict | None) -> dict | None:
        """Cambia el _id de MongoDB por el nombre del campo (id_producto, id_cliente...)."""
        # Solo si se encontró un documento
        if jb_documento is not None:
            # pop saca el _id y se guarda con el nombre del campo, por ejemplo id_producto
            jb_documento[self.jb_campo_id] = jb_documento.pop("_id")
        # Devuelve el documento (o None si no había)
        return jb_documento

    # Lista documentos, con filtro y orden opcionales (SELECT ... WHERE ... ORDER BY)
    def jb_listar(self, jb_filtro: dict | None = None, jb_orden: list | None = None) -> list[dict]:
        # find busca con el filtro (o todos) sin los campos ocultos; sort ordena (por defecto por _id ascendente)
        jb_cursor = self.jb_coleccion.find(jb_filtro or {}, self.jb_proyeccion).sort(jb_orden or [("_id", 1)])
        # Recorre los resultados y formatea cada documento
        return [self.jb_formatear(jb_documento) for jb_documento in jb_cursor]

    # Busca un documento por su id (SELECT ... WHERE id = ?)
    def jb_buscar_por_id(self, jb_id: int) -> dict | None:
        # find_one devuelve el documento o None, y luego se formatea
        return self.jb_formatear(self.jb_coleccion.find_one({"_id": jb_id}, self.jb_proyeccion))

    # Inserta un documento nuevo (INSERT)
    def jb_insertar(self, jb_datos: dict) -> dict:
        # Le asigna el siguiente id numérico de la colección
        jb_datos["_id"] = jb_siguiente_id(self.jb_nombre, self.jb_base)
        # Lo guarda en MongoDB
        self.jb_coleccion.insert_one(jb_datos)
        # Quita los campos ocultos antes de responder (por ejemplo, el hash de la contraseña)
        for jb_campo in self.jb_campos_ocultos:
            # pop con None no falla si el campo no está
            jb_datos.pop(jb_campo, None)
        # Devuelve el documento formateado
        return self.jb_formatear(jb_datos)

    # Modifica un documento (UPDATE)
    def jb_actualizar(self, jb_id: int, jb_datos: dict) -> dict | None:
        # $set cambia solo los campos enviados y deja los demás como estaban
        self.jb_coleccion.update_one({"_id": jb_id}, {"$set": jb_datos})
        # Vuelve a leer el documento para responderlo actualizado
        return self.jb_buscar_por_id(jb_id)

    # Borra un documento (DELETE)
    def jb_eliminar(self, jb_id: int) -> None:
        # Borra el documento con ese id
        self.jb_coleccion.delete_one({"_id": jb_id})

    # Dice si existe al menos un documento que cumpla el filtro
    def jb_existe(self, jb_filtro: dict) -> bool:
        # Cuenta como máximo 1 (más rápido que contar todos) y compara con 0
        return self.jb_coleccion.count_documents(jb_filtro, limit=1) > 0
