# EA4: qué tengo que hacer y paso a paso

Guía hecha a partir del instructivo EA4-Instructivo_Api_Rest_Gastronomia.pdf (11 páginas, incluida la Figura 1 con el modelo entidad-relación). No trae código: explica qué pide el instructivo, qué decisiones tienes que tomar y en qué orden hacer el trabajo.

- Fecha de esta guía: 26/10/2026
- Fecha de entrega: 28/10/2026

Cómo usar esta guía: las secciones 1 a 15 explican lo que pide el PDF. La sección 16 es el paso a paso. La 17 reúne lo que el PDF deja abierto y lo que te recomiendo decidir, la 18 las preguntas para el instructor y la 19 la lista de revisión final.

---

## 1. Datos de la actividad

| Dato | Lo que dice el PDF |
|---|---|
| Programa | Análisis y Desarrollo de Software |
| Ficha | 3312744 |
| Centro | Centro de Gestión y Desarrollo Sostenible Surcolombiano (CGDSS) |
| Competencia | Desarrollar la solución de software de acuerdo con el diseño y metodologías de desarrollo |
| Resultado de aprendizaje | Construir la base de datos para el software a partir del modelo de datos |
| Actividad | Transferencia del conocimiento: desarrollar la API REST con Python del proyecto formativo |
| Evidencia | EA4: construir el prototipo de una API REST con Python que haga CRUD a la base de datos de la Unidad Productiva de Gastronomía |
| Modalidad | Individual |
| Tipo de evidencia | Producto |
| Fechas | Inicio 14/10/2026, fin 28/10/2026 |
| Intensidad | 20 horas |

## 2. Qué te piden, en pocas palabras

Construir una API REST en Python, con FastAPI, para la Unidad Productiva de Gastronomía. La API tiene que:

1. Hacer CRUD (crear, consultar, actualizar y eliminar) de usuarios, categorías, productos, insumos, recetas, proveedores, compras, clientes, pedidos y calificaciones.
2. Guardar la información principal en MySQL, en la base de datos bd_gastronomia.
3. Guardar las calificaciones de los clientes en MongoDB, en la base de datos bd_gastronomia_nosql.
4. Proteger todos los endpoints con token JWT, menos el de iniciar sesión.
5. Dar permisos según el rol del usuario: ADMIN, CAJERO o COCINERO.
6. Cumplir las 6 reglas de negocio (RN01 a RN06).
7. Estar documentada en Swagger (/docs) y probada con una colección de Postman.

Aparte, como anexo obligatorio, tienes que documentar la base de datos en el Formato 6: Manual de Configuración de Base de Datos.

## 3. Qué tienes que entregar y cómo

| Entregable | Dónde va |
|---|---|
| Código fuente de la API | Repositorio de GitHub |
| Scripts de la base de datos (carpeta database/) | Repositorio de GitHub |
| Colección de Postman exportada, con pruebas de cada servicio | Repositorio de GitHub |
| docker-compose.yml, requirements.txt, .env.example y README.md | Repositorio de GitHub |
| Anexo: Manual de Configuración de Base de Datos (Formato 6) | Archivo aparte, subido al enlace que dé el instructor |
| Sustentación | Ante el instructor, llevando el enlace del repositorio de GitHub |

Importante: el archivo .env (contraseñas de las bases de datos y clave secreta del JWT) no se sube a GitHub. Lo que se sube es el .env.example, con los mismos nombres de variables pero sin datos reales.

## 4. El problema que vas a resolver

La unidad productiva elabora y vende platos, bebidas, panadería y repostería a aprendices, instructores, funcionarios y clientes externos, y atiende pedidos para eventos del centro. Hoy anota recetas, inventario, compras y ventas en cuadernos, hojas de cálculo y mensajes de WhatsApp. El líder de la unidad encontró estos problemas; al lado está lo que los resuelve:

| Problema | Lo resuelve |
|---|---|
| No hay control confiable del inventario de insumos (existencias, stock mínimo y vencimientos); hay faltantes y pérdidas por productos vencidos | RF07, RN02 y RN03 |
| Las recetas no están estandarizadas; no se sabe el costo de producción ni el margen de ganancia | RF05 y RF06 |
| Los pedidos llegan por varios medios y no se puede consultar su estado | RF10, RN01 y RN05 |
| No hay registro centralizado de las compras a cada proveedor | RF08 |
| No hay reportes de ventas por periodo ni de productos más vendidos | RF11 |
| No se conoce la opinión de los clientes | RF12 (MongoDB) |
| Cualquier persona manipula la información, sin control de acceso ni roles | RF01, RF02, JWT y roles |

Más adelante esta API la va a usar una aplicación web y una aplicación móvil. Por eso tiene que ser ordenada, segura y estar bien documentada.

## 5. Herramientas y recursos

Herramientas que pide el PDF:

- Docker Desktop, para correr MySQL y MongoDB en contenedores.
- MySQL 8 y MongoDB 7.
- MySQL Workbench, para ver la base de datos y sacar el modelo relacional.
- MongoDB Compass o Studio 3T, para ver la colección de calificaciones.
- Python 3.11 o superior.
- Visual Studio Code.
- Postman o Thunder Client.
- Git y GitHub.

Librerías de Python sugeridas: fastapi, uvicorn, sqlalchemy o pymysql, pymongo, pydantic, python-jose o PyJWT, passlib[bcrypt] y python-dotenv.

Recursos de apoyo que nombra el PDF: Guía de aprendizaje R4 (Construir la base de datos), Lista de chequeo EA4, Instructivo AA4 y diapositivas AA4 (API REST con Python), Formato 6 (Manual de Configuración de Base de Datos) y los requerimientos de la unidad productiva.

Consejo: consigue la Lista de chequeo EA4. Es con lo que te van a calificar, así que úsala para revisar tu trabajo antes de entregar.

## 6. Requerimientos funcionales (lo que la API debe hacer)

