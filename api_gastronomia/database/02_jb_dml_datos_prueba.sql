-- Script 02 (DML): datos de prueba de bd_gastronomia (10 o más registros en cada tabla).
-- Se ejecuta como root, después del script 01 (que deja las tablas vacías).
-- Las fechas se calculan desde el día en que se ejecuta el script (CURDATE y NOW), así los insumos
-- por vencer, los pedidos del día y los reportes de los últimos días siempre tienen datos.
-- Los pedidos ENTREGADO ya descontaron su inventario: el stock_actual de los insumos es el que quedó después.
-- Los totales de compras y pedidos cuadran con su detalle (RN01).

-- Todo se inserta en bd_gastronomia
USE bd_gastronomia;

-- usuarios: 10 usuarios, al menos uno por rol. Las contraseñas están cifradas con bcrypt (RN06).
-- Contraseñas de prueba: ADMIN = Admin123*   CAJERO = Cajero123*   COCINERO = Cocinero123*
INSERT INTO usuarios (id_usuario, identificacion, nombres, apellidos, correo, password, rol, estado) VALUES
  -- ADMIN ACTIVO: burbano@gastronomia.com / Admin123*
  (1, '1000000001', 'Administrador', 'del Sistema', 'burbano@gastronomia.com', '$2b$12$3JKw.vA78zuH0uuts/eU5.IArWLoUS7RxMSln0cLaI/0bJ/iR6/sq', 'ADMIN', 'ACTIVO'),
  -- ADMIN ACTIVO: laura.munoz@gastronomia.com / Admin123*
  (2, '1075201112', 'Laura Marcela', 'Muñoz Castro', 'laura.munoz@gastronomia.com', '$2b$12$UTYNQDICamTWPdI/2r9AveBLDdEf5q4Us5wyosCUsMwb9k4K6aD3i', 'ADMIN', 'ACTIVO'),
  -- CAJERO ACTIVO: carlos.rojas@gastronomia.com / Cajero123*
  (3, '1075202223', 'Carlos Andrés', 'Rojas Pérez', 'carlos.rojas@gastronomia.com', '$2b$12$slwChdHoThpdnY1Ez4XNfuMPe9.KzNxvEqTXJWLYuJ43DAVY1Ih1K', 'CAJERO', 'ACTIVO'),
  -- CAJERO ACTIVO: diana.gomez@gastronomia.com / Cajero123*
  (4, '1075203334', 'Diana Patricia', 'Gómez Ruiz', 'diana.gomez@gastronomia.com', '$2b$12$rygaho1ccizQNu8u9ubZqeYopOA4OL6DZhgDjfC3YDwDaskYanwI6', 'CAJERO', 'ACTIVO'),
  -- CAJERO ACTIVO: jhon.ortiz@gastronomia.com / Cajero123*
  (5, '1075204445', 'Jhon Fredy', 'Ortiz Silva', 'jhon.ortiz@gastronomia.com', '$2b$12$CXSI0z2W55maKXuf43CfS.3xmbNyJhjrNiVGM4rp3B0po9yX3liRq', 'CAJERO', 'ACTIVO'),
  -- COCINERO ACTIVO: maria.cruz@gastronomia.com / Cocinero123*
  (6, '1075205556', 'María Fernanda', 'Cruz Peña', 'maria.cruz@gastronomia.com', '$2b$12$6rY41NzQnJnl75zAN02WkeK88z6jZuWG1z8d7eT4IdUuVTHFJ4nJy', 'COCINERO', 'ACTIVO'),
  -- COCINERO ACTIVO: jose.vargas@gastronomia.com / Cocinero123*
  (7, '1075206667', 'José Luis', 'Vargas Díaz', 'jose.vargas@gastronomia.com', '$2b$12$4cHUwjMzXXAK1jKktaG09ehNwj1lEyUOrmw.VBkk2pKJdenU4ADE.', 'COCINERO', 'ACTIVO'),
  -- COCINERO ACTIVO: ana.torres@gastronomia.com / Cocinero123*
  (8, '1075207778', 'Ana Lucía', 'Torres Mora', 'ana.torres@gastronomia.com', '$2b$12$fat9Py0x9K7iKw1xd2wpT.W/Opdy3cziKTaR3FiHWkypogQ.OlxnC', 'COCINERO', 'ACTIVO'),
  -- CAJERO ACTIVO: pedro.ramirez@gastronomia.com / Cajero123*
  (9, '1075208889', 'Pedro Antonio', 'Ramírez León', 'pedro.ramirez@gastronomia.com', '$2b$12$uA4xwetWdFzHAr56NYv0feYGLMpO0qAMIv3Bc9XYDAMovagW5226u', 'CAJERO', 'ACTIVO'),
  -- CAJERO INACTIVO: sandra.castro@gastronomia.com / Cajero123*
  (10, '1075209990', 'Sandra Milena', 'Castro Ríos', 'sandra.castro@gastronomia.com', '$2b$12$4efLTFx2v8hvJA59Mn0qt.VC7mHjhG6deVU4oZ8mblUl0jgi/fA3O', 'CAJERO', 'INACTIVO');

