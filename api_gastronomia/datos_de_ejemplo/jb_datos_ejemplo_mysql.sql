-- DATOS DE EJEMPLO PARA MySQL (base bd_gastronomia)
-- Son los mismos datos del script database/02_jb_dml_datos_prueba.sql, divididos en bloques
-- para copiarlos y pegarlos en la terminal de MySQL, uno por uno y en orden.
-- La diferencia: aquí solo el primer usuario (el ADMIN) se inserta con SQL. Los otros 9 usuarios se
-- crean por medio de la API con su contraseña en texto plano, y la API la cifra con bcrypt (RN06).
-- MySQL no sabe cifrar con bcrypt: por eso un usuario insertado con SQL tiene que llevar el hash.
--
-- Antes de empezar:
--   Las tablas deben existir y estar VACÍAS. Ejecute el script database/01_jb_ddl_bd_gastronomia.sql
--   (borra la base y la crea de nuevo, vacía). Si ya ejecutó el script 02, los datos ya están:
--   no los pegue otra vez o MySQL responderá "Duplicate entry".
--
-- PASO 1. Abra una terminal en la carpeta api_gastronomia y entre a MySQL dentro del contenedor:
--            docker compose exec mysql mysql -u root -p
--         Escriba la contraseña de root (la de MYSQL_ROOT_PASSWORD en el .env). Aparece el indicador mysql>
--         Pegue los bloques 0 y 1. Copie cada bloque completo (desde su título hasta el punto y coma),
--         péguelo y pulse Enter. MySQL responde "Query OK". Si la terminal pregunta si quiere pegar
--         varias líneas, acepte.
-- PASO 2. Cree los otros 9 usuarios por medio de la API: siga el archivo jb_usuarios_por_api.ps1
--         (los usuarios y sus contraseñas en texto plano están en jb_usuarios_ejemplo.json).
-- PASO 3. Vuelva a la terminal de MySQL y pegue los bloques 2 al 13, en orden. El orden importa:
--         una tabla con llaves foráneas necesita que ya existan los datos a los que apunta.
--         Para salir de MySQL escriba: exit

-- ===== BLOQUE 0: entrar a la base de datos =====
USE bd_gastronomia;

-- ===== BLOQUE 1: el usuario ADMIN que inicia sesión: burbano@gastronomia.com, contraseña Admin123* (va cifrada con bcrypt porque MySQL no sabe cifrar) =====
INSERT INTO usuarios (id_usuario, identificacion, nombres, apellidos, correo, password, rol, estado) VALUES
(1, '1000000001', 'Administrador', 'del Sistema', 'burbano@gastronomia.com', '$2b$12$3JKw.vA78zuH0uuts/eU5.IArWLoUS7RxMSln0cLaI/0bJ/iR6/sq', 'ADMIN', 'ACTIVO');

-- ===== ALTO: antes de seguir, haga el PASO 2 (crear los usuarios por la API) =====

-- ===== BLOQUE 2: categorias (10) =====
INSERT INTO categorias (id_categoria, nombre, descripcion, estado) VALUES
(1, 'Platos', 'Platos fuertes y almuerzos', 'ACTIVO'),
(2, 'Bebidas', 'Jugos, limonadas y bebidas frías', 'ACTIVO'),
(3, 'Panadería', 'Panes y productos horneados', 'ACTIVO'),
(4, 'Repostería', 'Tortas, postres y dulces', 'ACTIVO'),
(5, 'Sopas', 'Sopas y cremas del día', 'ACTIVO'),
(6, 'Ensaladas', 'Ensaladas frescas', 'ACTIVO'),
(7, 'Desayunos', 'Desayunos completos', 'ACTIVO'),
(8, 'Comidas rápidas', 'Hamburguesas, perros y sándwiches', 'ACTIVO'),
(9, 'Pasabocas', 'Empanadas, buñuelos y fritos', 'ACTIVO'),
(10, 'Bebidas calientes', 'Café, chocolate y aromáticas', 'ACTIVO');

