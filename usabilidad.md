# Usabilidad: rutas y datos para Thunder Client

## Autenticación

Todas las rutas llevan en Auth > Bearer el `access_token` que devuelve el paso 1, menos los login (pasos 1, E2, E3 y N4) y la prueba E1.


---


### 1. Iniciar sesión - 200
`POST http://localhost:8000/api/v1/auth/login`
```json
{
  "correo": "burbano@gastronomia.com",
  "password": "ADMIN_1234"
}
```

- **Ver funcionando:** la respuesta trae `access_token`. En MySQL Workbench:
  `SELECT correo, rol, estado FROM usuarios WHERE correo = 'burbano@gastronomia.com';`
- **Código:**
  - `app/routers/jb_auth_router.py`, líneas 30 a 39 (`jb_login`)
  - `app/services/jb_auth_service.py`, líneas 14 a 36 (`jb_iniciar_sesion`)
  - `app/core/jb_security.py`, líneas 44 a 53 (`jb_verificar_password`)
  - `app/core/jb_security.py`, líneas 57 a 72 (`jb_crear_token`)


---


### 2. Ver mi perfil - 200
`GET http://localhost:8000/api/v1/auth/perfil`

- **Ver funcionando:** la respuesta trae su usuario, sin contraseña. En MySQL Workbench:
  `SELECT id_usuario, correo, rol FROM usuarios WHERE id_usuario = 1;`
- **Código:**
  - `app/routers/jb_auth_router.py`, líneas 68 a 76 (`jb_perfil`)
  - `app/core/jb_security.py`, líneas 82 a 133 (`jb_usuario_actual`)


---


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



<br>

---

## Usuarios

### 4. Listar usuarios - 200
`GET http://localhost:8000/api/v1/usuarios`

- **Ver funcionando:** la respuesta trae la lista de usuarios. En MySQL Workbench:
  `SELECT id_usuario, correo, rol, estado FROM usuarios;`
- **Código:**
  - `app/routers/jb_usuarios_router.py`, líneas 30 a 35 (`jb_listar_usuarios`)
  - `app/services/jb_usuario_service.py`, líneas 16 a 18 (`jb_listar`)


---


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


---


### 6. Consultar usuario - 200
`GET http://localhost:8000/api/v1/usuarios/12`

- **Ver funcionando:** la respuesta trae el usuario 12. En MySQL Workbench:
  `SELECT * FROM usuarios WHERE id_usuario = 12;`
- **Código:**
  - `app/routers/jb_usuarios_router.py`, líneas 39 a 44 (`jb_obtener_usuario`)
  - `app/services/jb_usuario_service.py`, líneas 22 a 30 (`jb_obtener`)


---


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



<br>

---

## Categorías

### 8. Listar categorías - 200
`GET http://localhost:8000/api/v1/categorias`

- **Ver funcionando:** la respuesta trae las 10 categorías. En MySQL Workbench:
  `SELECT * FROM categorias;`
- **Código:**
  - `app/routers/jb_categorias_router.py`, líneas 27 a 32 (`jb_listar_categorias`)
  - `app/services/jb_categoria_service.py`, líneas 14 a 16 (`jb_listar`)


---


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


---


### 10. Consultar categoría - 200
`GET http://localhost:8000/api/v1/categorias/11`

- **Ver funcionando:** la respuesta trae la categoría 11. En MySQL Workbench:
  `SELECT * FROM categorias WHERE id_categoria = 11;`
- **Código:**
  - `app/routers/jb_categorias_router.py`, líneas 36 a 42 (`jb_obtener_categoria`)
  - `app/services/jb_categoria_service.py`, líneas 20 a 28 (`jb_obtener`)


---


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



<br>

---

## Productos

### 12. Listar productos - 200
`GET http://localhost:8000/api/v1/productos`

- **Ver funcionando:** la respuesta trae los 15 productos con su `nombre_categoria`. En MySQL Workbench:
  `SELECT * FROM productos;`
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 38 a 43 (`jb_listar_productos`)
  - `app/services/jb_producto_service.py`, líneas 21 a 23 (`jb_listar`)


---


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
  - `app/routers/jb_productos_router.py`, líneas 94 a 103 (`jb_crear_producto`)
  - `app/services/jb_producto_service.py`, líneas 65 a 75 (`jb_crear`)
  - `app/services/jb_producto_service.py`, líneas 39 a 51 (`jb_validar_categoria`)


---


### 14. Consultar producto - 200
`GET http://localhost:8000/api/v1/productos/16`

- **Ver funcionando:** la respuesta trae el producto 16. En MySQL Workbench:
  `SELECT * FROM productos WHERE id_producto = 16;`
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 57 a 63 (`jb_obtener_producto`)
  - `app/services/jb_producto_service.py`, líneas 27 a 35 (`jb_obtener`)


---


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
  - `app/routers/jb_productos_router.py`, líneas 107 a 113 (`jb_actualizar_producto`)
  - `app/services/jb_producto_service.py`, líneas 79 a 99 (`jb_actualizar`)


---


### 16. Productos de una categoría - 200
`GET http://localhost:8000/api/v1/productos/categoria/11`

- **Ver funcionando:** la respuesta trae el Jugo de mora. En MySQL Workbench:
  `SELECT id_producto, nombre FROM productos WHERE id_categoria = 11;`
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 47 a 53 (`jb_productos_por_categoria`)
  - `app/services/jb_producto_service.py`, líneas 55 a 61 (`jb_por_categoria`)



<br>

---

## Insumos

### 17. Listar insumos - 200
`GET http://localhost:8000/api/v1/insumos`

- **Ver funcionando:** la respuesta trae los 18 insumos. En MySQL Workbench:
  `SELECT * FROM insumos;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 70 a 75 (`jb_listar_insumos`)
  - `app/services/jb_insumo_service.py`, líneas 19 a 21 (`jb_listar`)


---


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


---


### 19. Consultar insumo - 200
`GET http://localhost:8000/api/v1/insumos/19`

- **Ver funcionando:** la respuesta trae el insumo 19. En MySQL Workbench:
  `SELECT * FROM insumos WHERE id_insumo = 19;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 79 a 84 (`jb_obtener_insumo`)
  - `app/services/jb_insumo_service.py`, líneas 25 a 33 (`jb_obtener`)


---


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


---


### 21. Insumos con stock bajo - 200
`GET http://localhost:8000/api/v1/insumos/stock-bajo`

- **Ver funcionando:** la respuesta trae Leche entera, Mantequilla y Tomate con su `faltante`. En MySQL Workbench:
  `SELECT nombre, stock_actual, stock_minimo FROM insumos WHERE stock_actual <= stock_minimo;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 41 a 49 (`jb_insumos_stock_bajo`)
  - `app/services/jb_insumo_service.py`, líneas 94 a 96 (`jb_stock_bajo`)


---


### 22. Insumos por vencer - 200
`GET http://localhost:8000/api/v1/insumos/por-vencer?dias=7`

- **Ver funcionando:** la respuesta trae 5 insumos con sus `dias_restantes`. En MySQL Workbench:
  `SELECT nombre, fecha_vencimiento FROM insumos WHERE fecha_vencimiento BETWEEN CURDATE() AND CURDATE() + INTERVAL 7 DAY;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 53 a 66 (`jb_insumos_por_vencer`)
  - `app/services/jb_insumo_service.py`, líneas 100 a 105 (`jb_por_vencer`)



<br>

---

## Recetas

### 23. Listar recetas - 200
`GET http://localhost:8000/api/v1/recetas`

- **Ver funcionando:** la respuesta trae las 57 líneas de receta. En MySQL Workbench:
  `SELECT * FROM recetas;`
- **Código:**
  - `app/routers/jb_recetas_router.py`, líneas 32 a 37 (`jb_listar_recetas`)
  - `app/services/jb_receta_service.py`, líneas 16 a 18 (`jb_listar`)


---


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


---


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


---


### 26. Consultar línea de receta - 200
`GET http://localhost:8000/api/v1/recetas/58`

- **Ver funcionando:** la respuesta trae la línea 58. En MySQL Workbench:
  `SELECT * FROM recetas WHERE id_receta = 58;`
- **Código:**
  - `app/routers/jb_recetas_router.py`, líneas 41 a 46 (`jb_obtener_receta`)
  - `app/services/jb_receta_service.py`, líneas 22 a 30 (`jb_obtener`)


---


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


---


### 28. Receta del producto - 200
`GET http://localhost:8000/api/v1/productos/16/receta`

- **Ver funcionando:** la respuesta trae los 2 insumos con su `costo_linea`. En MySQL Workbench:
  `SELECT i.nombre, r.cantidad, i.costo_unitario FROM recetas r JOIN insumos i ON i.id_insumo = r.id_insumo WHERE r.id_producto = 16;`
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 67 a 76 (`jb_receta_producto`)
  - `app/services/jb_producto_service.py`, líneas 157 a 161 (`jb_receta`)
  - `app/services/jb_producto_service.py`, líneas 128 a 153 (`jb_lineas_receta`)


