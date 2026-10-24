"""Modelos de las colecciones de MongoDB.

En SQL el modelo de cada tabla se crea con CREATE TABLE (tipos, NOT NULL, CHECK, UNIQUE).
En MongoDB se define con una validación $jsonSchema (campos obligatorios, tipos, tamaños,
valores permitidos y mínimos) más los índices. Los scripts de la carpeta database/ usan
estas definiciones para crear las colecciones.
"""

# Regla para los ids: número entero (int o long) desde 1, como INT PK o INT FK en SQL
JB_ENTERO = {"bsonType": ["int", "long"], "minimum": 1}
# Regla para las fechas: tipo fecha de MongoDB, como DATETIME en SQL
JB_FECHA = {"bsonType": "date"}
# Regla para el estado: solo se permiten estos dos valores, como un ENUM en SQL
JB_ESTADO = {"enum": ["ACTIVO", "INACTIVO"]}
# Regla para las calificaciones: entero del 1 al 5
JB_CALIFICACION = {"bsonType": ["int", "long"], "minimum": 1, "maximum": 5}
# Regla para los correos: texto de máximo 120 caracteres con la forma algo@algo.algo
JB_CORREO = {"bsonType": "string", "maxLength": 120, "pattern": "^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$"}


# Función que arma la regla de un texto con tamaño máximo, como VARCHAR(n)
def jb_texto(jb_maximo: int, jb_opcional: bool = False) -> dict:
    # Si es opcional acepta texto o null (NULL en SQL); si no, solo texto (NOT NULL)
    return {"bsonType": ["string", "null"] if jb_opcional else "string", "maxLength": jb_maximo}


# Función que arma la regla de un número decimal, como DECIMAL con CHECK
def jb_decimal(jb_mayor_que_cero: bool = False) -> dict:
    """Decimal128 >= 0, o > 0 cuando jb_mayor_que_cero es True (equivale a un CHECK)."""
    # Por defecto: decimal mayor o igual a 0
    jb_regla = {"bsonType": "decimal", "minimum": 0}
    # Si se pide mayor que cero...
    if jb_mayor_que_cero:
        # ...el mínimo se vuelve exclusivo: el 0 ya no se acepta
        jb_regla["exclusiveMinimum"] = True
    # Devuelve la regla armada
    return jb_regla


# Función que arma la regla de un documento: qué campos son obligatorios y la regla de cada campo
def jb_objeto(jb_obligatorios: list[str], jb_propiedades: dict) -> dict:
    # "required" equivale a NOT NULL; "properties" tiene la regla de cada campo
    return {"bsonType": "object", "required": jb_obligatorios, "properties": jb_propiedades}