-- ===== BLOQUE 3: insumos (18). Las fechas de vencimiento se calculan desde hoy =====
INSERT INTO insumos (id_insumo, nombre, unidad_medida, stock_actual, stock_minimo, costo_unitario, fecha_vencimiento, estado) VALUES
(1, 'Arroz', 'kg', 45, 10, 4200, CURDATE() + INTERVAL 180 DAY, 'ACTIVO'),
(2, 'Pechuga de pollo', 'kg', 18.5, 8, 16000, CURDATE() + INTERVAL 4 DAY, 'ACTIVO'),
(3, 'Carne de res', 'kg', 14.2, 6, 28000, CURDATE() + INTERVAL 5 DAY, 'ACTIVO'),
(4, 'Papa', 'kg', 38, 10, 2500, CURDATE() + INTERVAL 20 DAY, 'ACTIVO'),
(5, 'Tomate', 'kg', 6.3, 8, 3800, CURDATE() + INTERVAL 6 DAY, 'ACTIVO'),
(6, 'Cebolla cabezona', 'kg', 11, 5, 3000, CURDATE() + INTERVAL 25 DAY, 'ACTIVO'),
(7, 'Harina de trigo', 'kg', 28, 10, 3500, CURDATE() + INTERVAL 120 DAY, 'ACTIVO'),
(8, 'Azúcar', 'kg', 24, 8, 4000, CURDATE() + INTERVAL 300 DAY, 'ACTIVO'),
(9, 'Huevos', 'unidad', 150, 60, 600, CURDATE() + INTERVAL 12 DAY, 'ACTIVO'),
(10, 'Leche entera', 'l', 9, 15, 4200, CURDATE() + INTERVAL 3 DAY, 'ACTIVO'),
(11, 'Lulo', 'kg', 9.5, 4, 7000, CURDATE() + INTERVAL 7 DAY, 'ACTIVO'),
(12, 'Mantequilla', 'kg', 2.4, 3, 22000, CURDATE() + INTERVAL 40 DAY, 'ACTIVO'),
(13, 'Queso campesino', 'kg', 5.8, 3, 18000, CURDATE() + INTERVAL 8 DAY, 'ACTIVO'),
(14, 'Café molido', 'kg', 4.2, 2, 32000, CURDATE() + INTERVAL 200 DAY, 'ACTIVO'),
(15, 'Aceite vegetal', 'l', 12, 4, 9000, CURDATE() + INTERVAL 365 DAY, 'ACTIVO'),
(16, 'Fríjol rojo', 'kg', 17, 5, 8000, CURDATE() + INTERVAL 240 DAY, 'ACTIVO'),
(17, 'Chocolate de mesa', 'kg', 3.5, 2, 20000, CURDATE() + INTERVAL 150 DAY, 'ACTIVO'),
(18, 'Margarina', 'kg', 0, 0, 15000, NULL, 'INACTIVO');

-- ===== BLOQUE 4: proveedores (10) =====
INSERT INTO proveedores (id_proveedor, nit, razon_social, telefono, correo, direccion, estado) VALUES
(1, '900123456-1', 'Distribuidora La Cosecha S.A.S.', '3101234567', 'ventas@lacosecha.com', 'Carrera 4 # 5-20, Pitalito', 'ACTIVO'),
(2, '900234567-2', 'Avícola El Campo Ltda.', '3112345678', 'pedidos@avicolaelcampo.com', 'Kilómetro 2 vía La Laguna, Pitalito', 'ACTIVO'),
(3, '900345678-3', 'Carnes del Huila S.A.S.', '3123456789', 'contacto@carnesdelhuila.com', 'Calle 8 # 3-45, Pitalito', 'ACTIVO'),
(4, '900456789-4', 'Lácteos San Agustín', '3134567890', 'ventas@lacteossanagustin.com', 'Vereda Obando, San Agustín', 'ACTIVO'),
(5, '900567890-5', 'Molinos del Sur S.A.', '3145678901', 'comercial@molinosdelsur.com', 'Zona industrial, Neiva', 'ACTIVO'),
(6, '900678901-6', 'Fruver Pitalito', '3156789012', 'fruver@pitalito.com', 'Plaza de mercado, local 12, Pitalito', 'ACTIVO'),
(7, '900789012-7', 'Café Especial del Huila', '3167890123', 'ventas@cafeespecialhuila.com', 'Calle 10 # 2-15, Pitalito', 'ACTIVO'),
(8, '900890123-8', 'Aceites y Grasas del Sur', '3178901234', 'pedidos@aceitesdelsur.com', 'Carrera 15 # 20-30, Neiva', 'ACTIVO'),
(9, '900901234-9', 'Distribuidora Dulce Hogar', '3189012345', 'dulcehogar@correo.com', 'Calle 5 # 7-11, Pitalito', 'ACTIVO'),
(10, '901012345-0', 'Granos y Abarrotes El Trigal', '3190123456', 'eltrigal@correo.com', 'Carrera 3 # 9-40, Garzón', 'ACTIVO');