| Código | Lo que dice el PDF | Qué significa en la práctica |
|---|---|---|
| RF01 | Autenticar usuarios con correo y contraseña y generar un token JWT con su rol | POST /auth/login. Si el correo y la contraseña son correctos, la API devuelve un token que lleva adentro el rol del usuario |
| RF02 | Gestionar usuarios con roles ADMIN, CAJERO y COCINERO | CRUD de /usuarios, solo para ADMIN |
| RF03 | Gestionar categorías de productos (platos, bebidas, panadería, repostería, etc.) | CRUD de /categorias |
| RF04 | Gestionar productos con su precio de venta y categoría | CRUD de /productos; cada producto pertenece a una categoría |
| RF05 | Gestionar la receta (ficha técnica) de cada producto: insumos y cantidades | CRUD de /recetas; cada registro dice "este producto usa esta cantidad de este insumo" |
| RF06 | Calcular el costo de producción de un producto a partir de su receta | GET /productos/{id}/costo |
| RF07 | Gestionar insumos y consultar los que están por debajo del stock mínimo o próximos a vencer | CRUD de /insumos, más /insumos/stock-bajo y /insumos/por-vencer |
| RF08 | Gestionar proveedores y registrar compras de insumos con su detalle | CRUD de /proveedores y /compras; una compra tiene varios ítems (detalle_compra) |
| RF09 | Gestionar clientes por tipo: APRENDIZ, INSTRUCTOR, FUNCIONARIO o EXTERNO | CRUD de /clientes |
| RF10 | Registrar pedidos con su detalle y cambiar su estado | CRUD de /pedidos y PATCH /pedidos/{id}/estado |
| RF11 | Generar reporte de ventas por rango de fechas y de productos más vendidos | /reportes/ventas y /reportes/productos-mas-vendidos |
| RF12 | Registrar y consultar calificaciones de los clientes sobre pedidos y productos (MongoDB) | CRUD de /calificaciones y /calificaciones/producto/{id_producto} |

## 7. Reglas de negocio (lo que la API debe hacer cumplir)

| Regla | Lo que dice el PDF | Cómo se cumple, en palabras |
|---|---|---|
| RN01 | El subtotal de cada ítem del pedido es cantidad x precio_unitario y el total del pedido es la suma de los subtotales. Los calcula la API, no el cliente | Al crear un pedido, quien lo registra solo envía qué productos y cuántos. La API busca el precio de venta de cada producto, calcula los subtotales y el total, y los guarda |
| RN02 | Al registrar una compra, se incrementa el stock_actual de cada insumo comprado y se actualiza su costo_unitario | Al guardar la compra, en la misma operación se suma la cantidad comprada al stock del insumo y su costo_unitario pasa a ser el de esa compra |
| RN03 | Cuando un pedido cambia a ENTREGADO, se descuentan del inventario los insumos según la receta de cada producto. Si no hay existencias suficientes, error 409 | Por cada producto del pedido: cantidad de la receta x cantidad pedida. Primero se revisa que todo alcance; si algún insumo no alcanza, no se descuenta nada y se responde 409 |
| RN04 | No se puede eliminar un producto, insumo, cliente o proveedor que tenga movimientos asociados; en ese caso su estado pasa a INACTIVO (borrado lógico) | En el DELETE: si el registro tiene movimientos, se cambia el estado a INACTIVO; si no tiene, se puede borrar de verdad |
| RN05 | Un pedido ENTREGADO o ANULADO no puede modificarse | Antes de editar un pedido o cambiar su estado, se revisa el estado actual; si es ENTREGADO o ANULADO, se rechaza |
| RN06 | Las contraseñas se guardan cifradas con bcrypt y nunca se devuelven en las respuestas | La contraseña se cifra antes de guardarla y ninguna respuesta de la API incluye el campo password |

Qué cuenta como "movimiento" para RN04 (el PDF no lo detalla; esta es mi propuesta):

- Producto: aparece en algún pedido (detalle_pedido) o tiene receta.
- Insumo: aparece en alguna compra (detalle_compra) o en alguna receta.
- Cliente: tiene pedidos.
- Proveedor: tiene compras.

## 8. La base de datos

### 8.1 MySQL: bd_gastronomia

El PDF da estas tablas con tipos sugeridos y dice que puedes agregar campos o entidades si tu análisis lo justifica. Los campos marcados "(sale del diagrama)" no están en las tablas del texto, pero sí en la Figura 1.

usuarios

- id_usuario: INT, llave primaria, autoincremental
- identificacion: VARCHAR(20), único
- nombres y apellidos: VARCHAR(80) cada uno
- correo: VARCHAR(120), único; es el usuario para iniciar sesión
- password: VARCHAR(255), cifrada con bcrypt
- rol: ENUM con ADMIN, CAJERO, COCINERO
- estado: ENUM con ACTIVO, INACTIVO

categorias

- id_categoria: INT, llave primaria, autoincremental
- nombre: VARCHAR(60), único
- descripcion: VARCHAR(200)
- estado: ENUM con ACTIVO, INACTIVO

productos

- id_producto: INT, llave primaria, autoincremental
- codigo: VARCHAR(20), único; código interno
- nombre: VARCHAR(100)
- descripcion: TEXT
- precio_venta: DECIMAL(10,2), mayor que 0
- unidad_venta: VARCHAR(20); porción, unidad, libra, etc.
- id_categoria: INT, llave foránea a categorias
- estado: ENUM con DISPONIBLE, AGOTADO, INACTIVO

insumos

- id_insumo: INT, llave primaria, autoincremental
- nombre: VARCHAR(100), único
- unidad_medida: ENUM con g, kg, ml, l, lb, unidad
- stock_actual: DECIMAL(10,2), mayor o igual a 0
- stock_minimo: DECIMAL(10,2); nivel mínimo de alerta
- costo_unitario: DECIMAL(10,2); costo por unidad de medida
- fecha_vencimiento: DATE, puede ser nulo; vencimiento del lote actual
- estado: ENUM con ACTIVO, INACTIVO

recetas (ficha técnica)

- id_receta: INT, llave primaria, autoincremental
- id_producto: INT, llave foránea a productos
- id_insumo: INT, llave foránea a insumos
- cantidad: DECIMAL(10,3); cantidad del insumo por cada unidad del producto

proveedores

- id_proveedor: INT, llave primaria, autoincremental
- nit: VARCHAR(20), único; NIT o documento
- razon_social: VARCHAR(120)
- telefono y correo: VARCHAR
- direccion: VARCHAR(150)
- estado: ENUM con ACTIVO, INACTIVO

compras

- id_compra: INT, llave primaria, autoincremental
- numero_factura: VARCHAR(30); factura del proveedor
- fecha_compra: DATETIME
- id_proveedor: INT, llave foránea a proveedores
- id_usuario: INT, llave foránea a usuarios; quien registra la compra
- total: DECIMAL(12,2)

detalle_compra

- id_detalle_compra: llave primaria (sale del diagrama)
- id_compra: llave foránea a compras (sale del diagrama)
- id_insumo: llave foránea a insumos
- cantidad, costo_unitario y subtotal

clientes

