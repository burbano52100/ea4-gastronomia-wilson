# Usabilidad: rutas y datos para Thunder Client

- Todas las rutas llevan en Auth > Bearer el `access_token` del paso 1, menos los login (pasos 1, E2 y E3) y la prueba E1.
- ID_CALIFICACION = el `id_calificacion` que devuelve el paso 55.
- Al lado de cada título va el código que debe responder la API.
- Debajo de cada paso:
  - **Ver funcionando:** qué mirar en la respuesta, y la consulta para MySQL Workbench o el filtro para MongoDB Compass.
  - **Código:** el archivo y las líneas donde está programado. Los archivos están dentro de la carpeta `api_gastronomia`.

1. Encender las bases de datos: doble clic en `C:\Users\BURBANO\bd_gastronomia_local\iniciar_bases.bat`

2. Encender el servidor (terminal de VS Code):

```
cd "C:\Users\BURBANO\Desktop\TRABAJOS\Miercoles\istructivo mongo db\api_gastronomia"
venv\Scripts\activate
uvicorn app.jb_main:jb_app --reload
```

3. Ver las bases de datos:
   - **MySQL Workbench:** ya está creada la conexión `API_WILSON` (Hostname `127.0.0.1`, Port `3306`, Username `root`, contraseña `1234` guardada, base `bd_gastronomia`). Ábrala con doble clic, escriba `USE bd_gastronomia;` y luego la consulta de cada paso. Para ejecutar, pulse el rayo.
   - **MongoDB Compass:** conéctese con `mongodb://jb_root:CLAVE@localhost:27018/?authSource=admin`, cambiando CLAVE por la de `MONGO_ROOT_PASSWORD` del `.env`. Abra `bd_gastronomia_nosql` > `calificaciones`.

4. Volver a los datos iniciales (después de hacer el recorrido):
   - En Workbench: File > Open SQL Script, abra `database/01_jb_ddl_bd_gastronomia.sql` y ejecútelo con el rayo. Haga lo mismo con el 02 y el 03.
   - En Compass: abra la pestaña MONGOSH, pegue todo el contenido de `database/04_jb_mongo_calificaciones.js` y pulse Enter.

---

## Autenticación

### 1. Iniciar sesión - 200
`POST http://localhost:8000/api/v1/auth/login`
```json
{
  "correo": "burbano@gastronomia.com",
  "password": "Admin123*"
}
```

- **Ver funcionando:** la respuesta trae `access_token`. En MySQL Workbench:
  `SELECT correo, rol, estado FROM usuarios WHERE correo = 'burbano@gastronomia.com';`
- **Código:**
  - `app/routers/jb_auth_router.py`, líneas 30 a 39 (`jb_login`)
  - `app/services/jb_auth_service.py`, líneas 14 a 36 (`jb_iniciar_sesion`)
  - `app/core/jb_security.py`, líneas 44 a 53 (`jb_verificar_password`)
  - `app/core/jb_security.py`, líneas 57 a 72 (`jb_crear_token`)

### 2. Ver mi perfil - 200
`GET http://localhost:8000/api/v1/auth/perfil`

- **Ver funcionando:** la respuesta trae su usuario, sin contraseña. En MySQL Workbench:
  `SELECT id_usuario, correo, rol FROM usuarios WHERE id_usuario = 1;`
- **Código:**
  - `app/routers/jb_auth_router.py`, líneas 68 a 76 (`jb_perfil`)
  - `app/core/jb_security.py`, líneas 82 a 133 (`jb_usuario_actual`)

### 3. Registrar usuario - 201
`POST http://localhost:8000/api/v1/auth/registro`
```json
{
  "identificacion": "1075999001",
  "nombres": "Luisa Fernanda",
  "apellidos": "Ortega Ruiz",
  "correo": "luisa.ortega@gastronomia.com",
  "password": "Cajera2026",
  "rol": "CAJERO"
}
```

- **Ver funcionando:** la respuesta trae `id_usuario` 11 y no trae la contraseña. En MySQL Workbench:
  `SELECT id_usuario, correo, rol, password FROM usuarios WHERE id_usuario = 11;`
- **Código:**
  - `app/routers/jb_auth_router.py`, líneas 43 a 64 (`jb_registro`)
  - `app/services/jb_usuario_service.py`, líneas 45 a 68 (`jb_crear`)
  - `app/core/jb_security.py`, líneas 37 a 40 (`jb_cifrar_password`)

## Usuarios

### 4. Listar usuarios - 200
`GET http://localhost:8000/api/v1/usuarios`

- **Ver funcionando:** la respuesta trae la lista de usuarios. En MySQL Workbench:
  `SELECT id_usuario, correo, rol, estado FROM usuarios;`
- **Código:**
  - `app/routers/jb_usuarios_router.py`, líneas 30 a 35 (`jb_listar_usuarios`)
  - `app/services/jb_usuario_service.py`, líneas 16 a 18 (`jb_listar`)

### 5. Crear usuario - 201
`POST http://localhost:8000/api/v1/usuarios`
```json
{
  "identificacion": "1075999002",
  "nombres": "Andrés Felipe",
  "apellidos": "Molina Ríos",
  "correo": "andres.molina@gastronomia.com",
  "password": "Cocina2026",
  "rol": "COCINERO"
}
```

- **Ver funcionando:** la respuesta trae `id_usuario` 12. En MySQL Workbench:
  `SELECT id_usuario, correo, rol, password FROM usuarios WHERE id_usuario = 12;`
- **Código:**
  - `app/routers/jb_usuarios_router.py`, líneas 48 a 57 (`jb_crear_usuario`)
  - `app/services/jb_usuario_service.py`, líneas 45 a 68 (`jb_crear`)
  - `app/core/jb_security.py`, líneas 37 a 40 (`jb_cifrar_password`)

### 6. Consultar usuario - 200
`GET http://localhost:8000/api/v1/usuarios/12`

- **Ver funcionando:** la respuesta trae el usuario 12. En MySQL Workbench:
  `SELECT * FROM usuarios WHERE id_usuario = 12;`
- **Código:**
  - `app/routers/jb_usuarios_router.py`, líneas 39 a 44 (`jb_obtener_usuario`)
  - `app/services/jb_usuario_service.py`, líneas 22 a 30 (`jb_obtener`)

### 7. Actualizar usuario - 200
`PUT http://localhost:8000/api/v1/usuarios/12`
```json
{
  "identificacion": "1075999002",
  "nombres": "Andrés Felipe",
  "apellidos": "Molina Ríos",
  "correo": "andres.molina@gastronomia.com",
  "rol": "COCINERO",
  "estado": "ACTIVO"
}
```

