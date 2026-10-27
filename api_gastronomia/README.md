# API REST - Unidad Productiva de Gastronomía (CGDSS)

Prototipo de API REST con Python (FastAPI) para la Unidad Productiva de Gastronomía del Centro de Gestión y Desarrollo Sostenible Surcolombiano. Evidencia EA4, ficha 3312744 (Análisis y Desarrollo de Software).

La API hace CRUD de usuarios, categorías, productos, insumos, recetas, proveedores, compras, clientes, pedidos y calificaciones. Guarda la información principal en **MySQL** (base `bd_gastronomia`) y las calificaciones de los clientes en **MongoDB** (base `bd_gastronomia_nosql`). Todos los endpoints están protegidos con **JWT**, menos `/auth/login`.

Regla del nombre: todos los archivos, funciones, clases y variables propios llevan el prefijo `jb_`.

## 1. Tecnologías

| Herramienta | Versión | Para qué |
|---|---|---|
| Python | 3.11 o superior | Lenguaje de la API |
| FastAPI | 0.162.0 | Rutas, validación y documentación Swagger |
| Uvicorn | 0.54.0 | Servidor que pone a funcionar la API |
| Pydantic | 2.14.1 | Validación de lo que entra y sale |
| SQLAlchemy | 2.1.6 | ORM: las tablas de MySQL como clases de Python |
| PyMySQL | 1.2.3 | Conector de Python a MySQL (con cryptography para MySQL 8) |
| PyMongo | 4.19.0 | Conector oficial de MongoDB |
| PyJWT | 2.15.1 | Crea y verifica los tokens JWT |
| bcrypt | 5.0.0 | Cifra las contraseñas (RN06) |
| python-dotenv | 1.2.4 | Lee el archivo .env |
| Docker Desktop | reciente | Corre MySQL y MongoDB en contenedores |
| MySQL | 8.4 (imagen mysql:8.4) | Base de datos relacional principal |
| MongoDB | 7.0 (imagen mongo:7.0) | Base de datos de las calificaciones |
| MySQL Workbench y MongoDB Compass | recientes | Ver las bases de datos |
| Thunder Client (VS Code) | reciente | Probar los endpoints |

Se usa la librería `bcrypt` directamente en vez de `passlib[bcrypt]`: passlib no se actualiza desde 2020 y falla con bcrypt 5. Se usa `PyJWT` en vez de `python-jose`, que es la que usa hoy la documentación de FastAPI.

## 2. Estructura del proyecto

Arquitectura por capas: la ruta recibe la petición, el servicio aplica las reglas de negocio y el repositorio habla con la base de datos.

- api_gastronomia/
  - app/
    - jb_main.py: punto de entrada; registra los routers con el prefijo /api/v1 y maneja los errores
    - core/: jb_config.py (lee el .env), jb_security.py (bcrypt, JWT y roles), jb_errores.py (errores en español), jb_respuestas.py, jb_utilidades.py
    - database/: jb_conexion_mysql.py (SQLAlchemy) y jb_conexion_mongo.py (PyMongo)
    - models/: jb_modelos.py, una clase por cada una de las 11 tablas
    - schemas/: un archivo por recurso con lo que entra y lo que sale (Pydantic)
    - repositories/: un archivo por recurso con las consultas a MySQL y a MongoDB
    - services/: un archivo por recurso con las reglas de negocio RN01 a RN06
    - routers/: un archivo por recurso con sus endpoints
  - database/
    - 01_jb_ddl_bd_gastronomia.sql: base de datos, 11 tablas, llaves, índices y restricciones
    - 02_jb_dml_datos_prueba.sql: datos de prueba (10 o más registros por tabla)
    - 03_jb_dcl_usuarios.sql: usuario de la API con privilegios mínimos
    - 04_jb_mongo_calificaciones.js: colección calificaciones con validación $jsonSchema, índices, usuario y datos
  - datos_de_ejemplo/: los mismos datos en bloques para copiar y pegar en la terminal (ver sección 5)
  - docker-compose.yml: levanta MySQL 8.4 y MongoDB 7.0
  - requirements.txt: librerías de Python
  - .env.example: variables que hacen falta, sin credenciales reales (el .env real no se sube a GitHub)

| Capa | Carpeta | Qué hace | Ejemplo |
|---|---|---|---|
| Rutas | app/routers | Reciben la petición, exigen el token y el rol, llaman al servicio | POST /pedidos |
| Servicios | app/services | Aplican las reglas de negocio | Calcular subtotales y total (RN01) |
| Repositorios | app/repositories | Consultan la base de datos | Guardar el pedido |
| Modelos | app/models | Representan las tablas | JbPedido |
| Esquemas | app/schemas | Validan lo que entra y sale | La cantidad debe ser mayor que 0 |