- id_cliente: INT, llave primaria, autoincremental
- identificacion: VARCHAR(20), único
- nombres y apellidos: VARCHAR(80) cada uno
- telefono y correo: VARCHAR
- tipo_cliente: ENUM con APRENDIZ, INSTRUCTOR, FUNCIONARIO, EXTERNO

pedidos

- id_pedido: INT, llave primaria, autoincremental
- fecha_pedido: DATETIME; fecha y hora del pedido
- id_cliente: INT, llave foránea a clientes
- id_usuario: INT, llave foránea a usuarios; quien registra el pedido
- tipo_pedido: ENUM con MESA, PARA_LLEVAR, EVENTO
- estado: ENUM con PENDIENTE, EN_PREPARACION, ENTREGADO, ANULADO
- total: DECIMAL(12,2); lo calcula la API
- observaciones (sale del diagrama)

detalle_pedido

- id_detalle: llave primaria (sale del diagrama)
- id_pedido: llave foránea a pedidos (sale del diagrama)
- id_producto: llave foránea a productos
- cantidad, precio_unitario y subtotal

En total son 11 tablas. El PDF no da los tipos de las tablas de detalle: usa DECIMAL para cantidades y dinero, igual que en las demás.

### 8.2 MongoDB: bd_gastronomia_nosql, colección calificaciones

Campos del documento de ejemplo que trae el PDF:

| Campo | Qué guarda | Ejemplo del PDF |
|---|---|---|
| id_pedido | Número del pedido en MySQL | 125 |
| id_cliente | Número del cliente en MySQL | 18 |
| fecha | Fecha y hora de la calificación | 20/10/2026 a las 12:30 |
| calificacion_servicio | Nota del servicio | 5 |
| comentario | Texto libre del cliente | Excelente atención y buen sabor |
| productos | Lista de productos calificados; cada uno con id_producto, nombre y calificacion | Almuerzo ejecutivo con 5, Jugo de lulo con 4 |

Por qué id_pedido e id_cliente son números de MySQL: así se une la calificación con el pedido y el cliente aunque estén guardados en motores distintos.

Por qué MongoDB para las calificaciones: cada calificación trae una lista de productos de tamaño variable y un comentario libre. En MongoDB eso se guarda como un solo documento, sin tablas extra ni uniones. Este argumento te sirve para la "Justificación del motor seleccionado" del anexo.

### 8.3 Relaciones (Figura 1 del PDF)

- Una categoría agrupa muchos productos (1:N).
- Un producto se elabora con muchos insumos y un insumo se usa en muchos productos (N:M). Se resuelve con la tabla recetas.
- Un cliente hace muchos pedidos (1:N).
- Un usuario registra muchos pedidos (1:N).
- Un pedido tiene muchos productos y un producto está en muchos pedidos (N:M). Se resuelve con detalle_pedido.
- Un proveedor tiene muchas compras (1:N).
- Un usuario registra muchas compras (1:N). Esta relación aparece en el diagrama.
- Una compra tiene muchos insumos y un insumo está en muchas compras (N:M). Se resuelve con detalle_compra.

El PDF dice que este modelo es una propuesta inicial que tú debes validar y ajustar. En la sección 17 están los ajustes que te recomiendo.

## 9. Endpoints

Todos van con el prefijo /api/v1. Por ejemplo, la ruta completa de productos es /api/v1/productos.

### 9.1 Autenticación

| Método | Ruta | Para qué | Quién lo usa |
|---|---|---|---|
| POST | /auth/login | Inicia sesión y devuelve el token JWT | Público (es el único endpoint público) |
| POST | /auth/registro | Registra un usuario | Solo ADMIN |
| GET | /auth/perfil | Devuelve los datos del usuario autenticado | Cualquier usuario con token |

### 9.2 CRUD básico

Cada recurso tiene los cinco servicios: GET /recurso (listar), GET /recurso/{id} (consultar uno), POST /recurso (crear), PUT /recurso/{id} (actualizar) y DELETE /recurso/{id} (eliminar).

| Recurso | Ruta base | Roles permitidos |
|---|---|---|
| Usuarios | /usuarios | ADMIN |
| Categorías | /categorias | ADMIN (consultar: todos) |
| Productos | /productos | ADMIN (consultar: todos) |
| Insumos | /insumos | ADMIN, COCINERO |
| Recetas | /recetas | ADMIN, COCINERO |
| Proveedores | /proveedores | ADMIN |
| Compras | /compras | ADMIN |
| Clientes | /clientes | ADMIN, CAJERO |
| Pedidos | /pedidos | ADMIN, CAJERO (cambio de estado: COCINERO) |
| Calificaciones (MongoDB) | /calificaciones | ADMIN, CAJERO |

"Consultar: todos" quiere decir que los GET los puede usar cualquier usuario con token válido, pero crear, actualizar y eliminar es solo para ADMIN.

### 9.3 Consultas y procesos de negocio

| Método | Ruta | Qué hace |
|---|---|---|
| GET | /productos/categoria/{id_categoria} | Productos de una categoría |
| GET | /productos/{id}/receta | Insumos y cantidades de la receta de un producto |
| GET | /productos/{id}/costo | Costo de producción (suma de cantidad x costo_unitario) y margen frente al precio de venta |
| GET | /insumos/stock-bajo | Insumos con stock_actual menor o igual a stock_minimo |
| GET | /insumos/por-vencer?dias=7 | Insumos que vencen en los próximos N días |
| GET | /proveedores/{id}/compras | Historial de compras a un proveedor |
| GET | /clientes/{id}/pedidos | Historial de pedidos de un cliente |
| GET | /pedidos/estado/{estado} | Pedidos filtrados por estado |
| PATCH | /pedidos/{id}/estado | Cambia el estado del pedido (aplica RN03 y RN05) |
| GET | /reportes/ventas?desde=&hasta= | Total vendido y número de pedidos en un rango de fechas |
| GET | /reportes/productos-mas-vendidos?limite=10 | Ranking de los productos más vendidos |
| GET | /calificaciones/producto/{id_producto} | Calificaciones y promedio de un producto (MongoDB) |

El PDF los da "como punto de partida": puedes agregar más si los necesitas.

### 9.4 Cuántos endpoints son

3 de autenticación + 50 del CRUD (10 recursos x 5 servicios) + 12 de consultas = 65 endpoints. Todos deben quedar documentados en Swagger y probados en Postman.

## 10. Arquitectura y estructura del proyecto

La API se hace con FastAPI y con arquitectura por capas. Cada capa tiene un solo trabajo:

