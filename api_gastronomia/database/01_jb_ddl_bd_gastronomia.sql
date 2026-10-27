-- Script 01 (DDL): crea la base de datos bd_gastronomia con sus 11 tablas, llaves, índices y restricciones.
-- Se ejecuta como root. Orden de los scripts: 01, 02 y 03 en MySQL; 04 en MongoDB.
-- Se puede ejecutar varias veces: primero borra la base si ya existe. CUIDADO: se pierden los datos.
--
-- Ajustes hechos al modelo del instructivo (el instructivo permite agregar campos si se justifica):
--   1. clientes.estado: RN04 pide borrado lógico de clientes y la tabla del instructivo no tenía estado.
--   2. pedidos.observaciones: aparece en el diagrama (Figura 1) aunque no en la tabla del texto.
--   3. recetas: la pareja producto-insumo no se repite (único compuesto).
--   4. stock_actual, stock_minimo y las cantidades de compras usan 3 decimales, igual que la receta
--      (por ejemplo 0.125 kg); con 2 decimales el descuento de RN03 se redondearía mal.
--   5. Restricciones CHECK, valores por defecto e índices en los campos por los que más se filtra.
--   6. Únicos extra: un proveedor no repite número de factura; un insumo no se repite en la misma compra
--      y un producto no se repite en el mismo pedido.

-- Borra la base si ya existe, para empezar desde cero
DROP DATABASE IF EXISTS bd_gastronomia;
-- Crea la base con utf8mb4 (tildes, eñes y cualquier símbolo) y su intercalación
CREATE DATABASE bd_gastronomia CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
-- Todo lo que sigue se crea dentro de bd_gastronomia
USE bd_gastronomia;

-- ---------------------------------------------------------------------
-- Primero las tablas que no dependen de otras (no tienen llaves foráneas)
-- ---------------------------------------------------------------------

-- usuarios: personas que usan el sistema, con su rol (RF01, RF02)
CREATE TABLE usuarios (
  -- Identificador, lo pone MySQL solo (1, 2, 3...)
  id_usuario INT NOT NULL AUTO_INCREMENT,
  -- Documento de identidad
  identificacion VARCHAR(20) NOT NULL,
  -- Nombres
  nombres VARCHAR(80) NOT NULL,
  -- Apellidos
  apellidos VARCHAR(80) NOT NULL,
  -- Correo: es el usuario para iniciar sesión
  correo VARCHAR(120) NOT NULL,
  -- Contraseña cifrada con bcrypt (RN06): nunca se guarda en texto plano
  password VARCHAR(255) NOT NULL,
  -- Rol que define los permisos
  rol ENUM('ADMIN', 'CAJERO', 'COCINERO') NOT NULL,
  -- Un usuario INACTIVO no puede iniciar sesión
  estado ENUM('ACTIVO', 'INACTIVO') NOT NULL DEFAULT 'ACTIVO',
  -- Llave primaria
  PRIMARY KEY (id_usuario),
  -- No se repite el documento
  CONSTRAINT uq_usuarios_identificacion UNIQUE (identificacion),
  -- No se repite el correo
  CONSTRAINT uq_usuarios_correo UNIQUE (correo)
) ENGINE = InnoDB;

-- categorias: grupos de productos: platos, bebidas, panadería, repostería... (RF03)
CREATE TABLE categorias (
  -- Identificador
  id_categoria INT NOT NULL AUTO_INCREMENT,
  -- Nombre de la categoría
  nombre VARCHAR(60) NOT NULL,
  -- Descripción opcional
  descripcion VARCHAR(200) NULL,
  -- Estado para el borrado lógico
  estado ENUM('ACTIVO', 'INACTIVO') NOT NULL DEFAULT 'ACTIVO',
  -- Llave primaria
  PRIMARY KEY (id_categoria),
  -- No se repite el nombre
  CONSTRAINT uq_categorias_nombre UNIQUE (nombre)
) ENGINE = InnoDB;