## 3. Puesta en marcha (con Docker)

Requisito en Windows: Docker Desktop usa WSL 2 y necesita la **virtualización activada en la BIOS** (Intel VT-x o AMD-V). Si `systeminfo` dice "Se habilitó la virtualización en el firmware: No", hay que activarla primero.

Todos los comandos se escriben en una terminal abierta en la carpeta `api_gastronomia`.

**Paso 1. Crear el archivo .env.** Copie `.env.example` como `.env` y complete los valores:

- `MYSQL_ROOT_PASSWORD` y `MONGO_ROOT_PASSWORD`: claves para root, sin espacios.
- `MYSQL_PASSWORD`: la misma clave que está en `database/03_jb_dcl_usuarios.sql` (JbApiGastro_2026).
- `MONGO_PASSWORD`: la misma clave que está en `database/04_jb_mongo_calificaciones.js` (JbMongoGastro_2026).
- `JWT_SECRET`: genérela con `python -c "import secrets; print(secrets.token_hex(32))"`.

**Paso 2. Levantar las bases de datos.**

```
docker compose up -d
docker compose ps
```

Espere a que los dos contenedores digan `healthy`. MySQL queda en el puerto 3306 y MongoDB en el 27018 (no en el 27017, para no chocar con un MongoDB instalado en Windows).

**Paso 3. Ejecutar los scripts en orden** (la carpeta database/ está dentro de los contenedores en /scripts):

```
docker compose exec -T mysql sh -c 'mysql -uroot -p$MYSQL_ROOT_PASSWORD < /scripts/01_jb_ddl_bd_gastronomia.sql'
docker compose exec -T mysql sh -c 'mysql -uroot -p$MYSQL_ROOT_PASSWORD < /scripts/02_jb_dml_datos_prueba.sql'
docker compose exec -T mysql sh -c 'mysql -uroot -p$MYSQL_ROOT_PASSWORD < /scripts/03_jb_dcl_usuarios.sql'
docker compose exec -T mongo sh -c 'mongosh -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin --quiet /scripts/04_jb_mongo_calificaciones.js'
```

Los scripts se pueden ejecutar otra vez: el 01 borra la base y la crea vacía, y el 04 borra la colección y la crea de nuevo.

**Paso 4. Instalar y arrancar la API.**

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.jb_main:jb_app --reload
```

**Paso 5. Probar.** Abra http://localhost:8000/docs (Swagger). Haga login, copie el `access_token`, pulse **Authorize** y péguelo.

## 4. Usuarios de prueba

| Correo | Contraseña | Rol |
|---|---|---|
| burbano@gastronomia.com | Admin123* | ADMIN |
| laura.munoz@gastronomia.com | Admin123* | ADMIN |
| carlos.rojas@gastronomia.com | Cajero123* | CAJERO |
| diana.gomez@gastronomia.com | Cajero123* | CAJERO |
| jhon.ortiz@gastronomia.com | Cajero123* | CAJERO |
| pedro.ramirez@gastronomia.com | Cajero123* | CAJERO |
| maria.cruz@gastronomia.com | Cocinero123* | COCINERO |
| jose.vargas@gastronomia.com | Cocinero123* | COCINERO |
| ana.torres@gastronomia.com | Cocinero123* | COCINERO |
| sandra.castro@gastronomia.com | Cajero123* | CAJERO, INACTIVO (no puede iniciar sesión) |

En la base solo se guarda el hash bcrypt de cada contraseña (RN06).

## 5. Cargar los datos: dos caminos

**Camino A (rápido):** los scripts 02 y 04 del paso 3 cargan todo de una vez.

**Camino B (paso a paso, desde la terminal):** la carpeta `datos_de_ejemplo/` tiene los mismos datos en bloques para copiar y pegar. Úselo en vez del script 02, sobre las tablas vacías que deja el script 01.

1. `jb_datos_ejemplo_mysql.sql`, bloques 0 y 1, en la terminal de MySQL (`docker compose exec mysql mysql -u root -p`). Crean el usuario ADMIN que inicia sesión. Es el único usuario que va en SQL: MySQL no sabe cifrar con bcrypt, por eso lleva el hash.
2. `jb_usuarios_por_api.ps1`, en una terminal de PowerShell, con la API encendida. Crea los otros 9 usuarios por medio de `POST /api/v1/usuarios`. Sus contraseñas están en texto plano en `jb_usuarios_ejemplo.json` y la API las cifra antes de guardarlas.
3. `jb_datos_ejemplo_mysql.sql`, bloques 2 al 13, otra vez en la terminal de MySQL. Las compras y los pedidos buscan a su usuario por correo, así no importa qué id le dio MySQL a cada uno.
4. `jb_datos_ejemplo_mongodb.js`, en la terminal de MongoDB (`docker compose exec mongo mongosh -u jb_root -p --authenticationDatabase admin`). Primero tiene que haber corrido el script 04 (crea la colección con su validador).

Cómo se cifra una contraseña que llega por la API:

1. El cliente envía la contraseña en texto plano dentro del JSON.
2. El esquema la valida: de 8 a 72 caracteres, con al menos una letra y un número.
3. `jb_cifrar_password` (en `app/core/jb_security.py`) calcula el hash bcrypt con una sal aleatoria.
4. Solo el hash se guarda en MySQL.
5. Ninguna respuesta incluye la contraseña.
6. En el login, bcrypt vuelve a calcular el hash de lo escrito y lo compara con el guardado.

En producción la API debe ir detrás de HTTPS, para que la contraseña no viaje legible por la red.

## 6. Probar con Thunder Client (VS Code)

1. Instale la extensión Thunder Client en VS Code.
2. Cree un entorno con dos variables: `url` = `http://localhost:8000/api/v1` y `token` (vacía).
3. Cree la petición de login: POST `{{url}}/auth/login`, pestaña Body > JSON:
   `{"correo": "burbano@gastronomia.com", "password": "Admin123*"}`
