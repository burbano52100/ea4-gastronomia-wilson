"""Modelos de las tablas de MySQL (bd_gastronomia) con SQLAlchemy.

Cada clase representa una tabla que crea database/01_jb_ddl_bd_gastronomia.sql.
Las tablas las crea ese script, no este archivo: aquí solo se describen para trabajar con ellas desde Python.
Las propiedades (@property) son datos calculados que la API incluye en sus respuestas.
"""
# date: solo fecha; datetime: fecha y hora
from datetime import date, datetime
# Decimal: números exactos para dinero y cantidades
from decimal import Decimal

# Tipos de columna y llave foránea de SQLAlchemy
from sqlalchemy import Date, DateTime, Enum, ForeignKey, Numeric, String, Text
# Mapped: tipo de un atributo; mapped_column: define una columna; relationship: relación con otra tabla
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Fecha de hoy en Colombia (para los días que le faltan a un insumo para vencer)
from app.core.jb_utilidades import jb_hoy
# Clase base de los modelos
from app.database.jb_conexion_mysql import JbBase


# Tabla usuarios
class JbUsuario(JbBase):
    """Usuarios del sistema y su rol (RF01, RF02)."""

    # Nombre de la tabla en MySQL
    __tablename__ = "usuarios"
    # Llave primaria autoincremental
    id_usuario: Mapped[int] = mapped_column(primary_key=True)
    # Documento de identidad (único)
    identificacion: Mapped[str] = mapped_column(String(20))
    # Nombres
    nombres: Mapped[str] = mapped_column(String(80))
    # Apellidos
    apellidos: Mapped[str] = mapped_column(String(80))
    # Correo para iniciar sesión (único)
    correo: Mapped[str] = mapped_column(String(120))
    # Hash bcrypt de la contraseña (RN06): ningún esquema de respuesta lo incluye
    password: Mapped[str] = mapped_column(String(255))
    # ADMIN, CAJERO o COCINERO
    rol: Mapped[str] = mapped_column(Enum("ADMIN", "CAJERO", "COCINERO"))
    # ACTIVO o INACTIVO
    estado: Mapped[str] = mapped_column(Enum("ACTIVO", "INACTIVO"), default="ACTIVO")


# Tabla categorias
class JbCategoria(JbBase):
    """Categorías de productos (RF03)."""

    # Nombre de la tabla en MySQL
    __tablename__ = "categorias"
    # Llave primaria
    id_categoria: Mapped[int] = mapped_column(primary_key=True)
    # Nombre (único)
    nombre: Mapped[str] = mapped_column(String(60))
    # Descripción opcional
    descripcion: Mapped[str | None] = mapped_column(String(200))
    # ACTIVO o INACTIVO
    estado: Mapped[str] = mapped_column(Enum("ACTIVO", "INACTIVO"), default="ACTIVO")


# Tabla insumos
class JbInsumo(JbBase):
    """Insumos del inventario (RF07)."""

    # Nombre de la tabla en MySQL
    __tablename__ = "insumos"
    # Llave primaria
    id_insumo: Mapped[int] = mapped_column(primary_key=True)
    # Nombre (único)
    nombre: Mapped[str] = mapped_column(String(100))
    # g, kg, ml, l, lb o unidad
    unidad_medida: Mapped[str] = mapped_column(Enum("g", "kg", "ml", "l", "lb", "unidad"))
    # Existencias actuales (3 decimales)
    stock_actual: Mapped[Decimal] = mapped_column(Numeric(10, 3), default=Decimal("0"))
    # Nivel mínimo de alerta
    stock_minimo: Mapped[Decimal] = mapped_column(Numeric(10, 3), default=Decimal("0"))
    # Costo por unidad de medida
    costo_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0"))
    # Vencimiento del lote actual (puede ser nulo)
    fecha_vencimiento: Mapped[date | None] = mapped_column(Date)
    # ACTIVO o INACTIVO
    estado: Mapped[str] = mapped_column(Enum("ACTIVO", "INACTIVO"), default="ACTIVO")

    # Dato calculado: cuánto falta para llegar al stock mínimo (0 si no falta nada)
    @property
    # Con @property se lee como un dato, sin paréntesis (por ejemplo jb_producto.nombre_categoria)
    def faltante(self) -> Decimal:
        # Si el stock actual ya llega al mínimo, no falta nada
        return max(self.stock_minimo - self.stock_actual, Decimal("0"))

    # Dato calculado: días que le quedan antes de vencer (None si no tiene fecha)
    @property
    # Con @property se lee como un dato, sin paréntesis (por ejemplo jb_producto.nombre_categoria)
    def dias_restantes(self) -> int | None:
        # Sin fecha de vencimiento no hay días que contar
        if self.fecha_vencimiento is None:
            # Devuelve None (en la respuesta JSON se ve como null)
            return None
        # Resta la fecha de hoy a la de vencimiento y toma los días
        return (self.fecha_vencimiento - jb_hoy()).days