| Capa | Carpeta | Qué hace | Ejemplo en este proyecto |
|---|---|---|---|
| Rutas (controladores) | app/routers | Reciben la petición HTTP, exigen el token y el rol, y llaman al servicio | La ruta para crear un pedido |
| Servicios | app/services | Aplican las reglas de negocio RN01 a RN06 | Calcular subtotales y total del pedido |
| Repositorios | app/repositories | Hacen las consultas a la base de datos | Guardar el pedido en MySQL |
| Modelos | app/models | Representan las tablas | La tabla pedidos |
| Esquemas | app/schemas | Validan los datos que entran y salen (Pydantic) | Que la cantidad sea mayor que 0 |
| Núcleo | app/core | Configuración y seguridad (JWT y bcrypt) | Crear y verificar el token |
| Conexiones | app/database | Conexión a MySQL y a MongoDB | Abrir la conexión con el usuario de la API |

Por qué por capas: si mañana cambia una regla de negocio, solo tocas el servicio; si cambia la base de datos, solo tocas los repositorios. Es como en una cocina: el mesero (ruta) toma el pedido, el chef (servicio) decide cómo prepararlo y el encargado de la despensa (repositorio) trae los ingredientes. Ninguno hace el trabajo del otro.

Estructura mínima que sugiere el PDF (recuerda que los nombres deben llevar tu inicial, ver sección 14):

- api_gastronomia/
  - app/
    - main.py: punto de entrada
    - core/: config.py y security.py (JWT y bcrypt)
    - database/: conexion_mysql.py y conexion_mongo.py
    - models/: modelos de las tablas
    - schemas/: validaciones con Pydantic
    - repositories/: consultas a la base de datos
    - services/: reglas de negocio RN01 a RN06
    - routers/: endpoints por recurso
  - database/
    - 01_ddl_bd_gastronomia.sql
    - 02_dml_datos_prueba.sql
    - 03_dcl_usuarios.sql
    - 04_mongo_calificaciones.js
  - docker-compose.yml: levanta MySQL y MongoDB
  - requirements.txt
  - .env.example: sin credenciales reales
  - README.md

## 11. Seguridad (obligatoria)

El sistema maneja datos de clientes, ventas y costos, por eso el PDF exige:

1. Todos los endpoints son privados, menos /auth/login.
2. El token se envía en el encabezado Authorization, con la palabra Bearer, un espacio y el token.
3. El token tiene tiempo de expiración.
4. Los permisos se validan por rol: la API responde 401 si no hay token o si es inválido, y 403 si el rol no tiene permiso.
5. Las credenciales de las bases de datos y la clave secreta del JWT van en el archivo .env, que no se sube a GitHub.
6. La API se conecta a MySQL con un usuario propio de privilegios mínimos, creado con comandos DCL. Nunca con root.
7. Las contraseñas se guardan cifradas con bcrypt y nunca se devuelven (RN06).

## 12. Validaciones y códigos HTTP

El PDF pide validar los datos de entrada y responder con códigos adecuados: nombra 400, 404, 409, 422 y 500, más 401 y 403 en la parte de seguridad. Cuándo usar cada uno en este proyecto:

| Código | Cuándo |
|---|---|
| 200 | La consulta o la actualización salió bien |
| 201 | Se creó un registro |
| 400 | La petición no tiene sentido para el negocio; por ejemplo, en el reporte la fecha "desde" es posterior a "hasta" |
| 401 | No hay token, el token es inválido o ya venció, o el correo o la contraseña del login están mal |
| 403 | El token es válido pero el rol no tiene permiso |
| 404 | El registro no existe |
| 409 | Conflicto: dato único repetido (correo, identificación, código, NIT, nombre), stock insuficiente al entregar un pedido (RN03) o intento de modificar un pedido ENTREGADO o ANULADO (RN05) |
| 422 | Datos con formato inválido: falta un campo, tipo equivocado, calificación fuera de 1 a 5, precio en 0 o negativo. FastAPI lo hace solo con los esquemas de Pydantic |
| 500 | Error inesperado del servidor; se responde sin mostrar detalles internos |

## 13. Documentación: Swagger y Postman

1. Swagger (/docs): cada endpoint con descripción, parámetros, cuerpo de la petición, respuestas y códigos de estado. FastAPI genera la base solo; tú agregas las descripciones, los ejemplos y los códigos de respuesta.
2. Postman: la colección se exporta y se guarda en el repositorio, con pruebas de cada servicio.

## 14. Regla del nombre: tu inicial en todo

El PDF dice: "Todos los archivos, variables, clases, funciones, rutas y controladores deben tener en el nombre la letra inicial del nombre del aprendiz". El ejemplo para Wilson es w_productos_router.py y w_obtener_productos().

Cómo aplicarla:

- Archivos .py: w_main.py, w_config.py, w_productos_router.py, w_productos_service.py, etc.
- Funciones, clases y variables también llevan la inicial, por ejemplo w_obtener_productos.
- Los archivos que las herramientas buscan por su nombre exacto se quedan igual: requirements.txt, docker-compose.yml, .env, .env.example y README.md.
- Si la inicial también va en las rutas de la URL o en los scripts de database/, pregúntaselo al instructor (está en la sección 18).

Define tu inicial desde el principio. Cambiarla al final obliga a renombrar todo el proyecto.

## 15. Anexo: Manual de Configuración de Base de Datos (Formato 6)

Se entrega como archivo aparte y se sube al enlace del instructor. Debe tener estas 12 secciones:

| Sección del formato | Qué debe contener |
|---|---|
| Historial de revisión y cambios | Versión, fechas y responsables de elaboración (tú), revisión (instructor) y aprobación (líder de la unidad productiva) |
| Introducción | Propósito de la base de datos y su relación con la API REST de la unidad |
| Alcance | Procesos cubiertos (recetas, inventario, compras, pedidos, ventas y calificaciones) y lo que queda fuera del prototipo |
| Responsables e involucrados | Aprendiz (responsable), instructor (revisor) y líder de la unidad productiva (involucrado), con su rol |
| Modelo Entidad Relación (MER) | Diagrama completo con entidades, atributos, llaves y cardinalidades, hecho en MySQL Workbench, draw.io o similar |
| Diccionario de datos | Por cada tabla: campo, tipo, tamaño, nulo, llave (PK, FK, UQ), valor por defecto, restricción CHECK y descripción. Incluir la estructura de la colección de MongoDB |
| Modelo relacional | Modelo físico generado desde MySQL Workbench con ingeniería inversa, mostrando tablas, tipos y relaciones |
| Justificación del motor seleccionado | Comparación de MySQL con PostgreSQL, SQL Server y Oracle, y por qué se usa MongoDB para las calificaciones |
| Requisitos de configuración | Herramientas y versiones: Docker, imágenes de MySQL y MongoDB, clientes (Workbench, Compass o Studio 3T), Python y librerías |
| Scripts | DDL (base de datos, tablas, llaves, índices y restricciones), DML (mínimo 10 registros de prueba por tabla principal), DCL (usuario de la API con privilegios mínimos) y script de MongoDB con validación $jsonSchema |
| Configuración y ejecución de la base de datos | Paso a paso: levantar los contenedores, ejecutar los scripts y evidenciar la creación (SHOW TABLES, DESCRIBE, consultas) con capturas que muestren fecha y hora |
| Otras consideraciones | Charset utf8mb4, zona horaria America/Bogota, respaldo y restauración (mysqldump y mongodump) y manejo seguro de credenciales |