4. En la pestaña Tests de esa petición, use la opción para guardar una variable del entorno: valor `json.access_token`, variable `{{token}}`. Así cada login actualiza el token solo.
5. En las demás peticiones, pestaña Auth > Bearer, escriba `{{token}}`.
6. Organice las peticiones en una colección con una carpeta por recurso.
7. Agregue pruebas en la pestaña Tests, por ejemplo que el código de respuesta sea 200 o 201. Incluya también los casos negativos: sin token (401), rol sin permiso (403), id que no existe (404) y dato repetido (409).
8. Exporte la colección (menú de la colección > Export) y guárdela en el repositorio: el instructivo pide entregar la colección de pruebas.

## 7. Endpoints (65)

Todas las rutas empiezan por `/api/v1`. "Todos" significa cualquier usuario con token válido.

| Método | Ruta | Roles |
|---|---|---|
| POST | /auth/login | Público (el único) |
| POST | /auth/registro | ADMIN |
| GET | /auth/perfil | Todos |
| GET, POST | /usuarios | ADMIN |
| GET, PUT, DELETE | /usuarios/{id} | ADMIN |
| GET | /categorias | Todos |
| GET | /categorias/{id} | Todos |
| POST | /categorias | ADMIN |
| PUT, DELETE | /categorias/{id} | ADMIN |
| GET | /productos | Todos |
| GET | /productos/{id} | Todos |
| POST | /productos | ADMIN |
| PUT, DELETE | /productos/{id} | ADMIN |
| GET | /productos/categoria/{id_categoria} | Todos |
| GET | /productos/{id}/receta | ADMIN, COCINERO |
| GET | /productos/{id}/costo | ADMIN |
| GET, POST | /insumos | ADMIN, COCINERO |
| GET, PUT, DELETE | /insumos/{id} | ADMIN, COCINERO |
| GET | /insumos/stock-bajo | ADMIN, COCINERO |
| GET | /insumos/por-vencer?dias=7 | ADMIN, COCINERO |
| GET, POST | /recetas | ADMIN, COCINERO |
| GET, PUT, DELETE | /recetas/{id} | ADMIN, COCINERO |
| GET, POST | /proveedores | ADMIN |
| GET, PUT, DELETE | /proveedores/{id} | ADMIN |
| GET | /proveedores/{id}/compras | ADMIN |
| GET, POST | /compras | ADMIN |
| GET, PUT, DELETE | /compras/{id} | ADMIN |
| GET, POST | /clientes | ADMIN, CAJERO |
| GET, PUT, DELETE | /clientes/{id} | ADMIN, CAJERO |
| GET | /clientes/{id}/pedidos | ADMIN, CAJERO |
| GET, POST | /pedidos | ADMIN, CAJERO |
| GET, PUT, DELETE | /pedidos/{id} | ADMIN, CAJERO |
| GET | /pedidos/estado/{estado} | ADMIN, CAJERO, COCINERO |
| PATCH | /pedidos/{id}/estado | ADMIN, CAJERO, COCINERO |
| GET | /reportes/ventas?desde=AAAA-MM-DD&hasta=AAAA-MM-DD | ADMIN |
| GET | /reportes/productos-mas-vendidos?limite=10 | ADMIN |
| GET, POST | /calificaciones | ADMIN, CAJERO |
| GET, PUT, DELETE | /calificaciones/{id} | ADMIN, CAJERO |
| GET | /calificaciones/producto/{id_producto} | ADMIN, CAJERO |