-- categorias: las cuatro de RF03 (Platos, Bebidas, Panadería, Repostería) y seis más
INSERT INTO categorias (id_categoria, nombre, descripcion, estado) VALUES
  -- Categoría 1
  (1, 'Platos', 'Platos fuertes y almuerzos', 'ACTIVO'),
  -- Categoría 2
  (2, 'Bebidas', 'Jugos, limonadas y bebidas frías', 'ACTIVO'),
  -- Categoría 3
  (3, 'Panadería', 'Panes y productos horneados', 'ACTIVO'),
  -- Categoría 4
  (4, 'Repostería', 'Tortas, postres y dulces', 'ACTIVO'),
  -- Categoría 5
  (5, 'Sopas', 'Sopas y cremas del día', 'ACTIVO'),
  -- Categoría 6
  (6, 'Ensaladas', 'Ensaladas frescas', 'ACTIVO'),
  -- Categoría 7
  (7, 'Desayunos', 'Desayunos completos', 'ACTIVO'),
  -- Categoría 8
  (8, 'Comidas rápidas', 'Hamburguesas, perros y sándwiches', 'ACTIVO'),
  -- Categoría 9
  (9, 'Pasabocas', 'Empanadas, buñuelos y fritos', 'ACTIVO'),
  -- Categoría 10
  (10, 'Bebidas calientes', 'Café, chocolate y aromáticas', 'ACTIVO');

-- insumos: stock actual, stock mínimo, costo y vencimiento.
-- Quedan con stock bajo: Tomate, Leche entera y Mantequilla.
-- Vencen en los próximos 7 días: Leche (3), Pechuga de pollo (4), Carne de res (5), Tomate (6) y Lulo (7).
INSERT INTO insumos (id_insumo, nombre, unidad_medida, stock_actual, stock_minimo, costo_unitario, fecha_vencimiento, estado) VALUES
  -- Insumo 1: Arroz, vence en 180 días
  (1, 'Arroz', 'kg', 45, 10, 4200, CURDATE() + INTERVAL 180 DAY, 'ACTIVO'),
  -- Insumo 2: Pechuga de pollo, vence en 4 días
  (2, 'Pechuga de pollo', 'kg', 18.5, 8, 16000, CURDATE() + INTERVAL 4 DAY, 'ACTIVO'),
  -- Insumo 3: Carne de res, vence en 5 días
  (3, 'Carne de res', 'kg', 14.2, 6, 28000, CURDATE() + INTERVAL 5 DAY, 'ACTIVO'),
  -- Insumo 4: Papa, vence en 20 días
  (4, 'Papa', 'kg', 38, 10, 2500, CURDATE() + INTERVAL 20 DAY, 'ACTIVO'),
  -- Insumo 5: Tomate, vence en 6 días
  (5, 'Tomate', 'kg', 6.3, 8, 3800, CURDATE() + INTERVAL 6 DAY, 'ACTIVO'),
  -- Insumo 6: Cebolla cabezona, vence en 25 días
  (6, 'Cebolla cabezona', 'kg', 11, 5, 3000, CURDATE() + INTERVAL 25 DAY, 'ACTIVO'),
  -- Insumo 7: Harina de trigo, vence en 120 días
  (7, 'Harina de trigo', 'kg', 28, 10, 3500, CURDATE() + INTERVAL 120 DAY, 'ACTIVO'),
  -- Insumo 8: Azúcar, vence en 300 días
  (8, 'Azúcar', 'kg', 24, 8, 4000, CURDATE() + INTERVAL 300 DAY, 'ACTIVO'),
  -- Insumo 9: Huevos, vence en 12 días
  (9, 'Huevos', 'unidad', 150, 60, 600, CURDATE() + INTERVAL 12 DAY, 'ACTIVO'),
  -- Insumo 10: Leche entera, vence en 3 días
  (10, 'Leche entera', 'l', 9, 15, 4200, CURDATE() + INTERVAL 3 DAY, 'ACTIVO'),
  -- Insumo 11: Lulo, vence en 7 días
  (11, 'Lulo', 'kg', 9.5, 4, 7000, CURDATE() + INTERVAL 7 DAY, 'ACTIVO'),
  -- Insumo 12: Mantequilla, vence en 40 días
  (12, 'Mantequilla', 'kg', 2.4, 3, 22000, CURDATE() + INTERVAL 40 DAY, 'ACTIVO'),
  -- Insumo 13: Queso campesino, vence en 8 días
  (13, 'Queso campesino', 'kg', 5.8, 3, 18000, CURDATE() + INTERVAL 8 DAY, 'ACTIVO'),
  -- Insumo 14: Café molido, vence en 200 días
  (14, 'Café molido', 'kg', 4.2, 2, 32000, CURDATE() + INTERVAL 200 DAY, 'ACTIVO'),
  -- Insumo 15: Aceite vegetal, vence en 365 días
  (15, 'Aceite vegetal', 'l', 12, 4, 9000, CURDATE() + INTERVAL 365 DAY, 'ACTIVO'),
  -- Insumo 16: Fríjol rojo, vence en 240 días
  (16, 'Fríjol rojo', 'kg', 17, 5, 8000, CURDATE() + INTERVAL 240 DAY, 'ACTIVO'),
  -- Insumo 17: Chocolate de mesa, vence en 150 días
  (17, 'Chocolate de mesa', 'kg', 3.5, 2, 20000, CURDATE() + INTERVAL 150 DAY, 'ACTIVO'),
  -- Insumo 18: Margarina (INACTIVO, sin movimientos)
  (18, 'Margarina', 'kg', 0, 0, 15000, NULL, 'INACTIVO');