---


### 29. Costo y margen del producto - 200
`GET http://localhost:8000/api/v1/productos/16/costo`

- **Ver funcionando:** la respuesta trae `costo_produccion` 840, `margen` 4160 y `margen_porcentaje` 83.2. En MySQL Workbench:
  `SELECT SUM(r.cantidad * i.costo_unitario) AS costo FROM recetas r JOIN insumos i ON i.id_insumo = r.id_insumo WHERE r.id_producto = 16;`
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 80 a 90 (`jb_costo_producto`)
  - `app/services/jb_producto_service.py`, líneas 165 a 195 (`jb_costo`)
  - `app/services/jb_producto_service.py`, líneas 128 a 153 (`jb_lineas_receta`)



<br>

---

## Proveedores

### 30. Listar proveedores - 200
`GET http://localhost:8000/api/v1/proveedores`

- **Ver funcionando:** la respuesta trae los 10 proveedores. En MySQL Workbench:
  `SELECT * FROM proveedores;`
- **Código:**
  - `app/routers/jb_proveedores_router.py`, líneas 34 a 39 (`jb_listar_proveedores`)
  - `app/services/jb_proveedor_service.py`, líneas 16 a 18 (`jb_listar`)


---


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


---


### 32. Consultar proveedor - 200
`GET http://localhost:8000/api/v1/proveedores/11`

- **Ver funcionando:** la respuesta trae el proveedor 11. En MySQL Workbench:
  `SELECT * FROM proveedores WHERE id_proveedor = 11;`
- **Código:**
  - `app/routers/jb_proveedores_router.py`, líneas 43 a 48 (`jb_obtener_proveedor`)
  - `app/services/jb_proveedor_service.py`, líneas 22 a 30 (`jb_obtener`)


---


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



<br>

---

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


---


### 35. Comprobar que subió el stock (RN02) - 200
`GET http://localhost:8000/api/v1/insumos/19`

- **Ver funcionando:** la respuesta trae `stock_actual` 18 y `costo_unitario` 6200. En MySQL Workbench:
  `SELECT stock_actual, costo_unitario FROM insumos WHERE id_insumo = 19;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 79 a 84 (`jb_obtener_insumo`)
  - `app/services/jb_insumo_service.py`, líneas 25 a 33 (`jb_obtener`)


---


### 36. Listar compras - 200
`GET http://localhost:8000/api/v1/compras`

- **Ver funcionando:** la respuesta trae las compras con su detalle. En MySQL Workbench:
  `SELECT * FROM compras ORDER BY fecha_compra DESC;`
- **Código:**
  - `app/routers/jb_compras_router.py`, líneas 30 a 35 (`jb_listar_compras`)
  - `app/services/jb_compra_service.py`, líneas 23 a 25 (`jb_listar`)


---


### 37. Consultar compra - 200
`GET http://localhost:8000/api/v1/compras/11`

- **Ver funcionando:** la respuesta trae la compra 11 con sus 2 ítems. En MySQL Workbench:
  `SELECT * FROM compras WHERE id_compra = 11;`
- **Código:**
  - `app/routers/jb_compras_router.py`, líneas 39 a 44 (`jb_obtener_compra`)
  - `app/services/jb_compra_service.py`, líneas 29 a 37 (`jb_obtener`)


---


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


---


### 39. Compras de un proveedor - 200
`GET http://localhost:8000/api/v1/proveedores/11/compras`

- **Ver funcionando:** la respuesta trae la compra 11. En MySQL Workbench:
  `SELECT * FROM compras WHERE id_proveedor = 11;`
- **Código:**
  - `app/routers/jb_proveedores_router.py`, líneas 52 a 58 (`jb_compras_proveedor`)
  - `app/services/jb_proveedor_service.py`, líneas 91 a 95 (`jb_compras`)



<br>

---

## Clientes

### 40. Listar clientes - 200
`GET http://localhost:8000/api/v1/clientes`

- **Ver funcionando:** la respuesta trae los 18 clientes. En MySQL Workbench:
  `SELECT * FROM clientes;`
- **Código:**
  - `app/routers/jb_clientes_router.py`, líneas 34 a 39 (`jb_listar_clientes`)
  - `app/services/jb_cliente_service.py`, líneas 16 a 18 (`jb_listar`)


---


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


---


### 42. Consultar cliente - 200
`GET http://localhost:8000/api/v1/clientes/19`

- **Ver funcionando:** la respuesta trae el cliente 19. En MySQL Workbench:
  `SELECT * FROM clientes WHERE id_cliente = 19;`
- **Código:**
  - `app/routers/jb_clientes_router.py`, líneas 43 a 48 (`jb_obtener_cliente`)
  - `app/services/jb_cliente_service.py`, líneas 22 a 30 (`jb_obtener`)


---


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



<br>