-- ===== BLOQUE 5: clientes (18) =====
INSERT INTO clientes (id_cliente, identificacion, nombres, apellidos, telefono, correo, tipo_cliente, estado) VALUES
(1, '1075300001', 'Juan Camilo', 'Pérez Gómez', '3201000001', 'juan.perez@soy.sena.edu.co', 'APRENDIZ', 'ACTIVO'),
(2, '1075300002', 'Valentina', 'Rodríguez Silva', '3201000002', 'valentina.rodriguez@soy.sena.edu.co', 'APRENDIZ', 'ACTIVO'),
(3, '1075300003', 'Santiago', 'López Muñoz', '3201000003', 'santiago.lopez@soy.sena.edu.co', 'APRENDIZ', 'ACTIVO'),
(4, '1075300004', 'Daniela', 'Martínez Rojas', '3201000004', 'daniela.martinez@soy.sena.edu.co', 'APRENDIZ', 'ACTIVO'),
(5, '1075300005', 'Kevin Alejandro', 'Guzmán Ortiz', '3201000005', 'kevin.guzman@soy.sena.edu.co', 'APRENDIZ', 'ACTIVO'),
(6, '12198765', 'Hernando', 'Cabrera Luna', '3152000006', 'hcabrera@sena.edu.co', 'INSTRUCTOR', 'ACTIVO'),
(7, '36178945', 'Gloria Inés', 'Perdomo Vargas', '3152000007', 'gperdomo@sena.edu.co', 'INSTRUCTOR', 'ACTIVO'),
(8, '83245671', 'Álvaro', 'Quintero Bahamón', '3152000008', 'aquintero@sena.edu.co', 'INSTRUCTOR', 'ACTIVO'),
(9, '26456789', 'Marleny', 'Losada Cuéllar', '3152000009', 'mlosada@sena.edu.co', 'FUNCIONARIO', 'ACTIVO'),
(10, '12234567', 'Fabio Nelson', 'Salazar Trujillo', '3152000010', 'fsalazar@sena.edu.co', 'FUNCIONARIO', 'ACTIVO'),
(11, '55123456', 'Rosa Elena', 'Medina Polanco', '3152000011', 'rmedina@sena.edu.co', 'FUNCIONARIO', 'ACTIVO'),
(12, '1080100012', 'Camila', 'Andrade Rivera', '3163000012', 'camila.andrade@gmail.com', 'EXTERNO', 'ACTIVO'),
(13, '1080100013', 'Luis Eduardo', 'Chávez Ortega', '3163000013', 'luis.chavez@gmail.com', 'EXTERNO', 'ACTIVO'),
(14, '1080100014', 'Paola Andrea', 'Fierro Calderón', '3163000014', 'paola.fierro@hotmail.com', 'EXTERNO', 'ACTIVO'),
(15, '1080100015', 'Nicolás', 'Bermeo Castro', '3163000015', 'nicolas.bermeo@gmail.com', 'EXTERNO', 'ACTIVO'),
(16, '1075300016', 'Sofía', 'Cerquera Díaz', '3201000016', 'sofia.cerquera@soy.sena.edu.co', 'APRENDIZ', 'ACTIVO'),
(17, '1075300017', 'Mateo', 'Ibarra Plazas', '3201000017', 'mateo.ibarra@soy.sena.edu.co', 'APRENDIZ', 'INACTIVO'),
(18, '1080100018', 'Jorge Enrique', 'Muñoz Benavides', '3163000018', 'jorge.munoz@gmail.com', 'EXTERNO', 'ACTIVO');