-- proveedores: 10 proveedores de la región
INSERT INTO proveedores (id_proveedor, nit, razon_social, telefono, correo, direccion, estado) VALUES
  -- Proveedor 1
  (1, '900123456-1', 'Distribuidora La Cosecha S.A.S.', '3101234567', 'ventas@lacosecha.com', 'Carrera 4 # 5-20, Pitalito', 'ACTIVO'),
  -- Proveedor 2
  (2, '900234567-2', 'Avícola El Campo Ltda.', '3112345678', 'pedidos@avicolaelcampo.com', 'Kilómetro 2 vía La Laguna, Pitalito', 'ACTIVO'),
  -- Proveedor 3
  (3, '900345678-3', 'Carnes del Huila S.A.S.', '3123456789', 'contacto@carnesdelhuila.com', 'Calle 8 # 3-45, Pitalito', 'ACTIVO'),
  -- Proveedor 4
  (4, '900456789-4', 'Lácteos San Agustín', '3134567890', 'ventas@lacteossanagustin.com', 'Vereda Obando, San Agustín', 'ACTIVO'),
  -- Proveedor 5
  (5, '900567890-5', 'Molinos del Sur S.A.', '3145678901', 'comercial@molinosdelsur.com', 'Zona industrial, Neiva', 'ACTIVO'),
  -- Proveedor 6
  (6, '900678901-6', 'Fruver Pitalito', '3156789012', 'fruver@pitalito.com', 'Plaza de mercado, local 12, Pitalito', 'ACTIVO'),
  -- Proveedor 7
  (7, '900789012-7', 'Café Especial del Huila', '3167890123', 'ventas@cafeespecialhuila.com', 'Calle 10 # 2-15, Pitalito', 'ACTIVO'),
  -- Proveedor 8
  (8, '900890123-8', 'Aceites y Grasas del Sur', '3178901234', 'pedidos@aceitesdelsur.com', 'Carrera 15 # 20-30, Neiva', 'ACTIVO'),
  -- Proveedor 9
  (9, '900901234-9', 'Distribuidora Dulce Hogar', '3189012345', 'dulcehogar@correo.com', 'Calle 5 # 7-11, Pitalito', 'ACTIVO'),
  -- Proveedor 10 (sin compras)
  (10, '901012345-0', 'Granos y Abarrotes El Trigal', '3190123456', 'eltrigal@correo.com', 'Carrera 3 # 9-40, Garzón', 'ACTIVO');