# Cada modelo tiene su esquema de validación y sus índices: ([campos], es_unico)
JB_MODELOS = {
    # Colección usuarios (tabla usuarios del instructivo)
    "usuarios": {
        # Validación de cada documento
        "esquema": jb_objeto(
            # Campos obligatorios
            ["_id", "identificacion", "nombres", "apellidos", "correo", "password", "rol", "estado"],
            # Regla de cada campo
            {
                # Identificador numérico (PK)
                "_id": JB_ENTERO,
                # Documento de identidad, máximo 20 caracteres
                "identificacion": jb_texto(20),
                # Nombres, máximo 80 caracteres
                "nombres": jb_texto(80),
                # Apellidos, máximo 80 caracteres
                "apellidos": jb_texto(80),
                # Correo con formato válido
                "correo": JB_CORREO,
                # Hash bcrypt de la contraseña (RN06)
                "password": jb_texto(255),
                # Rol: solo uno de estos tres
                "rol": {"enum": ["ADMIN", "CAJERO", "COCINERO"]},
                # ACTIVO o INACTIVO
                "estado": JB_ESTADO,
            },
        ),
        # Índices únicos: no se repiten el correo ni la identificación (UNIQUE)
        "indices": [(["correo"], True), (["identificacion"], True)],
    },
    # Colección categorias
    "categorias": {
        # Validación de cada documento
        "esquema": jb_objeto(
            # Campos obligatorios
            ["_id", "nombre", "estado"],
            # Regla de cada campo
            {
                # Identificador numérico (PK)
                "_id": JB_ENTERO,
                # Nombre de la categoría, máximo 60 caracteres
                "nombre": jb_texto(60),
                # Descripción opcional, máximo 200 caracteres
                "descripcion": jb_texto(200, True),
                # ACTIVO o INACTIVO
                "estado": JB_ESTADO,
            },
        ),
        # El nombre no se repite
        "indices": [(["nombre"], True)],
    },
    # Colección productos
    "productos": {
        # Validación de cada documento
        "esquema": jb_objeto(
            # Campos obligatorios
            ["_id", "codigo", "nombre", "precio_venta", "unidad_venta", "id_categoria", "estado"],
            # Regla de cada campo
            {
                # Identificador numérico (PK)
                "_id": JB_ENTERO,
                # Código interno, máximo 20 caracteres
                "codigo": jb_texto(20),
                # Nombre, máximo 100 caracteres
                "nombre": jb_texto(100),
                # Descripción opcional sin límite de tamaño (TEXT en SQL)
                "descripcion": {"bsonType": ["string", "null"]},
                # Precio mayor que 0, como CHECK (precio_venta > 0)
                "precio_venta": jb_decimal(jb_mayor_que_cero=True),
                # Porción, unidad, vaso..., máximo 20 caracteres
                "unidad_venta": jb_texto(20),
                # Categoría a la que pertenece (FK hacia categorias)
                "id_categoria": JB_ENTERO,
                # Estado del producto: solo uno de estos tres
                "estado": {"enum": ["DISPONIBLE", "AGOTADO", "INACTIVO"]},
            },
        ),
        # El código no se repite; índice normal en id_categoria para buscar rápido por categoría
        "indices": [(["codigo"], True), (["id_categoria"], False)],
    },
    # Colección insumos (inventario)
    "insumos": {
        # Validación de cada documento
        "esquema": jb_objeto(
            # Campos obligatorios
            ["_id", "nombre", "unidad_medida", "stock_actual", "stock_minimo", "costo_unitario", "estado"],
            # Regla de cada campo
            {
                # Identificador numérico (PK)
                "_id": JB_ENTERO,
                # Nombre, máximo 100 caracteres
                "nombre": jb_texto(100),
                # Unidad de medida: solo una de estas
                "unidad_medida": {"enum": ["g", "kg", "ml", "l", "lb", "unidad"]},
                # Existencias, mayor o igual a 0
                "stock_actual": jb_decimal(),
                # Nivel mínimo de alerta, mayor o igual a 0
                "stock_minimo": jb_decimal(),
                # Costo por unidad de medida, mayor o igual a 0
                "costo_unitario": jb_decimal(),
                # Fecha de vencimiento del lote actual, o null si no vence
                "fecha_vencimiento": {"bsonType": ["date", "null"]},
                # ACTIVO o INACTIVO
                "estado": JB_ESTADO,
            },
        ),
        # El nombre no se repite; índice en fecha_vencimiento para la consulta "por vencer"
        "indices": [(["nombre"], True), (["fecha_vencimiento"], False)],
    },
    # Colección recetas (relación N:M entre productos e insumos)
    "recetas": {
        # Validación de cada documento
        "esquema": jb_objeto(
            # Campos obligatorios
            ["_id", "id_producto", "id_insumo", "cantidad"],
            # Regla de cada campo
            {
                # Identificador numérico (PK)
                "_id": JB_ENTERO,
                # Producto (FK hacia productos)
                "id_producto": JB_ENTERO,
                # Insumo que usa (FK hacia insumos)
                "id_insumo": JB_ENTERO,
                # Cantidad del insumo por unidad de producto, mayor que 0
                "cantidad": jb_decimal(jb_mayor_que_cero=True),
            },
        ),
        # Un insumo aparece una sola vez en la receta de un producto; índice en id_insumo para buscar sus usos
        "indices": [(["id_producto", "id_insumo"], True), (["id_insumo"], False)],
    },
    # Colección proveedores
    "proveedores": {
        # Validación de cada documento
        "esquema": jb_objeto(
            # Campos obligatorios
            ["_id", "nit", "razon_social", "estado"],
            # Regla de cada campo
            {
                # Identificador numérico (PK)
                "_id": JB_ENTERO,
                # NIT o documento, máximo 20 caracteres
                "nit": jb_texto(20),
                # Nombre o razón social, máximo 120 caracteres
                "razon_social": jb_texto(120),
                # Teléfono opcional, máximo 20 caracteres
                "telefono": jb_texto(20, True),
                # Correo opcional: copia la regla de correo pero acepta también null
                "correo": {**JB_CORREO, "bsonType": ["string", "null"]},
                # Dirección opcional, máximo 150 caracteres
                "direccion": jb_texto(150, True),
                # ACTIVO o INACTIVO
                "estado": JB_ESTADO,
            },
        ),
        # El NIT no se repite
        "indices": [(["nit"], True)],
    },
    # Colección compras (con el detalle_compra guardado dentro de cada compra)
    "compras": {
        # Validación de cada documento
        "esquema": jb_objeto(
            # Campos obligatorios
            ["_id", "numero_factura", "fecha_compra", "id_proveedor", "id_usuario", "total", "detalle"],
            # Regla de cada campo
            {
                # Identificador numérico (PK)
                "_id": JB_ENTERO,
                # Número de la factura del proveedor, máximo 30 caracteres
                "numero_factura": jb_texto(30),
                # Fecha y hora de la compra
                "fecha_compra": JB_FECHA,
                # Proveedor (FK hacia proveedores)
                "id_proveedor": JB_ENTERO,
                # Usuario que registró la compra (FK hacia usuarios)
                "id_usuario": JB_ENTERO,
                # Valor total, mayor o igual a 0
                "total": jb_decimal(),
                # Detalle de la compra: una lista de ítems
                "detalle": {
                    # Debe ser una lista
                    "bsonType": "array",
                    # Con al menos un ítem
                    "minItems": 1,
                    # Regla de cada ítem de la lista
                    "items": jb_objeto(
                        # Campos obligatorios de cada ítem
                        ["id_insumo", "cantidad", "costo_unitario", "subtotal"],
                        # Regla de cada campo del ítem
                        {
                            # Insumo comprado (FK hacia insumos)
                            "id_insumo": JB_ENTERO,
                            # Cantidad comprada, mayor que 0
                            "cantidad": jb_decimal(jb_mayor_que_cero=True),
                            # Costo por unidad, mayor o igual a 0
                            "costo_unitario": jb_decimal(),
                            # cantidad x costo_unitario, mayor o igual a 0
                            "subtotal": jb_decimal(),
                        },
                    ),
                },
            },
        ),
        # Un proveedor no repite número de factura; índices para buscar por fecha y por insumo comprado
        "indices": [(["id_proveedor", "numero_factura"], True), (["fecha_compra"], False), (["detalle.id_insumo"], False)],
    },
    # Colección clientes
    "clientes": {
        # Validación de cada documento
        "esquema": jb_objeto(
            # Campos obligatorios
            ["_id", "identificacion", "nombres", "apellidos", "tipo_cliente", "estado"],
            # Regla de cada campo
            {
                # Identificador numérico (PK)
                "_id": JB_ENTERO,
                # Documento de identidad, máximo 20 caracteres
                "identificacion": jb_texto(20),
                # Nombres, máximo 80 caracteres
                "nombres": jb_texto(80),
                # Apellidos, máximo 80 caracteres
                "apellidos": jb_texto(80),
                # Teléfono opcional, máximo 20 caracteres
                "telefono": jb_texto(20, True),
                # Correo opcional: copia la regla de correo pero acepta también null
                "correo": {**JB_CORREO, "bsonType": ["string", "null"]},
                # Tipo de cliente: solo uno de estos cuatro
                "tipo_cliente": {"enum": ["APRENDIZ", "INSTRUCTOR", "FUNCIONARIO", "EXTERNO"]},
                # ACTIVO o INACTIVO (agregado para cumplir RN04)
                "estado": JB_ESTADO,
            },
        ),
        # La identificación no se repite
        "indices": [(["identificacion"], True)],
    },
    # Colección pedidos (con el detalle_pedido guardado dentro de cada pedido)
    "pedidos": {
        # Validación de cada documento
        "esquema": jb_objeto(
            # Campos obligatorios
            ["_id", "fecha_pedido", "id_cliente", "id_usuario", "tipo_pedido", "estado", "total", "detalle"],
            # Regla de cada campo
            {
                # Identificador numérico (PK)
                "_id": JB_ENTERO,
                # Fecha y hora del pedido
                "fecha_pedido": JB_FECHA,
                # Cliente que pide (FK hacia clientes)
                "id_cliente": JB_ENTERO,
                # Usuario que registró el pedido (FK hacia usuarios)
                "id_usuario": JB_ENTERO,
                # Tipo de pedido: solo uno de estos tres
                "tipo_pedido": {"enum": ["MESA", "PARA_LLEVAR", "EVENTO"]},
                # Estado del pedido: solo uno de estos cuatro
                "estado": {"enum": ["PENDIENTE", "EN_PREPARACION", "ENTREGADO", "ANULADO"]},
                # Observaciones opcionales, máximo 255 caracteres
                "observaciones": jb_texto(255, True),
                # Total calculado por la API (RN01), mayor o igual a 0
                "total": jb_decimal(),
                # Detalle del pedido: una lista de ítems
                "detalle": {
                    # Debe ser una lista
                    "bsonType": "array",
                    # Con al menos un ítem
                    "minItems": 1,
                    # Regla de cada ítem de la lista
                    "items": jb_objeto(
                        # Campos obligatorios de cada ítem
                        ["id_producto", "cantidad", "precio_unitario", "subtotal"],
                        # Regla de cada campo del ítem
                        {
                            # Producto pedido (FK hacia productos)
                            "id_producto": JB_ENTERO,
                            # Cantidad: entero desde 1
                            "cantidad": JB_ENTERO,
                            # Precio del producto al momento del pedido
                            "precio_unitario": jb_decimal(),
                            # cantidad x precio_unitario (RN01)
                            "subtotal": jb_decimal(),
                        },
                    ),
                },
            },
        ),
        # Índices para buscar rápido por fecha (reportes), estado, cliente y producto vendido
        "indices": [(["fecha_pedido"], False), (["estado"], False), (["id_cliente"], False), (["detalle.id_producto"], False)],
    },
}

