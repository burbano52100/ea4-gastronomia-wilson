// Script 04 (MongoDB): crea la base bd_gastronomia_nosql y la colección calificaciones con validación
// $jsonSchema, sus índices, el usuario de la API con privilegios mínimos y 10 calificaciones de prueba.
// Se ejecuta con mongosh como root, después de los scripts de MySQL (las calificaciones son de pedidos
// ENTREGADO que crea el script 02). Se puede ejecutar varias veces: borra la colección y la vuelve a crear.

// Base de datos de las calificaciones (si no existe, MongoDB la crea con la primera colección)
var jbBd = db.getSiblingDB('bd_gastronomia_nosql');

// Borra la colección si ya existe, para empezar desde cero
jbBd.calificaciones.drop();

// Crea la colección con su validador. Es el equivalente a definir las columnas de una tabla:
// MongoDB rechaza cualquier documento que no cumpla estas reglas, aunque no pase por la API.
jbBd.createCollection('calificaciones', {
  // Reglas que debe cumplir cada documento
  validator: {
    // JSON Schema: describe la forma del documento
    $jsonSchema: {
      // Cada documento es un objeto
      bsonType: 'object',
      // Título que se ve en MongoDB Compass
      title: 'Calificación de un pedido',
      // Campos obligatorios (como NOT NULL en MySQL)
      required: ['id_pedido', 'id_cliente', 'fecha', 'calificacion_servicio', 'productos'],
      // No se aceptan campos distintos a los de properties (por eso _id va en la lista)
      additionalProperties: false,
      // Tipo y reglas de cada campo
      properties: {
        // Identificador que pone MongoDB
        _id: { bsonType: 'objectId' },
        // Número del pedido en MySQL (entero mayor que 0)
        id_pedido: { bsonType: ['int', 'long'], minimum: 1, description: 'id_pedido de la tabla pedidos de MySQL' },
        // Número del cliente en MySQL (entero mayor que 0)
        id_cliente: { bsonType: ['int', 'long'], minimum: 1, description: 'id_cliente de la tabla clientes de MySQL' },
        // Fecha y hora de la calificación, guardada como fecha (no como texto)
        fecha: { bsonType: 'date', description: 'Fecha y hora en que se registró la calificación' },
        // Nota del servicio: entero de 1 a 5 (como un CHECK en MySQL)
        calificacion_servicio: { bsonType: ['int', 'long'], minimum: 1, maximum: 5, description: 'Nota de 1 a 5' },
        // Comentario libre: texto de máximo 500 caracteres, o null
        comentario: { bsonType: ['string', 'null'], maxLength: 500 },
        // Productos calificados: lista con al menos un elemento (lo que en MySQL sería una tabla de detalle)
        productos: {
          // Es una lista
          bsonType: 'array',
          // Con al menos un producto
          minItems: 1,
          // Forma de cada elemento de la lista
          items: {
            // Cada elemento es un objeto
            bsonType: 'object',
            // Sus tres campos son obligatorios
            required: ['id_producto', 'nombre', 'calificacion'],
            // No se aceptan otros campos
            additionalProperties: false,
            // Reglas de cada campo del producto
            properties: {
              // Número del producto en MySQL
              id_producto: { bsonType: ['int', 'long'], minimum: 1 },
              // Nombre del producto (lo copia la API desde MySQL)
              nombre: { bsonType: 'string', minLength: 1, maxLength: 100 },
              // Nota del producto: entero de 1 a 5
              calificacion: { bsonType: ['int', 'long'], minimum: 1, maximum: 5 }
            }
          }
        }
      }
    }
  },
  // strict: revisa todas las inserciones y actualizaciones
  validationLevel: 'strict',
  // error: rechaza el documento que no cumpla (no solo avisa)
  validationAction: 'error'
});