-- clientes: de los cuatro tipos. El cliente 18 es el del ejemplo de calificación del instructivo.
INSERT INTO clientes (id_cliente, identificacion, nombres, apellidos, telefono, correo, tipo_cliente, estado) VALUES
  -- Cliente 1: APRENDIZ
  (1, '1075300001', 'Juan Camilo', 'Pérez Gómez', '3201000001', 'juan.perez@soy.sena.edu.co', 'APRENDIZ', 'ACTIVO'),
  -- Cliente 2: APRENDIZ
  (2, '1075300002', 'Valentina', 'Rodríguez Silva', '3201000002', 'valentina.rodriguez@soy.sena.edu.co', 'APRENDIZ', 'ACTIVO'),
  -- Cliente 3: APRENDIZ
  (3, '1075300003', 'Santiago', 'López Muñoz', '3201000003', 'santiago.lopez@soy.sena.edu.co', 'APRENDIZ', 'ACTIVO'),
  -- Cliente 4: APRENDIZ
  (4, '1075300004', 'Daniela', 'Martínez Rojas', '3201000004', 'daniela.martinez@soy.sena.edu.co', 'APRENDIZ', 'ACTIVO'),
  -- Cliente 5: APRENDIZ
  (5, '1075300005', 'Kevin Alejandro', 'Guzmán Ortiz', '3201000005', 'kevin.guzman@soy.sena.edu.co', 'APRENDIZ', 'ACTIVO'),
  -- Cliente 6: INSTRUCTOR
  (6, '12198765', 'Hernando', 'Cabrera Luna', '3152000006', 'hcabrera@sena.edu.co', 'INSTRUCTOR', 'ACTIVO'),
  -- Cliente 7: INSTRUCTOR
  (7, '36178945', 'Gloria Inés', 'Perdomo Vargas', '3152000007', 'gperdomo@sena.edu.co', 'INSTRUCTOR', 'ACTIVO'),
  -- Cliente 8: INSTRUCTOR
  (8, '83245671', 'Álvaro', 'Quintero Bahamón', '3152000008', 'aquintero@sena.edu.co', 'INSTRUCTOR', 'ACTIVO'),
  -- Cliente 9: FUNCIONARIO
  (9, '26456789', 'Marleny', 'Losada Cuéllar', '3152000009', 'mlosada@sena.edu.co', 'FUNCIONARIO', 'ACTIVO'),
  -- Cliente 10: FUNCIONARIO
  (10, '12234567', 'Fabio Nelson', 'Salazar Trujillo', '3152000010', 'fsalazar@sena.edu.co', 'FUNCIONARIO', 'ACTIVO'),
  -- Cliente 11: FUNCIONARIO
  (11, '55123456', 'Rosa Elena', 'Medina Polanco', '3152000011', 'rmedina@sena.edu.co', 'FUNCIONARIO', 'ACTIVO'),
  -- Cliente 12: EXTERNO
  (12, '1080100012', 'Camila', 'Andrade Rivera', '3163000012', 'camila.andrade@gmail.com', 'EXTERNO', 'ACTIVO'),
  -- Cliente 13: EXTERNO
  (13, '1080100013', 'Luis Eduardo', 'Chávez Ortega', '3163000013', 'luis.chavez@gmail.com', 'EXTERNO', 'ACTIVO'),
  -- Cliente 14: EXTERNO
  (14, '1080100014', 'Paola Andrea', 'Fierro Calderón', '3163000014', 'paola.fierro@hotmail.com', 'EXTERNO', 'ACTIVO'),
  -- Cliente 15: EXTERNO
  (15, '1080100015', 'Nicolás', 'Bermeo Castro', '3163000015', 'nicolas.bermeo@gmail.com', 'EXTERNO', 'ACTIVO'),
  -- Cliente 16: APRENDIZ
  (16, '1075300016', 'Sofía', 'Cerquera Díaz', '3201000016', 'sofia.cerquera@soy.sena.edu.co', 'APRENDIZ', 'ACTIVO'),
  -- Cliente 17: APRENDIZ (INACTIVO, sin pedidos)
  (17, '1075300017', 'Mateo', 'Ibarra Plazas', '3201000017', 'mateo.ibarra@soy.sena.edu.co', 'APRENDIZ', 'INACTIVO'),
  -- Cliente 18: EXTERNO
  (18, '1080100018', 'Jorge Enrique', 'Muñoz Benavides', '3163000018', 'jorge.munoz@gmail.com', 'EXTERNO', 'ACTIVO');