- **Ver funcionando:** la respuesta trae los datos nuevos. En MySQL Workbench:
  `SELECT nombres, rol, estado FROM usuarios WHERE id_usuario = 12;`
- **Código:**
  - `app/routers/jb_usuarios_router.py`, líneas 61 a 70 (`jb_actualizar_usuario`)
  - `app/services/jb_usuario_service.py`, líneas 72 a 96 (`jb_actualizar`)
  - `app/services/jb_usuario_service.py`, líneas 34 a 41 (`jb_validar_otro_admin`)

## Categorías

### 8. Listar categorías - 200
`GET http://localhost:8000/api/v1/categorias`

- **Ver funcionando:** la respuesta trae las 10 categorías. En MySQL Workbench:
  `SELECT * FROM categorias;`
- **Código:**
  - `app/routers/jb_categorias_router.py`, líneas 27 a 32 (`jb_listar_categorias`)
  - `app/services/jb_categoria_service.py`, líneas 14 a 16 (`jb_listar`)

### 9. Crear categoría - 201
`POST http://localhost:8000/api/v1/categorias`
```json
{
  "nombre": "Bebidas frías",
  "descripcion": "Jugos, limonadas y malteadas"
}
```

- **Ver funcionando:** la respuesta trae `id_categoria` 11. En MySQL Workbench:
  `SELECT * FROM categorias WHERE id_categoria = 11;`
- **Código:**
  - `app/routers/jb_categorias_router.py`, líneas 46 a 52 (`jb_crear_categoria`)
  - `app/services/jb_categoria_service.py`, líneas 32 a 40 (`jb_crear`)

### 10. Consultar categoría - 200
`GET http://localhost:8000/api/v1/categorias/11`

- **Ver funcionando:** la respuesta trae la categoría 11. En MySQL Workbench:
  `SELECT * FROM categorias WHERE id_categoria = 11;`
- **Código:**
  - `app/routers/jb_categorias_router.py`, líneas 36 a 42 (`jb_obtener_categoria`)
  - `app/services/jb_categoria_service.py`, líneas 20 a 28 (`jb_obtener`)

### 11. Actualizar categoría - 200
`PUT http://localhost:8000/api/v1/categorias/11`
```json
{
  "nombre": "Bebidas frías",
  "descripcion": "Jugos, limonadas, malteadas y sodas",
  "estado": "ACTIVO"
}
```

- **Ver funcionando:** la respuesta trae la descripción nueva. En MySQL Workbench:
  `SELECT nombre, descripcion, estado FROM categorias WHERE id_categoria = 11;`
- **Código:**
  - `app/routers/jb_categorias_router.py`, líneas 56 a 62 (`jb_actualizar_categoria`)
  - `app/services/jb_categoria_service.py`, líneas 44 a 60 (`jb_actualizar`)

## Productos

### 12. Listar productos - 200
`GET http://localhost:8000/api/v1/productos`

- **Ver funcionando:** la respuesta trae los 15 productos con su `nombre_categoria`. En MySQL Workbench:
  `SELECT * FROM productos;`
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 35 a 40 (`jb_listar_productos`)
  - `app/services/jb_producto_service.py`, líneas 21 a 23 (`jb_listar`)

### 13. Crear producto - 201
`POST http://localhost:8000/api/v1/productos`
```json
{
  "codigo": "BEB-010",
  "nombre": "Jugo de mora",
  "descripcion": "Jugo natural de mora en agua",
  "precio_venta": 4500,
  "unidad_venta": "vaso",
  "id_categoria": 11
}
```

- **Ver funcionando:** la respuesta trae `id_producto` 16, estado DISPONIBLE. En MySQL Workbench:
  `SELECT * FROM productos WHERE id_producto = 16;`
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 91 a 100 (`jb_crear_producto`)
  - `app/services/jb_producto_service.py`, líneas 65 a 75 (`jb_crear`)
  - `app/services/jb_producto_service.py`, líneas 39 a 51 (`jb_validar_categoria`)

### 14. Consultar producto - 200
`GET http://localhost:8000/api/v1/productos/16`

- **Ver funcionando:** la respuesta trae el producto 16. En MySQL Workbench:
  `SELECT * FROM productos WHERE id_producto = 16;`
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 54 a 60 (`jb_obtener_producto`)
  - `app/services/jb_producto_service.py`, líneas 27 a 35 (`jb_obtener`)

### 15. Actualizar producto - 200
`PUT http://localhost:8000/api/v1/productos/16`
```json
{
  "codigo": "BEB-010",
  "nombre": "Jugo de mora",
  "descripcion": "Jugo natural de mora en agua",
  "precio_venta": 5000,
  "unidad_venta": "vaso",
  "id_categoria": 11,
  "estado": "DISPONIBLE"
}
```

- **Ver funcionando:** la respuesta trae `precio_venta` 5000. En MySQL Workbench:
  `SELECT precio_venta, estado FROM productos WHERE id_producto = 16;`
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 104 a 110 (`jb_actualizar_producto`)
  - `app/services/jb_producto_service.py`, líneas 79 a 99 (`jb_actualizar`)

### 16. Productos de una categoría - 200
`GET http://localhost:8000/api/v1/productos/categoria/11`

- **Ver funcionando:** la respuesta trae el Jugo de mora. En MySQL Workbench:
  `SELECT id_producto, nombre FROM productos WHERE id_categoria = 11;`
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 44 a 50 (`jb_productos_por_categoria`)
  - `app/services/jb_producto_service.py`, líneas 55 a 61 (`jb_por_categoria`)

## Insumos

### 17. Listar insumos - 200
`GET http://localhost:8000/api/v1/insumos`

- **Ver funcionando:** la respuesta trae los 18 insumos. En MySQL Workbench:
  `SELECT * FROM insumos;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 70 a 75 (`jb_listar_insumos`)
  - `app/services/jb_insumo_service.py`, líneas 19 a 21 (`jb_listar`)

### 18. Crear insumo - 201
`POST http://localhost:8000/api/v1/insumos`
```json
{
  "nombre": "Mora",
  "unidad_medida": "kg",
  "stock_actual": 5,
  "stock_minimo": 2,
  "costo_unitario": 6000,
  "fecha_vencimiento": "2026-11-10"
}
```

