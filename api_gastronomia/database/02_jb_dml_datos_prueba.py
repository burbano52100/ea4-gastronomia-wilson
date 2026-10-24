"""02 - DML: datos iniciales de bd_gastronomia.

Equivale a 02_dml_datos_prueba.sql. Se ejecuta después del 01.
Solo carga los datos que trae el instructivo y el usuario administrador:
- Las categorías que nombra el requerimiento RF03: platos, bebidas, panadería y repostería.
- Un usuario ADMIN, necesario para iniciar sesión y obtener el token (todos los demás datos
  se registran después desde la API).

Uso: python database/02_jb_dml_datos_prueba.py

PARA CAMBIAR EL CORREO O LA CONTRASEÑA DEL ADMINISTRADOR: edite JB_ADMIN (más abajo)
y vuelva a crear las bases (01 --reiniciar, 02, 04 --reiniciar).
"""
# re: expresiones regulares, para revisar el formato del correo
import re
# sys: para detener el script y modificar la ruta de búsqueda de módulos
import sys
# Path: manejo de rutas de archivos
from pathlib import Path

# Agrega la carpeta api_gastronomia a la ruta de Python para poder importar "app" y "database"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Cifra las contraseñas con bcrypt (RN06); noqa: E402 le dice al revisor de estilo que este import va aquí a propósito
from app.core.jb_security import jb_cifrar_password  # noqa: E402
# La base principal
from app.database.jb_conexion_mongo import jb_db  # noqa: E402
# Patrón (expresión regular) que debe cumplir un correo
from app.schemas.jb_tipos import JB_PATRON_CORREO  # noqa: E402
# Deja los contadores de ids en el último id insertado
from database.jb_utilidades_bd import jb_ajustar_contadores  # noqa: E402

# ======================= CAMBIE AQUÍ EL USUARIO ADMINISTRADOR =======================
# Con este correo y esta contraseña se inicia sesión en POST /api/v1/auth/login.
# El correo debe tener formato de correo (nombre@dominio.com) y la contraseña de 6 a 72 caracteres.
JB_ADMIN = {
    # Documento de identidad (de 5 a 20 letras, números o guiones)
    "identificacion": "1000000001",
    # Nombres
    "nombres": "Administrador",
    # Apellidos
    "apellidos": "del Sistema",
    # Correo con el que se inicia sesión
    "correo": "burbano@gastronomia.com",
    # Contraseña en texto plano: el script la guarda cifrada con bcrypt
    "password": "Admin123*",
}
# ====================================================================================

# Categorías que nombra el instructivo en RF03: (id, nombre)
JB_CATEGORIAS = [
    (1, "Platos"),
    (2, "Bebidas"),
    (3, "Panadería"),
    (4, "Repostería"),
]


# Revisa que el administrador cumpla las mismas reglas que exige la API
def jb_validar_admin() -> None:
    # Si el correo no tiene formato de correo...
    if not re.match(JB_PATRON_CORREO, JB_ADMIN["correo"]):
        # ...explica el problema
        print(f"El correo '{JB_ADMIN['correo']}' no es válido: debe tener la forma nombre@dominio.com")
        # ...y detiene el script sin guardar nada
        sys.exit(1)
    # bcrypt solo usa 72 bytes; la API exige mínimo 6 caracteres
    if len(JB_ADMIN["password"]) < 6 or len(JB_ADMIN["password"].encode("utf-8")) > 72:
        # Explica el problema
        print("La contraseña del administrador debe tener de 6 a 72 caracteres")
        # Detiene el script sin guardar nada
        sys.exit(1)


# Función principal: inserta el administrador y las categorías
def jb_main() -> None:
    # Si ya hay usuarios, la base tiene datos: se detiene para no duplicarlos
    if jb_db.usuarios.count_documents({}) > 0:
        # Explica qué hacer
        print("bd_gastronomia ya tiene datos. Ejecute primero: python database/01_jb_ddl_bd_gastronomia.py --reiniciar")
        # Termina el script con código de error 1
        sys.exit(1)
    # Revisa correo y contraseña del administrador
    jb_validar_admin()
    # Mensaje de inicio
    print(f"DML: insertando los datos iniciales en '{jb_db.name}'")

    # Inserta el administrador con id 1
    jb_db.usuarios.insert_one({
        # Id del usuario
        "_id": 1,
        # Documento de identidad
        "identificacion": JB_ADMIN["identificacion"],
        # Nombres
        "nombres": JB_ADMIN["nombres"],
        # Apellidos
        "apellidos": JB_ADMIN["apellidos"],
        # Correo en minúsculas (el login busca el correo en minúsculas)
        "correo": JB_ADMIN["correo"].lower(),
        # Contraseña cifrada con bcrypt (RN06)
        "password": jb_cifrar_password(JB_ADMIN["password"]),
        # Rol de administrador
        "rol": "ADMIN",
        # Usuario activo
        "estado": "ACTIVO",
    })
    # Inserta las categorías del instructivo, todas ACTIVAS y sin descripción
    jb_db.categorias.insert_many([
        # Documento de la categoría
        {"_id": jb_id, "nombre": jb_nombre, "descripcion": None, "estado": "ACTIVO"}
        # Recorre las filas separando el id y el nombre
        for jb_id, jb_nombre in JB_CATEGORIAS
    ])

    # Colecciones que recibieron datos
    jb_colecciones = ["usuarios", "categorias"]
    # Deja cada contador en el último id para que la API siga la numeración (la siguiente categoría será la 5)
    jb_ajustar_contadores(jb_db, jb_colecciones)
    # Muestra cuántos documentos quedaron en cada colección
    for jb_nombre in jb_colecciones:
        # count_documents({}) cuenta todos los documentos de la colección
        print(f"  [OK] {jb_nombre}: {jb_db[jb_nombre].count_documents({})} documentos")
    # Recuerda con qué usuario se inicia sesión
    print(f"  Usuario administrador: {JB_ADMIN['correo'].lower()} (la contraseña es la que está en JB_ADMIN)")
    # Mensaje final
    print("DML terminado.")


# Solo se ejecuta si se corre el archivo directamente (python database/02_jb_dml_datos_prueba.py)
if __name__ == "__main__":
    # Llama a la función principal
    jb_main()