-- productos: el 4 (Almuerzo ejecutivo) y el 9 (Jugo de lulo) son los del ejemplo del instructivo.
-- El 13 está AGOTADO y el 15 INACTIVO: ninguno de los dos se puede pedir.
INSERT INTO productos (id_producto, codigo, nombre, descripcion, precio_venta, unidad_venta, id_categoria, estado) VALUES
  -- Producto 1: Arroz con pollo (DISPONIBLE)
  (1, 'PLA-001', 'Arroz con pollo', 'Arroz con pollo desmechado y verduras', 14000, 'porción', 1, 'DISPONIBLE'),
  -- Producto 2: Sobrebarriga en salsa (DISPONIBLE)
  (2, 'PLA-002', 'Sobrebarriga en salsa', 'Sobrebarriga en salsa criolla con papa y arroz', 18000, 'porción', 1, 'DISPONIBLE'),
  -- Producto 3: Sopa de verduras (DISPONIBLE)
  (3, 'SOP-001', 'Sopa de verduras', 'Sopa del día con papa y verduras', 7000, 'porción', 5, 'DISPONIBLE'),
  -- Producto 4: Almuerzo ejecutivo (DISPONIBLE)
  (4, 'PLA-003', 'Almuerzo ejecutivo', 'Arroz, carne de res, fríjol y papa', 15000, 'porción', 1, 'DISPONIBLE'),
  -- Producto 5: Pan de queso (DISPONIBLE)
  (5, 'PAN-001', 'Pan de queso', 'Pan horneado con queso campesino', 1800, 'unidad', 3, 'DISPONIBLE'),
  -- Producto 6: Pan tajado (DISPONIBLE)
  (6, 'PAN-002', 'Pan tajado', 'Pan tajado artesanal', 6000, 'libra', 3, 'DISPONIBLE'),
  -- Producto 7: Torta de chocolate (DISPONIBLE)
  (7, 'REP-001', 'Torta de chocolate', 'Porción de torta de chocolate', 6500, 'porción', 4, 'DISPONIBLE'),
  -- Producto 8: Brownie (DISPONIBLE)
  (8, 'REP-002', 'Brownie', 'Brownie de chocolate', 4500, 'unidad', 4, 'DISPONIBLE'),
  -- Producto 9: Jugo de lulo (DISPONIBLE)
  (9, 'BEB-001', 'Jugo de lulo', 'Jugo natural de lulo en agua', 4500, 'vaso', 2, 'DISPONIBLE'),
  -- Producto 10: Café tinto (DISPONIBLE)
  (10, 'BEB-002', 'Café tinto', 'Tinto de café huilense', 1500, 'vaso', 10, 'DISPONIBLE'),
  -- Producto 11: Desayuno tradicional (DISPONIBLE)
  (11, 'DES-001', 'Desayuno tradicional', 'Huevos al gusto, queso y café con leche', 9000, 'porción', 7, 'DISPONIBLE'),
  -- Producto 12: Ensalada de la casa (DISPONIBLE)
  (12, 'ENS-001', 'Ensalada de la casa', 'Tomate, cebolla y queso campesino', 8000, 'porción', 6, 'DISPONIBLE'),
  -- Producto 13: Hamburguesa sencilla (AGOTADO)
  (13, 'RAP-001', 'Hamburguesa sencilla', 'Carne de res, pan, tomate y queso', 13000, 'unidad', 8, 'AGOTADO'),
  -- Producto 14: Empanada de carne (DISPONIBLE)
  (14, 'PAS-001', 'Empanada de carne', 'Empanada frita de carne y papa', 2500, 'unidad', 9, 'DISPONIBLE'),
  -- Producto 15: Limonada natural (INACTIVO)
  (15, 'BEB-003', 'Limonada natural', 'Limonada con hielo', 4000, 'vaso', 2, 'INACTIVO');

-- recetas: cantidad de cada insumo por una unidad del producto (el producto 15 no tiene receta)
INSERT INTO recetas (id_producto, id_insumo, cantidad) VALUES
  -- Receta del producto 1 (Arroz con pollo): costo de producción 2775
  (1, 1, 0.15),
  (1, 2, 0.12),
  (1, 6, 0.03),
  (1, 15, 0.015),
  -- Receta del producto 2 (Sobrebarriga en salsa): costo de producción 6789
  (2, 3, 0.2),
  (2, 4, 0.15),
  (2, 5, 0.05),
  (2, 6, 0.04),
  (2, 1, 0.12),
  -- Receta del producto 3 (Sopa de verduras): costo de producción 542
  (3, 4, 0.12),
  (3, 5, 0.04),
  (3, 6, 0.03),
  -- Receta del producto 4 (Almuerzo ejecutivo): costo de producción 4970
  (4, 1, 0.15),
  (4, 3, 0.12),
  (4, 16, 0.08),
  (4, 4, 0.1),
  (4, 15, 0.01),
  -- Receta del producto 5 (Pan de queso): costo de producción 670
  (5, 7, 0.04),
  (5, 13, 0.02),
  (5, 12, 0.005),
  (5, 9, 0.1),
  -- Receta del producto 6 (Pan tajado): costo de producción 1780
  (6, 7, 0.3),
  (6, 12, 0.02),
  (6, 8, 0.02),
  (6, 10, 0.05),
  -- Receta del producto 7 (Torta de chocolate): costo de producción 1565
  (7, 7, 0.05),
  (7, 8, 0.04),
  (7, 9, 0.5),
  (7, 17, 0.03),
  (7, 12, 0.015),
  -- Receta del producto 8 (Brownie): costo de producción 1765
  (8, 17, 0.04),
  (8, 8, 0.03),
  (8, 7, 0.03),
  (8, 9, 0.5),
  (8, 12, 0.02),
  -- Receta del producto 9 (Jugo de lulo): costo de producción 940
  (9, 11, 0.12),
  (9, 8, 0.025),
  -- Receta del producto 10 (Café tinto): costo de producción 360
  (10, 14, 0.01),
  (10, 8, 0.01),
  -- Receta del producto 11 (Desayuno tradicional): costo de producción 3060
  (11, 9, 2),
  (11, 13, 0.05),
  (11, 14, 0.01),
  (11, 10, 0.1),
  (11, 12, 0.01),
  -- Receta del producto 12 (Ensalada de la casa): costo de producción 1340
  (12, 5, 0.1),
  (12, 6, 0.05),
  (12, 13, 0.04),
  (12, 15, 0.01),
  -- Receta del producto 13 (Hamburguesa sencilla): costo de producción 5194
  (13, 3, 0.15),
  (13, 7, 0.08),
  (13, 5, 0.03),
  (13, 6, 0.02),
  (13, 13, 0.03),
  -- Receta del producto 14 (Empanada de carne): costo de producción 1515
  (14, 3, 0.04),
  (14, 4, 0.03),
  (14, 7, 0.04),
  (14, 15, 0.02);