-- ===== BLOQUE 6: productos (15) =====
INSERT INTO productos (id_producto, codigo, nombre, descripcion, precio_venta, unidad_venta, id_categoria, estado) VALUES
(1, 'PLA-001', 'Arroz con pollo', 'Arroz con pollo desmechado y verduras', 14000, 'porción', 1, 'DISPONIBLE'),
(2, 'PLA-002', 'Sobrebarriga en salsa', 'Sobrebarriga en salsa criolla con papa y arroz', 18000, 'porción', 1, 'DISPONIBLE'),
(3, 'SOP-001', 'Sopa de verduras', 'Sopa del día con papa y verduras', 7000, 'porción', 5, 'DISPONIBLE'),
(4, 'PLA-003', 'Almuerzo ejecutivo', 'Arroz, carne de res, fríjol y papa', 15000, 'porción', 1, 'DISPONIBLE'),
(5, 'PAN-001', 'Pan de queso', 'Pan horneado con queso campesino', 1800, 'unidad', 3, 'DISPONIBLE'),
(6, 'PAN-002', 'Pan tajado', 'Pan tajado artesanal', 6000, 'libra', 3, 'DISPONIBLE'),
(7, 'REP-001', 'Torta de chocolate', 'Porción de torta de chocolate', 6500, 'porción', 4, 'DISPONIBLE'),
(8, 'REP-002', 'Brownie', 'Brownie de chocolate', 4500, 'unidad', 4, 'DISPONIBLE'),
(9, 'BEB-001', 'Jugo de lulo', 'Jugo natural de lulo en agua', 4500, 'vaso', 2, 'DISPONIBLE'),
(10, 'BEB-002', 'Café tinto', 'Tinto de café huilense', 1500, 'vaso', 10, 'DISPONIBLE'),
(11, 'DES-001', 'Desayuno tradicional', 'Huevos al gusto, queso y café con leche', 9000, 'porción', 7, 'DISPONIBLE'),
(12, 'ENS-001', 'Ensalada de la casa', 'Tomate, cebolla y queso campesino', 8000, 'porción', 6, 'DISPONIBLE'),
(13, 'RAP-001', 'Hamburguesa sencilla', 'Carne de res, pan, tomate y queso', 13000, 'unidad', 8, 'AGOTADO'),
(14, 'PAS-001', 'Empanada de carne', 'Empanada frita de carne y papa', 2500, 'unidad', 9, 'DISPONIBLE'),
(15, 'BEB-003', 'Limonada natural', 'Limonada con hielo', 4000, 'vaso', 2, 'INACTIVO');

-- ===== BLOQUE 7: recetas (57): cantidad de cada insumo por una unidad del producto =====
INSERT INTO recetas (id_producto, id_insumo, cantidad) VALUES
(1, 1, 0.15),
(1, 2, 0.12),
(1, 6, 0.03),
(1, 15, 0.015),
(2, 3, 0.2),
(2, 4, 0.15),
(2, 5, 0.05),
(2, 6, 0.04),
(2, 1, 0.12),
(3, 4, 0.12),
(3, 5, 0.04),
(3, 6, 0.03),
(4, 1, 0.15),
(4, 3, 0.12),
(4, 16, 0.08),
(4, 4, 0.1),
(4, 15, 0.01),
(5, 7, 0.04),
(5, 13, 0.02),
(5, 12, 0.005),
(5, 9, 0.1),
(6, 7, 0.3),
(6, 12, 0.02),
(6, 8, 0.02),
(6, 10, 0.05),
(7, 7, 0.05),
(7, 8, 0.04),
(7, 9, 0.5),
(7, 17, 0.03),
(7, 12, 0.015),
(8, 17, 0.04),
(8, 8, 0.03),
(8, 7, 0.03),
(8, 9, 0.5),
(8, 12, 0.02),
(9, 11, 0.12),
(9, 8, 0.025),
(10, 14, 0.01),
(10, 8, 0.01),
(11, 9, 2),
(11, 13, 0.05),
(11, 14, 0.01),
(11, 10, 0.1),
(11, 12, 0.01),
(12, 5, 0.1),
(12, 6, 0.05),
(12, 13, 0.04),
(12, 15, 0.01),
(13, 3, 0.15),
(13, 7, 0.08),
(13, 5, 0.03),
(13, 6, 0.02),
(13, 13, 0.03),
(14, 3, 0.04),
(14, 4, 0.03),
(14, 7, 0.04),
(14, 15, 0.02);

