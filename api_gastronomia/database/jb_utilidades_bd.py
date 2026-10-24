"""Funciones compartidas por los scripts de base de datos."""
# sys: para detener el script
import sys
# datetime: para poner la fecha y hora en el nombre del respaldo
from datetime import datetime

# Database: el tipo de una base de datos de pymongo (se usa en las anotaciones de tipo)
from pymongo.database import Database


# Revisa si la base ya tiene colecciones y decide qué hacer
def jb_preparar_base(jb_base: Database, jb_reiniciar: bool) -> None:
    """Si la base ya tiene colecciones: sin --reiniciar se detiene; con --reiniciar las respalda y las borra."""
    # Nombres de las colecciones que ya existen (sin las internas de MongoDB, que empiezan por "system.")
    jb_existentes = sorted(jb_nombre for jb_nombre in jb_base.list_collection_names() if not jb_nombre.startswith("system."))
    # Si la base está vacía, no hay nada que hacer
    if not jb_existentes:
        # Sale de la función
        return
    # Si tiene colecciones y NO se pidió --reiniciar...
    if not jb_reiniciar:
        # ...avisa qué colecciones hay
        print(f"La base '{jb_base.name}' ya tiene colecciones: {', '.join(jb_existentes)}.")
        # ...explica cómo reemplazarla
        print("Para reemplazarla ejecute el script con --reiniciar (antes se guarda un respaldo).")
        # ...y detiene el script con código de error 1, sin borrar nada
        sys.exit(1)
    # Nombre del respaldo: la base + _respaldo_ + fecha y hora, por ejemplo bd_gastronomia_respaldo_20261024_093000
    jb_respaldo = f"{jb_base.name}_respaldo_{datetime.now():%Y%m%d_%H%M%S}"
    # Recorre cada colección existente
    for jb_nombre in jb_existentes:
        # $out copia todos los documentos de la colección a la base de respaldo
        jb_base[jb_nombre].aggregate([{"$out": {"db": jb_respaldo, "coll": jb_nombre}}])
        # Borra la colección original
        jb_base.drop_collection(jb_nombre)
    # Avisa dónde quedó el respaldo
    print(f"  Respaldo de {len(jb_existentes)} colecciones guardado en la base '{jb_respaldo}'.")


# Crea las colecciones con su validación e índices
def jb_crear_colecciones(jb_base: Database, jb_modelos: dict) -> None:
    """Crea cada colección con su validación $jsonSchema (equivale a CREATE TABLE) y sus índices."""
    # Recorre cada modelo: nombre de la colección y su definición
    for jb_nombre, jb_modelo in jb_modelos.items():
        # Crea la colección
        jb_base.create_collection(
            # Nombre de la colección
            jb_nombre,
            # Reglas $jsonSchema que debe cumplir cada documento
            validator={"$jsonSchema": jb_modelo["esquema"]},
            # strict: la validación se aplica a todo lo que se inserte o modifique
            validationLevel="strict",
            # error: si un documento no cumple, MongoDB lo rechaza
            validationAction="error",
        )
        # Recorre los índices del modelo: campos y si es único
        for jb_campos, jb_unico in jb_modelo["indices"]:
            # Crea el índice (1 = orden ascendente); unique=True equivale a UNIQUE en SQL
            jb_base[jb_nombre].create_index([(jb_campo, 1) for jb_campo in jb_campos], unique=jb_unico)
        # Muestra que la colección quedó creada
        print(f"  [OK] {jb_nombre}: validación $jsonSchema + {len(jb_modelo['indices'])} índice(s)")
    # Crea la colección de contadores de ids
    jb_base.create_collection("contadores")
    # Muestra que quedó creada
    print("  [OK] contadores: secuencias de ids (equivale a AUTO_INCREMENT)")


# Ajusta los contadores después de insertar datos con ids fijos
def jb_ajustar_contadores(jb_base: Database, jb_colecciones: list[str]) -> None:
    """Deja cada contador en el último _id usado para que la API continúe la numeración."""
    # Recorre cada colección
    for jb_nombre in jb_colecciones:
        # Busca el documento con el _id más alto (orden descendente) y trae solo el _id
        jb_ultimo = jb_base[jb_nombre].find_one(sort=[("_id", -1)], projection={"_id": 1})
        # Guarda ese número en el contador de la colección
        jb_base.contadores.update_one(
            # El contador de esta colección; $set pone el último id (o 0 si la colección está vacía)
            {"_id": jb_nombre}, {"$set": {"valor": jb_ultimo["_id"] if jb_ultimo else 0}}, upsert=True
        )