// Índice único: un pedido se califica una sola vez (como UNIQUE en MySQL)
jbBd.calificaciones.createIndex({ id_pedido: 1 }, { unique: true, name: 'uq_calificaciones_pedido' });
// Índice para buscar rápido las calificaciones de un producto (GET /calificaciones/producto/{id})
jbBd.calificaciones.createIndex({ 'productos.id_producto': 1 }, { name: 'idx_calificaciones_producto' });
// Índice para ordenar por fecha
jbBd.calificaciones.createIndex({ fecha: -1 }, { name: 'idx_calificaciones_fecha' });

// Rol con privilegios mínimos: solo consultar, insertar, actualizar y borrar documentos de calificaciones
// (es el equivalente al GRANT SELECT, INSERT, UPDATE, DELETE del script 03 de MySQL)
if (jbBd.getRole('jb_rol_api_calificaciones')) {
  // Si el rol ya existe se borra, para poder ejecutar el script varias veces
  jbBd.dropRole('jb_rol_api_calificaciones');
}
// Crea el rol
jbBd.createRole({
  // Nombre del rol
  role: 'jb_rol_api_calificaciones',
  // Permisos: sobre la colección calificaciones, solo estas cuatro acciones
  privileges: [{ resource: { db: 'bd_gastronomia_nosql', collection: 'calificaciones' }, actions: ['find', 'insert', 'update', 'remove'] }],
  // No hereda permisos de otros roles
  roles: []
});

// Usuario con el que se conecta la API (nunca con root)
if (jbBd.getUser('jb_api_gastronomia')) {
  // Si el usuario ya existe se borra, para poder ejecutar el script varias veces
  jbBd.dropUser('jb_api_gastronomia');
}
// Crea el usuario. CONTRASEÑA DE DESARROLLO: debe ser la misma de MONGO_PASSWORD en el archivo .env.
jbBd.createUser({ user: 'jb_api_gastronomia', pwd: 'JbMongoGastro_2026', roles: [{ role: 'jb_rol_api_calificaciones', db: 'bd_gastronomia_nosql' }] });

// Milisegundos de un minuto y de un día, para calcular las fechas desde hoy
var jbMinuto = 60 * 1000;
var jbDia = 24 * 60 * jbMinuto;
// Momento en que se ejecuta el script
var jbAhora = Date.now();