El PDF trae un ejemplo de diccionario de datos para la tabla productos con estas columnas: Campo, Tipo, Nulo, Llave, Defecto o Restricción, y Descripción. Por ejemplo: precio_venta es DECIMAL(10,2), no nulo, con la restricción CHECK de que sea mayor que 0; y estado es ENUM, no nulo, con valor por defecto DISPONIBLE. Haz una tabla así para cada una de las 11 tablas.

---

## 16. Paso a paso para hacerlo

Te quedan 2 días: hoy es 26/10/2026 y la entrega es el 28/10/2026. Sigue las fases en orden, porque cada una se apoya en la anterior. No dejes el anexo para el último momento: es obligatorio y se entrega aparte. Ve llenándolo mientras avanzas, porque varias fases te dejan capturas y textos que van directo al anexo.

Al final de cada fase está el punto de control ("Listo cuando"). No pases a la siguiente fase sin cumplirlo.

### Fase 0. Antes de empezar

1. Lee esta guía completa y vuelve a mirar el PDF.
2. Consigue la Lista de chequeo EA4 y la plantilla del Formato 6.
3. Define tu inicial para los nombres.
4. Envía al instructor las preguntas de la sección 18.

Listo cuando: tienes la lista de chequeo, la plantilla del anexo y tu inicial definida.

### Fase 1. Preparar el equipo

1. Instala Docker Desktop. En Windows usa WSL 2 y necesita la virtualización activada en la BIOS.
2. Instala o verifica: Python 3.11 o superior, Visual Studio Code, Git, Postman, MySQL Workbench y MongoDB Compass.
3. Si ya tienes MySQL o MongoDB instalados en Windows como servicio, ocupan los mismos puertos que usarán los contenedores (3306 y 27017). Detén esos servicios o configura otros puertos en Docker.
4. Ten lista tu cuenta de GitHub.

Por qué Docker: no instalas MySQL ni MongoDB directamente en Windows, y cualquier persona (el instructor, por ejemplo) levanta exactamente las mismas bases con un solo archivo.

Listo cuando: Docker Desktop abre sin errores y todas las herramientas están instaladas.

### Fase 2. Crear el repositorio y la estructura

1. Crea la carpeta api_gastronomia con las carpetas de la sección 10.
2. Inicia Git en la carpeta, crea el repositorio en GitHub y conéctalos.
3. Antes del primer commit, crea el archivo .gitignore y pon en él el .env, la carpeta del entorno virtual y las carpetas de caché de Python. Por qué: si el .env se sube una sola vez, las contraseñas quedan guardadas en el historial de Git aunque después lo borres.
4. Crea el entorno virtual de Python, actívalo e instala las librerías. Anótalas con su versión en requirements.txt.
5. Crea el .env con tus valores reales y el .env.example con los mismos nombres de variables pero valores de ejemplo. Vas a necesitar: servidor, puerto, usuario, contraseña y nombre de la base de MySQL (el usuario de la API, no root); dirección y nombre de la base de MongoDB; clave secreta del JWT, algoritmo y minutos de vigencia del token.

Listo cuando: el repositorio está en GitHub con la estructura, y el .env no aparece en GitHub.

### Fase 3. Levantar MySQL y MongoDB con Docker

1. Escribe el docker-compose.yml con dos servicios: MySQL 8 y MongoDB 7.
2. En MySQL configura: contraseña de root tomada de variables de entorno (no escrita en el archivo), charset utf8mb4, zona horaria America/Bogota, puerto y un volumen.
3. En MongoDB configura: puerto y volumen.
4. Levanta los contenedores.
5. Conéctate a MySQL con Workbench y a MongoDB con Compass.

Por qué el volumen: sin volumen, si borras el contenedor pierdes todos los datos.

Listo cuando: Workbench y Compass se conectan. Toma una captura donde se vean la fecha y la hora; va para el anexo.

### Fase 4. Validar y ajustar el modelo de datos

1. Revisa la Figura 1 del PDF y las tablas de la sección 8.
2. Aplica los ajustes de la sección 17 (estado en clientes, observaciones en pedidos, restricciones, valores por defecto e índices).
3. Dibuja el MER final en MySQL Workbench o draw.io: entidades, atributos, llaves y cardinalidades.

Por qué antes de los scripts: el script DDL sale de este modelo. Si el modelo está mal, todo lo que sigue sale mal.

Listo cuando: tienes el MER final guardado como imagen para el anexo.

### Fase 5. Scripts de la carpeta database/

1. Script 01, DDL: crea la base bd_gastronomia con utf8mb4 y las 11 tablas, con llaves primarias, foráneas, campos únicos, índices, CHECK, ENUM y valores por defecto. Crea primero las tablas que no dependen de otras (usuarios, categorias, insumos, proveedores, clientes) y después las demás (productos, recetas, compras, detalle_compra, pedidos, detalle_pedido). Por qué ese orden: una llave foránea no se puede crear si la tabla a la que apunta todavía no existe.
2. Script 02, DML: mínimo 10 registros de prueba por tabla principal (para no tener dudas, pon 10 o más en cada tabla). Que sean coherentes:
   - Al menos un usuario por rol: ADMIN, CAJERO y COCINERO.
   - Las contraseñas de los usuarios ya cifradas con bcrypt. Si guardas texto plano, el login no funciona y además incumples RN06.
   - Totales de pedidos y compras que cuadren con su detalle (RN01).
   - Recetas que usen insumos que existan.
   - Algunos insumos con stock bajo y otros por vencer, para poder probar esas consultas.
   - Pedidos en los cuatro estados.