# Tabla proveedores
class JbProveedor(JbBase):
    """Proveedores de insumos (RF08)."""

    # Nombre de la tabla en MySQL
    __tablename__ = "proveedores"
    # Llave primaria
    id_proveedor: Mapped[int] = mapped_column(primary_key=True)
    # NIT o documento (único)
    nit: Mapped[str] = mapped_column(String(20))
    # Nombre o razón social
    razon_social: Mapped[str] = mapped_column(String(120))
    # Teléfono (opcional)
    telefono: Mapped[str | None] = mapped_column(String(20))
    # Correo (opcional)
    correo: Mapped[str | None] = mapped_column(String(120))
    # Dirección (opcional)
    direccion: Mapped[str | None] = mapped_column(String(150))
    # ACTIVO o INACTIVO
    estado: Mapped[str] = mapped_column(Enum("ACTIVO", "INACTIVO"), default="ACTIVO")


# Tabla clientes
class JbCliente(JbBase):
    """Clientes por tipo (RF09)."""

    # Nombre de la tabla en MySQL
    __tablename__ = "clientes"
    # Llave primaria
    id_cliente: Mapped[int] = mapped_column(primary_key=True)
    # Documento (único)
    identificacion: Mapped[str] = mapped_column(String(20))
    # Nombres
    nombres: Mapped[str] = mapped_column(String(80))
    # Apellidos
    apellidos: Mapped[str] = mapped_column(String(80))
    # Teléfono (opcional)
    telefono: Mapped[str | None] = mapped_column(String(20))
    # Correo (opcional)
    correo: Mapped[str | None] = mapped_column(String(120))
    # APRENDIZ, INSTRUCTOR, FUNCIONARIO o EXTERNO
    tipo_cliente: Mapped[str] = mapped_column(Enum("APRENDIZ", "INSTRUCTOR", "FUNCIONARIO", "EXTERNO"))
    # ACTIVO o INACTIVO (campo agregado por RN04)
    estado: Mapped[str] = mapped_column(Enum("ACTIVO", "INACTIVO"), default="ACTIVO")


# Tabla productos
class JbProducto(JbBase):
    """Productos que se venden (RF04)."""

    # Nombre de la tabla en MySQL
    __tablename__ = "productos"
    # Llave primaria
    id_producto: Mapped[int] = mapped_column(primary_key=True)
    # Código interno (único)
    codigo: Mapped[str] = mapped_column(String(20))
    # Nombre
    nombre: Mapped[str] = mapped_column(String(100))
    # Descripción opcional
    descripcion: Mapped[str | None] = mapped_column(Text)
    # Precio de venta
    precio_venta: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    # Porción, unidad, libra, vaso...
    unidad_venta: Mapped[str] = mapped_column(String(20))
    # Llave foránea a categorias
    id_categoria: Mapped[int] = mapped_column(ForeignKey("categorias.id_categoria"))
    # DISPONIBLE, AGOTADO o INACTIVO
    estado: Mapped[str] = mapped_column(Enum("DISPONIBLE", "AGOTADO", "INACTIVO"), default="DISPONIBLE")
    # Categoría del producto; selectin la carga en una consulta aparte
    categoria: Mapped[JbCategoria] = relationship(lazy="selectin")

    # Dato calculado: nombre de la categoría, para mostrarlo en las respuestas
    @property
    # Con @property se lee como un dato, sin paréntesis (por ejemplo jb_producto.nombre_categoria)
    def nombre_categoria(self) -> str | None:
        # Si la categoría está cargada devuelve su nombre
        return self.categoria.nombre if self.categoria else None