- **Ver funcionando:** la respuesta trae `id_insumo` 19. En MySQL Workbench:
  `SELECT * FROM insumos WHERE id_insumo = 19;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 88 a 94 (`jb_crear_insumo`)
  - `app/services/jb_insumo_service.py`, líneas 37 a 45 (`jb_crear`)

### 19. Consultar insumo - 200
`GET http://localhost:8000/api/v1/insumos/19`

- **Ver funcionando:** la respuesta trae el insumo 19. En MySQL Workbench:
  `SELECT * FROM insumos WHERE id_insumo = 19;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 79 a 84 (`jb_obtener_insumo`)
  - `app/services/jb_insumo_service.py`, líneas 25 a 33 (`jb_obtener`)

### 20. Actualizar insumo - 200
`PUT http://localhost:8000/api/v1/insumos/19`
```json
{
  "nombre": "Mora",
  "unidad_medida": "kg",
  "stock_actual": 8,
  "stock_minimo": 2,
  "costo_unitario": 6000,
  "fecha_vencimiento": "2026-11-15",
  "estado": "ACTIVO"
}
```

- **Ver funcionando:** la respuesta trae `stock_actual` 8. En MySQL Workbench:
  `SELECT stock_actual, fecha_vencimiento FROM insumos WHERE id_insumo = 19;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 98 a 107 (`jb_actualizar_insumo`)
  - `app/services/jb_insumo_service.py`, líneas 49 a 65 (`jb_actualizar`)

### 21. Insumos con stock bajo - 200
`GET http://localhost:8000/api/v1/insumos/stock-bajo`

- **Ver funcionando:** la respuesta trae Leche entera, Mantequilla y Tomate con su `faltante`. En MySQL Workbench:
  `SELECT nombre, stock_actual, stock_minimo FROM insumos WHERE stock_actual <= stock_minimo;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 41 a 49 (`jb_insumos_stock_bajo`)
  - `app/services/jb_insumo_service.py`, líneas 94 a 96 (`jb_stock_bajo`)

### 22. Insumos por vencer - 200
`GET http://localhost:8000/api/v1/insumos/por-vencer?dias=7`

- **Ver funcionando:** la respuesta trae 5 insumos con sus `dias_restantes`. En MySQL Workbench:
  `SELECT nombre, fecha_vencimiento FROM insumos WHERE fecha_vencimiento BETWEEN CURDATE() AND CURDATE() + INTERVAL 7 DAY;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 53 a 66 (`jb_insumos_por_vencer`)
  - `app/services/jb_insumo_service.py`, líneas 100 a 105 (`jb_por_vencer`)

## Recetas

### 23. Listar recetas - 200
`GET http://localhost:8000/api/v1/recetas`

- **Ver funcionando:** la respuesta trae las 57 líneas de receta. En MySQL Workbench:
  `SELECT * FROM recetas;`
- **Código:**
  - `app/routers/jb_recetas_router.py`, líneas 32 a 37 (`jb_listar_recetas`)
  - `app/services/jb_receta_service.py`, líneas 16 a 18 (`jb_listar`)

### 24. Agregar mora a la receta - 201
`POST http://localhost:8000/api/v1/recetas`
```json
{
  "id_producto": 16,
  "id_insumo": 19,
  "cantidad": 0.15
}
```

- **Ver funcionando:** la respuesta trae `id_receta` 58. En MySQL Workbench:
  `SELECT * FROM recetas WHERE id_producto = 16;`
- **Código:**
  - `app/routers/jb_recetas_router.py`, líneas 50 a 60 (`jb_crear_receta`)
  - `app/services/jb_receta_service.py`, líneas 62 a 77 (`jb_crear`)

### 25. Agregar azúcar a la receta - 201
`POST http://localhost:8000/api/v1/recetas`
```json
{
  "id_producto": 16,
  "id_insumo": 8,
  "cantidad": 0.03
}
```

- **Ver funcionando:** la respuesta trae `id_receta` 59. En MySQL Workbench:
  `SELECT * FROM recetas WHERE id_producto = 16;`
- **Código:**
  - `app/routers/jb_recetas_router.py`, líneas 50 a 60 (`jb_crear_receta`)
  - `app/services/jb_receta_service.py`, líneas 62 a 77 (`jb_crear`)

### 26. Consultar línea de receta - 200
`GET http://localhost:8000/api/v1/recetas/58`

- **Ver funcionando:** la respuesta trae la línea 58. En MySQL Workbench:
  `SELECT * FROM recetas WHERE id_receta = 58;`
- **Código:**
  - `app/routers/jb_recetas_router.py`, líneas 41 a 46 (`jb_obtener_receta`)
  - `app/services/jb_receta_service.py`, líneas 22 a 30 (`jb_obtener`)

### 27. Actualizar línea de receta - 200
`PUT http://localhost:8000/api/v1/recetas/58`
```json
{
  "id_producto": 16,
  "id_insumo": 19,
  "cantidad": 0.12
}
```

- **Ver funcionando:** la respuesta trae `cantidad` 0.12. En MySQL Workbench:
  `SELECT cantidad FROM recetas WHERE id_receta = 58;`
- **Código:**
  - `app/routers/jb_recetas_router.py`, líneas 64 a 70 (`jb_actualizar_receta`)
  - `app/services/jb_receta_service.py`, líneas 81 a 103 (`jb_actualizar`)

### 28. Receta del producto - 200
`GET http://localhost:8000/api/v1/productos/16/receta`

- **Ver funcionando:** la respuesta trae los 2 insumos con su `costo_linea`. En MySQL Workbench:
  `SELECT i.nombre, r.cantidad, i.costo_unitario FROM recetas r JOIN insumos i ON i.id_insumo = r.id_insumo WHERE r.id_producto = 16;`
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 64 a 73 (`jb_receta_producto`)
  - `app/services/jb_producto_service.py`, líneas 157 a 161 (`jb_receta`)
  - `app/services/jb_producto_service.py`, líneas 128 a 153 (`jb_lineas_receta`)

### 29. Costo y margen del producto - 200
`GET http://localhost:8000/api/v1/productos/16/costo`

- **Ver funcionando:** la respuesta trae `costo_produccion` 840, `margen` 4160 y `margen_porcentaje` 83.2. En MySQL Workbench:
  `SELECT SUM(r.cantidad * i.costo_unitario) AS costo FROM recetas r JOIN insumos i ON i.id_insumo = r.id_insumo WHERE r.id_producto = 16;`
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 77 a 87 (`jb_costo_producto`)
  - `app/services/jb_producto_service.py`, líneas 165 a 195 (`jb_costo`)
  - `app/services/jb_producto_service.py`, líneas 128 a 153 (`jb_lineas_receta`)