3. Script 03, DCL: crea el usuario de la API con permiso solo para consultar, insertar, actualizar y eliminar datos (SELECT, INSERT, UPDATE y DELETE) en bd_gastronomia. Sin permisos para crear o borrar tablas y sin acceso a otras bases. Por qué: si alguien roba esas credenciales, el daño queda limitado.
4. Script 04, MongoDB: crea la base bd_gastronomia_nosql y la colección calificaciones con validación $jsonSchema (campos obligatorios, tipos de dato, calificaciones entre 1 y 5), índices por id_pedido y por el id_producto de la lista productos, y documentos de prueba que correspondan a pedidos ENTREGADO del DML. El documento de ejemplo del PDF usa el pedido 125 y el cliente 18: si lo incluyes, esos números tienen que existir en tu DML, o cámbialos. Lo puedes ejecutar con mongosh, que viene dentro del contenedor de MongoDB, o pegando su contenido en la terminal mongosh de Compass. Por qué el validador: así MongoDB rechaza documentos mal formados aunque alguien los inserte sin pasar por la API.
5. Ejecuta los 4 scripts en orden y deja evidencia: SHOW TABLES, DESCRIBE de cada tabla, consultas a los datos y la colección con su validador en Compass. Capturas con fecha y hora visibles.

Listo cuando: puedes borrar las bases, volver a ejecutar los 4 scripts y todo queda igual. Así sabes que el instructor también va a poder montarla.

### Fase 6. Esqueleto de la API

1. En core, la configuración que lee las variables del .env.
2. En database, la conexión a MySQL (con el usuario de la API, no root) y la conexión a MongoDB.
3. En el punto de entrada (main), crea la aplicación FastAPI con título, descripción y versión, y registra los routers con el prefijo /api/v1.
4. Arranca la API con uvicorn y abre /docs en el navegador.

Listo cuando: /docs abre y la API se conecta a las dos bases sin errores.

### Fase 7. Seguridad (antes que los CRUD)

Por qué primero: todos los endpoints la necesitan. Si la dejas para el final, tienes que volver a tocar todas las rutas.

1. Funciones para cifrar una contraseña con bcrypt y para verificarla.
2. Funciones para crear el token JWT (con el id del usuario, su rol y la fecha de vencimiento) y para verificarlo.
3. Una dependencia de "usuario actual": lee el encabezado Authorization, valida el token y busca al usuario. Si no hay token, es inválido, ya venció o el usuario está INACTIVO, responde 401.
4. Una dependencia de roles: recibe la lista de roles permitidos y responde 403 si el rol del usuario no está en esa lista.
5. Los tres endpoints de /auth: login (público), registro (solo ADMIN) y perfil (cualquier usuario con token).
6. Configura Swagger para que el botón Authorize funcione con el token.

Listo cuando: en /docs haces login con el ADMIN del DML y recibes el token; /auth/perfil responde 200 con token y 401 sin token; y ninguna respuesta muestra la contraseña.

### Fase 8. CRUD de los 10 recursos

Hazlos en este orden, porque unos dependen de otros: usuarios, categorías, productos, insumos, recetas, proveedores, clientes, compras, pedidos y calificaciones.

Para cada recurso, la misma receta:

1. Esquemas: uno para crear, uno para actualizar y uno para responder. El de respuesta de usuarios no lleva password.
2. Repositorio: listar, buscar por id, insertar, actualizar y eliminar o inactivar.
3. Servicio: validaciones de negocio (que la categoría exista, que el código no se repita, RN04 al eliminar, etc.).
4. Router: los 5 endpoints con sus roles, códigos de respuesta y documentación.
5. Pruébalo en /docs antes de pasar al siguiente recurso.

Lo particular de cada recurso:

- Usuarios: cifrar la contraseña al crear y al cambiarla; correo e identificación únicos (409); al eliminar, inactivar si ya registró pedidos o compras.
- Categorías: nombre único; los GET son para todos los roles y lo demás solo para ADMIN.
- Productos: precio_venta mayor que 0; la categoría debe existir; RN04 al eliminar.
- Insumos: unidad de medida válida; stock no negativo; RN04 al eliminar.
- Recetas: el producto y el insumo deben existir; cantidad mayor que 0; no repetir el mismo insumo en la receta del mismo producto.
- Proveedores: NIT único; RN04 al eliminar.
- Clientes: tipo de cliente válido; identificación única; RN04 al eliminar.
- Compras: se crean con su detalle (insumo, cantidad y costo unitario). La API calcula subtotales y total, toma del token el usuario que registra y aplica RN02, todo en una sola transacción. Para el PUT y el DELETE, mira la sección 17.
- Pedidos: se crean con su detalle, enviando solo producto y cantidad. La API toma el precio de venta actual de cada producto, calcula subtotales y total (RN01), toma del token el usuario que registra y crea el pedido en estado PENDIENTE. El PUT solo funciona si el pedido no está ENTREGADO ni ANULADO (RN05). Para el DELETE, mira la sección 17.
- Calificaciones: van a MongoDB. Valida que el pedido exista en MySQL y esté ENTREGADO, que el cliente sea el del pedido y que los productos calificados estén en ese pedido. El {id} de estas rutas es el identificador de MongoDB (24 caracteres); si llega con otro formato, responde con un error claro.

Listo cuando: cada recurso responde bien a sus 5 servicios y respeta los roles (prueba al menos un rol permitido y uno no permitido).

### Fase 9. Consultas y procesos de negocio

1. Productos por categoría: si la categoría no existe, 404.
2. Receta de un producto: insumos, cantidades y unidad de medida.
3. Costo de un producto (RF06): costo = suma de (cantidad de la receta x costo_unitario actual del insumo). Margen = precio de venta menos costo, y también en porcentaje sobre el precio de venta. Decide qué responder si el producto no tiene receta (por ejemplo, 404 con un mensaje claro).
4. Stock bajo: insumos activos con stock_actual menor o igual a stock_minimo.
5. Por vencer: insumos con fecha de vencimiento entre hoy y hoy más N días. N vale 7 si no lo envían y no puede ser negativo.
6. Compras de un proveedor y pedidos de un cliente: 404 si el proveedor o el cliente no existe.
7. Pedidos por estado: si el estado no es uno de los cuatro válidos, 422.
8. Cambio de estado (PATCH): primero RN05 (si está ENTREGADO o ANULADO, 409). Si el nuevo estado es ENTREGADO, aplica RN03 dentro de una transacción: calcula todo lo que se necesita, verifica que alcance y descuenta; si algo no alcanza, 409 sin descontar nada. Si dos productos del pedido usan el mismo insumo, suma lo que necesitan los dos antes de compararlo con el stock.
9. Reporte de ventas: desde y hasta son obligatorios; si desde es posterior a hasta, 400. Cuenta solo pedidos ENTREGADO. Ojo: si hasta es una fecha sin hora, tiene que incluir todo ese día.
10. Productos más vendidos: suma de cantidades por producto en pedidos ENTREGADO, de mayor a menor, hasta el número que diga "limite" (10 si no lo envían).
11. Calificaciones de un producto: busca en MongoDB los documentos donde ese producto aparece en la lista productos y devuelve las calificaciones y el promedio.