# Tabla recetas
class JbReceta(JbBase):
    """Ficha técnica: cantidad de cada insumo por unidad de producto (RF05)."""

    # Nombre de la tabla en MySQL
    __tablename__ = "recetas"
    # Llave primaria
    id_receta: Mapped[int] = mapped_column(primary_key=True)
    # Llave foránea a productos
    id_producto: Mapped[int] = mapped_column(ForeignKey("productos.id_producto"))
    # Llave foránea a insumos
    id_insumo: Mapped[int] = mapped_column(ForeignKey("insumos.id_insumo"))
    # Cantidad del insumo por cada unidad del producto (3 decimales)
    cantidad: Mapped[Decimal] = mapped_column(Numeric(10, 3))
    # Producto de la receta
    producto: Mapped[JbProducto] = relationship(lazy="selectin")
    # Insumo de la receta
    insumo: Mapped[JbInsumo] = relationship(lazy="selectin")

    # Dato calculado: nombre del producto
    @property
    # Con @property se lee como un dato, sin paréntesis (por ejemplo jb_producto.nombre_categoria)
    def nombre_producto(self) -> str:
        # Toma el nombre del producto relacionado
        return self.producto.nombre

    # Dato calculado: nombre del insumo
    @property
    # Con @property se lee como un dato, sin paréntesis (por ejemplo jb_producto.nombre_categoria)
    def nombre_insumo(self) -> str:
        # Toma el nombre del insumo relacionado
        return self.insumo.nombre

    # Dato calculado: unidad de medida del insumo
    @property
    # Con @property se lee como un dato, sin paréntesis (por ejemplo jb_producto.nombre_categoria)
    def unidad_medida(self) -> str:
        # Toma la unidad del insumo relacionado
        return self.insumo.unidad_medida


# Tabla detalle_compra (va antes de compras porque compras la usa en su relación)
class JbDetalleCompra(JbBase):
    """Ítems de una compra (RF08)."""

    # Nombre de la tabla en MySQL
    __tablename__ = "detalle_compra"
    # Llave primaria
    id_detalle_compra: Mapped[int] = mapped_column(primary_key=True)
    # Llave foránea a compras
    id_compra: Mapped[int] = mapped_column(ForeignKey("compras.id_compra"))
    # Llave foránea a insumos
    id_insumo: Mapped[int] = mapped_column(ForeignKey("insumos.id_insumo"))
    # Cantidad comprada
    cantidad: Mapped[Decimal] = mapped_column(Numeric(10, 3))
    # Costo por unidad en esta compra
    costo_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    # cantidad x costo_unitario
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    # Insumo comprado
    insumo: Mapped[JbInsumo] = relationship(lazy="selectin")

    # Dato calculado: nombre del insumo
    @property
    # Con @property se lee como un dato, sin paréntesis (por ejemplo jb_producto.nombre_categoria)
    def nombre_insumo(self) -> str:
        # Toma el nombre del insumo relacionado
        return self.insumo.nombre


# Tabla compras
class JbCompra(JbBase):
    """Compras de insumos a un proveedor (RF08, RN02)."""

    # Nombre de la tabla en MySQL
    __tablename__ = "compras"
    # Llave primaria
    id_compra: Mapped[int] = mapped_column(primary_key=True)
    # Número de la factura del proveedor
    numero_factura: Mapped[str] = mapped_column(String(30))
    # Fecha y hora de la compra
    fecha_compra: Mapped[datetime] = mapped_column(DateTime)
    # Llave foránea a proveedores
    id_proveedor: Mapped[int] = mapped_column(ForeignKey("proveedores.id_proveedor"))
    # Llave foránea a usuarios: quién registró la compra
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"))
    # Suma de los subtotales
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    # Proveedor de la compra
    proveedor: Mapped[JbProveedor] = relationship(lazy="selectin")
    # Ítems de la compra; delete-orphan: un ítem que se quita de la lista se borra de la tabla
    detalle: Mapped[list[JbDetalleCompra]] = relationship(
        # Se cargan en una consulta aparte, ordenados por su id
        lazy="selectin", order_by=JbDetalleCompra.id_detalle_compra,
        # Guardar o borrar la compra guarda o borra también sus ítems
        cascade="all, delete-orphan",
    )

    # Dato calculado: razón social del proveedor
    @property
    # Con @property se lee como un dato, sin paréntesis (por ejemplo jb_producto.nombre_categoria)
    def nombre_proveedor(self) -> str:
        # Toma la razón social del proveedor relacionado
        return self.proveedor.razon_social