-- compras: el costo de cada ítem es el costo_unitario actual del insumo (RN02 lo deja igual al de la última compra)
INSERT INTO compras (id_compra, numero_factura, fecha_compra, id_proveedor, id_usuario, total) VALUES
  -- Compra 1 al proveedor 1: total 185000
  (1, 'FAC-1001', TIMESTAMP(CURDATE() - INTERVAL 20 DAY, '09:00:00'), 1, 1, 185000),
  -- Compra 2 al proveedor 2: total 312000
  (2, 'AVI-2050', TIMESTAMP(CURDATE() - INTERVAL 18 DAY, '08:30:00'), 2, 1, 312000),
  -- Compra 3 al proveedor 3: total 336000
  (3, 'CDH-0345', TIMESTAMP(CURDATE() - INTERVAL 15 DAY, '10:15:00'), 3, 2, 336000),
  -- Compra 4 al proveedor 4: total 240000
  (4, 'LSA-0778', TIMESTAMP(CURDATE() - INTERVAL 12 DAY, '07:45:00'), 4, 2, 240000),
  -- Compra 5 al proveedor 5: total 147500
  (5, 'MDS-4410', TIMESTAMP(CURDATE() - INTERVAL 10 DAY, '11:00:00'), 5, 1, 147500),
  -- Compra 6 al proveedor 6: total 191400
  (6, 'FRV-0091', TIMESTAMP(CURDATE() - INTERVAL 8 DAY, '06:50:00'), 6, 1, 191400),
  -- Compra 7 al proveedor 7: total 128000
  (7, 'CEH-1203', TIMESTAMP(CURDATE() - INTERVAL 7 DAY, '09:30:00'), 7, 2, 128000),
  -- Compra 8 al proveedor 8: total 90000
  (8, 'AGS-5512', TIMESTAMP(CURDATE() - INTERVAL 6 DAY, '14:10:00'), 8, 1, 90000),
  -- Compra 9 al proveedor 9: total 100000
  (9, 'DDH-0067', TIMESTAMP(CURDATE() - INTERVAL 4 DAY, '10:40:00'), 9, 2, 100000),
  -- Compra 10 al proveedor 6: total 47000
  (10, 'FRV-0102', TIMESTAMP(CURDATE() - INTERVAL 2 DAY, '07:05:00'), 6, 1, 47000);

-- detalle_compra: subtotal = cantidad x costo_unitario
INSERT INTO detalle_compra (id_compra, id_insumo, cantidad, costo_unitario, subtotal) VALUES
  -- Ítems de la compra 1
  (1, 1, 25, 4200, 105000),
  (1, 16, 10, 8000, 80000),
  -- Ítems de la compra 2
  (2, 2, 15, 16000, 240000),
  (2, 9, 120, 600, 72000),
  -- Ítems de la compra 3
  (3, 3, 12, 28000, 336000),
  -- Ítems de la compra 4
  (4, 10, 20, 4200, 84000),
  (4, 13, 5, 18000, 90000),
  (4, 12, 3, 22000, 66000),
  -- Ítems de la compra 5
  (5, 7, 25, 3500, 87500),
  (5, 8, 15, 4000, 60000),
  -- Ítems de la compra 6
  (6, 4, 30, 2500, 75000),
  (6, 5, 8, 3800, 30400),
  (6, 6, 10, 3000, 30000),
  (6, 11, 8, 7000, 56000),
  -- Ítems de la compra 7
  (7, 14, 4, 32000, 128000),
  -- Ítems de la compra 8
  (8, 15, 10, 9000, 90000),
  -- Ítems de la compra 9
  (9, 17, 3, 20000, 60000),
  (9, 8, 10, 4000, 40000),
  -- Ítems de la compra 10
  (10, 5, 5, 3800, 19000),
  (10, 11, 4, 7000, 28000);

