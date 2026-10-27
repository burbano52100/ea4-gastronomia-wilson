// DATOS DE EJEMPLO PARA MongoDB (base bd_gastronomia_nosql, colección calificaciones)
// Son las mismas 10 calificaciones del script database/04_jb_mongo_calificaciones.js, en bloques
// para copiarlos y pegarlos en la terminal de MongoDB (mongosh), uno por uno y en orden.
//
// Antes de empezar:
//   1. La colección debe existir con su validador: ejecute antes el script database/04_jb_mongo_calificaciones.js.
//   2. Las calificaciones son de pedidos que crea MySQL: cargue primero los datos de MySQL.
//   3. Abra una terminal en la carpeta api_gastronomia y entre a MongoDB dentro del contenedor:
//          docker compose exec mongo mongosh -u jb_root -p --authenticationDatabase admin
//      Escriba la contraseña de root (la de MONGO_ROOT_PASSWORD en el .env). Aparece el indicador test>
//   4. Copie un bloque completo, péguelo y pulse Enter. Siga con el bloque siguiente.
//   5. Para salir de mongosh escriba: exit

// ===== BLOQUE 1: entrar a la base de datos de las calificaciones =====
db = db.getSiblingDB('bd_gastronomia_nosql')

// ===== BLOQUE 2: vaciar la colección (borra solo los documentos; el validador y los índices se quedan) =====
db.calificaciones.deleteMany({})

// ===== BLOQUE 3: insertar las 10 calificaciones (las fechas se calculan desde hoy) =====
db.calificaciones.insertMany([
  { id_pedido: NumberInt(110), id_cliente: NumberInt(1), fecha: new Date(Date.now() - 8 * 86400000 - 30 * 60000), calificacion_servicio: NumberInt(5), comentario: 'Muy buena atención', productos: [{ id_producto: NumberInt(4), nombre: 'Almuerzo ejecutivo', calificacion: NumberInt(5) }, { id_producto: NumberInt(9), nombre: 'Jugo de lulo', calificacion: NumberInt(5) }] },
  { id_pedido: NumberInt(111), id_cliente: NumberInt(6), fecha: new Date(Date.now() - 8 * 86400000 - 31 * 60000), calificacion_servicio: NumberInt(4), comentario: 'Buen sabor, la espera fue un poco larga', productos: [{ id_producto: NumberInt(1), nombre: 'Arroz con pollo', calificacion: NumberInt(4) }, { id_producto: NumberInt(9), nombre: 'Jugo de lulo', calificacion: NumberInt(4) }] },
  { id_pedido: NumberInt(113), id_cliente: NumberInt(12), fecha: new Date(Date.now() - 7 * 86400000 - 32 * 60000), calificacion_servicio: NumberInt(5), comentario: 'La torta estaba deliciosa', productos: [{ id_producto: NumberInt(7), nombre: 'Torta de chocolate', calificacion: NumberInt(5) }, { id_producto: NumberInt(10), nombre: 'Café tinto', calificacion: NumberInt(4) }] },
  { id_pedido: NumberInt(114), id_cliente: NumberInt(2), fecha: new Date(Date.now() - 6 * 86400000 - 33 * 60000), calificacion_servicio: NumberInt(3), comentario: 'La sobrebarriga llegó tibia', productos: [{ id_producto: NumberInt(2), nombre: 'Sobrebarriga en salsa', calificacion: NumberInt(3) }, { id_producto: NumberInt(9), nombre: 'Jugo de lulo', calificacion: NumberInt(4) }] },
  { id_pedido: NumberInt(116), id_cliente: NumberInt(7), fecha: new Date(Date.now() - 4 * 86400000 - 34 * 60000), calificacion_servicio: NumberInt(5), comentario: 'Excelente almuerzo', productos: [{ id_producto: NumberInt(4), nombre: 'Almuerzo ejecutivo', calificacion: NumberInt(5) }, { id_producto: NumberInt(12), nombre: 'Ensalada de la casa', calificacion: NumberInt(4) }] },
  { id_pedido: NumberInt(118), id_cliente: NumberInt(13), fecha: new Date(Date.now() - 2 * 86400000 - 35 * 60000), calificacion_servicio: NumberInt(4), comentario: null, productos: [{ id_producto: NumberInt(1), nombre: 'Arroz con pollo', calificacion: NumberInt(4) }, { id_producto: NumberInt(9), nombre: 'Jugo de lulo', calificacion: NumberInt(5) }] },
  { id_pedido: NumberInt(121), id_cliente: NumberInt(14), fecha: new Date(Date.now() - 1 * 86400000 - 36 * 60000), calificacion_servicio: NumberInt(4), comentario: 'Todo bien', productos: [{ id_producto: NumberInt(1), nombre: 'Arroz con pollo', calificacion: NumberInt(5) }, { id_producto: NumberInt(12), nombre: 'Ensalada de la casa', calificacion: NumberInt(4) }, { id_producto: NumberInt(9), nombre: 'Jugo de lulo', calificacion: NumberInt(4) }] },
  { id_pedido: NumberInt(123), id_cliente: NumberInt(15), fecha: new Date(Date.now() - 0 * 86400000 - 37 * 60000), calificacion_servicio: NumberInt(2), comentario: 'Demoraron mucho en atender', productos: [{ id_producto: NumberInt(4), nombre: 'Almuerzo ejecutivo', calificacion: NumberInt(3) }, { id_producto: NumberInt(9), nombre: 'Jugo de lulo', calificacion: NumberInt(3) }] },
  { id_pedido: NumberInt(124), id_cliente: NumberInt(16), fecha: new Date(Date.now() - 0 * 86400000 - 38 * 60000), calificacion_servicio: NumberInt(5), comentario: 'Los brownies son los mejores', productos: [{ id_producto: NumberInt(8), nombre: 'Brownie', calificacion: NumberInt(5) }, { id_producto: NumberInt(10), nombre: 'Café tinto', calificacion: NumberInt(5) }] },
  { id_pedido: NumberInt(125), id_cliente: NumberInt(18), fecha: new Date(Date.now() - 60 * 60000), calificacion_servicio: NumberInt(5), comentario: 'Excelente atención y buen sabor', productos: [{ id_producto: NumberInt(4), nombre: 'Almuerzo ejecutivo', calificacion: NumberInt(5) }, { id_producto: NumberInt(9), nombre: 'Jugo de lulo', calificacion: NumberInt(4) }] }
])

// ===== BLOQUE 4: comprobar lo que quedó =====
db.calificaciones.countDocuments()
db.calificaciones.find({}, { _id: 0, id_pedido: 1, id_cliente: 1, calificacion_servicio: 1, comentario: 1 })

// ===== BLOQUE 5 (evidencia para el anexo): el validador rechaza un documento con nota 7 =====
// La respuesta esperada es un error "Document failed validation": la base protege los datos sola,
// igual que un CHECK en MySQL.
db.calificaciones.insertOne({ id_pedido: NumberInt(999), id_cliente: NumberInt(1), fecha: new Date(), calificacion_servicio: NumberInt(7), comentario: 'prueba', productos: [{ id_producto: NumberInt(4), nombre: 'Almuerzo ejecutivo', calificacion: NumberInt(5) }] })