# Tabla detalle_pedido (va antes de pedidos porque pedidos la usa en su relación)
class JbDetallePedido(JbBase):
    """Ítems de un pedido (RF10, RN01)."""

    # Nombre de la tabla en MySQL
    __tablename__ = "detalle_pedido"
    # Llave primaria
    id_detalle: Mapped[int] = mapped_column(primary_key=True)
    # Llave foránea a pedidos
    id_pedido: Mapped[int] = mapped_column(ForeignKey("pedidos.id_pedido"))
    # Llave foránea a productos
    id_producto: Mapped[int] = mapped_column(ForeignKey("productos.id_producto"))
    # Cantidad pedida (2 decimales)
    cantidad: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    # Precio del producto al momento del pedido (lo pone la API)
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    # cantidad x precio_unitario (lo calcula la API)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    # Producto pedido
    producto: Mapped[JbProducto] = relationship(lazy="selectin")

    # Dato calculado: nombre del producto
    @property
    # Con @property se lee como un dato, sin paréntesis (por ejemplo jb_producto.nombre_categoria)
    def nombre_producto(self) -> str:
        # Toma el nombre del producto relacionado
        return self.producto.nombre


# Tabla pedidos
class JbPedido(JbBase):
    """Pedidos de los clientes (RF10, RN01, RN03, RN05)."""

    # Nombre de la tabla en MySQL
    __tablename__ = "pedidos"
    # Llave primaria
    id_pedido: Mapped[int] = mapped_column(primary_key=True)
    # Fecha y hora del pedido
    fecha_pedido: Mapped[datetime] = mapped_column(DateTime)
    # Llave foránea a clientes
    id_cliente: Mapped[int] = mapped_column(ForeignKey("clientes.id_cliente"))
    # Llave foránea a usuarios: quién registró el pedido
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"))
    # MESA, PARA_LLEVAR o EVENTO
    tipo_pedido: Mapped[str] = mapped_column(Enum("MESA", "PARA_LLEVAR", "EVENTO"))
    # PENDIENTE, EN_PREPARACION, ENTREGADO o ANULADO
    estado: Mapped[str] = mapped_column(
        # Valores permitidos del ENUM
        Enum("PENDIENTE", "EN_PREPARACION", "ENTREGADO", "ANULADO"),
        # Todo pedido nuevo empieza PENDIENTE
        default="PENDIENTE",
    )
    # Suma de los subtotales (RN01)
    total: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=Decimal("0"))
    # Notas del pedido (opcional)
    observaciones: Mapped[str | None] = mapped_column(String(255))
    # Cliente del pedido
    cliente: Mapped[JbCliente] = relationship(lazy="selectin")
    # Ítems del pedido; delete-orphan: un ítem que se quita de la lista se borra de la tabla
    detalle: Mapped[list[JbDetallePedido]] = relationship(
        # Se cargan en una consulta aparte, ordenados por su id
        lazy="selectin", order_by=JbDetallePedido.id_detalle,
        # Guardar el pedido guarda también sus ítems
        cascade="all, delete-orphan",
    )

    # Dato calculado: nombre completo del cliente
    @property
    # Con @property se lee como un dato, sin paréntesis (por ejemplo jb_producto.nombre_categoria)
    def nombre_cliente(self) -> str:
        # Une nombres y apellidos del cliente relacionado
        return f"{self.cliente.nombres} {self.cliente.apellidos}"