-- insumos: ingredientes y materias primas del inventario (RF07)
CREATE TABLE insumos (
  -- Identificador
  id_insumo INT NOT NULL AUTO_INCREMENT,
  -- Nombre del insumo
  nombre VARCHAR(100) NOT NULL,
  -- Unidad en la que se mide
  unidad_medida ENUM('g', 'kg', 'ml', 'l', 'lb', 'unidad') NOT NULL,
  -- Existencias actuales (3 decimales, igual que la receta)
  stock_actual DECIMAL(10,3) NOT NULL DEFAULT 0,
  -- Nivel mínimo: por debajo de este valor el insumo sale en stock bajo
  stock_minimo DECIMAL(10,3) NOT NULL DEFAULT 0,
  -- Costo por unidad de medida (lo actualiza cada compra, RN02)
  costo_unitario DECIMAL(10,2) NOT NULL DEFAULT 0,
  -- Fecha de vencimiento del lote actual; puede quedar vacía
  fecha_vencimiento DATE NULL,
  -- Estado para el borrado lógico (RN04)
  estado ENUM('ACTIVO', 'INACTIVO') NOT NULL DEFAULT 'ACTIVO',
  -- Llave primaria
  PRIMARY KEY (id_insumo),
  -- No se repite el nombre
  CONSTRAINT uq_insumos_nombre UNIQUE (nombre),
  -- El stock nunca puede quedar negativo (RN03)
  CONSTRAINT ck_insumos_stock_actual CHECK (stock_actual >= 0),
  -- El stock mínimo no puede ser negativo
  CONSTRAINT ck_insumos_stock_minimo CHECK (stock_minimo >= 0),
  -- El costo no puede ser negativo
  CONSTRAINT ck_insumos_costo CHECK (costo_unitario >= 0),
  -- Índice para buscar rápido los insumos por vencer
  INDEX idx_insumos_vencimiento (fecha_vencimiento)
) ENGINE = InnoDB;

-- proveedores: a quién se le compran los insumos (RF08)
CREATE TABLE proveedores (
  -- Identificador
  id_proveedor INT NOT NULL AUTO_INCREMENT,
  -- NIT o documento
  nit VARCHAR(20) NOT NULL,
  -- Nombre o razón social
  razon_social VARCHAR(120) NOT NULL,
  -- Teléfono de contacto
  telefono VARCHAR(20) NULL,
  -- Correo de contacto
  correo VARCHAR(120) NULL,
  -- Dirección
  direccion VARCHAR(150) NULL,
  -- Estado para el borrado lógico (RN04)
  estado ENUM('ACTIVO', 'INACTIVO') NOT NULL DEFAULT 'ACTIVO',
  -- Llave primaria
  PRIMARY KEY (id_proveedor),
  -- No se repite el NIT
  CONSTRAINT uq_proveedores_nit UNIQUE (nit)
) ENGINE = InnoDB;

-- clientes: quienes hacen pedidos, por tipo (RF09)
CREATE TABLE clientes (
  -- Identificador
  id_cliente INT NOT NULL AUTO_INCREMENT,
  -- Documento de identidad
  identificacion VARCHAR(20) NOT NULL,
  -- Nombres
  nombres VARCHAR(80) NOT NULL,
  -- Apellidos
  apellidos VARCHAR(80) NOT NULL,
  -- Teléfono de contacto
  telefono VARCHAR(20) NULL,
  -- Correo de contacto
  correo VARCHAR(120) NULL,
  -- Tipo de cliente
  tipo_cliente ENUM('APRENDIZ', 'INSTRUCTOR', 'FUNCIONARIO', 'EXTERNO') NOT NULL,
  -- Campo agregado: estado para el borrado lógico que pide RN04
  estado ENUM('ACTIVO', 'INACTIVO') NOT NULL DEFAULT 'ACTIVO',
  -- Llave primaria
  PRIMARY KEY (id_cliente),
  -- No se repite el documento
  CONSTRAINT uq_clientes_identificacion UNIQUE (identificacion)
) ENGINE = InnoDB;

-- ---------------------------------------------------------------------
-- Después las tablas que dependen de las anteriores (tienen llaves foráneas)
-- ---------------------------------------------------------------------