---

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
  - `app/routers/jb_pedidos_router.py`, líneas 73 a 84 (`jb_crear_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 136 a 165 (`jb_crear`)
  - `app/services/jb_pedido_service.py`, líneas 98 a 132 (`jb_armar_detalle`)


---


### 45. Listar pedidos - 200
`GET http://localhost:8000/api/v1/pedidos`

- **Ver funcionando:** la respuesta trae los pedidos con su detalle. En MySQL Workbench:
  `SELECT * FROM pedidos ORDER BY fecha_pedido DESC;`
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 40 a 45 (`jb_listar_pedidos`)
  - `app/services/jb_pedido_service.py`, líneas 37 a 39 (`jb_listar`)


---


### 46. Consultar pedido - 200
`GET http://localhost:8000/api/v1/pedidos/130`

- **Ver funcionando:** la respuesta trae el pedido 130. En MySQL Workbench:
  `SELECT * FROM pedidos WHERE id_pedido = 130;`
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 63 a 69 (`jb_obtener_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 43 a 51 (`jb_obtener`)


---


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
  - `app/routers/jb_pedidos_router.py`, líneas 88 a 97 (`jb_actualizar_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 169 a 197 (`jb_actualizar`)
  - `app/services/jb_pedido_service.py`, líneas 73 a 78 (`jb_validar_abierto`)
  - `app/services/jb_pedido_service.py`, líneas 98 a 132 (`jb_armar_detalle`)


---


### 48. Pedidos por estado - 200
`GET http://localhost:8000/api/v1/pedidos/estado/PENDIENTE`

- **Ver funcionando:** la respuesta trae los pedidos PENDIENTE. En MySQL Workbench:
  `SELECT id_pedido, estado FROM pedidos WHERE estado = 'PENDIENTE';`
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 49 a 59 (`jb_pedidos_por_estado`)
  - `app/services/jb_pedido_service.py`, líneas 55 a 57 (`jb_por_estado`)


---


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
  - `app/routers/jb_pedidos_router.py`, líneas 101 a 113 (`jb_cambiar_estado_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 267 a 287 (`jb_cambiar_estado`)
  - `app/services/jb_pedido_service.py`, líneas 24 a 33 (`JB_TRANSICIONES`)


---


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
  - `app/routers/jb_pedidos_router.py`, líneas 101 a 113 (`jb_cambiar_estado_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 267 a 287 (`jb_cambiar_estado`)
  - `app/services/jb_pedido_service.py`, líneas 232 a 263 (`jb_descontar_inventario`)
  - `app/services/jb_pedido_service.py`, líneas 216 a 228 (`jb_insumos_necesarios`)


---


### 51. Comprobar que bajó el stock (RN03) - 200
`GET http://localhost:8000/api/v1/insumos/19`

- **Ver funcionando:** la respuesta trae `stock_actual` 17.76. En MySQL Workbench:
  `SELECT stock_actual FROM insumos WHERE id_insumo = 19;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 79 a 84 (`jb_obtener_insumo`)
  - `app/services/jb_insumo_service.py`, líneas 25 a 33 (`jb_obtener`)


---


### 52. Pedidos de un cliente - 200
`GET http://localhost:8000/api/v1/clientes/19/pedidos`

- **Ver funcionando:** la respuesta trae el pedido 130. En MySQL Workbench:
  `SELECT * FROM pedidos WHERE id_cliente = 19;`
- **Código:**
  - `app/routers/jb_clientes_router.py`, líneas 52 a 58 (`jb_pedidos_cliente`)
  - `app/services/jb_cliente_service.py`, líneas 91 a 95 (`jb_pedidos`)



<br>

---

## Reportes

### 53. Ventas por fechas - 200
`GET http://localhost:8000/api/v1/reportes/ventas?desde=2026-10-01&hasta=2026-10-31`

- **Ver funcionando:** la respuesta trae `numero_pedidos`, `total_vendido` y `promedio_por_pedido`. En MySQL Workbench:
  `SELECT COUNT(*), SUM(total) FROM pedidos WHERE estado = 'ENTREGADO' AND fecha_pedido >= '2026-10-01' AND fecha_pedido < '2026-11-01';`
- **Código:**
  - `app/routers/jb_reportes_router.py`, líneas 35 a 51 (`jb_reporte_ventas`)
  - `app/services/jb_reporte_service.py`, líneas 17 a 44 (`jb_ventas`)
  - `app/repositories/jb_reporte_repository.py`, líneas 17 a 37 (`jb_ventas`)


---


### 54. Productos más vendidos - 200
`GET http://localhost:8000/api/v1/reportes/productos-mas-vendidos?limite=5`

- **Ver funcionando:** la respuesta trae el ranking con su `posicion`. En MySQL Workbench:
  `SELECT p.nombre, SUM(d.cantidad) AS vendidos FROM detalle_pedido d JOIN pedidos pe ON pe.id_pedido = d.id_pedido JOIN productos p ON p.id_producto = d.id_producto WHERE pe.estado = 'ENTREGADO' GROUP BY p.id_producto, p.nombre ORDER BY vendidos DESC LIMIT 5;`
- **Código:**
  - `app/routers/jb_reportes_router.py`, líneas 55 a 68 (`jb_productos_mas_vendidos`)
  - `app/services/jb_reporte_service.py`, líneas 48 a 68 (`jb_mas_vendidos`)
  - `app/repositories/jb_reporte_repository.py`, líneas 41 a 65 (`jb_mas_vendidos`)



<br>

---

## Calificaciones (MongoDB)

Las calificaciones son la única clase que se guarda en MongoDB. Las demás (usuarios, clientes, productos, pedidos...) están en MySQL y se consultan con SQL en MySQL Workbench.

MongoDB no usa SQL: si en MONGOSH escribe `select * from clientes;`, responde `SyntaxError`. Sus comandos se escriben en JavaScript, en la pestaña MONGOSH de MongoDB Compass (ícono `>_` junto a la conexión, en la barra izquierda). Antes de los comandos de los pasos 55 a 60, escriba esto una vez y pulse Enter:

`use bd_gastronomia_nosql`

Debe responder `switched to db bd_gastronomia_nosql`. Después escriba el comando de cada paso y pulse Enter.

| Para | MySQL Workbench (SQL) | MongoDB Compass, pestaña MONGOSH |
|---|---|---|
| Elegir la base | `USE bd_gastronomia;` | `use bd_gastronomia_nosql` |
| Ver las tablas (en MongoDB, colecciones) | `SHOW TABLES;` | `show collections` |
| Ver todo | `SELECT * FROM tabla;` | `db.coleccion.find()` |
| Buscar | `SELECT * FROM tabla WHERE campo = 130;` | `db.coleccion.find({ campo: 130 })` |
| Ver solo algunos campos | `SELECT campo1, campo2 FROM tabla WHERE campo = 130;` | `db.coleccion.find({ campo: 130 }, { campo1: 1, campo2: 1 })` |
| Contar | `SELECT COUNT(*) FROM tabla;` | `db.coleccion.countDocuments()` |

En MongoDB la tabla se llama colección y cada fila es un documento. Lo que va dentro de `find( )` es lo mismo que se escribe en la casilla Filter de la pestaña Documents.


---


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

- **Ver funcionando:** la respuesta trae `id_calificacion` (24 caracteres) y el nombre de cada producto. Anote el `id_calificacion` (ID_CALIFICACION), porque lo usan los pasos 57, 58 y 60. En MongoDB Compass, pestaña MONGOSH:
  `db.calificaciones.find({ id_pedido: 130 })`
- **Código:**
  - `app/routers/jb_calificaciones_router.py`, líneas 76 a 87 (`jb_crear_calificacion`)
  - `app/services/jb_calificacion_service.py`, líneas 104 a 131 (`jb_crear`)
  - `app/services/jb_calificacion_service.py`, líneas 65 a 100 (`jb_validar_contra_mysql`)


---


### 56. Listar calificaciones - 200
`GET http://localhost:8000/api/v1/calificaciones`

- **Ver funcionando:** la respuesta trae las 11 calificaciones. En MongoDB Compass, pestaña MONGOSH:
  `db.calificaciones.find()`
  Para contarlas:
  `db.calificaciones.countDocuments()`
- **Código:**
  - `app/routers/jb_calificaciones_router.py`, líneas 43 a 48 (`jb_listar_calificaciones`)
  - `app/services/jb_calificacion_service.py`, líneas 47 a 49 (`jb_listar`)


---


### 57. Consultar calificación - 200
`GET http://localhost:8000/api/v1/calificaciones/ID_CALIFICACION`

- **Ver funcionando:** la respuesta trae la calificación del pedido 130. En MongoDB Compass, pestaña MONGOSH, cambiando ID_CALIFICACION por el id del paso 55 (MongoDB guarda el id como ObjectId):
  `db.calificaciones.find({ _id: ObjectId("ID_CALIFICACION") })`
- **Código:**
  - `app/routers/jb_calificaciones_router.py`, líneas 66 a 72 (`jb_obtener_calificacion`)
  - `app/services/jb_calificacion_service.py`, líneas 53 a 61 (`jb_obtener`)


---


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

- **Ver funcionando:** la respuesta trae `calificacion_servicio` 4. En MongoDB Compass, pestaña MONGOSH. El segundo `{ }` elige los campos que se muestran, como las columnas del SELECT:
  `db.calificaciones.find({ id_pedido: 130 }, { calificacion_servicio: 1, comentario: 1, productos: 1 })`
- **Código:**
  - `app/routers/jb_calificaciones_router.py`, líneas 91 a 100 (`jb_actualizar_calificacion`)
  - `app/services/jb_calificacion_service.py`, líneas 135 a 158 (`jb_actualizar`)


---


### 59. Calificaciones y promedio de un producto - 200
`GET http://localhost:8000/api/v1/calificaciones/producto/16`

- **Ver funcionando:** la respuesta trae `total_calificaciones` y `promedio` 4. En MongoDB Compass, pestaña MONGOSH:
  `db.calificaciones.find({ "productos.id_producto": 16 })`
  El promedio, con el mismo cálculo que hace la API (responde `total` 1 y `promedio` 4):
  `db.calificaciones.aggregate([{ $unwind: "$productos" }, { $match: { "productos.id_producto": 16 } }, { $group: { _id: "$productos.id_producto", total: { $sum: 1 }, promedio: { $avg: "$productos.calificacion" } } }])`
- **Código:**
  - `app/routers/jb_calificaciones_router.py`, líneas 52 a 62 (`jb_calificaciones_producto`)
  - `app/services/jb_calificacion_service.py`, líneas 172 a 213 (`jb_por_producto`)
  - `app/repositories/jb_calificacion_repository.py`, líneas 75 a 95 (`jb_resumen_producto`)



<br>

---

## Pruebas de errores

### E1. Sin token - 401
`GET http://localhost:8000/api/v1/auth/perfil`
(en Auth elija "No Auth")

- **Ver funcionando:** la respuesta trae `detalle`: "Token requerido...". Este error no cambia nada en la base.
- **Código:**
  - `app/routers/jb_auth_router.py`, líneas 68 a 76 (`jb_perfil`)
  - `app/core/jb_security.py`, líneas 82 a 133 (`jb_usuario_actual`)


---


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


---


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


---


### E4. No existe - 404
`GET http://localhost:8000/api/v1/productos/999`

- **Ver funcionando:** la respuesta trae `detalle`: "El producto 999 no existe". Este error no cambia nada en la base.
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 57 a 63 (`jb_obtener_producto`)
  - `app/services/jb_producto_service.py`, líneas 27 a 35 (`jb_obtener`)
  - `app/services/jb_comun.py`, líneas 7 a 10 (`jb_no_encontrado`)


---


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


---


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
  - `app/routers/jb_pedidos_router.py`, líneas 88 a 97 (`jb_actualizar_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 169 a 197 (`jb_actualizar`)
  - `app/services/jb_pedido_service.py`, líneas 73 a 78 (`jb_validar_abierto`)


---


### E7. Cambio de estado no permitido - 409
`PATCH http://localhost:8000/api/v1/pedidos/128/estado`
```json
{
  "estado": "ENTREGADO"
}
```

- **Ver funcionando:** la respuesta trae `detalle`: "Un pedido PENDIENTE solo puede pasar a EN_PREPARACION o ANULADO". Este error no cambia nada en la base.
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 101 a 113 (`jb_cambiar_estado_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 267 a 287 (`jb_cambiar_estado`)
  - `app/services/jb_pedido_service.py`, líneas 24 a 33 (`JB_TRANSICIONES`)


---


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


---


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
  - `app/routers/jb_pedidos_router.py`, líneas 73 a 84 (`jb_crear_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 136 a 165 (`jb_crear`)
  - `app/services/jb_pedido_service.py`, líneas 82 a 94 (`jb_validar_cliente`)


---


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
  - `app/routers/jb_productos_router.py`, líneas 94 a 103 (`jb_crear_producto`)
  - `app/services/jb_producto_service.py`, líneas 65 a 75 (`jb_crear`)
  - `app/schemas/jb_tipos.py`, líneas 52 a 52 (`JbDineroPositivo`)
  - `app/core/jb_errores.py`, líneas 168 a 212 (`jb_traducir_error`)


---


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
  - `app/routers/jb_pedidos_router.py`, líneas 73 a 84 (`jb_crear_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 136 a 165 (`jb_crear`)
  - `app/schemas/jb_tipos.py`, líneas 76 a 81 (`JbModeloEntrada`)



<br>

---

## Eliminar (en este orden)

### 60. Eliminar calificación - 200
`DELETE http://localhost:8000/api/v1/calificaciones/ID_CALIFICACION`

- **Ver funcionando:** la respuesta trae `tipo_borrado` FISICO. En MongoDB Compass, pestaña MONGOSH. Debe responder 0, porque ya no existe:
  `db.calificaciones.countDocuments({ id_pedido: 130 })`
- **Código:**
  - `app/routers/jb_calificaciones_router.py`, líneas 104 a 110 (`jb_eliminar_calificacion`)
  - `app/services/jb_calificacion_service.py`, líneas 162 a 168 (`jb_eliminar`)


---


### 61. Anular pedido - 200
`DELETE http://localhost:8000/api/v1/pedidos/129`

- **Ver funcionando:** la respuesta trae `tipo_borrado` LOGICO. En MySQL Workbench:
  `SELECT estado FROM pedidos WHERE id_pedido = 129;`
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 117 a 127 (`jb_eliminar_pedido`)
  - `app/services/jb_pedido_service.py`, líneas 201 a 212 (`jb_eliminar`)


---


### 62. Eliminar compra - 200
`DELETE http://localhost:8000/api/v1/compras/11`

- **Ver funcionando:** la respuesta trae `tipo_borrado` FISICO. En MySQL Workbench:
  `SELECT stock_actual FROM insumos WHERE id_insumo = 19;`
- **Código:**
  - `app/routers/jb_compras_router.py`, líneas 78 a 88 (`jb_eliminar_compra`)
  - `app/services/jb_compra_service.py`, líneas 176 a 210 (`jb_eliminar`)


---


### 63. Eliminar línea de receta - 200
`DELETE http://localhost:8000/api/v1/recetas/59`

- **Ver funcionando:** la respuesta trae `tipo_borrado` FISICO. En MySQL Workbench:
  `SELECT * FROM recetas WHERE id_receta = 59;`
- **Código:**
  - `app/routers/jb_recetas_router.py`, líneas 74 a 80 (`jb_eliminar_receta`)
  - `app/services/jb_receta_service.py`, líneas 107 a 120 (`jb_eliminar`)


---


### 64. Eliminar cliente - 200
`DELETE http://localhost:8000/api/v1/clientes/19`

- **Ver funcionando:** la respuesta trae `tipo_borrado` LOGICO. En MySQL Workbench:
  `SELECT estado FROM clientes WHERE id_cliente = 19;`
- **Código:**
  - `app/routers/jb_clientes_router.py`, líneas 82 a 87 (`jb_eliminar_cliente`)
  - `app/services/jb_cliente_service.py`, líneas 66 a 87 (`jb_eliminar`)


---


### 65. Eliminar proveedor - 200
`DELETE http://localhost:8000/api/v1/proveedores/11`

- **Ver funcionando:** la respuesta trae `tipo_borrado` FISICO. En MySQL Workbench:
  `SELECT * FROM proveedores WHERE id_proveedor = 11;`
- **Código:**
  - `app/routers/jb_proveedores_router.py`, líneas 82 a 88 (`jb_eliminar_proveedor`)
  - `app/services/jb_proveedor_service.py`, líneas 66 a 87 (`jb_eliminar`)


---


### 66. Eliminar insumo - 200
`DELETE http://localhost:8000/api/v1/insumos/19`

- **Ver funcionando:** la respuesta trae `tipo_borrado` LOGICO. En MySQL Workbench:
  `SELECT estado FROM insumos WHERE id_insumo = 19;`
- **Código:**
  - `app/routers/jb_insumos_router.py`, líneas 111 a 119 (`jb_eliminar_insumo`)
  - `app/services/jb_insumo_service.py`, líneas 69 a 90 (`jb_eliminar`)


---


### 67. Eliminar producto - 200
`DELETE http://localhost:8000/api/v1/productos/16`

- **Ver funcionando:** la respuesta trae `tipo_borrado` LOGICO. En MySQL Workbench:
  `SELECT estado FROM productos WHERE id_producto = 16;`
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 117 a 126 (`jb_eliminar_producto`)
  - `app/services/jb_producto_service.py`, líneas 103 a 124 (`jb_eliminar`)


---


### 68. Eliminar categoría - 200
`DELETE http://localhost:8000/api/v1/categorias/11`

- **Ver funcionando:** la respuesta trae `tipo_borrado` LOGICO. En MySQL Workbench:
  `SELECT estado FROM categorias WHERE id_categoria = 11;`
- **Código:**
  - `app/routers/jb_categorias_router.py`, líneas 66 a 72 (`jb_eliminar_categoria`)
  - `app/services/jb_categoria_service.py`, líneas 64 a 85 (`jb_eliminar`)


---


### 69. Eliminar usuario - 200
`DELETE http://localhost:8000/api/v1/usuarios/12`

- **Ver funcionando:** la respuesta trae `tipo_borrado` FISICO. En MySQL Workbench:
  `SELECT * FROM usuarios WHERE id_usuario = 12;`
- **Código:**
  - `app/routers/jb_usuarios_router.py`, líneas 74 a 84 (`jb_eliminar_usuario`)
  - `app/services/jb_usuario_service.py`, líneas 100 a 127 (`jb_eliminar`)


---


### 70. Eliminar usuario - 200
`DELETE http://localhost:8000/api/v1/usuarios/11`

- **Ver funcionando:** la respuesta trae `tipo_borrado` FISICO. En MySQL Workbench:
  `SELECT * FROM usuarios WHERE id_usuario = 11;`
- **Código:**
  - `app/routers/jb_usuarios_router.py`, líneas 74 a 84 (`jb_eliminar_usuario`)
  - `app/services/jb_usuario_service.py`, líneas 100 a 127 (`jb_eliminar`)



<br>

---

## Descuento en un producto

`PATCH /api/v1/productos/{id_producto}/descuento`, solo para ADMIN. Baja el precio de venta de un producto en un porcentaje, con esta fórmula: `precio nuevo = precio actual x (100 - porcentaje) / 100`. El Jugo de lulo (producto 9) cuesta 4500; con 10 % de descuento queda en 4050.

Los pedidos anteriores no cambian: la tabla `detalle_pedido` guarda el `precio_unitario` que tenía el producto cuando se registró cada pedido (RN01). El descuento solo se nota en los pedidos nuevos.


---


### Qué es PATCH, para qué sirve y cómo se ejecuta

**Qué es.** Cada petición lleva un método que le dice a la API qué hacer con el registro. PATCH es el método para **modificar solo una parte** de un registro que ya existe. Estos son los métodos que usa esta API:

| Método | Para qué | Ejemplo | Lleva body | Responde |
|---|---|---|---|---|
| GET | Consultar | `GET /productos/9` | No | 200 |
| POST | Crear un registro nuevo | `POST /productos` | Sí, con todos los datos del registro | 201 |
| PUT | Reemplazar un registro completo | `PUT /productos/9` | Sí, con todos los campos, aunque solo cambie uno | 200 |
| PATCH | Cambiar solo una parte | `PATCH /productos/9/descuento` | Sí, solo con lo que cambia | 200 |
| DELETE | Eliminar | `DELETE /productos/16` | No | 200 |

**Para qué sirve.** Para cambiar un dato sin enviar el registro completo. En esta API hay dos PATCH:

- `PATCH /pedidos/{id}/estado` (pasos 49 y 50): cambia solo el estado del pedido.
- `PATCH /productos/{id}/descuento` (paso N1): cambia solo el precio de venta.

Por ejemplo, para dejar el Jugo de lulo en 4050 con PUT hay que enviar el producto completo. Si falta un campo, la API responde 422 "Es obligatorio". Además, quien lo envía tiene que calcular el precio:

`PUT http://localhost:8000/api/v1/productos/9` (solo para comparar; no hace falta enviarla)
```json
{
  "codigo": "BEB-001",
  "nombre": "Jugo de lulo",
  "descripcion": "Jugo natural de lulo en agua",
  "precio_venta": 4050,
  "unidad_venta": "vaso",
  "id_categoria": 2,
  "estado": "DISPONIBLE"
}
```

Con PATCH basta con lo que cambia, y la API hace la cuenta:

`PATCH http://localhost:8000/api/v1/productos/9/descuento`
```json
{
  "porcentaje": 10
}
```

**Cómo se ejecuta.** La URL dice **a cuál** registro se le hace el cambio: el 9 de `/productos/9/descuento` es el id del producto. El body dice **qué** se cambia: el porcentaje. En Thunder Client:

1. En la barra izquierda de VS Code, abra Thunder Client (el ícono del rayo).
2. Cree la petición:
   - si ya tiene su colección: pestaña Collections, menú (...) de la carpeta Productos > New Request, y póngale de nombre `Aplicar descuento`. Así queda guardada en esa carpeta desde el principio;
   - si no: pulse **New Request** arriba. Al terminar, guárdela en su colección con la opción Save to Collection.
3. En la lista del método, que dice GET, elija **PATCH**.
4. En la dirección escriba `http://localhost:8000/api/v1/productos/9/descuento`. Cambie el 9 por el id del producto que quiera rebajar. Si creó el entorno de la sección 6 del README, también sirve `{{url}}/productos/9/descuento`.
5. Pestaña **Auth** > **Bearer**: pegue el `access_token` de un ADMIN, el del paso 1 (o `{{token}}` si usa el entorno).
6. Pestaña **Body** > **JSON**: escriba el body. Al elegir JSON, Thunder Client agrega solo el encabezado `Content-Type: application/json`.

```json
{
  "porcentaje": 10
}
```

7. Pulse **Send**. Debe salir **200 OK**, no 201, porque PATCH modifica un registro y no crea uno nuevo. La respuesta es:

```json
{
  "id_producto": 9,
  "nombre": "Jugo de lulo",
  "precio_anterior": 4500.0,
  "porcentaje": 10.0,
  "precio_nuevo": 4050.0
}
```

8. Pestaña **Tests**: agregue una prueba de que el código de respuesta sea igual a 200.

Reglas para escribir el body:

- Todo va entre llaves `{ }`.
- El nombre del campo va entre comillas dobles y escrito igual que en el esquema, en minúsculas: `"porcentaje"`.
- Después del nombre van dos puntos y el valor.
- Los números van sin comillas y con punto decimal: `10` o `12.5`, no `12,5`.
- Después del último campo no va coma.
- Solo se envía `porcentaje`: cualquier otro campo es rechazado.

Si el body está mal, la API responde **422** y no cambia nada en la base. Estos son los mensajes:

| Body enviado | Campo | Mensaje |
|---|---|---|
| `{}` | porcentaje | Es obligatorio |
| (Body vacío) | (todo el cuerpo) | Es obligatorio |
| `{"porcentaje": 10,}` (coma de más) | (todo el cuerpo) | El cuerpo no es un JSON válido: revise comas, comillas y llaves |
| `{porcentaje: 10}` (sin comillas en el nombre) | (todo el cuerpo) | El cuerpo no es un JSON válido: revise comas, comillas y llaves |
| `{"porcentaje": "diez"}` | porcentaje | Debe ser un número |
| `{"Porcentaje": 10}` (con mayúscula) | porcentaje y Porcentaje | Es obligatorio / Este campo no está permitido |
| `{"porcentaje": 10, "precio_venta": 3000}` | precio_venta | Este campo no está permitido |
| `{"porcentaje": 0}` | porcentaje | Debe ser mayor que 0 |
| `{"porcentaje": 100}` | porcentaje | Debe ser menor que 100 |
| `{"porcentaje": 12.345}` | porcentaje | Debe tener máximo 2 decimales |


---


### N1. Aplicar descuento - 200
`PATCH http://localhost:8000/api/v1/productos/9/descuento`
```json
{
  "porcentaje": 10
}
```

- **Ver funcionando:** la respuesta trae `precio_anterior` 4500, `porcentaje` 10 y `precio_nuevo` 4050. Si la envía otra vez, descuenta sobre el precio nuevo: 4050 pasa a 3645. En MySQL Workbench:
  `SELECT nombre, precio_venta FROM productos WHERE id_producto = 9;`
  Los pedidos anteriores siguen con su precio:
  `SELECT id_pedido, precio_unitario FROM detalle_pedido WHERE id_producto = 9;`
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 131 a 141 (`jb_descuento_producto`)
  - `app/services/jb_producto_service.py`, líneas 200 a 235 (`jb_aplicar_descuento`)
  - `app/schemas/jb_producto_schema.py`, líneas 131 a 136 (`JbDescuento`)
  - `app/schemas/jb_producto_schema.py`, líneas 140 a 150 (`JbDescuentoRespuesta`)


---


### N2. Descuento del 100 % - 422
`PATCH http://localhost:8000/api/v1/productos/9/descuento`
```json
{
  "porcentaje": 100
}
```

- **Ver funcionando:** la respuesta trae `errores` con el campo porcentaje: "Debe ser menor que 100". Este error no cambia nada en la base.
- **Código:**
  - `app/schemas/jb_producto_schema.py`, líneas 131 a 136 (`JbDescuento`)


---


### N3. Producto que no existe - 404
`PATCH http://localhost:8000/api/v1/productos/999/descuento`
```json
{
  "porcentaje": 10
}
```

- **Ver funcionando:** la respuesta trae `detalle`: "El producto 999 no existe". Este error no cambia nada en la base.
- **Código:**
  - `app/services/jb_producto_service.py`, líneas 200 a 235 (`jb_aplicar_descuento`)


---


### N4. Descuento con un usuario CAJERO - 403
Primero inicie sesión como CAJERO:

`POST http://localhost:8000/api/v1/auth/login`
```json
{
  "correo": "carlos.rojas@gastronomia.com",
  "password": "Cajero123*"
}
```
Luego, con ese token, envíe la petición N1.

- **Ver funcionando:** la respuesta trae `detalle`: "Acceso denegado: esta acción requiere el rol ADMIN". Este error no cambia nada en la base. Después vuelva a hacer el paso 1 para recuperar el token del ADMIN.
- **Código:**
  - `app/routers/jb_productos_router.py`, líneas 32 a 32 (`JB_ADMIN`)
  - `app/core/jb_security.py`, líneas 137 a 155 (`jb_requiere_roles`)



<br>

---

## Venta rápida de un producto

`POST /api/v1/pedidos/venta`, solo para ADMIN. Recibe el cliente, el producto y la cantidad, y en una sola petición:

1. revisa que el cliente exista y esté ACTIVO, y que el producto esté DISPONIBLE;
2. toma el precio de la base de datos y calcula el subtotal y el total (RN01);
3. registra el pedido ya ENTREGADO;
4. descuenta del inventario los insumos de la receta (RN03).

Una venta normal necesita tres peticiones: registrar el pedido (paso 44), pasarlo a EN_PREPARACION (paso 49) y luego a ENTREGADO (paso 50). La venta rápida lo hace en una sola, para el mostrador, cuando el cliente se lleva el producto de una vez.

**Todo o nada:** el pedido y el descuento del inventario van en la misma transacción. Si el inventario no alcanza, la API responde 409 y MySQL deshace el pedido: no queda nada guardado.

**Cómo se ejecuta.** En Thunder Client cree la petición igual que la del descuento, en la carpeta Pedidos, con el nombre `Venta rápida`:

- método **POST**;
- dirección `http://localhost:8000/api/v1/pedidos/venta`;
- Auth > Bearer con el token del ADMIN;
- Body > JSON con el JSON del paso N5;
- en Tests, que el código de respuesta sea igual a 201.

Antes de pulsar Send, mire el inventario en MySQL Workbench para comparar después:
`SELECT id_insumo, nombre, stock_actual FROM insumos WHERE id_insumo IN (8, 11);`


---


### N5. Venta rápida - 201
`POST http://localhost:8000/api/v1/pedidos/venta`
```json
{
  "id_cliente": 1,
  "id_producto": 9,
  "cantidad": 2
}
```

- **Ver funcionando:**
  - la respuesta trae `estado` ENTREGADO, `tipo_pedido` PARA_LLEVAR e `id_usuario` 1 (el ADMIN);
  - en el detalle, `precio_unitario` es 4050, el precio con el descuento de N1, y `subtotal` y `total` son 8100. Si no hizo N1, son 4500 y 9000;
  - anote el `id_pedido` de la respuesta (ID_VENTA), porque lo usa el paso N9.
  
  La receta del Jugo de lulo lleva 0.12 kg de lulo y 0.025 kg de azúcar por vaso. Por 2 vasos, el Lulo baja 0.24 y el Azúcar baja 0.05. Con los datos iniciales, el Lulo pasa de 9.5 a 9.26 y el Azúcar de 24 a 23.95. En MySQL Workbench:
  `SELECT id_insumo, nombre, stock_actual FROM insumos WHERE id_insumo IN (8, 11);`
  `SELECT * FROM pedidos ORDER BY id_pedido DESC LIMIT 1;`
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 136 a 147 (`jb_venta_rapida`)
  - `app/services/jb_pedido_service.py`, líneas 292 a 328 (`jb_vender`)
  - `app/schemas/jb_pedido_schema.py`, líneas 122 a 139 (`JbVentaCrear`)


---


### N6. Venta sin inventario suficiente (RN03) - 409
`POST http://localhost:8000/api/v1/pedidos/venta`
```json
{
  "id_cliente": 1,
  "id_producto": 9,
  "cantidad": 1000
}
```

- **Ver funcionando:** la respuesta trae `detalle`: "Inventario insuficiente para entregar el pedido (RN03)...", con lo que se necesita y lo que hay de cada insumo. No se guardó nada: la consulta de pedidos sigue mostrando la venta de N5 y el stock no cambió. El número de pedido que se alcanzó a usar no se vuelve a usar, así que la siguiente venta salta un número; MySQL hace eso con AUTO_INCREMENT. En MySQL Workbench:
  `SELECT * FROM pedidos ORDER BY id_pedido DESC LIMIT 1;`
  `SELECT id_insumo, nombre, stock_actual FROM insumos WHERE id_insumo IN (8, 11);`
- **Código:**
  - `app/services/jb_pedido_service.py`, líneas 292 a 328 (`jb_vender`)
  - `app/services/jb_pedido_service.py`, líneas 232 a 263 (`jb_descontar_inventario`)
  - `app/database/jb_conexion_mysql.py`, líneas 62 a 79 (`jb_obtener_sesion`)


---


### N7. Venta de un producto AGOTADO - 400
`POST http://localhost:8000/api/v1/pedidos/venta`
```json
{
  "id_cliente": 1,
  "id_producto": 13,
  "cantidad": 1
}
```

- **Ver funcionando:** la respuesta trae `detalle`: "El producto 'Hamburguesa sencilla' no se puede pedir: está AGOTADO". Este error no cambia nada en la base.
- **Código:**
  - `app/services/jb_pedido_service.py`, líneas 98 a 132 (`jb_armar_detalle`)


---


### N8. Venta con un usuario CAJERO - 403
Inicie sesión como CAJERO (igual que en N4) y, con ese token, envíe la petición N5.

- **Ver funcionando:** la respuesta trae `detalle`: "Acceso denegado: esta acción requiere el rol ADMIN". El cajero sí puede registrar pedidos con POST /pedidos, pero la venta rápida es solo para ADMIN. Este error no cambia nada en la base. Después vuelva a hacer el paso 1 para recuperar el token del ADMIN.
- **Código:**
  - `app/routers/jb_pedidos_router.py`, líneas 132 a 132 (`jb_solo_admin`)


---


### N9. La venta ya no se puede anular (RN05) - 409
`PATCH http://localhost:8000/api/v1/pedidos/ID_VENTA/estado`
```json
{
  "estado": "ANULADO"
}
```

- **Ver funcionando:** la respuesta trae `detalle`: "El pedido ID_VENTA está ENTREGADO y no puede modificarse (RN05)". La venta nace ENTREGADO, así que las reglas de los pedidos cerrados se le aplican sin escribir código nuevo. En MySQL Workbench:
  `SELECT id_pedido, estado FROM pedidos WHERE id_pedido = ID_VENTA;`
- **Código:**
  - `app/services/jb_pedido_service.py`, líneas 73 a 78 (`jb_validar_abierto`)


---


### Volver al precio original del Jugo de lulo

Ejecute en MySQL Workbench, o vuelva a los datos iniciales (paso 4 de "Antes de empezar", al final de esta guía):
`UPDATE productos SET precio_venta = 4500 WHERE id_producto = 9;`



<br>

---

## Cómo programar una funcionalidad nueva (paso a paso)

Esta parte explica, paso a paso y con el código, cómo se programaron las dos funcionalidades nuevas. Sirve de modelo si en la sustentación le piden hacer otra:

- **Ejemplo A. Descuento:** `PATCH /api/v1/productos/{id_producto}/descuento`. Cómo se usa: sección "Descuento en un producto", pasos N1 a N4.
- **Ejemplo B. Venta rápida:** `POST /api/v1/pedidos/venta`. Cómo se usa: sección "Venta rápida de un producto", pasos N5 a N9.

Los dos ya están en el proyecto. Cada bloque nuevo lleva arriba un comentario que empieza por `# ----- DESCUENTO` o `# ----- VENTA RAPIDA`. Para encontrarlos en VS Code, pulse Ctrl+Shift+F y busque `DESCUENTO` o `VENTA RAPIDA`; la tabla "Dónde está cada paso en el código" dice el archivo y las líneas. Los dos endpoints también están en la tabla de la sección 7 del README, que ahora cuenta 67 endpoints.


---


### Cómo viaja una petición dentro de la API

1. Thunder Client envía el método (GET, POST, PUT, PATCH o DELETE), la URL, el token y el JSON.
2. La **ruta** (`app/routers`) recibe la petición y revisa el token y el rol. Sin token responde 401; con un rol sin permiso, 403.
3. El **esquema** (`app/schemas`) revisa el JSON. Si falta un campo o un valor no sirve, responde 422 y la petición no llega al servicio.
4. El **servicio** (`app/services`) aplica la regla de negocio: calcula, compara con lo que hay en la base y decide (400, 404 o 409 si algo no se cumple).
5. El **repositorio** (`app/repositories`) hace las consultas a MySQL.
6. La ruta devuelve la respuesta con la forma del esquema de respuesta.

Por eso un endpoint nuevo se arma en este orden: primero el esquema (qué entra y qué sale), después el servicio (la regla) y al final la ruta (la dirección y el rol). En estos dos ejemplos no hace falta tocar el repositorio, porque las consultas que se necesitan ya existen. Al repositorio solo se le agrega una función cuando hace falta una consulta nueva.


---


### Dónde está cada paso en el código

Los archivos están dentro de la carpeta `api_gastronomia`. Las líneas incluyen el comentario `# -----` que marca cada bloque.

| Paso | Qué hay | Archivo | Líneas |
|---|---|---|---|
| A1 | import de `Decimal` | `app/schemas/jb_producto_schema.py` | 2 a 4 |
| A1 | esquemas `JbDescuento` y `JbDescuentoRespuesta` | `app/schemas/jb_producto_schema.py` | 129 a 150 |
| A2 | servicio `jb_aplicar_descuento` | `app/services/jb_producto_service.py` | 198 a 235 |
| A3 | import de los esquemas del descuento | `app/routers/jb_productos_router.py` | 14 a 16 |
| A3 | ruta `jb_descuento_producto` (PATCH /productos/{id}/descuento) | `app/routers/jb_productos_router.py` | 129 a 141 |
| B1 | esquema `JbVentaCrear` | `app/schemas/jb_pedido_schema.py` | 120 a 139 |
| B2 | servicio `jb_vender` | `app/services/jb_pedido_service.py` | 290 a 328 |
| B3 | import de `JbVentaCrear` | `app/routers/jb_pedidos_router.py` | 23 a 24 |
| B3 | ruta `jb_venta_rapida` (POST /pedidos/venta) | `app/routers/jb_pedidos_router.py` | 130 a 147 |


---


### Antes de empezar

1. Encienda las bases de datos: doble clic en `C:\Users\BURBANO\bd_gastronomia_local\iniciar_bases.bat`

2. Encienda el servidor en la terminal de VS Code. Corre con `--reload`: cada vez que guarda un archivo (Ctrl+S) se reinicia solo. Si el código tiene un error, la terminal lo muestra y la API no responde hasta que lo corrija.

   ```
   cd "C:\Users\BURBANO\Desktop\TRABAJOS\Miercoles\istructivo mongo db\api_gastronomia"
   venv\Scripts\activate
   uvicorn app.jb_main:jb_app --reload
   ```

3. Para ver las bases de datos:
   - **MySQL Workbench:** ya está creada la conexión `API_WILSON` (Hostname `127.0.0.1`, Port `3306`, Username `root`, contraseña `1234` guardada, base `bd_gastronomia`). Ábrala con doble clic, escriba `USE bd_gastronomia;` y luego la consulta de cada paso. Para ejecutar, pulse el rayo.
   - **MongoDB Compass:** conéctese con `mongodb://jb_root:CLAVE@localhost:27018/?authSource=admin`, cambiando CLAVE por la de `MONGO_ROOT_PASSWORD` del `.env`. Para ver los datos, abra la pestaña MONGOSH, escriba `use bd_gastronomia_nosql` y luego el comando de cada paso (55 a 60). Para ejecutar, pulse Enter. En MONGOSH no se escribe SQL: vea la tabla de equivalencias al inicio de la sección "Calificaciones (MongoDB)".

4. Vuelva a los datos iniciales antes de seguir los pasos de esta guía, si ya hizo otras pruebas, y también al terminar. Los ids de esta guía (usuario 11, categoría 11, producto 16, pedido 130...) salen de los datos iniciales: si la base tiene registros de otras pruebas, los ids cambian y las respuestas no coinciden con lo que dice cada paso.
   - En Workbench: File > Open SQL Script, abra `database/01_jb_ddl_bd_gastronomia.sql` y ejecútelo con el rayo. Haga lo mismo con el 02 y el 03.
   - En Compass: abra la pestaña MONGOSH, pegue todo el contenido de `database/04_jb_mongo_calificaciones.js` y pulse Enter.

5. Inicie sesión como ADMIN (paso 1) y copie el `access_token`.

6. Si arma otro endpoint copiando estos bloques, cópielos completos y tal cual. En Python los espacios al inicio de la línea (la sangría) son parte del código: no los cambie.



<br>

---

## Ejemplo A. Programar el descuento

**Por qué PATCH:** el descuento cambia solo una parte del producto, el precio. Con PUT habría que enviar el producto completo (ver "Qué es PATCH, para qué sirve y cómo se ejecuta", en la sección "Descuento en un producto").


---


### A1. Esquema: qué entra y qué sale

Archivo `app/schemas/jb_producto_schema.py`.

1. Líneas 2 a 4: el import de `Decimal`, arriba, después de la primera línea (el texto entre comillas triples):

```python
# ----- DESCUENTO (usabilidad.md, paso A1): import de Decimal -----
# Decimal: números exactos para el porcentaje del descuento
from decimal import Decimal
```

2. Líneas 129 a 150, al final del archivo: los dos esquemas.

```python
# ----- DESCUENTO (usabilidad.md, paso A1): esquemas JbDescuento y JbDescuentoRespuesta -----
# Datos para aplicar un descuento (PATCH /productos/{id}/descuento)
class JbDescuento(JbModeloEntrada):
    # Porcentaje de descuento: mayor que 0, menor que 100 y con máximo 2 decimales
    porcentaje: Decimal = Field(gt=0, lt=100, max_digits=5, decimal_places=2)

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{"porcentaje": 10}]})


# Resultado del descuento: el precio de antes y el de ahora
class JbDescuentoRespuesta(BaseModel):
    # Id del producto
    id_producto: int
    # Nombre del producto
    nombre: str
    # Precio antes del descuento
    precio_anterior: JbNumero
    # Porcentaje aplicado
    porcentaje: JbNumero
    # Precio después del descuento
    precio_nuevo: JbNumero
```

Qué significa:

- `JbDescuento` hereda de `JbModeloEntrada`: quita los espacios sobrantes de los textos y rechaza los campos que no conoce.
- `Field(gt=0, lt=100, ...)`: `gt` es "greater than" (mayor que) y `lt` es "less than" (menor que). Si el porcentaje no cumple, la API responde 422 sin llegar al servicio.
- `Decimal` guarda el número exacto. Con `float`, 0.1 + 0.2 da 0.30000000000000004, y con dinero eso no sirve.
- `JbDescuentoRespuesta` es la forma de la respuesta. `JbNumero` hace que los decimales salgan en el JSON como números.


---


### A2. Servicio: la regla del descuento

Archivo `app/services/jb_producto_service.py`, líneas 198 a 235, al final del archivo:

```python
# ----- DESCUENTO (usabilidad.md, paso A2): servicio jb_aplicar_descuento -----
# Baja el precio de venta de un producto en un porcentaje
def jb_aplicar_descuento(jb_sesion: Session, jb_id: int, jb_porcentaje: Decimal) -> dict:
    """Precio nuevo = precio actual x (100 - porcentaje) / 100. Los pedidos ya registrados no cambian:
    detalle_pedido guardó el precio que tenía el producto en ese momento (RN01)."""
    # Busca el producto y lo bloquea mientras se modifica
    jb_producto = jb_repositorio.jb_buscar_para_actualizar(jb_sesion, jb_id)
    # Si no existe...
    if jb_producto is None:
        # ...404
        raise jb_no_encontrado(f"El producto {jb_id}")
    # Guarda el precio de antes para mostrarlo en la respuesta
    jb_precio_anterior = jb_producto.precio_venta
    # Calcula el precio nuevo y lo redondea a 2 decimales
    jb_precio_nuevo = jb_dinero(jb_precio_anterior * (100 - jb_porcentaje) / 100)
    # La tabla no acepta precios en 0 (CHECK precio_venta > 0)
    if jb_precio_nuevo <= 0:
        # 400 explicando qué hacer
        raise jb_dato_invalido("Con ese descuento el precio quedaría en 0: use un porcentaje menor")
    # Cambia el precio de venta
    jb_producto.precio_venta = jb_precio_nuevo
    # Envía el UPDATE a MySQL
    jb_repositorio.jb_guardar(jb_sesion, jb_producto)
    # Confirma la transacción
    jb_sesion.commit()
    # Devuelve el precio de antes y el de ahora
    return {
        # Id del producto
        "id_producto": jb_id,
        # Nombre del producto
        "nombre": jb_producto.nombre,
        # Precio antes del descuento
        "precio_anterior": jb_precio_anterior,
        # Porcentaje aplicado
        "porcentaje": jb_porcentaje,
        # Precio después del descuento
        "precio_nuevo": jb_precio_nuevo,
    }
```

Qué significa:

- `jb_buscar_para_actualizar` hace `SELECT ... FOR UPDATE`: bloquea el producto mientras cambia, para que otro usuario no lo modifique al mismo tiempo.
- `jb_dinero` redondea a 2 decimales, igual que la columna `DECIMAL(10,2)`.
- `commit` confirma el cambio en MySQL. Sin `commit`, el cambio se pierde al terminar la petición.
- No hizo falta agregar imports: `Decimal`, `jb_dinero`, `jb_dato_invalido` y `jb_no_encontrado` ya estaban importados al inicio de ese archivo.


---


### A3. Ruta: la dirección y el rol

Archivo `app/routers/jb_productos_router.py`.

1. Líneas 14 a 16, dentro del bloque `from app.schemas.jb_producto_schema import (`, debajo de `JbCostoProducto`:

```python
    # ----- DESCUENTO (usabilidad.md, paso A3): esquemas del descuento -----
    JbDescuento,  # datos del descuento
    JbDescuentoRespuesta,  # forma de la respuesta del descuento
```

2. Líneas 129 a 141, al final del archivo:

```python
# ----- DESCUENTO (usabilidad.md, paso A3): ruta PATCH /api/v1/productos/{id_producto}/descuento -----
# PATCH /api/v1/productos/{id}/descuento: baja el precio de venta en un porcentaje (solo ADMIN)
@jb_router.patch("/{id_producto}/descuento", response_model=JbDescuentoRespuesta, dependencies=JB_ADMIN,
                 summary="Aplicar descuento", responses={**JB_R400, **JB_R404})  # título en Swagger y errores que puede responder
# Recibe el id_producto de la URL, el cuerpo JSON ya validado y la sesión de MySQL
def jb_descuento_producto(id_producto: int, jb_datos: JbDescuento, jb_sesion: JbSesion):
    """Baja el precio de venta en el porcentaje enviado (mayor que 0 y menor que 100).
    Cada descuento se calcula sobre el precio actual. Los pedidos ya registrados conservan su precio.

    **Roles:** ADMIN.
    """
    # Pasa el id y el porcentaje al servicio
    return jb_servicio.jb_aplicar_descuento(jb_sesion, id_producto, jb_datos.porcentaje)
```

Qué significa:

- `@jb_router.patch("/{id_producto}/descuento", ...)`: el router ya tiene el prefijo `/productos` y `app/jb_main.py` le pone `/api/v1` adelante. La dirección completa queda `/api/v1/productos/{id_producto}/descuento`.
- `{id_producto}` en la dirección y `id_producto: int` en la función tienen el mismo nombre: así FastAPI sabe que el 9 de `/productos/9/descuento` es el id del producto.
- `jb_datos: JbDescuento`: FastAPI lee el JSON y lo valida con el esquema del paso A1.
- `dependencies=JB_ADMIN`: solo deja pasar a ADMIN. `JB_ADMIN` ya está definido arriba en el archivo. Para permitir también al cajero, cambie `dependencies=JB_ADMIN` por `dependencies=[Depends(jb_requiere_roles("ADMIN", "CAJERO"))]`.
- `response_model=JbDescuentoRespuesta`: la forma de la respuesta.
- El texto entre comillas triples es la descripción que se ve en Swagger.


---


### A4. Guardar y ver el endpoint en Swagger

1. Si el servidor estaba encendido con `--reload`, ya se reinició solo con el código nuevo: en la terminal salió `Reloading...` y luego `Application startup complete.` Si estaba apagado, enciéndalo (paso 2 de "Antes de empezar").
2. Abra http://localhost:8000/docs. En la sección Productos aparece `PATCH /api/v1/productos/{id_producto}/descuento` con el título "Aplicar descuento".
3. Para usarlo, siga los pasos N1 a N4 de la sección "Descuento en un producto".



<br>

---

## Ejemplo B. Programar la venta rápida

**Por qué va en pedidos:** una venta es un pedido. Así el código nuevo reutiliza tres funciones que ya existen en `jb_pedido_service.py`: `jb_validar_cliente`, `jb_armar_detalle` (RN01) y `jb_descontar_inventario` (RN03). Además, la venta sale en los reportes como cualquier pedido ENTREGADO.


---


### B1. Esquema: qué entra

Archivo `app/schemas/jb_pedido_schema.py`, líneas 120 a 139, al final del archivo:

```python
# ----- VENTA RAPIDA (usabilidad.md, paso B1): esquema JbVentaCrear -----
# Datos para vender un producto en un solo paso (POST /pedidos/venta)
class JbVentaCrear(JbModeloEntrada):
    # Cliente que compra: debe existir y estar ACTIVO
    id_cliente: int = Field(gt=0)
    # Producto que se vende: debe estar DISPONIBLE
    id_producto: int = Field(gt=0)
    # Cantidad mayor que 0, con máximo 2 decimales
    cantidad: JbCantidadPedido
    # Tipo de pedido; si no se envía queda PARA_LLEVAR
    tipo_pedido: JbTipoPedido = "PARA_LLEVAR"
    # Observaciones opcionales, máximo 255 caracteres
    observaciones: str | None = Field(default=None, max_length=255)

    # Ejemplo que muestra Swagger al pulsar "Try it out"
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "id_cliente": 1,  # ejemplo del campo id_cliente
        "id_producto": 9,  # ejemplo del campo id_producto
        "cantidad": 2,  # ejemplo del campo cantidad
    }]})
```

Qué significa:

- Usa los mismos tipos que el pedido normal: `JbCantidadPedido` (mayor que 0, hasta 2 decimales) y `JbTipoPedido` (MESA, PARA_LLEVAR o EVENTO).
- `tipo_pedido: JbTipoPedido = "PARA_LLEVAR"`: el `=` le da un valor por defecto. Si el JSON no trae `tipo_pedido`, queda PARA_LLEVAR.
- No hay campos de precio ni de total porque los calcula la API (RN01). Si alguien los envía, la API responde 422, porque `JbModeloEntrada` rechaza los campos que no conoce.
- La respuesta usa el esquema que ya existe, `JbPedidoRespuesta`: no hay que crear otro.
- No hizo falta agregar imports: todo lo que usa ya estaba importado en ese archivo.


---


### B2. Servicio: la regla de la venta

Archivo `app/services/jb_pedido_service.py`, líneas 290 a 328, al final del archivo:

```python
# ----- VENTA RAPIDA (usabilidad.md, paso B2): servicio jb_vender -----
# Vende un producto en un solo paso: registra el pedido ya ENTREGADO y descuenta el inventario
def jb_vender(jb_sesion: Session, jb_datos: dict, jb_id_usuario: int) -> JbPedido:
    """Venta de mostrador: hace en una sola petición lo que normalmente son tres (registrar el pedido,
    pasarlo a EN_PREPARACION y a ENTREGADO). Todo va en una sola transacción: si el inventario
    no alcanza responde 409 (RN03) y no se guarda nada."""
    # Comprueba el cliente (400 si no existe o está INACTIVO)
    jb_cliente = jb_validar_cliente(jb_sesion, jb_datos["id_cliente"])
    # El producto y la cantidad, con la misma forma que un ítem de POST /pedidos
    jb_items = [{"id_producto": jb_datos["id_producto"], "cantidad": jb_datos["cantidad"]}]
    # RN01: valida el producto y calcula subtotal y total; el precio sale de la base de datos
    jb_detalle, jb_total = jb_armar_detalle(jb_sesion, jb_items)
    # Arma el pedido
    jb_pedido = JbPedido(
        # Fecha y hora actual de Colombia
        fecha_pedido=jb_ahora(),
        # Cliente
        cliente=jb_cliente,
        # Usuario que vende (viene del token)
        id_usuario=jb_id_usuario,
        # Tipo de pedido
        tipo_pedido=jb_datos["tipo_pedido"],
        # La venta queda entregada de una vez: el cliente se lleva el producto
        estado="ENTREGADO",
        # Total calculado (RN01)
        total=jb_total,
        # Observaciones; get devuelve None si no se enviaron
        observaciones=jb_datos.get("observaciones"),
        # Ítem de la venta
        detalle=jb_detalle,
    )
    # Inserta el pedido y su ítem sin confirmar todavía; así el ítem ya tiene el id del producto
    jb_repositorio.jb_guardar(jb_sesion, jb_pedido)
    # RN03: descuenta los insumos de la receta; si no alcanzan responde 409 y se deshace el INSERT
    jb_descontar_inventario(jb_sesion, jb_pedido)
    # Confirma todo junto: el pedido y el inventario
    jb_sesion.commit()
    # Devuelve el pedido registrado
    return jb_pedido
```

Qué significa:

- `jb_items` arma una lista con la misma forma que el `detalle` de POST /pedidos. Así se puede reutilizar `jb_armar_detalle` sin cambiarla.
- `jb_guardar` envía el INSERT a MySQL pero todavía no lo confirma. Hace falta antes de descontar el inventario, porque `jb_descontar_inventario` lee el `id_producto` de cada ítem, y ese dato se llena cuando se envía el INSERT.
- Si `jb_descontar_inventario` responde 409, el `commit` nunca se ejecuta y `jb_obtener_sesion` (en `app/database/jb_conexion_mysql.py`) hace rollback: el INSERT se deshace.
- No hizo falta agregar imports: `JbPedido`, `jb_ahora` y las tres funciones que reutiliza ya estaban en ese archivo.


---


### B3. Ruta: la dirección y el rol

Archivo `app/routers/jb_pedidos_router.py`.

1. Líneas 23 a 24, dentro del bloque `from app.schemas.jb_pedido_schema import (`, debajo de `JbPedidoRespuesta`:

```python
    # ----- VENTA RAPIDA (usabilidad.md, paso B3): esquema de la venta -----
    JbVentaCrear,  # datos de la venta rápida
```

2. Líneas 130 a 147, al final del archivo:

```python
# ----- VENTA RAPIDA (usabilidad.md, paso B3): ruta POST /api/v1/pedidos/venta -----
# Dependencia para la venta rápida: solo ADMIN
jb_solo_admin = jb_requiere_roles("ADMIN")


# POST /api/v1/pedidos/venta: vende un producto en un solo paso (201, solo ADMIN)
@jb_router.post("/venta", response_model=JbPedidoRespuesta, status_code=status.HTTP_201_CREATED,
                summary="Venta rápida de un producto", responses={**JB_R400, **JB_R409})  # título en Swagger y errores que puede responder
# jb_usuario es el ADMIN que hace la venta (sale del token)
def jb_venta_rapida(jb_datos: JbVentaCrear, jb_sesion: JbSesion, jb_usuario: Annotated[JbUsuario, Depends(jb_solo_admin)]):
    """Registra un pedido de un solo producto que queda ENTREGADO de una vez.
    **RN01:** el precio sale de la base de datos. **RN03:** descuenta del inventario los insumos de la receta;
    si no alcanzan responde 409 y no se guarda nada.

    **Roles:** ADMIN.
    """
    # Pasa los datos y el id del usuario del token al servicio
    return jb_servicio.jb_vender(jb_sesion, jb_datos.model_dump(), jb_usuario.id_usuario)
```

Qué significa:

- `jb_solo_admin = jb_requiere_roles("ADMIN")` crea la regla que solo deja pasar a ADMIN. Para permitir también al cajero: `jb_requiere_roles("ADMIN", "CAJERO")`.
- `jb_usuario: Annotated[JbUsuario, Depends(jb_solo_admin)]` revisa el rol y además entrega el usuario del token. Así el pedido queda con el `id_usuario` de quien vendió, sin pedirlo en el JSON.
- `status_code=status.HTTP_201_CREATED`: responde 201 porque crea un registro.
- `jb_datos.model_dump()` convierte el esquema validado en un diccionario, que es lo que recibe el servicio.
- La dirección `/venta` no choca con `/{id_pedido}`: esa dirección no tiene POST, solo GET, PUT y DELETE.


---


### B4. Ver el endpoint en Swagger

1. Si el servidor estaba encendido con `--reload`, ya se reinició solo con el código nuevo. Si estaba apagado, enciéndalo (paso 2 de "Antes de empezar").
2. En Swagger, en la sección Pedidos, aparece `POST /api/v1/pedidos/venta` con el título "Venta rápida de un producto".
3. Para usarlo, siga los pasos N5 a N9 de la sección "Venta rápida de un producto".



<br>

---

## Si algo sale mal al programar

Sirve si cambia este código o si arma otro endpoint igual.

| Lo que pasa | Qué revisar |
|---|---|
| La terminal muestra `NameError: name 'JbDescuento' is not defined` (o `JbVentaCrear`) | Falta agregar el nombre al bloque de imports de la ruta (paso A3.1 o B3.1) |
| La terminal muestra `IndentationError` | La sangría quedó mal. Cada nivel son 4 espacios: copie el bloque completo otra vez |
| La terminal muestra `NameError: name 'Decimal' is not defined` | Falta el import del paso A1.1 |
| N1 responde 404 "La ruta no existe" | La ruta nueva no se cargó: guarde el archivo y mire la terminal. Revise también la dirección |
| N5 responde 405 "Método HTTP no permitido" | La ruta nueva no se cargó, y FastAPI tomó `venta` como si fuera un `{id_pedido}`: guarde el archivo y mire la terminal |
| Responde 401 | Falta el token o ya venció: haga el paso 1 otra vez |
| Responde 403 | El token es de un usuario que no es ADMIN |
| Swagger no muestra el endpoint nuevo | Recargue la página con F5. Si sigue sin salir, el servidor no se reinició: mire la terminal |
