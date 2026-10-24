# API REST — Unidad Productiva de Gastronomía (CGDSS)

**EA4 · Análisis y Desarrollo de Software · Ficha 3312744**
Prototipo de API REST con **Python + FastAPI + MongoDB** que hace el CRUD de la información de la Unidad Productiva de Gastronomía: productos, recetas, insumos, proveedores, compras, clientes, pedidos, reportes y calificaciones. Todos los servicios están protegidos con **JWT** y **roles**.

> Prefijo del aprendiz: **`jb_`**. Todos los archivos, funciones, clases y variables del código lo llevan, como exige el instructivo. Si su inicial es otra, vea la sección [F1](#f1-regla-de-nombres-inicial-del-aprendiz).

---

## Índice

- [Resumen: qué pide el instructivo y dónde está](#resumen-qué-pide-el-instructivo-y-dónde-está)
- **PARTE A — Ponerla a funcionar**
  - [A1. Inicio rápido (en este computador ya está todo instalado)](#a1-inicio-rápido-en-este-computador-ya-está-todo-instalado)
  - [A2. Instalación desde cero (otro computador o clonado de GitHub)](#a2-instalación-desde-cero-otro-computador-o-clonado-de-github)
  - [A3. Comandos del día a día](#a3-comandos-del-día-a-día)
  - [A4. Ver las bases de datos en MongoDB Compass](#a4-ver-las-bases-de-datos-en-mongodb-compass)
  - [A5. Registrar sus datos (la base empieza vacía)](#a5-registrar-sus-datos-la-base-empieza-vacía)
- **PARTE B — Usarla desde el navegador (Swagger)**
- **PARTE C — Usarla desde Thunder Client (VS Code)**
- **PARTE D — Entender el proyecto (guía de estudio)**
- **PARTE E — Referencia: endpoints, ejemplos, diccionario de datos**
- **PARTE F — Entrega: GitHub, sustentación y anexo**
- **PARTE G — Solución de problemas**
- **PARTE H — Cómo hacer cambios que pida el instructor** (incluye el ejemplo completo de un **descuento manual**)

---

## Resumen: qué pide el instructivo y dónde está

| Pide el instructivo | Dónde está en el proyecto |
|---|---|
| API REST con Python (FastAPI) y arquitectura por capas | `app/` → `routers/`, `services/`, `repositories/`, `models/`, `schemas/` |
| CRUD de usuarios, categorías, productos, insumos, recetas, proveedores, compras, clientes, pedidos y calificaciones | 10 routers en `app/routers/` (5 servicios cada uno) |
| Endpoints de consulta y procesos de negocio | 12 endpoints extra: receta, costo, stock bajo, por vencer, historiales, estado, reportes, promedio |
| Reglas de negocio RN01 a RN06 | `app/services/` (ver [D4](#d4-dónde-está-cada-regla-de-negocio)) |
| JWT en todos los endpoints excepto `/auth/login`, con 401 y 403 | `app/core/jb_security.py` |
| Contraseñas con bcrypt que nunca se devuelven | `jb_security.py` + `jb_usuario_repository.py` |
| Credenciales en `.env`, que no se sube | `.env`, `.env.example` y `.gitignore` |
| Usuario de base de datos con privilegios mínimos (DCL) | `database/03_jb_dcl_usuarios.py` |
| Scripts DDL, DML, DCL y de MongoDB con `$jsonSchema` | carpeta `database/` |
| Documentación en Swagger (`/docs`) | http://localhost:8000/docs |
| Colección de Postman con pruebas de cada servicio | No se incluye: cada servicio se prueba en Swagger (`/docs`). Ver [F7](#f7-decisiones-tomadas-frente-al-instructivo) |

**Decisión importante.** El instructivo usa MySQL para los datos y MongoDB para las calificaciones. Este proyecto usa **solo MongoDB**, pero con la **misma separación en dos bases**:

| Base del instructivo | Base en este proyecto | Qué guarda |
|---|---|---|
| `bd_gastronomia` (MySQL) | `bd_gastronomia` (MongoDB) | usuarios, categorías, productos, insumos, recetas, proveedores, compras, clientes y pedidos |
| `bd_gastronomia_nosql` (MongoDB) | `bd_gastronomia_nosql` (MongoDB) | calificaciones |

---

# PARTE A — Ponerla a funcionar

## A1. Inicio rápido (en este computador ya está todo instalado)

Ya están listos el entorno virtual (`venv`), las librerías, el archivo `.env` y las bases de datos. Las bases empiezan **sin datos de prueba**: solo tienen el usuario administrador, las 4 categorías que nombra el instructivo y su ejemplo de calificación ([A5](#a5-registrar-sus-datos-la-base-empieza-vacía)). Solo hay que encender la API.

**Paso 1.** Abra la carpeta `api_gastronomia` en VS Code (*Archivo → Abrir carpeta*).

**Paso 2.** Abra una terminal (*Terminal → Nueva terminal*) y active el entorno virtual:

```powershell
.\venv\Scripts\Activate.ps1
```

✅ Al inicio de la línea debe aparecer `(venv)`.

**Paso 3.** Encienda la API:

```powershell
uvicorn app.jb_main:jb_app --reload
```

✅ Debe ver: `Uvicorn running on http://127.0.0.1:8000`

**Paso 4.** Abra en el navegador **http://localhost:8000**. Lo lleva solo a la documentación (Swagger). Continúe en la [PARTE B](#parte-b--usarla-desde-el-navegador-swagger).

> Para apagar la API, presione `Ctrl + C` en la terminal. Mientras la use, no cierre esa terminal.

## A2. Instalación desde cero (otro computador o clonado de GitHub)

**Requisitos:**
- **Python 3.11 o superior**: probado con 3.15.
- **MongoDB Community Server**: probado con 9.0, instalado como servicio de Windows.
- **MongoDB Compass**: para ver los datos.
- **VS Code**. La extensión **Thunder Client** es opcional ([PARTE C](#parte-c--usarla-desde-thunder-client-vs-code)).
- **Git**.

| # | Qué hacer | Comando | ✅ Cómo saber que funcionó |
|---|---|---|---|
| 1 | Verificar Python | `python --version` | `Python 3.11` o superior |
| 2 | Verificar que MongoDB está encendido | `Get-Service MongoDB` | `Status: Running` |
| 3 | Entrar a la carpeta del proyecto | `cd api_gastronomia` | — |
| 4 | Crear el entorno virtual | `python -m venv venv` | Aparece la carpeta `venv/` |
| 5 | Activarlo | `.\venv\Scripts\Activate.ps1` | Aparece `(venv)` |
| 6 | Instalar las librerías | `pip install -r requirements.txt` | `Successfully installed ...` |
| 7 | Crear el archivo de configuración | `Copy-Item .env.example .env` | Aparece el archivo `.env` |
| 8 | Generar la clave secreta del JWT | `python -c "import secrets; print(secrets.token_hex(32))"` | Copie el resultado en `JWT_SECRET=` dentro de `.env` |
| 9 | Crear las colecciones (DDL) | `python database/01_jb_ddl_bd_gastronomia.py` | `DDL terminado.` |
| 10 | Cargar los datos iniciales (DML): el admin y las 4 categorías | `python database/02_jb_dml_datos_prueba.py` | `DML terminado.` |
| 11 | Crear las calificaciones (NoSQL) | `python database/04_jb_mongo_calificaciones.py` | `Script NoSQL terminado.` |
| 12 | Encender la API | `uvicorn app.jb_main:jb_app --reload` | `Uvicorn running on http://127.0.0.1:8000` |

> **Si PowerShell no deja activar el entorno** ("la ejecución de scripts está deshabilitada"), ejecute una sola vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y repita el paso 5.
>
> **Si la base ya existe**, los scripts 01 y 04 se detienen para no borrar nada. Agrégueles `--reiniciar` ([A3](#a3-comandos-del-día-a-día)): antes de borrar guardan una copia en una base `<nombre>_respaldo_AAAAMMDD_HHMMSS`.
>
> El script **03** (usuario de MongoDB con privilegios mínimos) es aparte y opcional: vea [F6](#f6-activar-el-usuario-con-privilegios-mínimos-opcional).

**En VS Code, seleccione el intérprete del entorno virtual** para que no marque errores en los `import`: `Ctrl+Shift+P` → *Python: Select Interpreter* → `.\venv\Scripts\python.exe`.

## A3. Comandos del día a día

| Para… | Comando (con `(venv)` activo, dentro de `api_gastronomia`) |
|---|---|
| Encender la API | `uvicorn app.jb_main:jb_app --reload` |
| Encender la API en otro puerto | `uvicorn app.jb_main:jb_app --reload --port 8001` |
| Volver a crear las bases (vacías, con el admin) | Los 3 comandos de abajo |
| Crear el usuario de MongoDB con privilegios mínimos | `python database/03_jb_dcl_usuarios.py` |
| Ver los datos | Abrir **MongoDB Compass** → `mongodb://localhost:27017` |

**Volver a crear las bases** (borra lo que haya y deja solo el admin, las 4 categorías y el ejemplo de calificación del instructivo). Ejecute los 3 en este orden:

```powershell
python database/01_jb_ddl_bd_gastronomia.py --reiniciar
python database/02_jb_dml_datos_prueba.py
python database/04_jb_mongo_calificaciones.py --reiniciar
```

Con `--reiniciar`, los scripts 01 y 04 guardan primero un respaldo de la base ([F5](#f5-respaldo-y-restauración)). Úselo también después de cambiar `app/models/jb_modelos.py`, para que MongoDB aplique la validación nueva ([PARTE H](#parte-h--cómo-hacer-cambios-que-pida-el-instructor)).

## A4. Ver las bases de datos en MongoDB Compass

1. Abra **MongoDB Compass** desde el menú Inicio de Windows.
2. En la pantalla de conexión deje `mongodb://localhost:27017` y pulse **Connect**. Si ya tiene guardada la conexión `localhost:27017`, haga clic en ella.
3. A la izquierda aparecen las bases. Las de la API son estas:

   | Base | Colecciones |
   |---|---|
   | `bd_gastronomia` | `usuarios`, `categorias`, `productos`, `insumos`, `recetas`, `proveedores`, `compras`, `clientes`, `pedidos` y `contadores` |
   | `bd_gastronomia_nosql` | `calificaciones` y `contadores` |

   Las que terminan en `_respaldo_...` son copias automáticas ([F5](#f5-respaldo-y-restauración)). `admin`, `config` y `local` son internas de MongoDB: no las toque.
4. Haga clic en una colección. Arriba tiene estas pestañas:
   - **Documents**: los datos. Con los botones de la derecha los ve como lista, como JSON o como tabla.
   - **Schema**: pulse **Analyze** para ver los campos y sus tipos.
   - **Indexes**: los índices. Los que dicen **UNIQUE** no dejan repetir el valor.
   - **Validation**: la regla `$jsonSchema` de la colección.
5. Lo que registre con la API aparece aquí. Si no lo ve, pulse el botón de **recargar** (🔄) de la colección.

> Puede editar un documento con el lápiz ✏️, pero el cambio debe cumplir el `$jsonSchema`; si no, Compass muestra *Document failed validation*. Es mejor hacer los cambios con la API, porque además aplica las reglas de negocio. La contraseña se ve como un hash `$2b$12$...` y no se puede escribir a mano ([A5](#a5-registrar-sus-datos-la-base-empieza-vacía)).

## A5. Registrar sus datos (la base empieza vacía)

**Qué trae la base al crearla.** Solo los datos que da el instructivo, más el usuario administrador:

| Colección | Documentos | De dónde salen |
|---|---|---|
| `usuarios` | 1: el administrador | `JB_ADMIN` en `database/02_jb_dml_datos_prueba.py`. Sin un usuario no se podría obtener el token |
| `categorias` | 4: Platos, Bebidas, Panadería y Repostería | Requerimiento RF03 del instructivo |
| `calificaciones` (`bd_gastronomia_nosql`) | 1 | El documento de ejemplo del instructivo. Habla del pedido 125, el cliente 18 y los productos 4 y 9, que no existen porque el instructivo no da sus datos |
| Las demás | 0 | Usted las llena desde la API |

**El usuario administrador** es `burbano@gastronomia.com` con la contraseña `Admin123*`. Hay tres formas de cambiarlo:

- **En el código (recomendado).** Edite `JB_ADMIN` en `database/02_jb_dml_datos_prueba.py` y vuelva a crear las bases ([A3](#a3-comandos-del-día-a-día)).
  - El correo debe tener la forma `nombre@dominio.com` y la contraseña de 6 a 72 caracteres. Si no, el script avisa y no guarda nada.
  - Cambie también el ejemplo del login en `app/schemas/jb_auth_schema.py`, para que Swagger lo traiga ya escrito.
  - Si cambia `JB_ADMIN` y no vuelve a crear las bases, el admin sigue con los datos anteriores.
- **Desde la API, sin borrar datos.** Inicie sesión como admin y use `PUT /api/v1/usuarios/1` con todos los datos del usuario, el correo nuevo y la contraseña nueva.
- **En Compass.** El correo se cambia editando el documento de `usuarios`. La contraseña no, porque está cifrada. Para cambiarla ahí, genere el hash con este comando, desde `api_gastronomia` y con `(venv)` activo, y pegue el resultado (`$2b$12$...`) en el campo `password`:
  ```powershell
  python -c "from app.core.jb_security import jb_cifrar_password; print(jb_cifrar_password('SuClaveNueva'))"
  ```

**Orden para registrar los datos.** Cada paso necesita lo que se creó en los anteriores:

| # | Qué | Endpoint | Necesita |
|---|---|---|---|
| 1 | Usuarios CAJERO y COCINERO | `POST /usuarios` | — |
| 2 | Más categorías, si quiere (ya hay 4) | `POST /categorias` | — |
| 3 | Productos | `POST /productos` | Una categoría |
| 4 | Insumos | `POST /insumos` | — |
| 5 | Recetas | `POST /recetas` | Un producto y un insumo |
| 6 | Proveedores | `POST /proveedores` | — |
| 7 | Compras (suben el stock, RN02) | `POST /compras` | Un proveedor y los insumos |
| 8 | Clientes | `POST /clientes` | — |
| 9 | Pedidos | `POST /pedidos` | Un cliente y productos DISPONIBLES |
| 10 | Entregar un pedido (descuenta el inventario, RN03) | `PATCH /pedidos/{id}/estado` | Recetas de sus productos y stock suficiente |
| 11 | Calificaciones | `POST /calificaciones` | Un pedido ENTREGADO |
| 12 | Reportes | `GET /reportes/...` | Pedidos ENTREGADOS |

En Swagger cada `POST` trae un ejemplo al pulsar **Try it out**. Los ids de los ejemplos, como `"id_cliente": 1`, suponen que ese registro ya existe: cámbielos por los ids que le devolvió la API al crearlos.

---

# PARTE B — Usarla desde el navegador (Swagger)

FastAPI genera sola una página web para probar cada endpoint. No hace falta instalar nada.

| Dirección | Para qué sirve |
|---|---|
| http://localhost:8000 | Lo redirige a `/docs` |
| **http://localhost:8000/docs** | **Swagger UI**: probar los endpoints |
| http://localhost:8000/redoc | Documentación de solo lectura, más cómoda para leer |
| http://localhost:8000/openapi.json | La especificación OpenAPI en JSON |

> **¿Por qué al escribir `http://localhost:8000/api/v1/productos` en la barra del navegador sale un error 401?**
> Porque todos los endpoints son privados. El navegador no envía el token cuando usted escribe la dirección a mano. Por eso se prueba desde Swagger o desde Thunder Client.
>
> **¿Y por qué `http://localhost:8000/api/v1/auth/login` responde "Método HTTP no permitido"?** Porque el login es un `POST` (envía correo y contraseña) y la barra del navegador siempre hace `GET`. El login se hace desde Swagger (B1).

### Paso a paso en Swagger

**B1. Iniciar sesión**
1. Abra http://localhost:8000/docs.
2. Busque la sección **Autenticación** y abra `POST /api/v1/auth/login`.
3. Pulse **Try it out**. El cuerpo ya trae el usuario administrador de `JB_ADMIN` ([A5](#a5-registrar-sus-datos-la-base-empieza-vacía)):
   ```json
   { "correo": "burbano@gastronomia.com", "password": "Admin123*" }
   ```
4. Pulse **Execute**.
5. ✅ En *Response body* aparece `"access_token": "eyJhbGciOi..."`. Copie **solo el texto del token**, sin las comillas.

**B2. Autorizarse**
1. Suba al inicio de la página y pulse el botón **Authorize** 🔒.
2. Pegue el token en el campo *Value*. No escriba la palabra `Bearer`: Swagger la agrega sola.
3. Pulse **Authorize** y luego **Close**.
4. ✅ Los candados de los endpoints aparecen cerrados.

**B3. Consultar algo**
1. Abra `GET /api/v1/categorias`, pulse **Try it out** y luego **Execute**.
2. ✅ Respuesta 200 con las 4 categorías del instructivo: Platos, Bebidas, Panadería y Repostería.

**B4. Crear algo**
1. Abra `POST /api/v1/categorias` → **Try it out**. El ejemplo ya viene diligenciado.
2. Pulse **Execute**.
3. ✅ Respuesta **201** con el `id_categoria` nuevo.
4. Si lo ejecuta otra vez con el mismo nombre, la respuesta es **409** porque el nombre no se puede repetir.

**B5. Ver los errores de seguridad (se piden en la sustentación)**

| Para ver… | Haga esto |
|---|---|
| **401** sin token | Pulse **Authorize** → **Logout** y ejecute cualquier endpoint |
| **403** rol sin permiso | Cree un usuario CAJERO con `POST /api/v1/usuarios`, inicie sesión con él, autorícese con ese token y ejecute `GET /api/v1/reportes/ventas` |
| **404** no existe | `GET /api/v1/productos/999` |
| **409** conflicto | Cree dos veces la misma categoría |
| **422** datos mal formados | `POST /api/v1/productos` con `"precio_venta": 0` |

**B6. Cambiar de usuario**

Pulse **Authorize** → **Logout**, haga login con otro usuario y vuelva a autorizarse con el token nuevo.

> El token dura **60 minutos** (`JWT_MINUTOS` en `.env`). Si empieza a recibir 401 con el mensaje "El token expiró", haga login otra vez.

---

# PARTE C — Usarla desde Thunder Client (VS Code)

Thunder Client hace las mismas peticiones que Swagger, pero desde VS Code. Es opcional y las peticiones se crean a mano.

1. Encienda la API ([A1](#a1-inicio-rápido-en-este-computador-ya-está-todo-instalado)).
2. En VS Code pulse el ícono del **rayo ⚡** en la barra izquierda. La primera vez le pide iniciar sesión con una cuenta gratuita.
3. **Login:** **New Request** → método `POST` → URL `http://localhost:8000/api/v1/auth/login` → pestaña **Body** → **JSON**:
   ```json
   { "correo": "burbano@gastronomia.com", "password": "Admin123*" }
   ```
   Pulse **Send** y copie el `access_token` de la respuesta, sin las comillas.
4. **Cualquier otra petición:** **New Request** → elija el método y la URL, por ejemplo `POST http://localhost:8000/api/v1/pedidos` → pestaña **Auth** → **Bearer** → pegue el token → pestaña **Body** → **JSON**:
   ```json
   { "id_cliente": 1, "tipo_pedido": "MESA", "detalle": [ { "id_producto": 1, "cantidad": 2 } ] }
   ```
   Pulse **Send**.

> Los cuerpos de ejemplo de cada endpoint están en Swagger y en [E3](#e3-ejemplos-de-peticiones-y-respuestas).

---

# PARTE D — Entender el proyecto (guía de estudio)

## D1. La arquitectura por capas

```
 Cliente (Swagger / Thunder Client / futura app web o móvil)
    │  HTTP + JSON + "Authorization: Bearer <token>"
    ▼
 ┌───────────────┐   ¿Hay token? ¿Su rol tiene permiso?   →  401 / 403
 │  routers/     │   ¿El JSON tiene el formato correcto?  →  422  (schemas/)
 └──────┬────────┘
        ▼
 ┌───────────────┐   Reglas de negocio RN01..RN06          →  400 / 404 / 409
 │  services/    │
 └──────┬────────┘
        ▼
 ┌───────────────┐   Única capa que habla con MongoDB
 │ repositories/ │
 └──────┬────────┘
        ▼
   MongoDB:  bd_gastronomia  +  bd_gastronomia_nosql
   (models/ define la validación $jsonSchema de cada colección)
```

Como en un restaurante:
- El **router** es el mesero: recibe el pedido, revisa quién lo hace y entrega la respuesta.
- El **schema** es la carta: define qué se puede pedir y en qué formato.
- El **service** es el cocinero: aplica las reglas.
- El **repository** es la bodega: solo ahí se sacan y guardan cosas.

**Por qué se separa así:** cada archivo tiene una sola responsabilidad. Si mañana se cambia MongoDB por MySQL, solo se reescriben los `repositories/`.

## D2. Mapa de archivos

```
api_gastronomia/
├── app/
│   ├── jb_main.py                 Punto de entrada: crea la app, registra routers y manejadores de error
│   ├── core/
│   │   ├── jb_config.py           Lee el .env (MONGO_URI, JWT_SECRET, ...)
│   │   ├── jb_security.py         bcrypt, creación y verificación del JWT, control de roles
│   │   ├── jb_respuestas.py       Errores documentados en Swagger (400, 401, 403, 404, 409)
│   │   ├── jb_errores.py          Traduce al español los errores de FastAPI y Pydantic (422, 404, 405)
│   │   └── jb_utilidades.py       Hora de Colombia y redondeo de decimales
│   ├── database/
│   │   └── jb_conexion_mongo.py   Conexión a las 2 bases, Decimal128 y contador de ids
│   ├── models/
│   │   └── jb_modelos.py          Validación $jsonSchema e índices de cada colección (el "DDL")
│   ├── schemas/                   Pydantic: qué datos entran (Crear/Actualizar) y qué sale (Respuesta)
│   ├── repositories/              Consultas a MongoDB (find, insert, update, aggregate)
│   │   └── jb_base_repository.py  Las 5 operaciones CRUD que heredan todos los repositorios
│   ├── services/                  Reglas de negocio (RN01..RN06) y validaciones
│   └── routers/                   Endpoints de cada recurso, con roles y documentación
├── database/
│   ├── 01_jb_ddl_bd_gastronomia.py     DDL: colecciones + $jsonSchema + índices
│   ├── 02_jb_dml_datos_prueba.py       DML: usuario administrador (JB_ADMIN) y las 4 categorías del instructivo
│   ├── 03_jb_dcl_usuarios.py           DCL: usuario de MongoDB con privilegios mínimos
│   ├── 04_jb_mongo_calificaciones.py   NoSQL: calificaciones con $jsonSchema + datos
│   └── jb_utilidades_bd.py             Funciones que usan 01, 02 y 04: respaldo, colecciones y contadores
├── .env / .env.example / .gitignore
├── requirements.txt
└── README.md
```

## D3. Ruta de estudio recomendada

**Todo el código está comentado línea por línea, en español.** Encima de cada línea hay un comentario (`# ...`) que dice qué hace. Los textos entre comillas triples (`"""..."""`) debajo de cada función de los routers no son comentarios: son la descripción que muestra Swagger.

Lea los archivos **en este orden**. Al final de cada paso intente responder las preguntas en voz alta, porque son las que suelen hacer en la sustentación.

| # | Lea | Preguntas de autoevaluación |
|---|---|---|
| 1 | `core/jb_config.py` y `.env.example` | ¿Por qué la clave del JWT no está escrita en el código? ¿Qué pasa si falta `JWT_SECRET`? |
| 2 | `database/jb_conexion_mongo.py` | ¿Por qué hay dos bases? ¿Qué hace `jb_siguiente_id`? ¿Para qué sirve `JbDecimalCodec`? |
| 3 | `models/jb_modelos.py` | ¿Qué es `$jsonSchema`? ¿Qué equivale en MongoDB a `NOT NULL`, `UNIQUE` y `CHECK`? |
| 4 | `core/jb_security.py` | ¿Qué guarda el token? ¿Cuándo responde 401 y cuándo 403? ¿Por qué bcrypt no se puede "descifrar"? |
| 5 | Categorías completas: `schemas/jb_categoria_schema.py` → `repositories/jb_base_repository.py` → `services/jb_categoria_service.py` → `routers/jb_categorias_router.py` | ¿Qué hace cada capa? ¿Dónde se valida el 404? ¿Por qué hay tres esquemas (Crear, Actualizar, Respuesta)? |
| 6 | `jb_main.py` | ¿Cómo se registran los routers? ¿Quién convierte un correo repetido en 409? |
| 7 | `services/jb_pedido_service.py` | ¿Dónde se calcula el total (RN01)? ¿Cómo se descuenta el inventario sin transacciones (RN03)? |
| 8 | `services/jb_compra_service.py` | ¿Qué pasa con el inventario al crear, modificar o eliminar una compra (RN02)? |
| 9 | `repositories/jb_reporte_repository.py` | ¿Qué hace cada etapa: `$match`, `$unwind`, `$group`, `$sort`, `$lookup`? |
| 10 | `database/0*_jb_*.py` | ¿Cuál script equivale al DDL, cuál al DML y cuál al DCL? |

## D4. Dónde está cada regla de negocio

| Regla | Qué dice | Dónde está | Cómo demostrarla |
|---|---|---|---|
| **RN01** | Subtotal = cantidad × precio_unitario. El total es la suma de subtotales y lo calcula la API | `jb_pedido_service.jb_preparar_detalle()`. El esquema `JbPedidoCrear` no tiene campos de precio | Crear un pedido enviando solo productos y cantidades: la respuesta trae precios y total |
| **RN02** | Una compra suma al `stock_actual` y actualiza el `costo_unitario` | `jb_compra_service.jb_crear()` → `jb_insumo_repository.jb_registrar_entrada()` | Ver un insumo, registrar una compra de ese insumo y volver a verlo: el stock subió |
| **RN03** | Al pasar un pedido a ENTREGADO se descuentan los insumos de la receta. Si no alcanza, responde 409 | `jb_pedido_service.jb_descontar_inventario()` | Entregar un pedido normal (baja el stock) y uno con más unidades de las que alcanza el inventario (409, sin descontar nada) |
| **RN04** | No se borra lo que tiene movimientos: se pasa a INACTIVO | `jb_eliminar()` de productos, insumos, clientes, proveedores, usuarios y categorías | El `DELETE` de un producto que ya se vendió responde `"tipo_borrado": "LOGICO"`. Uno que nunca se vendió se borra con `"FISICO"` |
| **RN05** | Un pedido ENTREGADO o ANULADO no se modifica | `jb_pedido_service.jb_validar_abierto()` | El `PUT` de un pedido ENTREGADO responde 409 |
| **RN06** | Contraseñas con bcrypt que nunca se devuelven | `jb_security.jb_cifrar_password()`. `jb_usuario_repository` oculta `password` y los esquemas de respuesta no lo tienen | `GET /usuarios` no muestra `password`. En Compass se ve el hash `$2b$12$...` |

**Cómo se descuenta el inventario sin transacciones (RN03):** MongoDB instalado como servidor único no admite transacciones de varios documentos. Por eso el servicio hace lo siguiente:
1. **Calcula** cuánto necesita de cada insumo.
2. **Verifica todo** antes de descontar nada. Si falta algo, responde 409 y no toca el inventario.
3. **Descuenta** cada insumo con una actualización condicional (`stock_actual >= cantidad`). Si otro usuario consumió el insumo en ese instante, **devuelve** lo ya descontado.
4. **Protege el estado** con `jb_cambiar_estado_si()`, que solo cambia el estado si nadie lo cambió antes. Así un pedido no se entrega dos veces.

## D5. Recorrido completo de un pedido

1. **Login del cajero** con `POST /auth/login`:
   - `jb_auth_service.jb_iniciar_sesion()` busca el correo.
   - `bcrypt.checkpw` compara la contraseña.
   - `jb_crear_token()` firma `{"sub": "2", "rol": "CAJERO", "exp": ...}`.
2. **Crear el pedido** con `POST /pedidos` (`{"id_cliente": 1, "tipo_pedido": "MESA", "detalle": [{"id_producto": 1, "cantidad": 2}]}`):
   - **Router:** `jb_requiere_roles("ADMIN","CAJERO")` valida el token y el rol. Si falla, responde 401 o 403.
   - **Schema:** `JbPedidoCrear` valida que la cantidad sea mayor que 0 y que el tipo sea válido. Si no, responde 422.
   - **Service:** valida que el cliente exista y esté ACTIVO (si no, 400) y que los productos estén DISPONIBLES. Toma el precio de la base y calcula subtotales y total (**RN01**).
   - **Repository:** pide el siguiente id a `contadores` e inserta el documento con estado `PENDIENTE`.
3. **El cocinero lo prepara** con `PATCH /pedidos/{id}/estado` `{"estado": "EN_PREPARACION"}`.
4. **El cocinero lo entrega** con `PATCH ... {"estado": "ENTREGADO"}`:
   - El servicio revisa **RN05**.
   - Cambia el estado de forma segura.
   - Descuenta el inventario (**RN03**).
5. **Se modifica después**: `PUT /pedidos/{id}` responde **409** (**RN05**).
6. **El cliente califica**: `POST /calificaciones` guarda el documento en **bd_gastronomia_nosql**. La API toma el cliente y los nombres de los productos del pedido.
7. **El administrador consulta los reportes**: `GET /reportes/ventas` suma los pedidos ENTREGADOS con una agregación.

## D6. Cómo se pasó el modelo relacional a MongoDB

| Modelo del instructivo (SQL) | Cómo quedó en MongoDB | Por qué |
|---|---|---|
| Tabla | Colección | Equivalente directo |
| Fila | Documento JSON | Equivalente directo |
| `INT PK AUTO_INCREMENT` | `_id` numérico con la colección `contadores` | Ids 1, 2, 3… como en el instructivo, en vez de `ObjectId` |
| `FOREIGN KEY` | Campo con el id del otro documento (`id_categoria`, `id_cliente`…) que el servicio valida | MongoDB no tiene llaves foráneas: la API comprueba que exista |
| Tablas `detalle_pedido` y `detalle_compra` | Arreglo `detalle` **embebido** dentro del pedido o de la compra | El detalle siempre se lee junto con su pedido y no existe solo |
| Tabla `recetas` (N:M) | Colección `recetas` aparte | Tiene su propio CRUD (`/recetas`) y relaciona productos con insumos |
| `DECIMAL(10,2)` | `Decimal128` (en Python, `Decimal`) | El dinero no se guarda como `float` para evitar errores de redondeo |
| `NOT NULL`, `CHECK`, `ENUM`, `VARCHAR(n)` | `$jsonSchema`: `required`, `minimum`, `enum`, `maxLength` | La base rechaza datos inválidos aunque se inserten desde Compass |
| `UNIQUE` | Índice único | Al repetir el valor la API responde 409 |
| Zona horaria America/Bogota | `jb_ahora()` guarda la hora de Colombia (UTC-5) | Las fechas de pedidos y compras quedan en hora local |

---

# PARTE E — Referencia

## E1. Usuarios y roles

La base empieza con un solo usuario: el administrador de `JB_ADMIN` (`burbano@gastronomia.com` / `Admin123*`). Cómo cambiarlo está en [A5](#a5-registrar-sus-datos-la-base-empieza-vacía).

| Rol | Qué puede hacer | Cómo se crea |
|---|---|---|
| ADMIN | Todo | El primero lo crea el script 02; los demás, `POST /usuarios` |
| CAJERO | Clientes, pedidos y calificaciones | `POST /usuarios` con `"rol": "CAJERO"` |
| COCINERO | Insumos, recetas, ver pedidos y cambiar su estado | `POST /usuarios` con `"rol": "COCINERO"` |

Un usuario con estado INACTIVO no puede iniciar sesión: el login responde 403.

## E2. Endpoints (65)

Prefijo de todas las rutas: **`/api/v1`**. Todas exigen token, excepto `POST /auth/login`.

**Autenticación**

| Método | Ruta | Roles | Descripción |
|---|---|---|---|
| POST | `/auth/login` | **Público** | Inicia sesión y devuelve el token JWT |
| POST | `/auth/registro` | ADMIN | Registra un usuario |
| GET | `/auth/perfil` | Todos | Datos del usuario autenticado |

**CRUD** (cada recurso tiene `GET /recurso`, `GET /recurso/{id}`, `POST /recurso`, `PUT /recurso/{id}` y `DELETE /recurso/{id}`)

| Recurso | Ruta base | Roles |
|---|---|---|
| Usuarios | `/usuarios` | ADMIN |
| Categorías | `/categorias` | ADMIN (consultar: todos) |
| Productos | `/productos` | ADMIN (consultar: todos) |
| Insumos | `/insumos` | ADMIN, COCINERO |
| Recetas | `/recetas` | ADMIN, COCINERO |
| Proveedores | `/proveedores` | ADMIN |
| Compras | `/compras` | ADMIN |
| Clientes | `/clientes` | ADMIN, CAJERO |
| Pedidos | `/pedidos` | ADMIN, CAJERO (consultar y cambiar estado: también COCINERO) |
| Calificaciones (NoSQL) | `/calificaciones` | ADMIN, CAJERO |

**Consultas y procesos de negocio**

| Método | Ruta | Roles | Descripción |
|---|---|---|---|
| GET | `/productos/categoria/{id_categoria}` | Todos | Productos de una categoría |
| GET | `/productos/{id}/receta` | Todos | Insumos, cantidades y costo de cada línea de la receta |
| GET | `/productos/{id}/costo` | Todos | Costo de producción (Σ cantidad × costo_unitario) y margen |
| GET | `/insumos/stock-bajo` | ADMIN, COCINERO | Insumos con `stock_actual <= stock_minimo` |
| GET | `/insumos/por-vencer?dias=7` | ADMIN, COCINERO | Insumos que vencen en los próximos N días |
| GET | `/proveedores/{id}/compras` | ADMIN | Historial de compras a un proveedor |
| GET | `/clientes/{id}/pedidos` | ADMIN, CAJERO | Historial de pedidos de un cliente |
| GET | `/pedidos/estado/{estado}` | ADMIN, CAJERO, COCINERO | Pedidos por estado (PENDIENTE, EN_PREPARACION, ENTREGADO, ANULADO) |
| PATCH | `/pedidos/{id}/estado` | ADMIN, CAJERO, COCINERO | Cambia el estado del pedido (aplica RN03 y RN05) |
| GET | `/reportes/ventas?desde=&hasta=` | ADMIN | Total vendido, número de pedidos y ticket promedio en un rango |
| GET | `/reportes/productos-mas-vendidos?limite=10` | ADMIN | Ranking de productos más vendidos |
| GET | `/calificaciones/producto/{id_producto}` | ADMIN, CAJERO | Calificaciones y promedio de un producto |

**Comportamiento de los DELETE**

| Recurso | Si tiene movimientos | Si no tiene |
|---|---|---|
| Producto | Con pedidos → INACTIVO | Se borra junto con su receta |
| Insumo | En recetas o compras → INACTIVO | Se borra |
| Cliente | Con pedidos → INACTIVO | Se borra |
| Proveedor | Con compras → INACTIVO | Se borra |
| Usuario | Con pedidos o compras → INACTIVO | Se borra. No se puede borrar el propio usuario (400) |
| Categoría | Con productos → INACTIVO | Se borra |
| Pedido | Nunca se borra: queda **ANULADO**. Si ya está ENTREGADO o ANULADO → 409 | — |
| Compra | Resta del inventario lo que había sumado y se borra. Si ese inventario ya se consumió → 409 | — |
| Receta, calificación | — | Se borran |

## E3. Ejemplos de peticiones y respuestas

> Los ids, nombres y valores de estos ejemplos son ilustrativos. Con sus datos los números serán otros, pero la forma del JSON es la misma.

**Login** con `POST /api/v1/auth/login`:
```json
{ "correo": "burbano@gastronomia.com", "password": "Admin123*" }
```
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expira_en_minutos": 60,
  "id_usuario": 1,
  "nombre": "Laura Méndez Ruiz",
  "rol": "ADMIN"
}
```

**Crear pedido (RN01)** con `POST /api/v1/pedidos`. El cliente no envía precios:
```json
{
  "id_cliente": 1,
  "tipo_pedido": "MESA",
  "observaciones": "Sin cebolla",
  "detalle": [ { "id_producto": 1, "cantidad": 2 }, { "id_producto": 2, "cantidad": 2 } ]
}
```
Respuesta **201**. La API agregó precios, subtotales, total, fecha, usuario y estado:
```json
{
  "id_pedido": 15, "fecha_pedido": "2026-10-24T09:40:00", "id_cliente": 1, "id_usuario": 2,
  "tipo_pedido": "MESA", "estado": "PENDIENTE", "observaciones": "Sin cebolla", "total": 36000.0,
  "detalle": [
    { "id_producto": 1, "cantidad": 2, "precio_unitario": 14000.0, "subtotal": 28000.0 },
    { "id_producto": 2, "cantidad": 2, "precio_unitario": 4000.0, "subtotal": 8000.0 }
  ]
}
```

**Cambiar estado (RN03)** con `PATCH /api/v1/pedidos/15/estado`:
```json
{ "estado": "ENTREGADO" }
```
Si no hay inventario suficiente, la respuesta es **409**:
```json
{ "detalle": "Inventario insuficiente para entregar el pedido (RN03): Arroz: se necesitan 75.000, hay 50.000; Pechuga de pollo: se necesitan 100.000, hay 30.000; ..." }
```

**Costo de producción** con `GET /api/v1/productos/1/costo`:
```json
{ "id_producto": 1, "producto": "Almuerzo ejecutivo", "precio_venta": 14000.0,
  "costo_produccion": 5205.0, "margen": 8795.0, "margen_porcentaje": 62.82 }
```

**Registrar compra (RN02)** con `POST /api/v1/compras`:
```json
{
  "numero_factura": "FV-2050",
  "id_proveedor": 1,
  "detalle": [ { "id_insumo": 1, "cantidad": 10, "costo_unitario": 4300 },
               { "id_insumo": 5, "cantidad": 5,  "costo_unitario": 3900 } ]
}
```
La respuesta trae `total: 62500.0`. El arroz sube 10 kg y su costo unitario queda en 4300.

**Reporte de ventas** con `GET /api/v1/reportes/ventas?desde=2026-10-01&hasta=2026-10-31`:
```json
{ "desde": "2026-10-01", "hasta": "2026-10-31", "numero_pedidos": 10, "total_vendido": 307300.0, "ticket_promedio": 30730.0 }
```

**Calificar un pedido** con `POST /api/v1/calificaciones`. Solo se aceptan pedidos ENTREGADOS:
```json
{
  "id_pedido": 15,
  "calificacion_servicio": 5,
  "comentario": "Excelente atención y buen sabor",
  "productos": [ { "id_producto": 1, "calificacion": 5 }, { "id_producto": 2, "calificacion": 4 } ]
}
```

**Promedio de un producto** con `GET /api/v1/calificaciones/producto/1`:
```json
{ "id_producto": 1, "producto": "Almuerzo ejecutivo", "promedio": 4.33, "total_calificaciones": 3, "calificaciones": [ ... ] }
```

**Errores de seguridad:**
```json
{ "detalle": "Token requerido: envíe el encabezado Authorization: Bearer <token>" }
{ "detalle": "Acceso denegado: esta acción requiere el rol ADMIN" }
```

**Datos inválidos (422)** con `POST /api/v1/productos` y `{"codigo": "", "nombre": "T", "precio_venta": 0, "unidad_venta": "u", "id_categoria": "uno"}`. Cada error dice dónde está, en qué campo y qué pasó:
```json
{
  "detalle": "Los datos enviados no son válidos",
  "errores": [
    { "ubicacion": "cuerpo", "campo": "codigo", "mensaje": "No puede estar vacío" },
    { "ubicacion": "cuerpo", "campo": "nombre", "mensaje": "Debe tener al menos 2 caracteres" },
    { "ubicacion": "cuerpo", "campo": "precio_venta", "mensaje": "Debe ser mayor que 0" },
    { "ubicacion": "cuerpo", "campo": "id_categoria", "mensaje": "Debe ser un número entero" }
  ]
}
```

**Ruta o método equivocado:**
```json
{ "detalle": "La ruta no existe: revise la dirección (todas empiezan por /api/v1)" }
{ "detalle": "Método HTTP no permitido en esta ruta. Métodos permitidos: POST" }
```

### Todas las respuestas están en español

FastAPI y Pydantic generan algunos errores en inglés ("Field required", "Not Found", "Method Not Allowed"). El archivo `app/core/jb_errores.py` los traduce, y `app/jb_main.py` usa esa traducción en sus manejadores de errores:

| Error | Qué hace la API |
|---|---|
| 422 (datos inválidos) | `jb_manejar_validacion` traduce cada error con `jb_traducir_error` |
| 404 de una ruta que no existe, 405 de un método no permitido | `jb_manejar_http` cambia el texto en inglés por uno en español con `jb_mensaje_http` |
| 400, 401, 403, 404, 409 propios de la API | Ya están en español; `jb_manejar_http` los deja igual |
| Errores de MongoDB y 500 | Manejadores propios con mensajes en español |

La clave de los errores es `detalle`. En Swagger, las descripciones de las respuestas también están en español ("Respuesta exitosa", "Datos inválidos..."). Solo quedan en inglés dos cosas:
- **Los botones de Swagger** ("Try it out", "Execute", "Authorize"), porque son de la librería Swagger UI y no los genera la API.
- **`access_token` y `token_type: "bearer"`** en la respuesta del login, porque son los nombres estándar de OAuth 2 que esperan las aplicaciones web y móviles que consumirán la API.

> **Si aparece un error de validación nuevo en inglés** (porque se agregó un tipo de dato distinto), agregue su `type` y su mensaje en español al diccionario `JB_MENSAJES_VALIDACION` de `jb_errores.py`. Mientras no esté, la API responde "Valor no válido".

## E4. Códigos de respuesta

| Código | Significado en esta API | Ejemplo |
|---|---|---|
| 200 | Consulta, actualización o eliminación correcta | `GET /productos` |
| 201 | Registro creado | `POST /clientes` |
| 400 | El dato rompe una regla de negocio | Pedido con un producto AGOTADO; categoría inexistente al crear un producto; `desde > hasta` |
| 401 | Sin token, token inválido o expirado, o login incorrecto | `GET /productos` sin token |
| 403 | El rol no tiene permiso, o el usuario está INACTIVO | El cajero pide `/reportes/ventas` |
| 404 | El recurso de la URL no existe | `GET /pedidos/999` |
| 409 | Conflicto: dato único repetido, inventario insuficiente, pedido cerrado o pedido ya calificado | Crear dos veces el mismo código de producto |
| 422 | El JSON no cumple el esquema (tipo, tamaño, rango, enum) | `"precio_venta": 0`, `"calificacion": 6` |
| 500 | Error interno o MongoDB apagado | El servicio MongoDB está detenido |

## E5. Diccionario de datos

Convenciones:
- **Ob.** = obligatorio.
- **Único** = índice único.
- Todas las colecciones validan con `$jsonSchema` (`validationLevel: strict`).

**usuarios** (bd_gastronomia)

| Campo | Tipo BSON | Ob. | Llave / índice | Restricción / defecto | Descripción |
|---|---|---|---|---|---|
| `_id` (id_usuario) | int | Sí | PK | Auto (contadores) | Identificador |
| identificacion | string | Sí | Único | 5–20 caracteres | Documento |
| nombres | string | Sí | | máx. 80 | Nombres |
| apellidos | string | Sí | | máx. 80 | Apellidos |
| correo | string | Sí | Único | máx. 120, formato correo, minúsculas | Usuario de acceso |
| password | string | Sí | | hash bcrypt (máx. 255) | Contraseña cifrada (RN06) |
| rol | string | Sí | | enum ADMIN, CAJERO, COCINERO | Rol |
| estado | string | Sí | | enum ACTIVO, INACTIVO; defecto ACTIVO | Estado |

**categorias**

| Campo | Tipo | Ob. | Llave | Restricción / defecto | Descripción |
|---|---|---|---|---|---|
| `_id` (id_categoria) | int | Sí | PK | Auto | Identificador |
| nombre | string | Sí | Único | máx. 60 | Nombre |
| descripcion | string / null | No | | máx. 200 | Descripción |
| estado | string | Sí | | ACTIVO, INACTIVO; defecto ACTIVO | Estado |

**productos**

| Campo | Tipo | Ob. | Llave | Restricción / defecto | Descripción |
|---|---|---|---|---|---|
| `_id` (id_producto) | int | Sí | PK | Auto | Identificador |
| codigo | string | Sí | Único | máx. 20 | Código interno |
| nombre | string | Sí | | máx. 100 | Nombre |
| descripcion | string / null | No | | | Descripción |
| precio_venta | decimal | Sí | | > 0, 2 decimales | Precio de venta |
| unidad_venta | string | Sí | | máx. 20 | Porción, unidad, vaso… |
| id_categoria | int | Sí | Ref. categorias, índice | Debe existir y estar ACTIVA | Categoría |
| estado | string | Sí | | DISPONIBLE, AGOTADO, INACTIVO; defecto DISPONIBLE | Estado |

**insumos**

| Campo | Tipo | Ob. | Llave | Restricción / defecto | Descripción |
|---|---|---|---|---|---|
| `_id` (id_insumo) | int | Sí | PK | Auto | Identificador |
| nombre | string | Sí | Único | máx. 100 | Nombre |
| unidad_medida | string | Sí | | g, kg, ml, l, lb, unidad | Unidad |
| stock_actual | decimal | Sí | | ≥ 0, 3 decimales | Existencias |
| stock_minimo | decimal | Sí | | ≥ 0, 3 decimales | Nivel de alerta |
| costo_unitario | decimal | Sí | | ≥ 0, 2 decimales | Costo por unidad de medida |
| fecha_vencimiento | date / null | No | Índice | | Vencimiento del lote actual |
| estado | string | Sí | | ACTIVO, INACTIVO | Estado |

**recetas** (N:M entre productos e insumos)

| Campo | Tipo | Ob. | Llave | Restricción | Descripción |
|---|---|---|---|---|---|
| `_id` (id_receta) | int | Sí | PK | Auto | Identificador |
| id_producto | int | Sí | Ref. productos; único junto con id_insumo | Debe existir | Producto |
| id_insumo | int | Sí | Ref. insumos, índice | Debe existir y estar ACTIVO | Insumo |
| cantidad | decimal | Sí | | > 0, 3 decimales | Cantidad por unidad de producto |

**proveedores**

| Campo | Tipo | Ob. | Llave | Restricción | Descripción |
|---|---|---|---|---|---|
| `_id` (id_proveedor) | int | Sí | PK | Auto | Identificador |
| nit | string | Sí | Único | máx. 20, dígitos y guion | NIT o documento |
| razon_social | string | Sí | | máx. 120 | Razón social |
| telefono | string / null | No | | máx. 20 | Teléfono |
| correo | string / null | No | | máx. 120, formato correo | Correo |
| direccion | string / null | No | | máx. 150 | Dirección |
| estado | string | Sí | | ACTIVO, INACTIVO | Estado |

**compras** (con el detalle embebido)

| Campo | Tipo | Ob. | Llave | Restricción | Descripción |
|---|---|---|---|---|---|
| `_id` (id_compra) | int | Sí | PK | Auto | Identificador |
| numero_factura | string | Sí | Único junto con id_proveedor | máx. 30 | Factura del proveedor |
| fecha_compra | date | Sí | Índice | defecto: ahora | Fecha de la compra |
| id_proveedor | int | Sí | Ref. proveedores | ACTIVO | Proveedor |
| id_usuario | int | Sí | Ref. usuarios | Se toma del token | Usuario que registra |
| total | decimal | Sí | | Lo calcula la API | Valor total |
| detalle[] | array | Sí | Índice `detalle.id_insumo` | mínimo 1 ítem | Ítems de la compra |
| detalle.id_insumo / cantidad / costo_unitario / subtotal | int / decimal | Sí | | cantidad > 0; subtotal lo calcula la API | Ítem |

**clientes**

| Campo | Tipo | Ob. | Llave | Restricción | Descripción |
|---|---|---|---|---|---|
| `_id` (id_cliente) | int | Sí | PK | Auto | Identificador |
| identificacion | string | Sí | Único | 5–20 | Documento |
| nombres / apellidos | string | Sí | | máx. 80 | Nombres y apellidos |
| telefono / correo | string / null | No | | máx. 20 / 120 | Contacto |
| tipo_cliente | string | Sí | | APRENDIZ, INSTRUCTOR, FUNCIONARIO, EXTERNO | Tipo |
| estado | string | Sí | | ACTIVO, INACTIVO | **Agregado** para cumplir RN04 |

**pedidos** (con el detalle embebido)

| Campo | Tipo | Ob. | Llave | Restricción | Descripción |
|---|---|---|---|---|---|
| `_id` (id_pedido) | int | Sí | PK | Auto | Identificador |
| fecha_pedido | date | Sí | Índice | Hora de Colombia | Fecha y hora |
| id_cliente | int | Sí | Ref. clientes, índice | ACTIVO | Cliente |
| id_usuario | int | Sí | Ref. usuarios | Se toma del token | Usuario que registra |
| tipo_pedido | string | Sí | | MESA, PARA_LLEVAR, EVENTO | Tipo |
| estado | string | Sí | Índice | PENDIENTE, EN_PREPARACION, ENTREGADO, ANULADO | Estado |
| observaciones | string / null | No | | máx. 255 | Observaciones (está en el MER) |
| total | decimal | Sí | | Lo calcula la API (RN01) | Total |
| detalle[] | array | Sí | Índice `detalle.id_producto` | mínimo 1 | id_producto, cantidad (entero ≥ 1), precio_unitario, subtotal |

**calificaciones** (bd_gastronomia_nosql)

| Campo | Tipo | Ob. | Llave | Restricción | Descripción |
|---|---|---|---|---|---|
| `_id` (id_calificacion) | int | Sí | PK | Auto | Identificador |
| id_pedido | int | Sí | Único | Pedido ENTREGADO | Pedido calificado |
| id_cliente | int | Sí | Índice | Se toma del pedido | Cliente |
| fecha | date | Sí | | Ahora | Fecha |
| calificacion_servicio | int | Sí | | 1 a 5 | Calificación del servicio |
| comentario | string / null | No | | máx. 500 | Comentario |
| productos[] | array | Sí | Índice `productos.id_producto` | mínimo 1; productos que estén en el pedido | `{ id_producto, nombre, calificacion 1..5 }` |

**contadores** (en las dos bases): `{ _id: "<colección>", valor: <último id> }`. Equivale a `AUTO_INCREMENT`.

## E6. Scripts de base de datos

| Script | Equivale a | Qué hace |
|---|---|---|
| `01_jb_ddl_bd_gastronomia.py` | `01_ddl_bd_gastronomia.sql` | Crea las 9 colecciones con `$jsonSchema`, 18 índices y `contadores` |
| `02_jb_dml_datos_prueba.py` | `02_dml_datos_prueba.sql` | El usuario administrador (`JB_ADMIN`) y las 4 categorías de RF03: Platos, Bebidas, Panadería y Repostería. No carga datos de prueba |
| `03_jb_dcl_usuarios.py` | `03_dcl_usuarios.sql` | Crea o actualiza `jb_api_gastronomia` con `readWrite` **solo** en las dos bases de la API |
| `04_jb_mongo_calificaciones.py` | `04_mongo_calificaciones.js` | Crea `calificaciones` con `$jsonSchema` en `bd_gastronomia_nosql` y guarda el documento de ejemplo del instructivo |

**Orden de ejecución:** 01 → 02 → 04. El 03 es opcional ([F6](#f6-activar-el-usuario-con-privilegios-mínimos-opcional)). `jb_utilidades_bd.py` no se ejecuta solo: tiene las funciones que comparten los scripts 01, 02 y 04.

Se escribieron en Python porque así no hace falta instalar `mongosh`, y la validación se define una sola vez en `app/models/jb_modelos.py`.

## E7. Variables del archivo `.env`

| Variable | Ejemplo | Para qué |
|---|---|---|
| `MONGO_URI` | `mongodb://localhost:27017` | Conexión a MongoDB |
| `MONGO_DB` | `bd_gastronomia` | Base de datos principal |
| `MONGO_DB_NOSQL` | `bd_gastronomia_nosql` | Base de calificaciones |
| `MONGO_API_USUARIO` | `jb_api_gastronomia` | Nombre del usuario que crea el script DCL |
| `JWT_SECRET` | 64 caracteres hexadecimales | Firma de los tokens (mínimo 32 caracteres) |
| `JWT_MINUTOS` | `60` | Duración del token |

---

# PARTE F — Entrega

## F1. Regla de nombres (inicial del aprendiz)

El instructivo exige que archivos, variables, clases, funciones, rutas y controladores lleven la inicial del aprendiz. Así se aplicó aquí:

| Elemento | Ejemplo |
|---|---|
| Archivos | `jb_productos_router.py`, `jb_producto_service.py`, `01_jb_ddl_bd_gastronomia.py` |
| Funciones | `jb_obtener_producto()`, `jb_crear_token()` |
| Clases | `JbProductoCrear`, `JbProductoRepository` |
| Variables y constantes | `jb_pedido`, `jb_router`, `JB_MONGO_URI` |

**Lo que no lleva prefijo, a propósito:**
- Los nombres de los campos de datos (`id_producto`, `precio_venta`…) y las URL (`/api/v1/productos`), porque son el contrato definido en las tablas del instructivo.
- Los `__init__.py` y las carpetas de la estructura sugerida.

> Si la inicial correcta no es `jb`, hay que reemplazar `jb_` → `x_`, `Jb` → `X` y `JB_` → `X_` en todo el proyecto, incluidos los nombres de archivo.

## F2. Subir a GitHub

```powershell
git init
git add .
git status          # verifique que NO aparezcan .env ni venv/
git commit -m "API REST Gastronomía - EA4"
git branch -M main
git remote add origin https://github.com/SU_USUARIO/api_gastronomia.git
git push -u origin main
```

El `.gitignore` ya excluye `.env`, `venv/` y `__pycache__/`. El repositorio debe contener:
- el código fuente;
- la carpeta `database/`.

## F3. Guion para la sustentación (unos 10 minutos)

**Antes de sustentar**, registre unos datos siguiendo el orden de [A5](#a5-registrar-sus-datos-la-base-empieza-vacía): un CAJERO, un producto con su receta, los insumos de esa receta con stock, un cliente y dos pedidos. Uno de los pedidos debe pedir más unidades de las que alcanza el inventario.

1. **Arquitectura:** mostrar las carpetas de `app/` y explicar el recorrido router → service → repository ([D1](#d1-la-arquitectura-por-capas)).
2. **Base de datos en Compass** ([A4](#a4-ver-las-bases-de-datos-en-mongodb-compass)):
   - Las dos bases, `bd_gastronomia` y `bd_gastronomia_nosql`.
   - La pestaña **Validation** de una colección, que muestra el `$jsonSchema`.
   - Un pedido con su `detalle` embebido.
   - Un usuario con la contraseña en hash `$2b$12$...` (RN06).
3. **Seguridad en Swagger:**
   - Login y botón **Authorize**.
   - 401 sin token.
   - 403 con el cajero en reportes.
4. **RN01:** crear un pedido enviando solo cantidades y mostrar el total que calculó la API.
5. **RN03:**
   - Consultar el stock de un insumo de la receta.
   - Entregar el pedido normal.
   - Consultar el stock otra vez: bajó.
   - Entregar el pedido grande: 409 y el stock no cambió.
6. **RN05:** intentar modificar el pedido entregado → 409.
7. **RN04:** `DELETE` del producto que ya se vendió → LOGICO.
8. **RN02:** registrar una compra y ver cómo sube el stock.
9. **MongoDB NoSQL:** calificar el pedido y consultar el promedio del producto.
10. **Reportes:** ventas del mes y productos más vendidos.
11. **Buenas prácticas:**
    - `.env` y `.gitignore`.
    - El usuario de MongoDB con privilegios mínimos (script 03).
    - Las respuestas de error en JSON.

## F4. Anexo: qué sacar de aquí para el Manual de Configuración de Base de Datos

| Sección del formato | De dónde sale |
|---|---|
| Introducción y alcance | [Resumen](#resumen-qué-pide-el-instructivo-y-dónde-está). Fuera del prototipo quedan facturación electrónica, pagos, app web y app móvil |
| MER | Diagrama de la Figura 1 del instructivo + `clientes.estado` + `pedidos.observaciones`. Hacerlo en draw.io |
| Diccionario de datos | [E5](#e5-diccionario-de-datos) |
| Modelo físico | Captura de Compass: pestañas **Schema**, **Indexes** y **Validation** de cada colección |
| Justificación del motor | Por qué MongoDB y la comparación con MySQL, PostgreSQL, SQL Server y Oracle ([D6](#d6-cómo-se-pasó-el-modelo-relacional-a-mongodb)) |
| Requisitos de configuración | [A2](#a2-instalación-desde-cero-otro-computador-o-clonado-de-github) y `requirements.txt` |
| Scripts | [E6](#e6-scripts-de-base-de-datos) y el contenido de `database/` |
| Configuración y ejecución | Capturas de los scripts 01, 02 y 04 ([A2](#a2-instalación-desde-cero-otro-computador-o-clonado-de-github), pasos 9 a 11) y de Compass, **con la fecha y hora de Windows visibles** |
| Otras consideraciones | Hora de Colombia, Decimal128, respaldo y restauración ([F5](#f5-respaldo-y-restauración)) y manejo de credenciales (`.env`) |

## F5. Respaldo y restauración

**Respaldo automático.** Cada vez que se ejecuta el script 01 o el 04 con `--reiniciar`, la base actual se copia en `bd_gastronomia_respaldo_AAAAMMDD_HHMMSS` o `bd_gastronomia_nosql_respaldo_AAAAMMDD_HHMMSS`.

> En el servidor solo están las dos bases del proyecto (`bd_gastronomia` y `bd_gastronomia_nosql`) y las internas de MongoDB (`admin`, `config` y `local`). Cada vez que use `--reiniciar` aparecerá una base `..._respaldo_...` nueva. Si no la necesita, bórrela desde Compass: clic derecho en la base → *Drop database*.

**Con las herramientas oficiales (`mongodump` y `mongorestore`).** Instale primero las [MongoDB Database Tools](https://www.mongodb.com/try/download/database-tools).

```powershell
mongodump --db bd_gastronomia --out respaldos
mongodump --db bd_gastronomia_nosql --out respaldos
mongorestore --drop --db bd_gastronomia respaldos\bd_gastronomia
mongorestore --drop --db bd_gastronomia_nosql respaldos\bd_gastronomia_nosql
```

## F6. Activar el usuario con privilegios mínimos (opcional)

Hoy MongoDB funciona **sin autenticación**, que es lo normal en una instalación local de desarrollo. Para que la API se conecte con un usuario que **no es root**:

1. Cree un **administrador** del servidor, porque al activar la seguridad lo necesitará para administrar. En Compass abra la consola **MONGOSH** (abajo) y ejecute:
   ```js
   use admin
   db.createUser({ user: "admin", pwd: passwordPrompt(), roles: ["root"] })
   ```
2. Ejecute el DCL: `python database/03_jb_dcl_usuarios.py`. Escriba una contraseña de 8 o más caracteres.
3. Edite como administrador el archivo `C:\Program Files\MongoDB\Server\9.0\bin\mongod.cfg` y agregue:
   ```yaml
   security:
     authorization: enabled
   ```
4. Reinicie el servicio desde PowerShell como administrador: `Restart-Service MongoDB`.
5. En el `.env` cambie:
   ```
   MONGO_URI=mongodb://jb_api_gastronomia:SU_CLAVE@localhost:27017/?authSource=bd_gastronomia
   ```
6. ✅ La API funciona igual, pero ahora con un usuario que solo puede leer y escribir en sus dos bases.

> Los scripts con `--reiniciar` crean bases de respaldo. Para ejecutarlos con la seguridad activa use una cadena de conexión con el usuario `admin`.

## F7. Decisiones tomadas frente al instructivo

| Instructivo | Este proyecto | Motivo |
|---|---|---|
| MySQL + MongoDB | Solo MongoDB, en dos bases | Decisión del aprendiz. Se conserva la separación de datos estructurados y no estructurados |
| Scripts `.sql` y `.js` | Scripts `.py` | No se usa MySQL ni `mongosh`. Equivalen al DDL, DML y DCL |
| Colección de Postman con pruebas | No se incluye | Decisión del aprendiz. Cada servicio se prueba en Swagger (`/docs`) |
| Docker | MongoDB instalado como servicio | Decisión del aprendiz |
| `passlib[bcrypt]` | `bcrypt` directo | passlib ya no se mantiene y falla con bcrypt 5 |
| `python-jose` o `PyJWT` | `PyJWT` | Una de las dos opciones sugeridas |
| `clientes` sin estado | Se agregó `estado` | RN04 exige poder pasar un cliente a INACTIVO |
| Stock `DECIMAL(10,2)` | 3 decimales | Las recetas usan `DECIMAL(10,3)`. Con 2 decimales el descuento se redondearía |
| Roles de pedidos | El COCINERO también consulta pedidos | Necesita verlos para prepararlos y cambiarles el estado |
| `DELETE /pedidos/{id}` | Anula el pedido (no lo borra) | Un pedido es un movimiento de venta (RN04) |
| Calificación con `id_cliente` | La API toma el cliente y los nombres del pedido | Mismo criterio de RN01: la API calcula lo que puede deducir |
| DML con mínimo 10 registros de prueba por tabla principal | Solo el administrador y los datos que da el instructivo: 4 categorías y el ejemplo de calificación | Decisión del aprendiz: la base empieza vacía para registrar datos reales |

---

# PARTE G — Solución de problemas

| Síntoma | Causa | Solución |
|---|---|---|
| `uvicorn : El término 'uvicorn' no se reconoce` | No está activo el entorno virtual | `.\venv\Scripts\Activate.ps1` |
| "la ejecución de scripts está deshabilitada en este sistema" | Política de PowerShell | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `RuntimeError: Falta JWT_SECRET` | No existe `.env` o la clave tiene menos de 32 caracteres | [A2](#a2-instalación-desde-cero-otro-computador-o-clonado-de-github), pasos 7 y 8 |
| 500 "No hay conexión con MongoDB" | El servicio MongoDB está detenido | `Start-Service MongoDB` (PowerShell como administrador) |
| `[WinError 10048]` o "address already in use" | Ya hay una API encendida en el puerto 8000 | Cierre la otra terminal o use `--port 8001` (y ese puerto en la URL) |
| 401 "El token expiró" | Pasaron 60 minutos | Haga login otra vez y use el token nuevo |
| 401 "Correo o contraseña incorrectos" con el admin | No son los de `JB_ADMIN`, o se cambió `JB_ADMIN` sin volver a crear las bases | Revise `JB_ADMIN` en `database/02_jb_dml_datos_prueba.py` y [A3](#a3-comandos-del-día-a-día) |
| El script 02 dice que el correo o la contraseña no son válidos | `JB_ADMIN` no cumple las reglas | Correo con la forma `nombre@dominio.com` y contraseña de 6 a 72 caracteres |
| 400 "... no existe" al crear algo desde Swagger | El ejemplo usa un id que todavía no existe | Cree primero ese registro ([A5](#a5-registrar-sus-datos-la-base-empieza-vacía)) y use el id que le devolvió la API |
| 422 en `/insumos/stock-bajo` | Una ruta fija quedó después de `/{id}` | Ya está resuelto: las rutas fijas van primero en `jb_insumos_router.py` |
| El script 01 o el 04 dice "ya tiene colecciones" | Protección para no borrar datos | Agregue `--reiniciar` (se guarda un respaldo antes) |
| El script 02 termina con `DuplicateKeyError` | Ya había datos: no se ejecutó antes el 01 con `--reiniciar` | Ejecute los 3 comandos de [A3](#a3-comandos-del-día-a-día) en orden |
| VS Code subraya los `import` en rojo | VS Code usa otro intérprete | `Ctrl+Shift+P` → *Python: Select Interpreter* → `venv` |

---

# PARTE H — Cómo hacer cambios que pida el instructor

Esta parte sirve para cuando el instructor diga, por ejemplo, *"agrégale un descuento"*, *"ponle un campo nuevo"* o *"haz una sección de mesas"*. Primero está el **método** que sirve para cualquier cambio. Después vienen **ejemplos completos** con el código exacto. Todos los ejemplos se probaron sobre una copia de este proyecto.

## H1. Antes de tocar el código

1. **Guarde el estado actual** para poder volver atrás si algo sale mal:
   ```powershell
   git add . ; git commit -m "antes del cambio"
   ```
   Si se enreda, `git restore .` deja todo como estaba. Si no usa Git, copie la carpeta del proyecto.
2. **Deje la API encendida con `--reload`.** Cada vez que guarde un `.py` (`Ctrl+S`), la API se reinicia sola. **Mire la terminal**: si escribió algo mal, ahí aparece el error. Lea siempre la **última línea**, por ejemplo `NameError: name 'Decimal' is not defined`.
3. **Tenga Swagger abierto** (http://localhost:8000/docs) y recárguelo con `F5` después de cada cambio.

## H2. El método: el orden para cualquier cambio

Los cambios se hacen **de la base de datos hacia arriba**. En cada paso pregúntese si lo necesita:

| Paso | Capa | Archivo | Pregunta |
|---|---|---|---|
| 1 | Modelo | `app/models/jb_modelos.py` | ¿Cambia lo que se guarda en MongoDB? (campo, valores permitidos, restricción, colección nueva) |
| 2 | Schema | `app/schemas/jb_<recurso>_schema.py` | ¿Cambia lo que **entra** (Crear/Actualizar) o lo que **sale** (Respuesta)? |
| 3 | Repository | `app/repositories/jb_<recurso>_repository.py` | ¿Necesito una consulta nueva a MongoDB? |
| 4 | Service | `app/services/jb_<recurso>_service.py` | ¿Hay un cálculo, una regla o una validación nueva? |
| 5 | Router | `app/routers/jb_<recurso>_router.py` | ¿Hay un endpoint nuevo? ¿Cambian los roles? |
| 6 | Main | `app/jb_main.py` | ¿Creé un **archivo de router nuevo**? Hay que registrarlo |
| 7 | Base de datos | Los 3 comandos de [A3](#a3-comandos-del-día-a-día) | Solo si hice el paso 1. Vuelve a crear las bases con la validación nueva. Lo que creó en Swagger se borra (queda en el respaldo) y vuelven solo los datos iniciales ([A5](#a5-registrar-sus-datos-la-base-empieza-vacía)) |
| 8 | Probar | Swagger | Pruebe el caso correcto **y** los casos de error (400, 403, 404, 409, 422) |

> **Regla del instructivo:** todo lo nuevo lleva el prefijo **`jb_`**: archivos, funciones, clases (`Jb...`) y variables.

## H3. ¿Qué archivos toco? (tabla rápida)

| Si el instructor pide… | Toque | Ejemplo |
|---|---|---|
| Un descuento, recargo, impuesto o cálculo nuevo | Schema + service + router | [H4](#h4-ejemplo-completo-sección-de-descuento-manual-en-pedidos) |
| Un campo nuevo en una entidad | Modelo + schema (Crear y Respuesta) + volver a crear las bases | [H5](#h5-ejemplo-agregar-un-campo-calorías-a-productos) |
| Una consulta o filtro nuevo | Repository + service + router | [H6](#h6-ejemplo-endpoint-de-consulta-productos-por-rango-de-precio) |
| Que otro rol pueda usar un endpoint | Router | [H7](#h7-ejemplo-cambiar-los-roles-de-un-endpoint) |
| Un estado nuevo (por ejemplo `LISTO`) | Modelo + schema + volver a crear las bases | [H8](#h8-ejemplo-agregar-un-estado-nuevo-a-los-pedidos) |
| Una sección o recurso nuevo con su CRUD | 4 archivos nuevos + modelo + main | [H9](#h9-ejemplo-sección-nueva-con-crud-completo-mesas) |
| Cambiar un límite (precio mínimo, longitud de un texto…) | Schema: el `Field(...)` del campo. Si quiere que la base también lo controle, el modelo y volver a crear las bases | — |
| Cambiar un mensaje de error | El service, en el texto de `jb_dato_invalido(...)`, `jb_conflicto(...)` o `jb_no_encontrado(...)` | — |
| Cambiar cuánto dura el token | `.env` → `JWT_MINUTOS=120`. Luego apague y encienda la API: `--reload` no vigila el `.env` | — |

## H4. Ejemplo completo: sección de descuento manual en pedidos

**Lo que pide el instructor:** *"El cajero debe poder hacerle un descuento a mano a un pedido."*

**Cómo explicar el diseño:**
- Se crea una **sección nueva "Descuentos"** en Swagger con el endpoint `PATCH /api/v1/pedidos/{id_pedido}/descuento`.
- El cajero envía el porcentaje y el motivo:
  ```json
  { "porcentaje": 10, "motivo": "Descuento para aprendiz" }
  ```
- Lo pueden usar **ADMIN y CAJERO**. El porcentaje va de **0 a 50**, y **0 quita el descuento**.
- **La API calcula los valores**, igual que en RN01 (el cajero no escribe el total):
  - `valor_descuento = subtotal × porcentaje / 100`
  - `total = subtotal − valor_descuento`
- **RN05:** un pedido ENTREGADO o ANULADO no acepta descuento y responde 409.
- **Si después se modifica el pedido (PUT), el descuento se conserva** y se recalcula sobre el nuevo subtotal.
- **Los reportes de ventas ya incluyen el descuento**, porque suman el campo `total`.

**Archivos que se tocan** (✚ = archivo nuevo, ✎ = cambio):

| | Archivo | Qué se hace |
|---|---|---|
| ✎ | `app/schemas/jb_pedido_schema.py` | La respuesta del pedido muestra el subtotal y el descuento |
| ✚ | `app/schemas/jb_descuento_schema.py` | Qué datos recibe el descuento |
| ✎ | `app/services/jb_pedido_service.py` | Función que calcula subtotal, descuento y total |
| ✚ | `app/services/jb_descuento_service.py` | La regla de aplicar el descuento |
| ✚ | `app/routers/jb_descuentos_router.py` | El endpoint (la sección "Descuentos") |
| ✎ | `app/jb_main.py` | Registrar el router nuevo |
| ✎ | `app/models/jb_modelos.py` | (Recomendado) que MongoDB también valide los campos nuevos |

### Paso 1 — `app/schemas/jb_pedido_schema.py` ✎

**1a.** En los `import` de arriba, debajo de `from datetime import datetime`, agregue:
```python
# Decimal: números exactos, para los valores por defecto del descuento
from decimal import Decimal
```

**1b.** En la clase `JbPedidoRespuesta`, debajo de la línea `observaciones: str | None = None`, agregue:
```python
    # Suma de los subtotales, antes del descuento
    subtotal: JbNumero | None = None
    # Porcentaje de descuento (0 si no tiene)
    porcentaje_descuento: JbNumero = Decimal("0")
    # Valor del descuento en pesos
    valor_descuento: JbNumero = Decimal("0")
    # Por qué se hizo el descuento
    motivo_descuento: str | None = None
```
> Los campos nuevos tienen **valor por defecto** (`= None`, `= Decimal("0")`) porque los pedidos que ya existen no los tienen. Sin valor por defecto, consultar un pedido viejo daría error 500.

### Paso 2 — `app/schemas/jb_descuento_schema.py` ✚ (archivo nuevo)
```python
"""Esquema del descuento manual de un pedido."""
# Decimal: números exactos para el porcentaje
from decimal import Decimal

# ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import ConfigDict, Field

# Base de los esquemas de entrada (quita espacios de los textos)
from app.schemas.jb_tipos import JbModeloEntrada


# Datos que envía el cajero para hacer el descuento
class JbDescuentoPedido(JbModeloEntrada):
    # Porcentaje de 0 a 50 con máximo 2 decimales; con 0 se quita el descuento
    porcentaje: Decimal = Field(ge=0, le=50, decimal_places=2, description="De 0 a 50. Con 0 se quita el descuento")
    # Motivo del descuento: de 3 a 150 caracteres
    motivo: str = Field(min_length=3, max_length=150)

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{"porcentaje": 10, "motivo": "Descuento para aprendiz"}]})
```
`ge=0, le=50` significa "mayor o igual a 0 y menor o igual a 50". Si envían 60, FastAPI responde **422** sin que usted programe nada.

### Paso 3 — `app/services/jb_pedido_service.py` ✎

**3a.** Debajo de la línea `JB_ESTADOS_CERRADOS = ("ENTREGADO", "ANULADO")` agregue:
```python


# Calcula subtotal, descuento y total de un pedido
def jb_calcular_totales(jb_subtotal: Decimal, jb_porcentaje: Decimal) -> dict:
    """Descuento: valor_descuento = subtotal x porcentaje / 100 y total = subtotal - valor_descuento."""
    # Valor del descuento en pesos, redondeado a 2 decimales
    jb_valor_descuento = jb_dinero(jb_subtotal * jb_porcentaje / 100)
    # Devuelve los cuatro campos que se guardan en el pedido
    return {
        # Suma de los subtotales
        "subtotal": jb_subtotal,
        # Porcentaje aplicado
        "porcentaje_descuento": jb_porcentaje,
        # Descuento en pesos
        "valor_descuento": jb_valor_descuento,
        # Total = subtotal - descuento
        "total": jb_dinero(jb_subtotal - jb_valor_descuento),
    }
```

**3b.** En la función **`jb_crear`**, busque estas dos líneas:
```python
        # Total calculado (RN01)
        "total": jb_total,
```
y cámbielas por:
```python
        # Subtotal, descuento (0 al crear) y total (RN01)
        **jb_calcular_totales(jb_total, Decimal("0")),
```

**3c.** En la función **`jb_actualizar`**, busque estas dos líneas:
```python
        # Total recalculado (RN01)
        "total": jb_total,
```
y cámbielas por:
```python
        # Subtotal, el descuento que ya tenía el pedido y total (RN01)
        **jb_calcular_totales(jb_total, jb_pedido.get("porcentaje_descuento", Decimal("0"))),
```
> **¿Qué hace el `**`?** "Desempaca" el diccionario que devuelve `jb_calcular_totales`. Es como escribir a mano las cuatro líneas `"subtotal": ...`, `"porcentaje_descuento": ...`, `"valor_descuento": ...` y `"total": ...`. En `jb_actualizar` se usa el porcentaje que ya tenía el pedido, para que **el descuento no se pierda** al modificarlo.

### Paso 4 — `app/services/jb_descuento_service.py` ✚ (archivo nuevo)
```python
"""Descuento manual de pedidos: el cajero escribe el porcentaje y el motivo."""
# Decimal: números exactos para dinero
from decimal import Decimal

# Redondeo de dinero a 2 decimales
from app.core.jb_utilidades import jb_dinero
# Acceso a pedidos
from app.repositories.jb_pedido_repository import jb_pedido_repository
# Funciones del servicio de pedidos que se reutilizan
from app.services.jb_pedido_service import jb_calcular_totales, jb_obtener, jb_validar_abierto


# Aplica (o quita, con 0) el descuento a un pedido
def jb_aplicar_descuento(jb_id_pedido: int, jb_porcentaje: Decimal, jb_motivo: str) -> dict:
    # Busca el pedido: 404 si no existe
    jb_pedido = jb_obtener(jb_id_pedido)
    # RN05: un pedido ENTREGADO o ANULADO responde 409
    jb_validar_abierto(jb_pedido)
    # Subtotal = suma de los subtotales del detalle (empieza en 0)
    jb_subtotal = jb_dinero(sum((jb_item["subtotal"] for jb_item in jb_pedido["detalle"]), Decimal("0")))
    # Calcula subtotal, porcentaje, valor del descuento y total
    jb_cambios = jb_calcular_totales(jb_subtotal, jb_porcentaje)
    # Guarda el motivo; si el porcentaje es 0 (se quitó el descuento) queda en None
    jb_cambios["motivo_descuento"] = jb_motivo if jb_porcentaje > 0 else None
    # Guarda los cambios y devuelve el pedido actualizado
    return jb_pedido_repository.jb_actualizar(jb_id_pedido, jb_cambios)
```
Este servicio **reutiliza** lo que ya existía: `jb_obtener` da el 404, `jb_validar_abierto` aplica RN05 y `jb_actualizar` del repositorio guarda. No hay que escribir consultas nuevas a MongoDB.

### Paso 5 — `app/routers/jb_descuentos_router.py` ✚ (archivo nuevo)
```python
"""Endpoints de descuentos manuales sobre pedidos. Roles: ADMIN, CAJERO."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad)
from fastapi import APIRouter, Depends

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Esquema de lo que envía el cajero
from app.schemas.jb_descuento_schema import JbDescuentoPedido
# Esquema del pedido que se responde
from app.schemas.jb_pedido_schema import JbPedidoRespuesta
# Servicio del descuento, con el nombre corto jb_servicio
from app.services import jb_descuento_service as jb_servicio

# Router: rutas /pedidos, sección "Descuentos" de Swagger; TODOS sus endpoints exigen ADMIN o CAJERO
jb_router = APIRouter(prefix="/pedidos", tags=["Descuentos"], responses=JB_PRIVADO,
                      dependencies=[Depends(jb_requiere_roles("ADMIN", "CAJERO"))])


# PATCH /api/v1/pedidos/{id}/descuento
@jb_router.patch("/{id_pedido}/descuento", response_model=JbPedidoRespuesta, summary="Aplicar descuento manual",
                 responses={**JB_R404, **JB_R409})
# Recibe el id de la URL y el cuerpo validado con JbDescuentoPedido
def jb_aplicar_descuento_pedido(id_pedido: int, jb_datos: JbDescuentoPedido):
    """El cajero escribe el porcentaje (0 a 50) y el motivo. La API calcula
    `valor_descuento = subtotal x porcentaje / 100` y `total = subtotal - valor_descuento`.
    Con porcentaje 0 se quita el descuento. **RN05:** un pedido ENTREGADO o ANULADO responde 409.

    **Roles:** ADMIN, CAJERO.
    """
    # Pasa el id, el porcentaje y el motivo al servicio
    return jb_servicio.jb_aplicar_descuento(id_pedido, jb_datos.porcentaje, jb_datos.motivo)
```

### Paso 6 — `app/jb_main.py` ✎ (registrar la sección)

**6a.** En el bloque `from app.routers import (...)`, agregue `jb_descuentos_router,` debajo de `jb_compras_router,`.

**6b.** En la lista `for jb_modulo in (...)`, agregue `jb_descuentos_router,` debajo de `jb_pedidos_router,`.

**6c.** En `JB_ETIQUETAS`, debajo de la línea de `"Pedidos"`, agregue esta línea. Esa lista no lleva comentarios por dentro: el de encima la explica toda.
```python
    {"name": "Descuentos", "description": "Descuento manual sobre un pedido abierto."},
```
> Si se le olvida el paso 6, la API arranca pero **la sección no aparece en Swagger**.

### Paso 7 — `app/models/jb_modelos.py` ✎ (recomendado)

En la colección `"pedidos"`, debajo de `"observaciones": jb_texto(255, True),` agregue:
```python
                # Suma de los subtotales, antes del descuento
                "subtotal": jb_decimal(),
                # Porcentaje de descuento: decimal de 0 a 50
                "porcentaje_descuento": {"bsonType": "decimal", "minimum": 0, "maximum": 50},
                # Valor del descuento en pesos, mayor o igual a 0
                "valor_descuento": jb_decimal(),
                # Motivo del descuento, opcional, máximo 150 caracteres
                "motivo_descuento": jb_texto(150, True),
```
y vuelva a crear las bases con los 3 comandos de [A3](#a3-comandos-del-día-a-día) para que MongoDB use la validación nueva.
> El descuento funciona aunque se salte este paso, porque los campos nuevos son opcionales y el `$jsonSchema` acepta campos adicionales. Con el paso 7, **la base de datos también impide** un descuento mayor a 50, aunque alguien lo intente desde Compass.

### Paso 8 — Probar en Swagger

La sección **Descuentos** aparece en http://localhost:8000/docs.

Para las pruebas necesita un cliente y dos productos: por ejemplo uno de 14000 y otro de 4000 ([A5](#a5-registrar-sus-datos-la-base-empieza-vacía)). Los valores de la tabla son con esos precios.

| # | Prueba | Resultado esperado |
|---|---|---|
| 1 | Login como CAJERO y **Authorize** | — |
| 2 | `POST /pedidos` con 2 unidades del producto de 14000 y 2 del de 4000 | **201**: `subtotal` 36000, `porcentaje_descuento` 0, `total` 36000. Anote el `id_pedido` |
| 3 | `PATCH /pedidos/{id_pedido}/descuento` con `{"porcentaje": 10, "motivo": "Descuento para aprendiz"}` | **200**: `valor_descuento` 3600, `total` 32400 |
| 4 | `PUT /pedidos/{id_pedido}` cambiando el producto de 4000 a cantidad 1 | **200**: `subtotal` 32000, `valor_descuento` 3200, `total` 28800 (el 10 % se conservó) |
| 5 | Descuento con `"porcentaje": 60` | **422** (máximo 50) |
| 6 | Descuento a un pedido ENTREGADO | **409** (RN05) |
| 7 | Descuento al pedido 999 | **404** |
| 8 | Login como COCINERO e intentar el descuento | **403** |
| 9 | Descuento con `"porcentaje": 0` | **200**: `total` vuelve al subtotal y `motivo_descuento` queda en `null` |

### Variantes que le pueden pedir

**A. Descuento en pesos en vez de porcentaje.**
- En `JbDescuentoPedido`, cambie `porcentaje` por `valor: JbDinero`. Importe `JbDinero` desde `app.schemas.jb_tipos`.
- En el servicio, calcule `jb_valor_descuento = min(jb_dinero(valor), jb_subtotal)` para que el descuento nunca supere el subtotal, y luego `total = subtotal - jb_valor_descuento`.

**B. Descuento automático según el tipo de cliente** (por ejemplo, aprendices 10 %, instructores 5 %). Esta variante va **en lugar de** escribir el porcentaje a mano. En `app/services/jb_pedido_service.py`:

1. Debajo de `JB_ESTADOS_CERRADOS = ...` agregue:
   ```python
   # Porcentaje de descuento de cada tipo de cliente
   JB_DESCUENTO_POR_TIPO = {"APRENDIZ": Decimal("10"), "INSTRUCTOR": Decimal("5")}


   # Devuelve el porcentaje de descuento que le toca a un cliente
   def jb_descuento_cliente(jb_id_cliente: int) -> Decimal:
       """Descuento automático según el tipo de cliente; los que no están en la tabla pagan completo."""
       # Busca el cliente
       jb_cliente = jb_cliente_repository.jb_buscar_por_id(jb_id_cliente)
       # Busca su tipo en la tabla; si no está, el descuento es 0
       return JB_DESCUENTO_POR_TIPO.get(jb_cliente["tipo_cliente"], Decimal("0"))
   ```
2. En `jb_crear`, cambie las dos líneas que puso en el paso 3b por:
   ```python
           # Subtotal, descuento según el tipo de cliente y total (RN01)
           **jb_calcular_totales(jb_total, jb_descuento_cliente(jb_datos["id_cliente"])),
   ```
3. ✅ Un pedido de un cliente APRENDIZ con subtotal 36000 queda con total **32400**. Uno de un cliente FUNCIONARIO no tiene descuento.

## H5. Ejemplo: agregar un campo (calorías a productos)

**Lo que pide el instructor:** *"Los productos deben guardar sus calorías."*

1. **Modelo.** En `app/models/jb_modelos.py`, colección `"productos"`, debajo de `"id_categoria": JB_ENTERO,`:
   ```python
                   # Calorías por porción: entero desde 0, o null si no se sabe
                   "calorias": {"bsonType": ["int", "long", "null"], "minimum": 0},
   ```
2. **Schema.** En `app/schemas/jb_producto_schema.py`:
   - En la clase `JbProductoCrear`, debajo de `id_categoria: int`:
     ```python
         # Calorías por porción, opcional, de 0 a 5000
         calorias: int | None = Field(default=None, ge=0, le=5000)
     ```
   - En la clase `JbProductoRespuesta`, debajo de `id_categoria: int`:
     ```python
         # Calorías, puede ser null
         calorias: int | None = None
     ```
   - `JbProductoActualizar` hereda de `JbProductoCrear`, así que recibe el campo sola.
3. **Base de datos:** vuelva a crear las bases ([A3](#a3-comandos-del-día-a-día)).
4. **Service, repository y router no cambian.** El router hace `jb_datos.model_dump()` y eso ya incluye `calorias`, y el repositorio guarda lo que recibe.
5. **Pruebas:**
   - `POST /productos` con `"calorias": 650` → 201 con `"calorias": 650`.
   - `"calorias": -5` → 422.
   - `GET` de un producto creado antes del cambio → `"calorias": null`.

> **Si el campo nuevo debe ser OBLIGATORIO**, quite el `= None` y póngalo en `"required"` del modelo. Los documentos que ya existen no lo tienen: vuelva a crear las bases (sus datos quedan en el respaldo) o agrégueles el campo uno por uno en Compass.

## H6. Ejemplo: endpoint de consulta (productos por rango de precio)

**Lo que pide el instructor:** *"Quiero consultar los productos entre dos precios."* Resultado: `GET /api/v1/productos/precio?minimo=3000&maximo=10000`

1. **Repository.** En `app/repositories/jb_producto_repository.py`:
   - Arriba, debajo del texto entre comillas triples (`"""Acceso a la colección productos."""`), agregue:
     ```python
     # Decimal: números exactos para comparar precios
     from decimal import Decimal
     ```
   - Dentro de la clase `JbProductoRepository`, debajo del método `jb_por_categoria`, agregue:
     ```python

         # Productos con precio entre un mínimo y un máximo, del más barato al más caro
         def jb_por_rango_precio(self, jb_minimo: Decimal, jb_maximo: Decimal) -> list[dict]:
             # $gte = mayor o igual, $lte = menor o igual; ordena por precio ascendente
             return self.jb_listar({"precio_venta": {"$gte": jb_minimo, "$lte": jb_maximo}}, [("precio_venta", 1)])
     ```
     `$gte` es "mayor o igual" y `$lte` es "menor o igual". Equivale a `WHERE precio_venta BETWEEN minimo AND maximo ORDER BY precio_venta`.
2. **Service.** Al final de `app/services/jb_producto_service.py`:
   ```python


   # Productos por rango de precio
   def jb_por_rango_precio(jb_minimo: Decimal, jb_maximo: Decimal) -> list[dict]:
       # Si el rango está al revés...
       if jb_minimo > jb_maximo:
           # ...responde 400
           raise jb_dato_invalido("El precio mínimo no puede ser mayor que el máximo")
       # Pide la consulta al repositorio
       return jb_producto_repository.jb_por_rango_precio(jb_minimo, jb_maximo)
   ```
3. **Router.** En `app/routers/jb_productos_router.py`:
   - Arriba, debajo del texto entre comillas triples, agregue:
     ```python
     # Decimal: números exactos para los precios
     from decimal import Decimal
     ```
   - En la línea `from fastapi import APIRouter, Depends, status` agregue `Query`: `from fastapi import APIRouter, Depends, Query, status`.
   - Pegue este endpoint **ANTES** del comentario `# GET /api/v1/productos/{id}: consulta uno`, que está encima de `@jb_router.get("/{id_producto}", ...`:
     ```python
     # GET /api/v1/productos/precio?minimo=...&maximo=...: va antes de /{id_producto}
     @jb_router.get("/precio", response_model=list[JbProductoRespuesta], dependencies=JB_TODOS,
                    summary="Productos por rango de precio", responses=JB_R400)
     # minimo y maximo vienen después del ?, son obligatorios y no pueden ser negativos
     def jb_productos_por_precio(minimo: Decimal = Query(ge=0), maximo: Decimal = Query(ge=0)):
         """Productos con precio de venta entre `minimo` y `maximo`. **Roles:** todos."""
         # Pide la consulta al servicio
         return jb_servicio.jb_por_rango_precio(minimo, maximo)


     ```
   > **¿Por qué ANTES?** FastAPI revisa las rutas en orden. Si `/{id_producto}` está primero, toma la palabra "precio" como si fuera un id, intenta convertirla en número y responde **422**.
4. **Pruebas:**
   - `?minimo=3000&maximo=10000` → 200 con los productos ordenados por precio.
   - `?minimo=10000&maximo=3000` → 400.
   - Sin parámetros → 422.

## H7. Ejemplo: cambiar los roles de un endpoint

**Lo que pide el instructor:** *"El cocinero también debe poder ver los clientes."*

- **Para todo un router**, en `app/routers/jb_clientes_router.py` cambie
  `dependencies=[Depends(jb_requiere_roles("ADMIN", "CAJERO"))]`
  por
  `dependencies=[Depends(jb_requiere_roles("ADMIN", "CAJERO", "COCINERO"))]`.
- **Para un solo endpoint**, cambie la lista `dependencies=...` de ese `@jb_router.get/post/...`. Por ejemplo, en categorías, `JB_ADMIN` → `JB_TODOS`.
- Actualice el texto `**Roles:** ...` del docstring, porque eso es lo que muestra Swagger, y la tabla [E2](#e2-endpoints-65).
- ✅ Prueba: login como COCINERO → `GET /clientes` debe dar 200 (antes daba 403).

## H8. Ejemplo: agregar un estado nuevo a los pedidos

**Lo que pide el instructor:** *"Agrega el estado LISTO (preparado, esperando entrega)."*

1. **Modelo.** En `jb_modelos.py`, en `"pedidos"`, agregue `"LISTO"` a la lista (y en el comentario de encima cambie "cuatro" por "cinco"):
   ```python
   "estado": {"enum": ["PENDIENTE", "EN_PREPARACION", "LISTO", "ENTREGADO", "ANULADO"]},
   ```
2. **Schema.** En `jb_pedido_schema.py`, agréguelo también:
   ```python
   JbEstadoPedido = Literal["PENDIENTE", "EN_PREPARACION", "LISTO", "ENTREGADO", "ANULADO"]
   ```
3. **Base de datos:** vuelva a crear las bases ([A3](#a3-comandos-del-día-a-día)). **Este paso es obligatorio**: sin él, MongoDB rechaza el valor nuevo y la API responde 400 "Los datos no cumplen la validación de la base de datos".
4. ✅ Pruebas:
   - `PATCH /pedidos/{id}/estado` con `{"estado": "LISTO"}` → 200.
   - `GET /pedidos/estado/LISTO` → aparece el pedido.

## H9. Ejemplo: sección nueva con CRUD completo (mesas)

**Lo que pide el instructor:** *"Haz una sección para administrar las mesas del restaurante."*

Se crean **4 archivos nuevos**, uno por capa, siguiendo el molde de categorías. Luego se toca el modelo y el main.

**1. Modelo.** En `app/models/jb_modelos.py`, al final de `JB_MODELOS`, justo antes de la `}` que lo cierra (antes del comentario `# Base de datos NoSQL`), agregue:
```python
    # Colección mesas
    "mesas": {
        # Validación de cada documento
        "esquema": jb_objeto(
            # Campos obligatorios
            ["_id", "numero", "capacidad", "estado"],
            # Regla de cada campo
            {
                # Identificador numérico (PK)
                "_id": JB_ENTERO,
                # Número de la mesa: entero de 1 a 200
                "numero": {"bsonType": ["int", "long"], "minimum": 1, "maximum": 200},
                # Cuántas personas caben: de 1 a 30
                "capacidad": {"bsonType": ["int", "long"], "minimum": 1, "maximum": 30},
                # Ubicación opcional, máximo 60 caracteres
                "ubicacion": jb_texto(60, True),
                # ACTIVO o INACTIVO
                "estado": JB_ESTADO,
            },
        ),
        # El número de mesa no se repite
        "indices": [(["numero"], True)],
    },
```

**2. `app/schemas/jb_mesa_schema.py`** ✚
```python
"""Esquemas de las mesas del restaurante."""
# BaseModel: clase base; ConfigDict: configuración del esquema; Field: reglas de un campo
from pydantic import BaseModel, ConfigDict, Field

# JbEstado: ACTIVO o INACTIVO; JbModeloEntrada: base de los esquemas de entrada
from app.schemas.jb_tipos import JbEstado, JbModeloEntrada


# Datos para crear una mesa
class JbMesaCrear(JbModeloEntrada):
    # Número de la mesa: de 1 a 200
    numero: int = Field(ge=1, le=200)
    # Capacidad: de 1 a 30 personas
    capacidad: int = Field(ge=1, le=30)
    # Ubicación opcional, máximo 60 caracteres
    ubicacion: str | None = Field(default=None, max_length=60)

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{"numero": 1, "capacidad": 4, "ubicacion": "Terraza"}]})


# Datos para modificar una mesa: los mismos de crear más el estado
class JbMesaActualizar(JbMesaCrear):
    # Estado; si no se envía queda ACTIVO
    estado: JbEstado = "ACTIVO"


# Mesa como la devuelve la API
class JbMesaRespuesta(BaseModel):
    # Id de la mesa
    id_mesa: int
    # Número
    numero: int
    # Capacidad
    capacidad: int
    # Ubicación, puede ser null
    ubicacion: str | None = None
    # ACTIVO o INACTIVO
    estado: JbEstado
```

**3. `app/repositories/jb_mesa_repository.py`** ✚. Hereda el CRUD completo de `JbRepositorioBase`.
```python
"""Acceso a la colección mesas."""
# Clase con el CRUD genérico
from app.repositories.jb_base_repository import JbRepositorioBase


# Repositorio de mesas: solo usa el CRUD heredado
class JbMesaRepository(JbRepositorioBase):
    # Constructor
    def __init__(self):
        # Colección "mesas"; el _id se responde como "id_mesa"
        super().__init__("mesas", "id_mesa")


# Instancia única que usa el servicio
jb_mesa_repository = JbMesaRepository()
```

**4. `app/services/jb_mesa_service.py`** ✚
```python
"""Reglas de negocio de las mesas."""
# Acceso a mesas
from app.repositories.jb_mesa_repository import jb_mesa_repository
# Respuestas y errores comunes
from app.services.jb_comun import jb_borrado_fisico, jb_no_encontrado


# Lista todas las mesas
def jb_listar() -> list[dict]:
    # Pide la lista al repositorio
    return jb_mesa_repository.jb_listar()


# Busca una mesa o responde 404
def jb_obtener(jb_id: int) -> dict:
    # Busca por id
    jb_mesa = jb_mesa_repository.jb_buscar_por_id(jb_id)
    # Si no existe...
    if jb_mesa is None:
        # ...responde 404
        raise jb_no_encontrado(f"La mesa {jb_id}")
    # Devuelve la mesa
    return jb_mesa


# Crea una mesa
def jb_crear(jb_datos: dict) -> dict:
    # Toda mesa nueva empieza ACTIVA
    jb_datos["estado"] = "ACTIVO"
    # La inserta (si el número ya existe, la API responde 409)
    return jb_mesa_repository.jb_insertar(jb_datos)


# Modifica una mesa
def jb_actualizar(jb_id: int, jb_datos: dict) -> dict:
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # Guarda los cambios y devuelve la mesa actualizada
    return jb_mesa_repository.jb_actualizar(jb_id, jb_datos)


# Elimina una mesa
def jb_eliminar(jb_id: int) -> dict:
    # Comprueba que exista (404 si no)
    jb_obtener(jb_id)
    # La borra
    jb_mesa_repository.jb_eliminar(jb_id)
    # Responde que se borró
    return jb_borrado_fisico(f"La mesa {jb_id}")
```

**5. `app/routers/jb_mesas_router.py`** ✚
```python
"""Endpoints de las mesas. Roles: ADMIN (consulta: ADMIN y CAJERO)."""
# APIRouter: agrupa endpoints; Depends: dependencias (seguridad); status: nombres de los códigos HTTP
from fastapi import APIRouter, Depends, status

# Respuestas de error que se documentan en Swagger
from app.core.jb_respuestas import JB_PRIVADO, JB_R404, JB_R409
# Dependencia que exige uno de los roles indicados
from app.core.jb_security import jb_requiere_roles
# Esquemas de mesas (lo que entra y lo que sale)
from app.schemas.jb_mesa_schema import JbMesaActualizar, JbMesaCrear, JbMesaRespuesta
# Esquema de la respuesta de los DELETE
from app.schemas.jb_tipos import JbResultadoEliminacion
# Servicio de mesas, con el nombre corto jb_servicio
from app.services import jb_mesa_service as jb_servicio

# Router: rutas /mesas, sección "Mesas" de Swagger
jb_router = APIRouter(prefix="/mesas", tags=["Mesas"], responses=JB_PRIVADO)
# Seguridad para consultar: ADMIN o CAJERO
JB_CONSULTA = [Depends(jb_requiere_roles("ADMIN", "CAJERO"))]
# Seguridad para crear, modificar y eliminar: solo ADMIN
JB_ADMIN = [Depends(jb_requiere_roles("ADMIN"))]


# GET /api/v1/mesas: lista todas
@jb_router.get("", response_model=list[JbMesaRespuesta], dependencies=JB_CONSULTA, summary="Listar mesas")
def jb_listar_mesas():
    """**Roles:** ADMIN, CAJERO."""
    # Pide la lista al servicio
    return jb_servicio.jb_listar()


# GET /api/v1/mesas/{id}: consulta una
@jb_router.get("/{id_mesa}", response_model=JbMesaRespuesta, dependencies=JB_CONSULTA,
               summary="Consultar una mesa", responses=JB_R404)
def jb_obtener_mesa(id_mesa: int):
    """**Roles:** ADMIN, CAJERO."""
    # Busca la mesa (404 si no existe)
    return jb_servicio.jb_obtener(id_mesa)


# POST /api/v1/mesas: crea una (201)
@jb_router.post("", response_model=JbMesaRespuesta, status_code=status.HTTP_201_CREATED, dependencies=JB_ADMIN,
                summary="Crear mesa", responses=JB_R409)
# El cuerpo se valida con JbMesaCrear
def jb_crear_mesa(jb_datos: JbMesaCrear):
    """El número de mesa no se repite (409). **Roles:** ADMIN."""
    # Convierte el esquema en diccionario y lo pasa al servicio
    return jb_servicio.jb_crear(jb_datos.model_dump())


# PUT /api/v1/mesas/{id}: modifica una
@jb_router.put("/{id_mesa}", response_model=JbMesaRespuesta, dependencies=JB_ADMIN,
               summary="Actualizar mesa", responses={**JB_R404, **JB_R409})
# Recibe el id de la URL y el cuerpo validado con JbMesaActualizar
def jb_actualizar_mesa(id_mesa: int, jb_datos: JbMesaActualizar):
    """**Roles:** ADMIN."""
    # Pasa el id y los datos al servicio
    return jb_servicio.jb_actualizar(id_mesa, jb_datos.model_dump())


# DELETE /api/v1/mesas/{id}: elimina una
@jb_router.delete("/{id_mesa}", response_model=JbResultadoEliminacion, dependencies=JB_ADMIN,
                  summary="Eliminar mesa", responses=JB_R404)
def jb_eliminar_mesa(id_mesa: int):
    """**Roles:** ADMIN."""
    # Pide al servicio que la elimine
    return jb_servicio.jb_eliminar(id_mesa)
```

**6. Registrar la sección en `app/jb_main.py`:**
- Agregue `jb_mesas_router,` en el bloque `from app.routers import (...)`, debajo de `jb_insumos_router,`.
- Agréguelo también en la lista `for jb_modulo in (...)`, debajo de `jb_calificaciones_router,`.
- En `JB_ETIQUETAS` agregue `{"name": "Mesas", "description": "Mesas del restaurante."},`.

**7. Crear la colección en MongoDB:** vuelva a crear las bases ([A3](#a3-comandos-del-día-a-día)). El script 01 debe mostrar `[OK] mesas: validación $jsonSchema + 1 índice(s)`.

**8. Pruebas:**
- `POST /mesas` con `{"numero": 1, "capacidad": 4, "ubicacion": "Terraza"}` → 201.
- Repetir el número → 409.
- `"capacidad": 0` → 422.
- El cajero hace `GET /mesas` → 200, pero `POST` → 403.

> **Si la mesa debe quedar ligada a los pedidos** (por ejemplo, un pedido tipo MESA guarda `id_mesa`), eso es un **campo nuevo** en pedidos: aplique [H5](#h5-ejemplo-agregar-un-campo-calorías-a-productos) y valide en `jb_pedido_service.jb_crear` que la mesa exista, igual que se valida el cliente en `jb_validar_cliente`.

## H10. Errores típicos al hacer cambios

| Lo que ve | Por qué pasa | Cómo se arregla |
|---|---|---|
| En la terminal: `NameError: name 'Decimal' is not defined` | Usó algo sin importarlo | Agregue el `import` arriba del archivo (`from decimal import Decimal`) |
| `ImportError: cannot import name 'JbDescuentoPedido'` | El nombre del `import` no coincide con la clase, o el archivo no se guardó | Revise mayúsculas y minúsculas y guarde con `Ctrl+S` |
| `IndentationError` | Mezcló espacios o tabulaciones | Use 4 espacios por nivel, alineado con el código de alrededor |
| La sección o el endpoint nuevo no aparece en Swagger | No registró el router en `jb_main.py`, o no recargó la página | Paso 6 de [H4](#h4-ejemplo-completo-sección-de-descuento-manual-en-pedidos) y `F5` en el navegador |
| 422 en una ruta fija nueva (`/productos/precio`) | Quedó debajo de `/{id_producto}` | Muévala arriba ([H6](#h6-ejemplo-endpoint-de-consulta-productos-por-rango-de-precio)) |
| 500 y en la terminal `ResponseValidationError` | La respuesta tiene un campo obligatorio que los documentos viejos no tienen | Póngale valor por defecto en el schema de respuesta (`= None`) |
| 400 "Los datos no cumplen la validación de la base de datos" | El `$jsonSchema` de MongoDB rechazó el dato | Revise `jb_modelos.py` y vuelva a crear las bases ([A3](#a3-comandos-del-día-a-día)) |
| El script 02 termina con `DuplicateKeyError` después de agregar un índice único | Los datos iniciales del 02 (`JB_ADMIN` o `JB_CATEGORIAS`) tienen valores repetidos en ese campo | Corríjalos en `02_jb_dml_datos_prueba.py` o quite `True` del índice |
| El cambio en `.env` no hace efecto | `--reload` solo vigila los `.py` | `Ctrl+C` y vuelva a ejecutar `uvicorn ...` |