## Proveedores

### 30. Listar proveedores - 200
`GET http://localhost:8000/api/v1/proveedores`

- **Ver funcionando:** la respuesta trae los 10 proveedores. En MySQL Workbench:
  `SELECT * FROM proveedores;`
- **Código:**
  - `app/routers/jb_proveedores_router.py`, líneas 34 a 39 (`jb_listar_proveedores`)
  - `app/services/jb_proveedor_service.py`, líneas 16 a 18 (`jb_listar`)

### 31. Crear proveedor - 201
`POST http://localhost:8000/api/v1/proveedores`
```json
{
  "nit": "901555666-7",
  "razon_social": "Frutas del Macizo S.A.S.",
  "telefono": "3201112233",
  "correo": "ventas@frutasdelmacizo.com",
  "direccion": "Carrera 7 # 4-10, Pitalito"
}
```

- **Ver funcionando:** la respuesta trae `id_proveedor` 11. En MySQL Workbench:
  `SELECT * FROM proveedores WHERE id_proveedor = 11;`
- **Código:**
  - `app/routers/jb_proveedores_router.py`, líneas 62 a 68 (`jb_crear_proveedor`)
  - `app/services/jb_proveedor_service.py`, líneas 34 a 42 (`jb_crear`)

### 32. Consultar proveedor - 200
`GET http://localhost:8000/api/v1/proveedores/11`

- **Ver funcionando:** la respuesta trae el proveedor 11. En MySQL Workbench:
  `SELECT * FROM proveedores WHERE id_proveedor = 11;`
- **Código:**
  - `app/routers/jb_proveedores_router.py`, líneas 43 a 48 (`jb_obtener_proveedor`)
  - `app/services/jb_proveedor_service.py`, líneas 22 a 30 (`jb_obtener`)

### 33. Actualizar proveedor - 200
`PUT http://localhost:8000/api/v1/proveedores/11`
```json
{
  "nit": "901555666-7",
  "razon_social": "Frutas del Macizo S.A.S.",
  "telefono": "3201112233",
  "correo": "ventas@frutasdelmacizo.com",
  "direccion": "Carrera 7 # 4-10, Pitalito",
  "estado": "ACTIVO"
}
```

- **Ver funcionando:** la respuesta trae el proveedor actualizado. En MySQL Workbench:
  `SELECT razon_social, estado FROM proveedores WHERE id_proveedor = 11;`
- **Código:**
  - `app/routers/jb_proveedores_router.py`, líneas 72 a 78 (`jb_actualizar_proveedor`)
  - `app/services/jb_proveedor_service.py`, líneas 46 a 62 (`jb_actualizar`)

## Compras

### 34. Registrar compra - 201
`POST http://localhost:8000/api/v1/compras`
```json
{
  "numero_factura": "FMZ-0001",
  "id_proveedor": 11,
  "detalle": [
    { "id_insumo": 19, "cantidad": 10, "costo_unitario": 6200 },
    { "id_insumo": 8, "cantidad": 5, "costo_unitario": 4000 }
  ]
}
```

- **Ver funcionando:** la respuesta trae `id_compra` 11 y `total` 82000. En MySQL Workbench:
  `SELECT * FROM detalle_compra WHERE id_compra = 11;`
- **Código:**
  - `app/routers/jb_compras_router.py`, líneas 48 a 60 (`jb_crear_compra`)
  - `app/services/jb_compra_service.py`, líneas 88 a 146 (`jb_crear`)
  - `app/services/jb_compra_service.py`, líneas 74 a 84 (`jb_bloquear_insumos`)

### 35. Comprobar que subió el stock (RN02) - 200
`GET http://localhost:8000/api/v1/insumos/19`

- **Ver funcionando:** la respuesta trae `stock_actual` 18 y `costo_unitario` 6200. En MySQL Workbench:
  `SELECT stock_actual, costo_unitario FROM insumos WHERE id_insumo = 19;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 79 a 84 (`jb_obtener_insumo`)
  - `app/services/jb_insumo_service.py`, líneas 25 a 33 (`jb_obtener`)

### 36. Listar compras - 200
`GET http://localhost:8000/api/v1/compras`

- **Ver funcionando:** la respuesta trae las compras con su detalle. En MySQL Workbench:
  `SELECT * FROM compras ORDER BY fecha_compra DESC;`
- **Código:**
  - `app/routers/jb_compras_router.py`, líneas 30 a 35 (`jb_listar_compras`)
  - `app/services/jb_compra_service.py`, líneas 23 a 25 (`jb_listar`)

### 37. Consultar compra - 200
`GET http://localhost:8000/api/v1/compras/11`

- **Ver funcionando:** la respuesta trae la compra 11 con sus 2 ítems. En MySQL Workbench:
  `SELECT * FROM compras WHERE id_compra = 11;`
- **Código:**
  - `app/routers/jb_compras_router.py`, líneas 39 a 44 (`jb_obtener_compra`)
  - `app/services/jb_compra_service.py`, líneas 29 a 37 (`jb_obtener`)

### 38. Actualizar datos de la compra - 200
`PUT http://localhost:8000/api/v1/compras/11`
```json
{
  "numero_factura": "FMZ-0001-A",
  "fecha_compra": "2026-10-25T09:30:00",
  "id_proveedor": 11
}
```

- **Ver funcionando:** la respuesta trae `numero_factura` FMZ-0001-A. En MySQL Workbench:
  `SELECT numero_factura, fecha_compra FROM compras WHERE id_compra = 11;`
- **Código:**
  - `app/routers/jb_compras_router.py`, líneas 64 a 74 (`jb_actualizar_compra`)
  - `app/services/jb_compra_service.py`, líneas 150 a 172 (`jb_actualizar`)

### 39. Compras de un proveedor - 200
`GET http://localhost:8000/api/v1/proveedores/11/compras`

- **Ver funcionando:** la respuesta trae la compra 11. En MySQL Workbench:
  `SELECT * FROM compras WHERE id_proveedor = 11;`
- **Código:**
  - `app/routers/jb_proveedores_router.py`, líneas 52 a 58 (`jb_compras_proveedor`)
  - `app/services/jb_proveedor_service.py`, líneas 91 a 95 (`jb_compras`)

## Clientes

### 40. Listar clientes - 200
`GET http://localhost:8000/api/v1/clientes`

- **Ver funcionando:** la respuesta trae los 18 clientes. En MySQL Workbench:
  `SELECT * FROM clientes;`
