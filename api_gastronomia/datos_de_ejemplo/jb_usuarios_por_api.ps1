# CREAR LOS USUARIOS DE EJEMPLO POR MEDIO DE LA API (PASO 2 de jb_datos_ejemplo_mysql.sql)
# Los usuarios y sus contraseñas están en texto plano en jb_usuarios_ejemplo.json.
# Cada usuario se envía a POST /api/v1/usuarios: la API revisa la contraseña, la cifra con bcrypt
# y guarda solo el hash (RN06). La respuesta nunca trae la contraseña.
#
# Antes de empezar:
#   1. Ya pegó en MySQL los bloques 0 y 1 de jb_datos_ejemplo_mysql.sql (crean el ADMIN que inicia sesión).
#   2. La API está encendida en otra terminal: uvicorn app.jb_main:jb_app --reload
#   3. Abra una terminal de PowerShell en la carpeta api_gastronomia, copie cada paso y péguelo en orden.

# PASO 2.1: dirección base de la API
$jbApi = "http://localhost:8000/api/v1"

# PASO 2.2: iniciar sesión como ADMIN (la contraseña viaja en texto plano y la API la compara con el hash)
$jbLogin = Invoke-RestMethod -Method Post -Uri "$jbApi/auth/login" -ContentType "application/json; charset=utf-8" -Body '{"correo": "burbano@gastronomia.com", "password": "Admin123*"}'
# Encabezado Authorization: Bearer <token> que llevan las demás peticiones
$jbEncabezados = @{ Authorization = "Bearer $($jbLogin.access_token)" }

# PASO 2.3: leer los usuarios del archivo JSON (texto plano) y enviarlos uno por uno
$jbUsuarios = Get-Content -Raw -Encoding UTF8 "datos_de_ejemplo\jb_usuarios_ejemplo.json" | ConvertFrom-Json
# Recorre cada usuario del archivo
foreach ($jbUsuario in $jbUsuarios) {
  # Lo convierte en JSON y lo envía; la API cifra la contraseña y responde el usuario sin ella
  $jbCreado = Invoke-RestMethod -Method Post -Uri "$jbApi/usuarios" -Headers $jbEncabezados -ContentType "application/json; charset=utf-8" -Body ($jbUsuario | ConvertTo-Json)
  # Muestra el id, el correo y el rol del usuario creado
  "Creado: id $($jbCreado.id_usuario) - $($jbCreado.correo) - $($jbCreado.rol)"
}

# PASO 2.4 (opcional): dejar INACTIVO a un usuario con PUT, para probar que un usuario INACTIVO
# no puede iniciar sesión. Los datos salen del archivo JSON; de la API solo se toma el id.
# Datos de Sandra tomados del archivo JSON
$jbSandra = $jbUsuarios | Where-Object { $_.correo -eq "sandra.castro@gastronomia.com" }
# Id de Sandra, tomado de la lista de usuarios de la API. Los paréntesis alrededor de Invoke-RestMethod
# hacen que PowerShell recorra la lista usuario por usuario (sin ellos, Where-Object recibe la lista entera)
$jbIdSandra = ((Invoke-RestMethod -Uri "$jbApi/usuarios" -Headers $jbEncabezados) | Where-Object { $_.correo -eq $jbSandra.correo }).id_usuario
# Cuerpo del PUT: los mismos datos con estado INACTIVO (sin password: se conserva la que tiene)
$jbCuerpo = @{ identificacion = $jbSandra.identificacion; nombres = $jbSandra.nombres; apellidos = $jbSandra.apellidos; correo = $jbSandra.correo; rol = $jbSandra.rol; estado = "INACTIVO" } | ConvertTo-Json
# Envía el PUT y muestra el estado que quedó
(Invoke-RestMethod -Method Put -Uri "$jbApi/usuarios/$jbIdSandra" -Headers $jbEncabezados -ContentType "application/json; charset=utf-8" -Body $jbCuerpo).estado

# Listo: vuelva a la terminal de MySQL y siga con el PASO 3 (bloques 2 al 13).