Listo cuando: cada consulta devuelve resultados correctos con los datos de prueba. Compara una o dos a mano en Workbench.

### Fase 10. Errores y validaciones

1. Usa el mismo formato de error en toda la API (siempre el mismo campo con el mensaje).
2. Maneja los códigos de la sección 12.
3. Los errores 500 no deben mostrar detalles internos al cliente; regístralos en la consola.
4. Revisa una vez más que password no aparezca en ninguna respuesta.

Listo cuando: provocaste a propósito cada código de error y todos responden con el mismo formato.

### Fase 11. Documentación en Swagger

Para cada endpoint: resumen, descripción (incluye qué roles lo pueden usar), descripción de cada parámetro, ejemplo del cuerpo y las respuestas posibles con su código. Agrupa los endpoints por recurso con etiquetas.

Listo cuando: alguien que no conoce tu proyecto entiende cada endpoint solo leyendo /docs.

### Fase 12. Colección de Postman

1. Crea un entorno con variables: la dirección base de la API y el token.
2. Configura la petición de login para que guarde el token en la variable automáticamente.
3. Haz una carpeta por recurso con todas sus peticiones: los 65 endpoints.
4. En cada petición agrega pruebas: el código de estado esperado y los campos importantes de la respuesta.
5. Agrega casos negativos: sin token (401), rol sin permiso (403), id que no existe (404), dato repetido (409), dato inválido (422), stock insuficiente (409) y modificar un pedido entregado (409).
6. Ordena las peticiones para que la colección cree sus propios datos antes de usarlos y elimine al final lo que creó. Así se puede correr varias veces seguidas.
7. Corre la colección completa con el Collection Runner.
8. Exporta la colección en formato JSON (Collection v2.1) y guárdala en el repositorio. Si exportas también el entorno, que no lleve contraseñas reales.

Listo cuando: el archivo de la colección está en el repositorio y el Runner pasa todas las pruebas.

### Fase 13. README.md

Escribe en el README: qué es el proyecto, tecnologías, requisitos, cómo levantar las bases con Docker, cómo ejecutar los scripts, cómo crear el .env a partir del .env.example, cómo arrancar la API, usuarios de prueba por rol, lista de endpoints, cómo usar la colección de Postman y tus datos (nombre y ficha).

Listo cuando: otra persona puede montar el proyecto siguiendo solo el README.

### Fase 14. Anexo: Formato 6

Llena las 12 secciones de la sección 15 de esta guía. Ya tienes buena parte: el MER de la fase 4, los scripts y las capturas de la fase 5, y las versiones de las herramientas de la fase 1. Te falta:

1. El diccionario de datos de las 11 tablas y de la colección de MongoDB.
2. El modelo relacional con ingeniería inversa en Workbench.
3. La comparación de MySQL con PostgreSQL, SQL Server y Oracle (por ejemplo: licencia y costo, facilidad de uso, rendimiento, imagen oficial de Docker y soporte en Python) y la justificación de MongoDB para las calificaciones.
4. Un respaldo y una restauración de prueba con mysqldump y mongodump (y mongorestore), con capturas.

Listo cuando: las 12 secciones están completas y tienen capturas con fecha y hora.

### Fase 15. Prueba final y entrega

1. Revisa la Lista de chequeo EA4 punto por punto.
2. Clona tu repositorio en otra carpeta y sigue tu README desde cero: contenedores, scripts, .env, API y Postman. Si algo falla, corrígelo. Por qué: es exactamente lo que va a hacer el instructor.
3. Confirma que el .env no está en GitHub y que el .env.example sí.
4. Sube el anexo al enlace del instructor.
5. Envía el enlace del repositorio.

### Fase 16. Sustentación

Prepara una demostración en este orden:

1. Contenedores arriba y las bases abiertas en Workbench y Compass.
2. La estructura del proyecto y qué hace cada capa.
3. /docs con todos los endpoints documentados.
4. Login con cada rol, y un 401 y un 403.
5. Crear un pedido y mostrar que la API calculó subtotales y total (RN01).
6. Registrar una compra y mostrar que subió el stock y cambió el costo (RN02).
7. Entregar un pedido y mostrar el descuento de insumos; luego uno sin stock suficiente que da 409 (RN03).
8. Eliminar un producto con movimientos y mostrar que quedó INACTIVO (RN04).
9. Intentar modificar un pedido entregado y obtener 409 (RN05).
10. Mostrar en Workbench la contraseña cifrada y que la API nunca la devuelve (RN06).
11. Los reportes y las calificaciones con su promedio.
12. Correr la colección de Postman.

Prepárate para explicar: qué es un token JWT y por qué vence, por qué bcrypt, por qué dos motores de base de datos, por qué arquitectura por capas y qué es un usuario de privilegios mínimos.

---

## 17. Lo que el PDF deja abierto y lo que te recomiendo decidir

El PDF deja algunas cosas sin definir. Estas son mis recomendaciones como programador. Lo que decidas, escríbelo en el README y en el anexo.

### Datos y modelo

1. La tabla clientes no tiene campo estado, ni en el texto ni en el diagrama, pero RN04 pide borrado lógico de clientes. Agrégale estado (ACTIVO, INACTIVO).
2. La tabla pedidos tiene observaciones en el diagrama, pero no en el texto. Inclúyelo.
3. En recetas, que no se pueda repetir la misma pareja de producto e insumo (único compuesto).
4. Restricciones CHECK: precio_venta mayor que 0; stock_actual, stock_minimo y costo_unitario no negativos; cantidades mayores que 0.
5. Valores por defecto: estado ACTIVO (DISPONIBLE en productos y PENDIENTE en pedidos), y fecha y hora actuales en pedidos y compras.
6. Índices en las llaves foráneas y en los campos por los que más se filtra: estado y fecha de pedidos, y fecha de vencimiento de insumos.

### Reglas y procesos