-- ===== BLOQUE 8: compras (10). El usuario que registró cada compra se busca por su correo =====
INSERT INTO compras (id_compra, numero_factura, fecha_compra, id_proveedor, id_usuario, total) VALUES
(1, 'FAC-1001', TIMESTAMP(CURDATE() - INTERVAL 20 DAY, '09:00:00'), 1, (SELECT id_usuario FROM usuarios WHERE correo = 'burbano@gastronomia.com'), 185000),
(2, 'AVI-2050', TIMESTAMP(CURDATE() - INTERVAL 18 DAY, '08:30:00'), 2, (SELECT id_usuario FROM usuarios WHERE correo = 'burbano@gastronomia.com'), 312000),
(3, 'CDH-0345', TIMESTAMP(CURDATE() - INTERVAL 15 DAY, '10:15:00'), 3, (SELECT id_usuario FROM usuarios WHERE correo = 'laura.munoz@gastronomia.com'), 336000),
(4, 'LSA-0778', TIMESTAMP(CURDATE() - INTERVAL 12 DAY, '07:45:00'), 4, (SELECT id_usuario FROM usuarios WHERE correo = 'laura.munoz@gastronomia.com'), 240000),
(5, 'MDS-4410', TIMESTAMP(CURDATE() - INTERVAL 10 DAY, '11:00:00'), 5, (SELECT id_usuario FROM usuarios WHERE correo = 'burbano@gastronomia.com'), 147500),
(6, 'FRV-0091', TIMESTAMP(CURDATE() - INTERVAL 8 DAY, '06:50:00'), 6, (SELECT id_usuario FROM usuarios WHERE correo = 'burbano@gastronomia.com'), 191400),
(7, 'CEH-1203', TIMESTAMP(CURDATE() - INTERVAL 7 DAY, '09:30:00'), 7, (SELECT id_usuario FROM usuarios WHERE correo = 'laura.munoz@gastronomia.com'), 128000),
(8, 'AGS-5512', TIMESTAMP(CURDATE() - INTERVAL 6 DAY, '14:10:00'), 8, (SELECT id_usuario FROM usuarios WHERE correo = 'burbano@gastronomia.com'), 90000),
(9, 'DDH-0067', TIMESTAMP(CURDATE() - INTERVAL 4 DAY, '10:40:00'), 9, (SELECT id_usuario FROM usuarios WHERE correo = 'laura.munoz@gastronomia.com'), 100000),
(10, 'FRV-0102', TIMESTAMP(CURDATE() - INTERVAL 2 DAY, '07:05:00'), 6, (SELECT id_usuario FROM usuarios WHERE correo = 'burbano@gastronomia.com'), 47000);

-- ===== BLOQUE 9: detalle_compra (20): subtotal = cantidad x costo_unitario =====
INSERT INTO detalle_compra (id_compra, id_insumo, cantidad, costo_unitario, subtotal) VALUES
(1, 1, 25, 4200, 105000),
(1, 16, 10, 8000, 80000),
(2, 2, 15, 16000, 240000),
(2, 9, 120, 600, 72000),
(3, 3, 12, 28000, 336000),
(4, 10, 20, 4200, 84000),
(4, 13, 5, 18000, 90000),
(4, 12, 3, 22000, 66000),
(5, 7, 25, 3500, 87500),
(5, 8, 15, 4000, 60000),
(6, 4, 30, 2500, 75000),
(6, 5, 8, 3800, 30400),
(6, 6, 10, 3000, 30000),
(6, 11, 8, 7000, 56000),
(7, 14, 4, 32000, 128000),
(8, 15, 10, 9000, 90000),
(9, 17, 3, 20000, 60000),
(9, 8, 10, 4000, 40000),
(10, 5, 5, 3800, 19000),
(10, 11, 4, 7000, 28000);