-- productos: lo que se vende, con su precio y categoría (RF04)
CREATE TABLE productos (
  -- Identificador
  id_producto INT NOT NULL AUTO_INCREMENT,
  -- Código interno
  codigo VARCHAR(20) NOT NULL,
  -- Nombre del producto
  nombre VARCHAR(100) NOT NULL,
  -- Descripción opcional
  descripcion TEXT NULL,
  -- Precio de venta
  precio_venta DECIMAL(10,2) NOT NULL,
  -- Porción, unidad, libra, vaso...
  unidad_venta VARCHAR(20) NOT NULL,
  -- Categoría a la que pertenece
  id_categoria INT NOT NULL,
  -- AGOTADO e INACTIVO no se pueden pedir
  estado ENUM('DISPONIBLE', 'AGOTADO', 'INACTIVO') NOT NULL DEFAULT 'DISPONIBLE',
  -- Llave primaria
  PRIMARY KEY (id_producto),
  -- No se repite el código
  CONSTRAINT uq_productos_codigo UNIQUE (codigo),
  -- El precio debe ser mayor que 0
  CONSTRAINT ck_productos_precio CHECK (precio_venta > 0),
  -- Una categoría agrupa muchos productos (1:N); no se borra una categoría que tenga productos
  CONSTRAINT fk_productos_categoria FOREIGN KEY (id_categoria) REFERENCES categorias (id_categoria)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE = InnoDB;

-- recetas: ficha técnica; resuelve la relación N:M entre productos e insumos (RF05)
CREATE TABLE recetas (
  -- Identificador
  id_receta INT NOT NULL AUTO_INCREMENT,
  -- Producto que se prepara
  id_producto INT NOT NULL,
  -- Insumo que usa
  id_insumo INT NOT NULL,
  -- Cantidad del insumo por cada unidad del producto
  cantidad DECIMAL(10,3) NOT NULL,
  -- Llave primaria
  PRIMARY KEY (id_receta),
  -- Un insumo aparece una sola vez en la receta de un producto
  CONSTRAINT uq_recetas_producto_insumo UNIQUE (id_producto, id_insumo),
  -- La cantidad debe ser mayor que 0
  CONSTRAINT ck_recetas_cantidad CHECK (cantidad > 0),
  -- Relación con productos
  CONSTRAINT fk_recetas_producto FOREIGN KEY (id_producto) REFERENCES productos (id_producto)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  -- Relación con insumos
  CONSTRAINT fk_recetas_insumo FOREIGN KEY (id_insumo) REFERENCES insumos (id_insumo)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE = InnoDB;

-- compras: compras de insumos a un proveedor (RF08)
CREATE TABLE compras (
  -- Identificador
  id_compra INT NOT NULL AUTO_INCREMENT,
  -- Número de la factura del proveedor
  numero_factura VARCHAR(30) NOT NULL,
  -- Fecha y hora de la compra (por defecto, ahora)
  fecha_compra DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- Proveedor (1:N)
  id_proveedor INT NOT NULL,
  -- Usuario que registró la compra (1:N)
  id_usuario INT NOT NULL,
  -- Suma de los subtotales (la calcula la API)
  total DECIMAL(12,2) NOT NULL DEFAULT 0,
  -- Llave primaria
  PRIMARY KEY (id_compra),
  -- Un proveedor no repite número de factura
  CONSTRAINT uq_compras_proveedor_factura UNIQUE (id_proveedor, numero_factura),
  -- El total no puede ser negativo
  CONSTRAINT ck_compras_total CHECK (total >= 0),
  -- Relación con proveedores
  CONSTRAINT fk_compras_proveedor FOREIGN KEY (id_proveedor) REFERENCES proveedores (id_proveedor)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  -- Relación con usuarios
  CONSTRAINT fk_compras_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  -- Índice para los historiales por fecha
  INDEX idx_compras_fecha (fecha_compra)
) ENGINE = InnoDB;

-- detalle_compra: ítems de cada compra; resuelve la relación N:M entre compras e insumos
CREATE TABLE detalle_compra (
  -- Identificador
  id_detalle_compra INT NOT NULL AUTO_INCREMENT,
  -- Compra a la que pertenece
  id_compra INT NOT NULL,
  -- Insumo comprado
  id_insumo INT NOT NULL,
  -- Cantidad comprada (3 decimales, igual que el stock)
  cantidad DECIMAL(10,3) NOT NULL,
  -- Costo por unidad en esta compra
  costo_unitario DECIMAL(10,2) NOT NULL,
  -- cantidad x costo_unitario (lo calcula la API)
  subtotal DECIMAL(12,2) NOT NULL,
  -- Llave primaria
  PRIMARY KEY (id_detalle_compra),
  -- Un insumo aparece una sola vez en cada compra
  CONSTRAINT uq_detalle_compra_compra_insumo UNIQUE (id_compra, id_insumo),
  -- La cantidad debe ser mayor que 0
  CONSTRAINT ck_detalle_compra_cantidad CHECK (cantidad > 0),
  -- El costo no puede ser negativo
  CONSTRAINT ck_detalle_compra_costo CHECK (costo_unitario >= 0),
  -- El subtotal no puede ser negativo
  CONSTRAINT ck_detalle_compra_subtotal CHECK (subtotal >= 0),
  -- Si se borra la compra, se borran sus ítems
  CONSTRAINT fk_detalle_compra_compra FOREIGN KEY (id_compra) REFERENCES compras (id_compra)
    ON UPDATE CASCADE ON DELETE CASCADE,
  -- Relación con insumos
  CONSTRAINT fk_detalle_compra_insumo FOREIGN KEY (id_insumo) REFERENCES insumos (id_insumo)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE = InnoDB;

-- pedidos: pedidos de los clientes y su estado (RF10)
CREATE TABLE pedidos (
  -- Identificador
  id_pedido INT NOT NULL AUTO_INCREMENT,
  -- Fecha y hora del pedido (por defecto, ahora)
  fecha_pedido DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  -- Cliente que pide (1:N)
  id_cliente INT NOT NULL,
  -- Usuario que registra el pedido (1:N)
  id_usuario INT NOT NULL,
  -- Mesa, para llevar o evento
  tipo_pedido ENUM('MESA', 'PARA_LLEVAR', 'EVENTO') NOT NULL,
  -- Estado del pedido; ENTREGADO y ANULADO ya no se modifican (RN05)
  estado ENUM('PENDIENTE', 'EN_PREPARACION', 'ENTREGADO', 'ANULADO') NOT NULL DEFAULT 'PENDIENTE',
  -- Suma de los subtotales (la calcula la API, RN01)
  total DECIMAL(12,2) NOT NULL DEFAULT 0,
  -- Campo del diagrama: notas del pedido (por ejemplo, "sin cebolla")
  observaciones VARCHAR(255) NULL,
  -- Llave primaria
  PRIMARY KEY (id_pedido),
  -- El total no puede ser negativo
  CONSTRAINT ck_pedidos_total CHECK (total >= 0),
  -- Relación con clientes
  CONSTRAINT fk_pedidos_cliente FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  -- Relación con usuarios
  CONSTRAINT fk_pedidos_usuario FOREIGN KEY (id_usuario) REFERENCES usuarios (id_usuario)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  -- Índice para filtrar por estado
  INDEX idx_pedidos_estado (estado),
  -- Índice para los reportes por rango de fechas
  INDEX idx_pedidos_fecha (fecha_pedido)
) ENGINE = InnoDB;

-- detalle_pedido: ítems de cada pedido; resuelve la relación N:M entre pedidos y productos
CREATE TABLE detalle_pedido (
  -- Identificador
  id_detalle INT NOT NULL AUTO_INCREMENT,
  -- Pedido al que pertenece
  id_pedido INT NOT NULL,
  -- Producto pedido
  id_producto INT NOT NULL,
  -- Cantidad pedida (2 decimales: permite, por ejemplo, 1.5 libras de pan)
  cantidad DECIMAL(10,2) NOT NULL,
  -- Precio del producto en el momento del pedido (lo pone la API, RN01)
  precio_unitario DECIMAL(10,2) NOT NULL,
  -- cantidad x precio_unitario (lo calcula la API, RN01)
  subtotal DECIMAL(12,2) NOT NULL,
  -- Llave primaria
  PRIMARY KEY (id_detalle),
  -- Un producto aparece una sola vez en cada pedido
  CONSTRAINT uq_detalle_pedido_pedido_producto UNIQUE (id_pedido, id_producto),
  -- La cantidad debe ser mayor que 0
  CONSTRAINT ck_detalle_pedido_cantidad CHECK (cantidad > 0),
  -- El precio debe ser mayor que 0
  CONSTRAINT ck_detalle_pedido_precio CHECK (precio_unitario > 0),
  -- El subtotal no puede ser negativo
  CONSTRAINT ck_detalle_pedido_subtotal CHECK (subtotal >= 0),
  -- Si se borra el pedido, se borran sus ítems
  CONSTRAINT fk_detalle_pedido_pedido FOREIGN KEY (id_pedido) REFERENCES pedidos (id_pedido)
    ON UPDATE CASCADE ON DELETE CASCADE,
  -- Relación con productos
  CONSTRAINT fk_detalle_pedido_producto FOREIGN KEY (id_producto) REFERENCES productos (id_producto)
    ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE = InnoDB;

-- Muestra las tablas creadas (evidencia para el anexo)
SHOW TABLES;