-- pedidos: del 110 al 129. 14 ENTREGADO, 2 ANULADO, 2 EN_PREPARACION y 2 PENDIENTE.
-- El 125 es el del ejemplo de calificación del instructivo (cliente 18, productos 4 y 9).
INSERT INTO pedidos (id_pedido, fecha_pedido, id_cliente, id_usuario, tipo_pedido, estado, total, observaciones) VALUES
  -- Pedido 110: ENTREGADO, total 19500
  (110, TIMESTAMP(CURDATE() - INTERVAL 9 DAY, '12:15:00'), 1, 3, 'MESA', 'ENTREGADO', 19500, NULL),
  -- Pedido 111: ENTREGADO, total 18500
  (111, TIMESTAMP(CURDATE() - INTERVAL 9 DAY, '12:40:00'), 6, 3, 'MESA', 'ENTREGADO', 18500, 'Sin cebolla'),
  -- Pedido 112: ENTREGADO, total 12000
  (112, TIMESTAMP(CURDATE() - INTERVAL 8 DAY, '07:30:00'), 9, 4, 'PARA_LLEVAR', 'ENTREGADO', 12000, NULL),
  -- Pedido 113: ENTREGADO, total 16000
  (113, TIMESTAMP(CURDATE() - INTERVAL 8 DAY, '15:10:00'), 12, 4, 'MESA', 'ENTREGADO', 16000, NULL),
  -- Pedido 114: ENTREGADO, total 22500
  (114, TIMESTAMP(CURDATE() - INTERVAL 7 DAY, '12:20:00'), 2, 5, 'MESA', 'ENTREGADO', 22500, NULL),
  -- Pedido 115: ENTREGADO, total 110000
  (115, TIMESTAMP(CURDATE() - INTERVAL 6 DAY, '10:00:00'), 10, 3, 'EVENTO', 'ENTREGADO', 110000, 'Reunión de área, 10 personas'),
  -- Pedido 116: ENTREGADO, total 23000
  (116, TIMESTAMP(CURDATE() - INTERVAL 5 DAY, '12:35:00'), 7, 4, 'MESA', 'ENTREGADO', 23000, NULL),
  -- Pedido 117: ENTREGADO, total 16200
  (117, TIMESTAMP(CURDATE() - INTERVAL 4 DAY, '16:00:00'), 3, 5, 'PARA_LLEVAR', 'ENTREGADO', 16200, NULL),
  -- Pedido 118: ENTREGADO, total 37000
  (118, TIMESTAMP(CURDATE() - INTERVAL 3 DAY, '12:10:00'), 13, 9, 'MESA', 'ENTREGADO', 37000, NULL),
  -- Pedido 119: ANULADO, total 9000
  (119, TIMESTAMP(CURDATE() - INTERVAL 3 DAY, '17:20:00'), 4, 3, 'MESA', 'ANULADO', 9000, 'El cliente canceló'),
  -- Pedido 120: ANULADO, total 18000
  (120, TIMESTAMP(CURDATE() - INTERVAL 2 DAY, '12:50:00'), 11, 4, 'PARA_LLEVAR', 'ANULADO', 18000, 'Pedido duplicado'),
  -- Pedido 121: ENTREGADO, total 26500
  (121, TIMESTAMP(CURDATE() - INTERVAL 2 DAY, '13:30:00'), 14, 5, 'MESA', 'ENTREGADO', 26500, NULL),
  -- Pedido 122: ENTREGADO, total 10500
  (122, TIMESTAMP(CURDATE() - INTERVAL 1 DAY, '07:40:00'), 5, 9, 'MESA', 'ENTREGADO', 10500, NULL),
  -- Pedido 123: ENTREGADO, total 39000
  (123, TIMESTAMP(CURDATE() - INTERVAL 1 DAY, '12:25:00'), 15, 3, 'MESA', 'ENTREGADO', 39000, NULL),
  -- Pedido 124: ENTREGADO, total 16500
  (124, TIMESTAMP(CURDATE() - INTERVAL 1 DAY, '16:45:00'), 16, 4, 'PARA_LLEVAR', 'ENTREGADO', 16500, NULL),
  -- Pedido 125: ENTREGADO, total 19500
  (125, NOW() - INTERVAL 150 MINUTE, 18, 3, 'MESA', 'ENTREGADO', 19500, NULL),
  -- Pedido 126: EN_PREPARACION, total 25000
  (126, NOW() - INTERVAL 90 MINUTE, 8, 5, 'MESA', 'EN_PREPARACION', 25000, NULL),
  -- Pedido 127: EN_PREPARACION, total 10000
  (127, NOW() - INTERVAL 60 MINUTE, 1, 9, 'PARA_LLEVAR', 'EN_PREPARACION', 10000, NULL),
  -- Pedido 128: PENDIENTE, total 10500
  (128, NOW() - INTERVAL 30 MINUTE, 6, 3, 'MESA', 'PENDIENTE', 10500, NULL),
  -- Pedido 129: PENDIENTE, total 17300
  (129, NOW() - INTERVAL 10 MINUTE, 12, 4, 'PARA_LLEVAR', 'PENDIENTE', 17300, 'Para recoger en 20 minutos');