-- ===== BLOQUE 10: pedidos (20, del 110 al 129). Las fechas se calculan desde hoy; el usuario que registró cada pedido se busca por su correo =====
INSERT INTO pedidos (id_pedido, fecha_pedido, id_cliente, id_usuario, tipo_pedido, estado, total, observaciones) VALUES
(110, TIMESTAMP(CURDATE() - INTERVAL 9 DAY, '12:15:00'), 1, (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rojas@gastronomia.com'), 'MESA', 'ENTREGADO', 19500, NULL),
(111, TIMESTAMP(CURDATE() - INTERVAL 9 DAY, '12:40:00'), 6, (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rojas@gastronomia.com'), 'MESA', 'ENTREGADO', 18500, 'Sin cebolla'),
(112, TIMESTAMP(CURDATE() - INTERVAL 8 DAY, '07:30:00'), 9, (SELECT id_usuario FROM usuarios WHERE correo = 'diana.gomez@gastronomia.com'), 'PARA_LLEVAR', 'ENTREGADO', 12000, NULL),
(113, TIMESTAMP(CURDATE() - INTERVAL 8 DAY, '15:10:00'), 12, (SELECT id_usuario FROM usuarios WHERE correo = 'diana.gomez@gastronomia.com'), 'MESA', 'ENTREGADO', 16000, NULL),
(114, TIMESTAMP(CURDATE() - INTERVAL 7 DAY, '12:20:00'), 2, (SELECT id_usuario FROM usuarios WHERE correo = 'jhon.ortiz@gastronomia.com'), 'MESA', 'ENTREGADO', 22500, NULL),
(115, TIMESTAMP(CURDATE() - INTERVAL 6 DAY, '10:00:00'), 10, (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rojas@gastronomia.com'), 'EVENTO', 'ENTREGADO', 110000, 'Reunión de área, 10 personas'),
(116, TIMESTAMP(CURDATE() - INTERVAL 5 DAY, '12:35:00'), 7, (SELECT id_usuario FROM usuarios WHERE correo = 'diana.gomez@gastronomia.com'), 'MESA', 'ENTREGADO', 23000, NULL),
(117, TIMESTAMP(CURDATE() - INTERVAL 4 DAY, '16:00:00'), 3, (SELECT id_usuario FROM usuarios WHERE correo = 'jhon.ortiz@gastronomia.com'), 'PARA_LLEVAR', 'ENTREGADO', 16200, NULL),
(118, TIMESTAMP(CURDATE() - INTERVAL 3 DAY, '12:10:00'), 13, (SELECT id_usuario FROM usuarios WHERE correo = 'pedro.ramirez@gastronomia.com'), 'MESA', 'ENTREGADO', 37000, NULL),
(119, TIMESTAMP(CURDATE() - INTERVAL 3 DAY, '17:20:00'), 4, (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rojas@gastronomia.com'), 'MESA', 'ANULADO', 9000, 'El cliente canceló'),
(120, TIMESTAMP(CURDATE() - INTERVAL 2 DAY, '12:50:00'), 11, (SELECT id_usuario FROM usuarios WHERE correo = 'diana.gomez@gastronomia.com'), 'PARA_LLEVAR', 'ANULADO', 18000, 'Pedido duplicado'),
(121, TIMESTAMP(CURDATE() - INTERVAL 2 DAY, '13:30:00'), 14, (SELECT id_usuario FROM usuarios WHERE correo = 'jhon.ortiz@gastronomia.com'), 'MESA', 'ENTREGADO', 26500, NULL),
(122, TIMESTAMP(CURDATE() - INTERVAL 1 DAY, '07:40:00'), 5, (SELECT id_usuario FROM usuarios WHERE correo = 'pedro.ramirez@gastronomia.com'), 'MESA', 'ENTREGADO', 10500, NULL),
(123, TIMESTAMP(CURDATE() - INTERVAL 1 DAY, '12:25:00'), 15, (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rojas@gastronomia.com'), 'MESA', 'ENTREGADO', 39000, NULL),
(124, TIMESTAMP(CURDATE() - INTERVAL 1 DAY, '16:45:00'), 16, (SELECT id_usuario FROM usuarios WHERE correo = 'diana.gomez@gastronomia.com'), 'PARA_LLEVAR', 'ENTREGADO', 16500, NULL),
(125, NOW() - INTERVAL 150 MINUTE, 18, (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rojas@gastronomia.com'), 'MESA', 'ENTREGADO', 19500, NULL),
(126, NOW() - INTERVAL 90 MINUTE, 8, (SELECT id_usuario FROM usuarios WHERE correo = 'jhon.ortiz@gastronomia.com'), 'MESA', 'EN_PREPARACION', 25000, NULL),
(127, NOW() - INTERVAL 60 MINUTE, 1, (SELECT id_usuario FROM usuarios WHERE correo = 'pedro.ramirez@gastronomia.com'), 'PARA_LLEVAR', 'EN_PREPARACION', 10000, NULL),
(128, NOW() - INTERVAL 30 MINUTE, 6, (SELECT id_usuario FROM usuarios WHERE correo = 'carlos.rojas@gastronomia.com'), 'MESA', 'PENDIENTE', 10500, NULL),
(129, NOW() - INTERVAL 10 MINUTE, 12, (SELECT id_usuario FROM usuarios WHERE correo = 'diana.gomez@gastronomia.com'), 'PARA_LLEVAR', 'PENDIENTE', 17300, 'Para recoger en 20 minutos');

-- ===== BLOQUE 11: detalle_pedido (39): subtotal = cantidad x precio_unitario (RN01) =====
INSERT INTO detalle_pedido (id_pedido, id_producto, cantidad, precio_unitario, subtotal) VALUES
(110, 4, 1, 15000, 15000),
(110, 9, 1, 4500, 4500),
(111, 1, 1, 14000, 14000),
(111, 9, 1, 4500, 4500),
(112, 11, 1, 9000, 9000),
(112, 10, 2, 1500, 3000),
(113, 7, 2, 6500, 13000),
(113, 10, 2, 1500, 3000),
(114, 2, 1, 18000, 18000),
(114, 9, 1, 4500, 4500),
(115, 14, 20, 2500, 50000),
(115, 10, 10, 1500, 15000),
(115, 8, 10, 4500, 45000),
(116, 4, 1, 15000, 15000),
(116, 12, 1, 8000, 8000),
(117, 6, 1.5, 6000, 9000),
(117, 5, 4, 1800, 7200),
(118, 1, 2, 14000, 28000),
(118, 9, 2, 4500, 9000),
(119, 11, 1, 9000, 9000),
(120, 2, 1, 18000, 18000),
(121, 1, 1, 14000, 14000),
(121, 12, 1, 8000, 8000),
(121, 9, 1, 4500, 4500),
(122, 11, 1, 9000, 9000),
(122, 10, 1, 1500, 1500),
(123, 4, 2, 15000, 30000),
(123, 9, 2, 4500, 9000),
(124, 8, 3, 4500, 13500),
(124, 10, 2, 1500, 3000),
(125, 4, 1, 15000, 15000),
(125, 9, 1, 4500, 4500),
(126, 2, 1, 18000, 18000),
(126, 3, 1, 7000, 7000),
(127, 14, 4, 2500, 10000),
(128, 11, 1, 9000, 9000),
(128, 10, 1, 1500, 1500),
(129, 5, 6, 1800, 10800),
(129, 7, 1, 6500, 6500);

-- ===== BLOQUE 12: comprobar cuántos registros quedaron en cada tabla =====
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

-- ===== BLOQUE 13 (evidencia para el anexo): tablas, estructura y algunas consultas =====
SHOW TABLES;
DESCRIBE productos;
SELECT id_producto, codigo, nombre, precio_venta, estado FROM productos;
SELECT id_pedido, fecha_pedido, estado, total FROM pedidos ORDER BY id_pedido;