- **Código:**
  - `app/routers/jb_clientes_router.py`, líneas 34 a 39 (`jb_listar_clientes`)
  - `app/services/jb_cliente_service.py`, líneas 16 a 18 (`jb_listar`)

### 41. Crear cliente - 201
`POST http://localhost:8000/api/v1/clientes`
```json
{
  "identificacion": "1075400099",
  "nombres": "Andrea",
  "apellidos": "Trujillo Paz",
  "telefono": "3209998877",
  "correo": "andrea.trujillo@soy.sena.edu.co",
  "tipo_cliente": "APRENDIZ"
}
```

- **Ver funcionando:** la respuesta trae `id_cliente` 19. En MySQL Workbench:
  `SELECT * FROM clientes WHERE id_cliente = 19;`
- **Código:**
  - `app/routers/jb_clientes_router.py`, líneas 62 a 68 (`jb_crear_cliente`)
  - `app/services/jb_cliente_service.py`, líneas 34 a 42 (`jb_crear`)

### 42. Consultar cliente - 200
`GET http://localhost:8000/api/v1/clientes/19`

- **Ver funcionando:** la respuesta trae el cliente 19. En MySQL Workbench:
  `SELECT * FROM clientes WHERE id_cliente = 19;`
- **Código:**
  - `app/routers/jb_clientes_router.py`, líneas 43 a 48 (`jb_obtener_cliente`)
  - `app/services/jb_cliente_service.py`, líneas 22 a 30 (`jb_obtener`)

### 43. Actualizar cliente - 200
`PUT http://localhost:8000/api/v1/clientes/19`
```json
{
  "identificacion": "1075400099",
  "nombres": "Andrea",
  "apellidos": "Trujillo Paz",
  "telefono": "3209998877",
  "correo": "andrea.trujillo@soy.sena.edu.co",
  "tipo_cliente": "APRENDIZ",
  "estado": "ACTIVO"
}
```

- **Ver funcionando:** la respuesta trae el cliente actualizado. En MySQL Workbench:
  `SELECT nombres, estado FROM clientes WHERE id_cliente = 19;`
- **Código:**
  - `app/routers/jb_clientes_router.py`, líneas 72 a 78 (`jb_actualizar_cliente`)
  - `app/services/jb_cliente_service.py`, líneas 46 a 62 (`jb_actualizar`)

## Pedidos

### 44. Registrar pedido - 201
`POST http://localhost:8000/api/v1/pedidos`
```json
{
  "id_cliente": 19,
  "tipo_pedido": "MESA",
  "observaciones": "Sin hielo",
  "detalle": [
    { "id_producto": 16, "cantidad": 2 },
    { "id_producto": 1, "cantidad": 1 }
  ]
}
```