-- detalle_pedido: precio_unitario = precio de venta del producto; subtotal = cantidad x precio_unitario (RN01)
INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, precio_unitario, subtotal) VALUES
  -- Ítems del pedido 110
  (110, 4, 1, 15000, 15000),
  (110, 9, 1, 4500, 4500),
  -- Ítems del pedido 111
  (111, 1, 1, 14000, 14000),
  (111, 9, 1, 4500, 4500),
  -- Ítems del pedido 112
  (112, 11, 1, 9000, 9000),
  (112, 10, 2, 1500, 3000),
  -- Ítems del pedido 113
  (113, 7, 2, 6500, 13000),
  (113, 10, 2, 1500, 3000),
  -- Ítems del pedido 114
  (114, 2, 1, 18000, 18000),
  (114, 9, 1, 4500, 4500),
  -- Ítems del pedido 115
  (115, 14, 20, 2500, 50000),
  (115, 10, 10, 1500, 15000),
  (115, 8, 10, 4500, 45000),
  -- Ítems del pedido 116
  (116, 4, 1, 15000, 15000),
  (116, 12, 1, 8000, 8000),
  -- Ítems del pedido 117
  (117, 6, 1.5, 6000, 9000),
  (117, 5, 4, 1800, 7200),
  -- Ítems del pedido 118
  (118, 1, 2, 14000, 28000),
  (118, 9, 2, 4500, 9000),
  -- Ítems del pedido 119
  (119, 11, 1, 9000, 9000),
  -- Ítems del pedido 120
  (120, 2, 1, 18000, 18000),
  -- Ítems del pedido 121
  (121, 1, 1, 14000, 14000),
  (121, 12, 1, 8000, 8000),
  (121, 9, 1, 4500, 4500),
  -- Ítems del pedido 122
  (122, 11, 1, 9000, 9000),
  (122, 10, 1, 1500, 1500),
  -- Ítems del pedido 123
  (123, 4, 2, 15000, 30000),
  (123, 9, 2, 4500, 9000),
  -- Ítems del pedido 124
  (124, 8, 3, 4500, 13500),
  (124, 10, 2, 1500, 3000),
  -- Ítems del pedido 125
  (125, 4, 1, 15000, 15000),
  (125, 9, 1, 4500, 4500),
  -- Ítems del pedido 126
  (126, 2, 1, 18000, 18000),
  (126, 3, 1, 7000, 7000),
  -- Ítems del pedido 127
  (127, 14, 4, 2500, 10000),
  -- Ítems del pedido 128
  (128, 11, 1, 9000, 9000),
  (128, 10, 1, 1500, 1500),
  -- Ítems del pedido 129
  (129, 5, 6, 1800, 10800),
  (129, 7, 1, 6500, 6500);

-- Cuenta los registros de cada tabla (evidencia para el anexo)
SELECT 'usuarios' AS tabla, COUNT(*) AS registros FROM usuarios
UNION ALL
SELECT 'categorias' AS tabla, COUNT(*) AS registros FROM categorias
UNION ALL
SELECT 'insumos' AS tabla, COUNT(*) AS registros FROM insumos
UNION ALL
SELECT 'proveedores' AS tabla, COUNT(*) AS registros FROM proveedores
UNION ALL
SELECT 'clientes' AS tabla, COUNT(*) AS registros FROM clientes
UNION ALL
SELECT 'productos' AS tabla, COUNT(*) AS registros FROM productos
UNION ALL
SELECT 'recetas' AS tabla, COUNT(*) AS registros FROM recetas
UNION ALL
SELECT 'compras' AS tabla, COUNT(*) AS registros FROM compras
UNION ALL
SELECT 'detalle_compra' AS tabla, COUNT(*) AS registros FROM detalle_compra
UNION ALL
SELECT 'pedidos' AS tabla, COUNT(*) AS registros FROM pedidos
UNION ALL
SELECT 'detalle_pedido' AS tabla, COUNT(*) AS registros FROM detalle_pedido;