Cuenta: 3 de autenticación + 50 del CRUD (10 recursos x 5 servicios) + 12 de consultas y procesos = 65.

## 8. Reglas de negocio y dónde están

| Regla | Qué hace la API | Archivo |
|---|---|---|
| RN01 | Quien registra el pedido envía solo productos y cantidades. La API toma el precio de venta, calcula subtotales y total. Si se envía un total, responde 422. | app/services/jb_pedido_service.py (jb_armar_detalle) |
| RN02 | Al registrar una compra, sube el stock de cada insumo y su costo pasa a ser el de esa compra, en una sola transacción. | app/services/jb_compra_service.py (jb_crear) |
| RN03 | Al pasar un pedido a ENTREGADO, descuenta los insumos de la receta (cantidad de la receta x cantidad pedida). Si algo no alcanza, responde 409 y no descuenta nada. | app/services/jb_pedido_service.py (jb_descontar_inventario) |
| RN04 | Un producto, insumo, cliente o proveedor con movimientos no se borra: queda INACTIVO. Sin movimientos, se borra. | servicio de cada recurso (jb_eliminar) |
| RN05 | Un pedido ENTREGADO o ANULADO no se modifica (409). | app/services/jb_pedido_service.py (jb_validar_abierto) |
| RN06 | Las contraseñas se guardan con bcrypt y nunca se devuelven. | app/core/jb_security.py y app/schemas/jb_usuario_schema.py |

## 9. Seguridad

- Todos los endpoints exigen el encabezado `Authorization: Bearer <token>`, menos `/auth/login`.
- El token dura los minutos de `JWT_MINUTOS` (60 por defecto) y lleva el id y el rol del usuario.
- En cada petición se busca al usuario en MySQL: si lo borraron o quedó INACTIVO, su token deja de servir (401).
- Sin token, con token inválido o vencido: 401. Rol sin permiso: 403.
- La API se conecta a MySQL con `jb_api_gastronomia`, que solo tiene SELECT, INSERT, UPDATE y DELETE sobre bd_gastronomia (script 03). Nunca usa root.
- A MongoDB se conecta con un usuario que solo puede consultar, insertar, actualizar y borrar en la colección calificaciones (script 04).
- Las claves están en el .env, que no se sube a GitHub. Las contraseñas de los usuarios de la API que aparecen en los scripts 03 y 04 son de desarrollo: en un servidor real se cambian allí y en el .env.
- Los puertos de las bases solo se abren en el propio equipo (127.0.0.1).

## 10. Códigos de respuesta

Los errores siempre responden `{"detalle": "mensaje en español"}`. El 422 agrega una lista `errores` con la ubicación, el campo y el mensaje de cada problema.

| Código | Cuándo |
|---|---|
| 200 | Consulta o actualización correcta |
| 201 | Registro creado |
| 400 | Rompe una regla: un id que no existe, un cliente INACTIVO, una fecha de compra en el futuro, "desde" posterior a "hasta" |
| 401 | Sin token, token inválido o vencido, credenciales incorrectas, usuario INACTIVO |
| 403 | El rol no tiene permiso |
| 404 | No existe |
| 409 | Dato repetido, inventario insuficiente (RN03), pedido cerrado (RN05), cambio de estado no permitido |
| 422 | Formato inválido: falta un campo, tipo equivocado, campo no permitido, nota fuera de 1 a 5 |
| 500 | Error del servidor o sin conexión a una base; no muestra detalles internos |

## 11. Decisiones tomadas frente al instructivo

El instructivo permite ajustar el modelo si se justifica. Estos son los ajustes y las decisiones tomadas:

1. `clientes.estado` (ACTIVO o INACTIVO): RN04 pide borrado lógico de clientes y la tabla no traía estado.
2. `pedidos.observaciones`: aparece en el diagrama de la Figura 1.
3. El stock y las cantidades de compra usan 3 decimales, igual que la receta (0.125 kg). Con 2 decimales, el descuento de RN03 se redondearía mal.
4. Restricciones únicas extra:
   - un insumo no se repite en la receta de un producto;
   - un proveedor no repite número de factura;
   - un insumo no se repite en una compra, ni un producto en un pedido.