// 10 calificaciones de pedidos ENTREGADO. Cada pedido es del cliente que lo hizo y sus productos son los del pedido.
// Los números se escriben con NumberInt para que MongoDB los guarde como enteros (el validador exige int).
jbBd.calificaciones.insertMany([
  // Calificación del pedido 110
  { id_pedido: NumberInt(110), id_cliente: NumberInt(1), fecha: new Date(jbAhora - 8 * jbDia - 30 * jbMinuto), calificacion_servicio: NumberInt(5), comentario: 'Muy buena atención', productos: [{ id_producto: NumberInt(4), nombre: 'Almuerzo ejecutivo', calificacion: NumberInt(5) }, { id_producto: NumberInt(9), nombre: 'Jugo de lulo', calificacion: NumberInt(5) }] },
  // Calificación del pedido 111
  { id_pedido: NumberInt(111), id_cliente: NumberInt(6), fecha: new Date(jbAhora - 8 * jbDia - 31 * jbMinuto), calificacion_servicio: NumberInt(4), comentario: 'Buen sabor, la espera fue un poco larga', productos: [{ id_producto: NumberInt(1), nombre: 'Arroz con pollo', calificacion: NumberInt(4) }, { id_producto: NumberInt(9), nombre: 'Jugo de lulo', calificacion: NumberInt(4) }] },
  // Calificación del pedido 113
  { id_pedido: NumberInt(113), id_cliente: NumberInt(12), fecha: new Date(jbAhora - 7 * jbDia - 32 * jbMinuto), calificacion_servicio: NumberInt(5), comentario: 'La torta estaba deliciosa', productos: [{ id_producto: NumberInt(7), nombre: 'Torta de chocolate', calificacion: NumberInt(5) }, { id_producto: NumberInt(10), nombre: 'Café tinto', calificacion: NumberInt(4) }] },
  // Calificación del pedido 114
  { id_pedido: NumberInt(114), id_cliente: NumberInt(2), fecha: new Date(jbAhora - 6 * jbDia - 33 * jbMinuto), calificacion_servicio: NumberInt(3), comentario: 'La sobrebarriga llegó tibia', productos: [{ id_producto: NumberInt(2), nombre: 'Sobrebarriga en salsa', calificacion: NumberInt(3) }, { id_producto: NumberInt(9), nombre: 'Jugo de lulo', calificacion: NumberInt(4) }] },
  // Calificación del pedido 116
  { id_pedido: NumberInt(116), id_cliente: NumberInt(7), fecha: new Date(jbAhora - 4 * jbDia - 34 * jbMinuto), calificacion_servicio: NumberInt(5), comentario: 'Excelente almuerzo', productos: [{ id_producto: NumberInt(4), nombre: 'Almuerzo ejecutivo', calificacion: NumberInt(5) }, { id_producto: NumberInt(12), nombre: 'Ensalada de la casa', calificacion: NumberInt(4) }] },
  // Calificación del pedido 118
  { id_pedido: NumberInt(118), id_cliente: NumberInt(13), fecha: new Date(jbAhora - 2 * jbDia - 35 * jbMinuto), calificacion_servicio: NumberInt(4), comentario: null, productos: [{ id_producto: NumberInt(1), nombre: 'Arroz con pollo', calificacion: NumberInt(4) }, { id_producto: NumberInt(9), nombre: 'Jugo de lulo', calificacion: NumberInt(5) }] },
  // Calificación del pedido 121
  { id_pedido: NumberInt(121), id_cliente: NumberInt(14), fecha: new Date(jbAhora - 1 * jbDia - 36 * jbMinuto), calificacion_servicio: NumberInt(4), comentario: 'Todo bien', productos: [{ id_producto: NumberInt(1), nombre: 'Arroz con pollo', calificacion: NumberInt(5) }, { id_producto: NumberInt(12), nombre: 'Ensalada de la casa', calificacion: NumberInt(4) }, { id_producto: NumberInt(9), nombre: 'Jugo de lulo', calificacion: NumberInt(4) }] },
  // Calificación del pedido 123
  { id_pedido: NumberInt(123), id_cliente: NumberInt(15), fecha: new Date(jbAhora - 0 * jbDia - 37 * jbMinuto), calificacion_servicio: NumberInt(2), comentario: 'Demoraron mucho en atender', productos: [{ id_producto: NumberInt(4), nombre: 'Almuerzo ejecutivo', calificacion: NumberInt(3) }, { id_producto: NumberInt(9), nombre: 'Jugo de lulo', calificacion: NumberInt(3) }] },
  // Calificación del pedido 124
  { id_pedido: NumberInt(124), id_cliente: NumberInt(16), fecha: new Date(jbAhora - 0 * jbDia - 38 * jbMinuto), calificacion_servicio: NumberInt(5), comentario: 'Los brownies son los mejores', productos: [{ id_producto: NumberInt(8), nombre: 'Brownie', calificacion: NumberInt(5) }, { id_producto: NumberInt(10), nombre: 'Café tinto', calificacion: NumberInt(5) }] },
  // Ejemplo del instructivo: pedido 125, cliente 18
  { id_pedido: NumberInt(125), id_cliente: NumberInt(18), fecha: new Date(jbAhora - 60 * jbMinuto), calificacion_servicio: NumberInt(5), comentario: 'Excelente atención y buen sabor', productos: [{ id_producto: NumberInt(4), nombre: 'Almuerzo ejecutivo', calificacion: NumberInt(5) }, { id_producto: NumberInt(9), nombre: 'Jugo de lulo', calificacion: NumberInt(4) }] }
]);

// Evidencia para el anexo: reglas del validador, índices y cantidad de documentos
printjson(jbBd.getCollectionInfos({ name: 'calificaciones' })[0].options.validator);
// Lista los índices de la colección
printjson(jbBd.calificaciones.getIndexes().map(jbIndice => jbIndice.name));
// Muestra cuántas calificaciones quedaron
print('Calificaciones registradas: ' + jbBd.calificaciones.countDocuments());