7. El precio_unitario del detalle del pedido se toma del producto en el momento del pedido. Así, si el precio cambia después, los pedidos viejos conservan el precio con el que se vendieron.
8. RN02 dice que se "actualiza" el costo_unitario: lo más simple es usar el costo de la última compra. Si prefieres un promedio, explícalo en el anexo.
9. PUT y DELETE de compras: el PDF no dice qué pasa con el stock. Propuesta: el PUT solo cambia los datos generales (factura, fecha y proveedor), no el detalle; el DELETE resta del stock lo que la compra había sumado, y si eso deja algún stock negativo, responde 409.
10. DELETE de pedidos: un pedido es parte del historial de ventas, así que en vez de borrarlo, déjalo ANULADO. Si ya está ENTREGADO o ANULADO, 409 (RN05).
11. Flujo de estados del pedido: de PENDIENTE pasa a EN_PREPARACION y de ahí a ENTREGADO; se puede anular desde PENDIENTE o EN_PREPARACION. ENTREGADO y ANULADO son estados finales (RN05).
12. No permitir pedir productos AGOTADO o INACTIVO, ni usar clientes, proveedores o insumos INACTIVO en movimientos nuevos. Un usuario INACTIVO no puede iniciar sesión.
13. Reportes: contar solo pedidos ENTREGADO; los ANULADO no son ventas.
14. Calificaciones: solo para pedidos ENTREGADO, una por pedido (si se repite, 409) y notas de 1 a 5.

### Roles que el PDF no define

15. El PDF da los roles del CRUD, pero no los de cada consulta. Propuesta:

| Endpoint | Roles propuestos | Por qué |
|---|---|---|
| /productos/categoria/{id_categoria} | Todos | Es una consulta de productos, y esas son para todos |
| /productos/{id}/receta | ADMIN, COCINERO | Igual que el CRUD de recetas |
| /productos/{id}/costo | ADMIN | Los costos son información sensible |
| /insumos/stock-bajo y /insumos/por-vencer | ADMIN, COCINERO | Igual que el CRUD de insumos |
| /proveedores/{id}/compras | ADMIN | Igual que proveedores y compras |
| /clientes/{id}/pedidos | ADMIN, CAJERO | Igual que el CRUD de clientes |
| /pedidos/estado/{estado} | ADMIN, CAJERO, COCINERO | El cocinero necesita ver los pedidos pendientes para prepararlos |
| PATCH /pedidos/{id}/estado | ADMIN, CAJERO, COCINERO | El PDF le da el cambio de estado al COCINERO, y el cajero necesita poder anular |
| /reportes/ventas y /reportes/productos-mas-vendidos | ADMIN | Información de ventas para la toma de decisiones |
| /calificaciones/producto/{id_producto} | ADMIN, CAJERO | Igual que el CRUD de calificaciones |

### Detalles técnicos

16. En FastAPI, declara las rutas fijas antes de las rutas con {id}. Por ejemplo, /insumos/stock-bajo y /insumos/por-vencer van antes de /insumos/{id}; si no, FastAPI cree que "stock-bajo" es un id y responde 422.
17. RN02 y RN03 deben ir en una transacción: o se guarda todo o no se guarda nada. Si algo falla a la mitad sin transacción, el inventario queda descuadrado.
18. passlib, la librería sugerida para bcrypt, no se actualiza desde hace años y falla con las versiones nuevas de la librería bcrypt. Si te da errores, usa la librería bcrypt directamente; el PDF dice "sugeridas", así que está permitido.
19. Si el login recibe el correo y la contraseña en JSON, configura en Swagger la seguridad de tipo Bearer, en la que se pega el token. El formulario de usuario y contraseña de OAuth2 que trae FastAPI no funciona con ese login.
20. Zona horaria America/Bogota en MySQL y en la API, para que las fechas de pedidos, vencimientos y reportes cuadren.
21. El PDF permite trabajar con Postman o Thunder Client, pero la entrega pide "la colección de Postman exportada". Lo más seguro es hacer la colección final en Postman.

## 18. Preguntas para el instructor

1. ¿La inicial también va en las rutas de la URL (por ejemplo /api/v1/productos) y en los nombres de los scripts de database/, o solo en los archivos de código, funciones, clases y variables?
2. ¿Están bien los roles que propongo para las consultas y los reportes (sección 17, punto 15)?
3. ¿El cambio de estado del pedido lo pueden hacer también ADMIN y CAJERO, o solo el COCINERO?
4. ¿Los reportes de ventas cuentan solo los pedidos ENTREGADO?
5. ¿Qué deben hacer el DELETE de pedidos y el de compras? (mi propuesta está en la sección 17, puntos 9 y 10)
6. ¿Puedo entregar la colección hecha en Thunder Client si la exporto, o tiene que ser de Postman?
7. Si en mi equipo no puedo usar Docker o MySQL, ¿hay otra opción permitida? No cambies de tecnología sin su aprobación: el PDF las pide de forma explícita.

## 19. Lista de revisión final

Estado al 27 de octubre de 2026, después de probar todo el proyecto. El detalle de las pruebas está en `api_gastronomia/README.md`, sección 15 "Pruebas realizadas".

- [x] API en FastAPI con arquitectura por capas (routers, services, repositories, models, schemas, core y database)
- [x] Los 65 endpoints con el prefijo /api/v1 (el proyecto tiene 67: se agregaron el descuento y la venta rápida)
- [x] Todos los endpoints privados menos /auth/login; 401 y 403 funcionando
- [x] Token JWT con expiración, enviado como Bearer en el encabezado Authorization
- [x] RN01 a RN06 funcionando
- [x] MySQL (bd_gastronomia) para todo menos las calificaciones, que van en MongoDB (bd_gastronomia_nosql)
- [x] La API se conecta a MySQL con un usuario de privilegios mínimos, no con root
- [x] .env fuera de GitHub y .env.example en GitHub
- [x] Carpeta database/ con DDL, DML (10 o más registros por tabla principal), DCL y script de MongoDB con $jsonSchema
- [x] docker-compose.yml con MySQL 8 y MongoDB 7 (está en el proyecto, pero no se pudo probar porque Docker no funciona en este equipo)
- [x] requirements.txt y README.md
- [x] Cada endpoint documentado en Swagger (los 67 tienen título y descripción)
- [ ] Colección de Postman exportada en el repositorio, con pruebas de cada servicio (pendiente: las pruebas se hacen con Thunder Client; falta exportar esa colección y guardarla en el repositorio)
- [x] Tu inicial en archivos, funciones, clases, variables, rutas y controladores (prefijo jb_; si también va en las rutas de la URL, está entre las preguntas de la sección 18)
- [ ] Anexo Formato 6 con sus 12 secciones, subido al enlace del instructor
- [ ] Sustentación preparada