5. Flujo de estados del pedido: de PENDIENTE pasa a EN_PREPARACION, y de ahí a ENTREGADO. Se puede ANULAR desde PENDIENTE o EN_PREPARACION.
6. DELETE de un pedido: lo deja ANULADO, porque es parte del historial de ventas.
7. Compras:
   - el PUT solo cambia factura, fecha y proveedor;
   - el DELETE resta del stock lo que la compra sumó, y responde 409 si el stock quedaría negativo.
8. Los reportes cuentan solo pedidos ENTREGADO. El día "hasta" se incluye completo.
9. Calificaciones:
   - solo para pedidos ENTREGADO, una por pedido;
   - el cliente debe ser el que hizo el pedido;
   - los productos deben estar en el pedido;
   - el nombre del producto lo copia la API desde MySQL.
10. Roles de las consultas que el instructivo no define:
    - la receta: ADMIN y COCINERO;
    - el costo y los reportes: solo ADMIN;
    - los pedidos por estado y el cambio de estado: ADMIN, CAJERO y COCINERO.
11. Debe quedar siempre al menos un ADMIN activo, y nadie puede eliminarse a sí mismo.
12. No se pueden pedir productos AGOTADO ni INACTIVO, ni registrar movimientos con clientes, proveedores o insumos INACTIVO.
13. Las pruebas de la API se hacen con Thunder Client (sección 6).

## 12. Evidencias para el anexo (Manual de Configuración de Base de Datos)

- **Tablas y estructura.** Entre a MySQL con `docker compose exec mysql mysql -u root -p`. Luego ejecute `USE bd_gastronomia;`, `SHOW TABLES;`, `DESCRIBE productos;` y algunas consultas. Tome las capturas con la fecha y la hora visibles.
- **Modelo relacional.** En MySQL Workbench, conéctese a 127.0.0.1:3306 con root y use Database > Reverse Engineer.
- **MongoDB.** En Compass, conéctese con `mongodb://jb_root:CLAVE@localhost:27018/?authSource=admin` y abra bd_gastronomia_nosql > calificaciones:
  - la pestaña Validation muestra el $jsonSchema;
  - la pestaña Schema muestra los tipos de cada campo.
- **Prueba del validador.** El bloque 5 de `datos_de_ejemplo/jb_datos_ejemplo_mongodb.js` intenta guardar una nota 7. MongoDB responde "Document failed validation".

## 13. Respaldo y restauración

Respaldo (queda en la carpeta del proyecto):

```
docker compose exec -T mysql sh -c 'mysqldump -uroot -p$MYSQL_ROOT_PASSWORD --databases bd_gastronomia > /tmp/respaldo_mysql.sql'
docker compose cp mysql:/tmp/respaldo_mysql.sql ./respaldo_mysql.sql
docker compose exec -T mongo sh -c 'mongodump -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin --db bd_gastronomia_nosql --gzip --archive=/tmp/respaldo_mongo.gz'
docker compose cp mongo:/tmp/respaldo_mongo.gz ./respaldo_mongo.gz
```

Restauración:

```
docker compose cp ./respaldo_mysql.sql mysql:/tmp/respaldo_mysql.sql
docker compose exec -T mysql sh -c 'mysql -uroot -p$MYSQL_ROOT_PASSWORD < /tmp/respaldo_mysql.sql'
docker compose cp ./respaldo_mongo.gz mongo:/tmp/respaldo_mongo.gz
docker compose exec -T mongo sh -c 'mongorestore -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin --gzip --archive=/tmp/respaldo_mongo.gz --drop'
```

## 14. Solución de problemas

| Problema | Qué hacer |
|---|---|
| Docker Desktop no arranca o pide WSL | Active la virtualización en la BIOS e instale WSL 2 |
| Un contenedor no arranca porque el puerto está ocupado | Cambie MYSQL_PORT o MONGO_PORT en el .env |
| La API no arranca: "Falta la variable ... en el archivo .env" | Copie .env.example como .env y complételo |
| 500 "No hay conexión con MySQL" | Revise que el contenedor esté encendido y que el script 03 se haya ejecutado con la misma clave del .env |
| 500 "MongoDB rechazó el usuario de la API" | Ejecute el script 04 y revise MONGO_USUARIO y MONGO_PASSWORD |
| El login responde 401 con datos correctos | El usuario puede estar INACTIVO; un usuario insertado a mano con SQL debe llevar el hash bcrypt, no la clave en texto plano |
| Tildes raras al ver respuestas en PowerShell 5.1 | Es solo la forma de mostrarlas; los datos quedan bien guardados. Envíe siempre `-ContentType "application/json; charset=utf-8"` |