- **Ver funcionando:** la respuesta trae `id_pedido` 130, estado PENDIENTE y `total` 24000. En MySQL Workbench:
  `SELECT * FROM detalle_pedido WHERE id_pedido = 130;`
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 71 a 82 (`jb_crear_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 136 a 165 (`jb_crear`)
  - `app/services/jb_pedido_service.py`, líneas 98 a 132 (`jb_armar_detalle`)

### 45. Listar pedidos - 200
`GET http://localhost:8000/api/v1/pedidos`

- **Ver funcionando:** la respuesta trae los pedidos con su detalle. En MySQL Workbench:
  `SELECT * FROM pedidos ORDER BY fecha_pedido DESC;`
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 38 a 43 (`jb_listar_pedidos`)
  - `app/services/jb_pedido_service.py`, líneas 37 a 39 (`jb_listar`)

### 46. Consultar pedido - 200
`GET http://localhost:8000/api/v1/pedidos/130`

- **Ver funcionando:** la respuesta trae el pedido 130. En MySQL Workbench:
  `SELECT * FROM pedidos WHERE id_pedido = 130;`
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 61 a 67 (`jb_obtener_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 43 a 51 (`jb_obtener`)

### 47. Actualizar pedido - 200
`PUT http://localhost:8000/api/v1/pedidos/130`
```json
{
  "id_cliente": 19,
  "tipo_pedido": "PARA_LLEVAR",
  "observaciones": "Sin hielo, para llevar",
  "detalle": [
    { "id_producto": 16, "cantidad": 2 },
    { "id_producto": 1, "cantidad": 1 }
  ]
}
```

- **Ver funcionando:** la respuesta trae `tipo_pedido` PARA_LLEVAR. En MySQL Workbench:
  `SELECT tipo_pedido, observaciones, total FROM pedidos WHERE id_pedido = 130;`
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 86 a 95 (`jb_actualizar_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 169 a 197 (`jb_actualizar`)
  - `app/services/jb_pedido_service.py`, líneas 73 a 78 (`jb_validar_abierto`)
  - `app/services/jb_pedido_service.py`, líneas 98 a 132 (`jb_armar_detalle`)

### 48. Pedidos por estado - 200
`GET http://localhost:8000/api/v1/pedidos/estado/PENDIENTE`

- **Ver funcionando:** la respuesta trae los pedidos PENDIENTE. En MySQL Workbench:
  `SELECT id_pedido, estado FROM pedidos WHERE estado = 'PENDIENTE';`
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 47 a 57 (`jb_pedidos_por_estado`)
  - `app/services/jb_pedido_service.py`, líneas 55 a 57 (`jb_por_estado`)

### 49. Pasar a EN_PREPARACION - 200
`PATCH http://localhost:8000/api/v1/pedidos/130/estado`
```json
{
  "estado": "EN_PREPARACION"
}
```

- **Ver funcionando:** la respuesta trae estado EN_PREPARACION. En MySQL Workbench:
  `SELECT estado FROM pedidos WHERE id_pedido = 130;`
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 99 a 111 (`jb_cambiar_estado_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 267 a 287 (`jb_cambiar_estado`)
  - `app/services/jb_pedido_service.py`, líneas 24 a 33 (`JB_TRANSICIONES`)

### 50. Entregar el pedido (RN03) - 200
`PATCH http://localhost:8000/api/v1/pedidos/130/estado`
```json
{
  "estado": "ENTREGADO"
}
```

- **Ver funcionando:** la respuesta trae estado ENTREGADO. En MySQL Workbench:
  `SELECT nombre, stock_actual FROM insumos WHERE id_insumo IN (1, 2, 6, 8, 15, 19);`
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 99 a 111 (`jb_cambiar_estado_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 267 a 287 (`jb_cambiar_estado`)
  - `app/services/jb_pedido_service.py`, líneas 232 a 263 (`jb_descontar_inventario`)
  - `app/services/jb_pedido_service.py`, líneas 216 a 228 (`jb_insumos_necesarios`)

### 51. Comprobar que bajó el stock (RN03) - 200
`GET http://localhost:8000/api/v1/insumos/19`

- **Ver funcionando:** la respuesta trae `stock_actual` 17.76. En MySQL Workbench:
  `SELECT stock_actual FROM insumos WHERE id_insumo = 19;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 79 a 84 (`jb_obtener_insumo`)
  - `app/services/jb_insumo_service.py`, líneas 25 a 33 (`jb_obtener`)

### 52. Pedidos de un cliente - 200
`GET http://localhost:8000/api/v1/clientes/19/pedidos`

- **Ver funcionando:** la respuesta trae el pedido 130. En MySQL Workbench:
  `SELECT * FROM pedidos WHERE id_cliente = 19;`
- **Código:**
  - `app/routers/jb_clientes_router.py`, líneas 52 a 58 (`jb_pedidos_cliente`)
  - `app/services/jb_cliente_service.py`, líneas 91 a 95 (`jb_pedidos`)

## Reportes

### 53. Ventas por fechas - 200
`GET http://localhost:8000/api/v1/reportes/ventas?desde=2026-10-01&hasta=2026-10-31`

- **Ver funcionando:** la respuesta trae `numero_pedidos`, `total_vendido` y `promedio_por_pedido`. En MySQL Workbench:
  `SELECT COUNT(*), SUM(total) FROM pedidos WHERE estado = 'ENTREGADO' AND fecha_pedido >= '2026-10-01' AND fecha_pedido < '2026-11-01';`
- **Código:**
  - `app/routers/jb_reportes_router.py`, líneas 35 a 51 (`jb_reporte_ventas`)
  - `app/services/jb_reporte_service.py`, líneas 17 a 44 (`jb_ventas`)
  - `app/repositories/jb_reporte_repository.py`, líneas 17 a 37 (`jb_ventas`)

### 54. Productos más vendidos - 200
`GET http://localhost:8000/api/v1/reportes/productos-mas-vendidos?limite=5`

- **Ver funcionando:** la respuesta trae el ranking con su `posicion`. En MySQL Workbench:
  `SELECT p.nombre, SUM(d.cantidad) AS vendidos FROM detalle_pedido d JOIN pedidos pe ON pe.id_pedido = d.id_pedido JOIN productos p ON p.id_producto = d.id_producto WHERE pe.estado = 'ENTREGADO' GROUP BY p.id_producto, p.nombre ORDER BY vendidos DESC LIMIT 5;`
- **Código:**
  - `app/routers/jb_reportes_router.py`, líneas 55 a 68 (`jb_productos_mas_vendidos`)
  - `app/services/jb_reporte_service.py`, líneas 48 a 68 (`jb_mas_vendidos`)
  - `app/repositories/jb_reporte_repository.py`, líneas 41 a 65 (`jb_mas_vendidos`)

## Calificaciones (MongoDB)

### 55. Registrar calificación - 201
`POST http://localhost:8000/api/v1/calificaciones`
```json
{
  "id_pedido": 130,
  "id_cliente": 19,
  "calificacion_servicio": 5,
  "comentario": "Excelente atención y buen sabor",
  "productos": [
    { "id_producto": 16, "calificacion": 5 },
    { "id_producto": 1, "calificacion": 4 }
  ]
}
```

- **Ver funcionando:** la respuesta trae `id_calificacion` (24 caracteres) y el nombre de cada producto. En MongoDB Compass, abra `bd_gastronomia_nosql` > `calificaciones` y escriba en Filter: `{ id_pedido: 130 }`
- **Código:**
  - `app/routers/jb_calificaciones_router.py`, líneas 76 a 87 (`jb_crear_calificacion`)
  - `app/services/jb_calificacion_service.py`, líneas 104 a 131 (`jb_crear`)
  - `app/services/jb_calificacion_service.py`, líneas 65 a 100 (`jb_validar_contra_mysql`)

### 56. Listar calificaciones - 200
`GET http://localhost:8000/api/v1/calificaciones`

- **Ver funcionando:** la respuesta trae las 11 calificaciones. En MongoDB Compass, abra `bd_gastronomia_nosql` > `calificaciones` y escriba en Filter: `{}`
- **Código:**
  - `app/routers/jb_calificaciones_router.py`, líneas 43 a 48 (`jb_listar_calificaciones`)
  - `app/services/jb_calificacion_service.py`, líneas 47 a 49 (`jb_listar`)

### 57. Consultar calificación - 200
`GET http://localhost:8000/api/v1/calificaciones/ID_CALIFICACION`

- **Ver funcionando:** la respuesta trae la calificación del pedido 130. En MongoDB Compass, abra `bd_gastronomia_nosql` > `calificaciones` y escriba en Filter: `{ id_pedido: 130 }`
- **Código:**
  - `app/routers/jb_calificaciones_router.py`, líneas 66 a 72 (`jb_obtener_calificacion`)
  - `app/services/jb_calificacion_service.py`, líneas 53 a 61 (`jb_obtener`)

### 58. Actualizar calificación - 200
`PUT http://localhost:8000/api/v1/calificaciones/ID_CALIFICACION`
```json
{
  "calificacion_servicio": 4,
  "comentario": "Buen sabor",
  "productos": [
    { "id_producto": 16, "calificacion": 4 }
  ]
}
```

- **Ver funcionando:** la respuesta trae `calificacion_servicio` 4. En MongoDB Compass, abra `bd_gastronomia_nosql` > `calificaciones` y escriba en Filter: `{ id_pedido: 130 }`
- **Código:**
  - `app/routers/jb_calificaciones_router.py`, líneas 91 a 100 (`jb_actualizar_calificacion`)
  - `app/services/jb_calificacion_service.py`, líneas 135 a 158 (`jb_actualizar`)

### 59. Calificaciones y promedio de un producto - 200
`GET http://localhost:8000/api/v1/calificaciones/producto/16`

- **Ver funcionando:** la respuesta trae `total_calificaciones` y `promedio` 4. En MongoDB Compass, abra `bd_gastronomia_nosql` > `calificaciones` y escriba en Filter: `{ "productos.id_producto": 16 }`
- **Código:**
  - `app/routers/jb_calificaciones_router.py`, líneas 52 a 62 (`jb_calificaciones_producto`)
  - `app/services/jb_calificacion_service.py`, líneas 172 a 213 (`jb_por_producto`)
  - `app/repositories/jb_calificacion_repository.py`, líneas 75 a 95 (`jb_resumen_producto`)

## Pruebas de errores

### E1. Sin token - 401
`GET http://localhost:8000/api/v1/auth/perfil`
(en Auth elija "No Auth")

- **Ver funcionando:** la respuesta trae `detalle`: "Token requerido...". Este error no cambia nada en la base.
- **Código:**
  - `app/routers/jb_auth_router.py`, líneas 68 a 76 (`jb_perfil`)
  - `app/core/jb_security.py`, líneas 82 a 133 (`jb_usuario_actual`)

### E2. Contraseña incorrecta - 401
`POST http://localhost:8000/api/v1/auth/login`
```json
{
  "correo": "burbano@gastronomia.com",
  "password": "mala1234"
}
```

- **Ver funcionando:** la respuesta trae `detalle`: "Correo o contraseña incorrectos". Este error no cambia nada en la base.
- **Código:**
  - `app/routers/jb_auth_router.py`, líneas 30 a 39 (`jb_login`)
  - `app/services/jb_auth_service.py`, líneas 14 a 36 (`jb_iniciar_sesion`)

### E3. Rol sin permiso - 403
Primero inicie sesión como COCINERO:

`POST http://localhost:8000/api/v1/auth/login`
```json
{
  "correo": "maria.cruz@gastronomia.com",
  "password": "Cocinero123*"
}
```
Luego, con ese token:

`GET http://localhost:8000/api/v1/usuarios`

(después vuelva a hacer el paso 1 para recuperar el token del ADMIN)

- **Ver funcionando:** la respuesta trae `detalle`: "Acceso denegado: esta acción requiere el rol ADMIN". Este error no cambia nada en la base.
- **Código:**
  - `app/routers/jb_usuarios_router.py`, líneas 30 a 35 (`jb_listar_usuarios`)
  - `app/services/jb_usuario_service.py`, líneas 16 a 18 (`jb_listar`)
  - `app/core/jb_security.py`, líneas 137 a 155 (`jb_requiere_roles`)

### E4. No existe - 404
`GET http://localhost:8000/api/v1/productos/999`

- **Ver funcionando:** la respuesta trae `detalle`: "El producto 999 no existe". Este error no cambia nada en la base.
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 54 a 60 (`jb_obtener_producto`)
  - `app/services/jb_producto_service.py`, líneas 27 a 35 (`jb_obtener`)
  - `app/services/jb_comun.py`, líneas 7 a 10 (`jb_no_encontrado`)

### E5. Dato repetido - 409
`POST http://localhost:8000/api/v1/categorias`
```json
{
  "nombre": "Platos"
}
```

- **Ver funcionando:** la respuesta trae `detalle`: "Ya existe una categoría con ese nombre" (lo detecta la restricción UNIQUE de MySQL). Este error no cambia nada en la base.
- **Código:**
  - `app/routers/jb_categorias_router.py`, líneas 46 a 52 (`jb_crear_categoria`)
  - `app/services/jb_categoria_service.py`, líneas 32 a 40 (`jb_crear`)
  - `app/core/jb_errores.py`, líneas 110 a 122 (`JB_MENSAJES_UNICOS`)
  - `app/core/jb_errores.py`, líneas 234 a 288 (`jb_traducir_error_mysql`)

### E6. Modificar un pedido entregado (RN05) - 409
`PUT http://localhost:8000/api/v1/pedidos/130`
```json
{
  "id_cliente": 19,
  "tipo_pedido": "PARA_LLEVAR",
  "observaciones": "Sin hielo, para llevar",
  "detalle": [
    { "id_producto": 16, "cantidad": 2 },
    { "id_producto": 1, "cantidad": 1 }
  ]
}
```

- **Ver funcionando:** la respuesta trae `detalle`: "El pedido 130 está ENTREGADO y no puede modificarse (RN05)". Este error no cambia nada en la base.
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 86 a 95 (`jb_actualizar_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 169 a 197 (`jb_actualizar`)
  - `app/services/jb_pedido_service.py`, líneas 73 a 78 (`jb_validar_abierto`)

### E7. Cambio de estado no permitido - 409
`PATCH http://localhost:8000/api/v1/pedidos/128/estado`
```json
{
  "estado": "ENTREGADO"
}
```

- **Ver funcionando:** la respuesta trae `detalle`: "Un pedido PENDIENTE solo puede pasar a EN_PREPARACION o ANULADO". Este error no cambia nada en la base.
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 99 a 111 (`jb_cambiar_estado_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 267 a 287 (`jb_cambiar_estado`)
  - `app/services/jb_pedido_service.py`, líneas 24 a 33 (`JB_TRANSICIONES`)

### E8. Calificación repetida - 409
`POST http://localhost:8000/api/v1/calificaciones`
```json
{
  "id_pedido": 130,
  "id_cliente": 19,
  "calificacion_servicio": 5,
  "comentario": "Excelente atención y buen sabor",
  "productos": [
    { "id_producto": 16, "calificacion": 5 },
    { "id_producto": 1, "calificacion": 4 }
  ]
}
```

- **Ver funcionando:** la respuesta trae `detalle`: "El pedido 130 ya tiene una calificación...". Este error no cambia nada en la base.
- **Código:**
  - `app/routers/jb_calificaciones_router.py`, líneas 76 a 87 (`jb_crear_calificacion`)
  - `app/services/jb_calificacion_service.py`, líneas 104 a 131 (`jb_crear`)

### E9. Cliente que no existe - 400
`POST http://localhost:8000/api/v1/pedidos`
```json
{
  "id_cliente": 999,
  "tipo_pedido": "MESA",
  "detalle": [
    { "id_producto": 1, "cantidad": 1 }
  ]
}
```

- **Ver funcionando:** la respuesta trae `detalle`: "El cliente 999 no existe". Este error no cambia nada en la base.
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 71 a 82 (`jb_crear_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 136 a 165 (`jb_crear`)
  - `app/services/jb_pedido_service.py`, líneas 82 a 94 (`jb_validar_cliente`)

### E10. Precio en 0 - 422
`POST http://localhost:8000/api/v1/productos`
```json
{
  "codigo": "BEB-011",
  "nombre": "Jugo de fresa",
  "precio_venta": 0,
  "unidad_venta": "vaso",
  "id_categoria": 11
}
```

- **Ver funcionando:** la respuesta trae `errores` con el campo precio_venta: "Debe ser mayor que 0". Este error no cambia nada en la base.
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 91 a 100 (`jb_crear_producto`)
  - `app/services/jb_producto_service.py`, líneas 65 a 75 (`jb_crear`)
  - `app/schemas/jb_tipos.py`, líneas 52 a 52 (`JbDineroPositivo`)
  - `app/core/jb_errores.py`, líneas 168 a 212 (`jb_traducir_error`)

### E11. Enviar el total, que lo calcula la API (RN01) - 422
`POST http://localhost:8000/api/v1/pedidos`
```json
{
  "id_cliente": 19,
  "tipo_pedido": "MESA",
  "total": 1000,
  "detalle": [
    { "id_producto": 1, "cantidad": 1 }
  ]
}
```

- **Ver funcionando:** la respuesta trae `errores` con el campo total: "Este campo no está permitido". Este error no cambia nada en la base.
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 71 a 82 (`jb_crear_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 136 a 165 (`jb_crear`)
  - `app/schemas/jb_tipos.py`, líneas 76 a 81 (`JbModeloEntrada`)

## Eliminar (en este orden)

### 60. Eliminar calificación - 200
`DELETE http://localhost:8000/api/v1/calificaciones/ID_CALIFICACION`

- **Ver funcionando:** la respuesta trae `tipo_borrado` FISICO. En MongoDB Compass, abra `bd_gastronomia_nosql` > `calificaciones` y escriba en Filter: `{ id_pedido: 130 }  (ya no aparece)`
- **Código:**
  - `app/routers/jb_calificaciones_router.py`, líneas 104 a 110 (`jb_eliminar_calificacion`)
  - `app/services/jb_calificacion_service.py`, líneas 162 a 168 (`jb_eliminar`)

### 61. Anular pedido - 200
`DELETE http://localhost:8000/api/v1/pedidos/129`

- **Ver funcionando:** la respuesta trae `tipo_borrado` LOGICO. En MySQL Workbench:
  `SELECT estado FROM pedidos WHERE id_pedido = 129;`
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 115 a 125 (`jb_eliminar_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 201 a 212 (`jb_eliminar`)

### 62. Eliminar compra - 200
`DELETE http://localhost:8000/api/v1/compras/11`

- **Ver funcionando:** la respuesta trae `tipo_borrado` FISICO. En MySQL Workbench:
  `SELECT stock_actual FROM insumos WHERE id_insumo = 19;`
- **Código:**
  - `app/routers/jb_compras_router.py`, líneas 78 a 88 (`jb_eliminar_compra`)
  - `app/services/jb_compra_service.py`, líneas 176 a 210 (`jb_eliminar`)

### 63. Eliminar línea de receta - 200
`DELETE http://localhost:8000/api/v1/recetas/59`

- **Ver funcionando:** la respuesta trae `tipo_borrado` FISICO. En MySQL Workbench:
  `SELECT * FROM recetas WHERE id_receta = 59;`
- **Código:**
  - `app/routers/jb_recetas_router.py`, líneas 74 a 80 (`jb_eliminar_receta`)
  - `app/services/jb_receta_service.py`, líneas 107 a 120 (`jb_eliminar`)

### 64. Eliminar cliente - 200
`DELETE http://localhost:8000/api/v1/clientes/19`

- **Ver funcionando:** la respuesta trae `tipo_borrado` LOGICO. En MySQL Workbench:
  `SELECT estado FROM clientes WHERE id_cliente = 19;`
- **Código:**
  - `app/routers/jb_clientes_router.py`, líneas 82 a 87 (`jb_eliminar_cliente`)
  - `app/services/jb_cliente_service.py`, líneas 66 a 87 (`jb_eliminar`)

### 65. Eliminar proveedor - 200
`DELETE http://localhost:8000/api/v1/proveedores/11`

- **Ver funcionando:** la respuesta trae `tipo_borrado` FISICO. En MySQL Workbench:
  `SELECT * FROM proveedores WHERE id_proveedor = 11;`
- **Código:**
  - `app/routers/jb_proveedores_router.py`, líneas 82 a 88 (`jb_eliminar_proveedor`)
  - `app/services/jb_proveedor_service.py`, líneas 66 a 87 (`jb_eliminar`)

### 66. Eliminar insumo - 200
`DELETE http://localhost:8000/api/v1/insumos/19`

- **Ver funcionando:** la respuesta trae `tipo_borrado` LOGICO. En MySQL Workbench:
  `SELECT estado FROM insumos WHERE id_insumo = 19;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 111 a 119 (`jb_eliminar_insumo`)
  - `app/services/jb_insumo_service.py`, líneas 69 a 90 (`jb_eliminar`)

### 67. Eliminar producto - 200
`DELETE http://localhost:8000/api/v1/productos/16`

- **Ver funcionando:** la respuesta trae `tipo_borrado` LOGICO. En MySQL Workbench:
  `SELECT estado FROM productos WHERE id_producto = 16;`
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 114 a 123 (`jb_eliminar_producto`)
  - `app/services/jb_producto_service.py`, líneas 103 a 124 (`jb_eliminar`)

### 68. Eliminar categoría - 200
`DELETE http://localhost:8000/api/v1/categorias/11`

- **Ver funcionando:** la respuesta trae `tipo_borrado` LOGICO. En MySQL Workbench:
  `SELECT estado FROM categorias WHERE id_categoria = 11;`
- **Código:**
  - `app/routers/jb_categorias_router.py`, líneas 66 a 72 (`jb_eliminar_categoria`)
  - `app/services/jb_categoria_service.py`, líneas 64 a 85 (`jb_eliminar`)

### 69. Eliminar usuario - 200
`DELETE http://localhost:8000/api/v1/usuarios/12`

- **Ver funcionando:** la respuesta trae `tipo_borrado` FISICO. En MySQL Workbench:
  `SELECT * FROM usuarios WHERE id_usuario = 12;`
- **Código:**
  - `app/routers/jb_usuarios_router.py`, líneas 74 a 84 (`jb_eliminar_usuario`)
  - `app/services/jb_usuario_service.py`, líneas 100 a 127 (`jb_eliminar`)

### 70. Eliminar usuario - 200
`DELETE http://localhost:8000/api/v1/usuarios/11`

- **Ver funcionando:** la respuesta trae `tipo_borrado` FISICO. En MySQL Workbench:
  `SELECT * FROM usuarios WHERE id_usuario = 11;`
- **Código:**
  - `app/routers/jb_usuarios_router.py`, líneas 74 a 84 (`jb_eliminar_usuario`)
  - `app/services/jb_usuario_service.py`, líneas 100 a 127 (`jb_eliminar`)
