"""CRUD mínimo de mesas con FastAPI y el MySQL de Laragon (root sin contraseña, puerto 3306).

Ejecutar (desde la carpeta crud): uvicorn jb_main:jb_app --reload --port 8002
Documentación: http://localhost:8002/docs
"""
# pymysql: conector de Python a MySQL
import pymysql
# FastAPI: la aplicación; HTTPException: responde un error con su código
from fastapi import FastAPI, HTTPException
# BaseModel: valida el JSON que llega; Field: reglas de un campo
from pydantic import BaseModel, Field

# Crea la aplicación
jb_app = FastAPI(title="CRUD de mesas")


# Abre una conexión con el MySQL de Laragon
def jb_conectar():
    # DictCursor: cada fila llega como diccionario {"columna": valor}, listo para responder en JSON
    return pymysql.connect(host="localhost", port=3306, user="root", password="", database="bd_crud",
                           charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor, autocommit=True)


# Ejecuta una consulta y devuelve las filas y el id que MySQL le dio al INSERT
def jb_consultar(jb_sql: str, jb_valores: tuple = ()):
    # with cierra la conexión al terminar, aunque haya error
    with jb_conectar() as jb_conexion, jb_conexion.cursor() as jb_cursor:
        # Se intenta ejecutar la consulta; los %s se llenan con jb_valores (evita inyección SQL)
        try:
            # Ejecuta la consulta
            jb_cursor.execute(jb_sql, jb_valores)
        # El número ya existe (UNIQUE): 1062 es "Duplicate entry"
        except pymysql.err.IntegrityError:
            # Responde 409
            raise HTTPException(409, "Ya existe una mesa con ese número")
        # Devuelve las filas encontradas y el id del último INSERT
        return jb_cursor.fetchall(), jb_cursor.lastrowid


# Datos que se envían para crear o actualizar una mesa (si algo no cumple, FastAPI responde 422)
class JbMesa(BaseModel):
    # Número de la mesa, mayor que 0
    numero: int = Field(gt=0)
    # Personas que caben, de 1 a 20
    capacidad: int = Field(ge=1, le=20)
    # Dónde está, de 1 a 50 letras
    ubicacion: str = Field(min_length=1, max_length=50)


# Busca una mesa o responde 404
def jb_buscar(jb_id: int) -> dict:
    # SELECT por id
    jb_filas, _ = jb_consultar("SELECT * FROM mesas WHERE id_mesa = %s", (jb_id,))
    # Si no hay filas...
    if not jb_filas:
        # ...responde 404
        raise HTTPException(404, f"La mesa {jb_id} no existe")
    # Devuelve la mesa
    return jb_filas[0]


# GET /mesas: lista todas
@jb_app.get("/mesas")
def jb_listar():
    # SELECT de todas, ordenadas por número
    jb_filas, _ = jb_consultar("SELECT * FROM mesas ORDER BY numero")
    # Responde la lista
    return jb_filas


# GET /mesas/{id}: consulta una
@jb_app.get("/mesas/{id_mesa}")
def jb_obtener(id_mesa: int):
    # Responde la mesa (404 si no existe)
    return jb_buscar(id_mesa)


# POST /mesas: crea una (201)
@jb_app.post("/mesas", status_code=201)
def jb_crear(jb_mesa: JbMesa):
    # INSERT con los datos recibidos
    _, jb_id = jb_consultar("INSERT INTO mesas (numero, capacidad, ubicacion) VALUES (%s, %s, %s)",
                            (jb_mesa.numero, jb_mesa.capacidad, jb_mesa.ubicacion))
    # Responde un mensaje y la mesa creada
    return {"mensaje": "Mesa creada", "mesa": jb_buscar(jb_id)}


# PUT /mesas/{id}: actualiza una
@jb_app.put("/mesas/{id_mesa}")
def jb_actualizar(id_mesa: int, jb_mesa: JbMesa):
    # Revisa que exista (404 si no)
    jb_buscar(id_mesa)
    # UPDATE con los datos recibidos
    jb_consultar("UPDATE mesas SET numero = %s, capacidad = %s, ubicacion = %s WHERE id_mesa = %s",
                 (jb_mesa.numero, jb_mesa.capacidad, jb_mesa.ubicacion, id_mesa))
    # Responde un mensaje y la mesa como quedó
    return {"mensaje": "Mesa actualizada", "mesa": jb_buscar(id_mesa)}


# DELETE /mesas/{id}: elimina una
@jb_app.delete("/mesas/{id_mesa}")
def jb_eliminar(id_mesa: int):
    # Revisa que exista (404 si no)
    jb_buscar(id_mesa)
    # DELETE por id
    jb_consultar("DELETE FROM mesas WHERE id_mesa = %s", (id_mesa,))
    # Responde un mensaje
    return {"mensaje": f"Mesa {id_mesa} eliminada"}