# Base de datos NoSQL: información no estructurada (opiniones de los clientes).
JB_MODELOS_NOSQL = {
    # Colección calificaciones (en bd_gastronomia_nosql)
    "calificaciones": {
        # Validación de cada documento
        "esquema": jb_objeto(
            # Campos obligatorios
            ["_id", "id_pedido", "id_cliente", "fecha", "calificacion_servicio", "productos"],
            # Regla de cada campo
            {
                # Identificador numérico
                "_id": JB_ENTERO,
                # Pedido calificado (está en la otra base)
                "id_pedido": JB_ENTERO,
                # Cliente que califica (está en la otra base)
                "id_cliente": JB_ENTERO,
                # Fecha y hora de la calificación
                "fecha": JB_FECHA,
                # Calificación del servicio, de 1 a 5
                "calificacion_servicio": JB_CALIFICACION,
                # Comentario opcional, máximo 500 caracteres
                "comentario": jb_texto(500, True),
                # Calificación de cada producto del pedido: una lista
                "productos": {
                    # Debe ser una lista
                    "bsonType": "array",
                    # Con al menos un producto
                    "minItems": 1,
                    # Regla de cada producto calificado
                    "items": jb_objeto(
                        # Campos obligatorios de cada producto calificado
                        ["id_producto", "nombre", "calificacion"],
                        # Id del producto, su nombre y su calificación de 1 a 5
                        {"id_producto": JB_ENTERO, "nombre": jb_texto(100), "calificacion": JB_CALIFICACION},
                    ),
                },
            },
        ),
        # Un pedido se califica una sola vez; índices para buscar por cliente y por producto
        "indices": [(["id_pedido"], True), (["id_cliente"], False), (["productos.id_producto"], False)],
    },
}
