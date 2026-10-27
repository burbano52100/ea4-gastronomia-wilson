-- Script 03 (DCL): crea el usuario con el que la API se conecta a MySQL, con privilegios mínimos.
-- Se ejecuta como root, después de los scripts 01 y 02.
-- La API NUNCA se conecta con root: si alguien roba estas credenciales, solo puede tocar los datos
-- de bd_gastronomia; no puede crear ni borrar tablas, ni ver otras bases, ni crear usuarios.

-- Borra el usuario si ya existe, para poder ejecutar el script varias veces
DROP USER IF EXISTS 'jb_api_gastronomia'@'%';

-- Crea el usuario. '%' permite conectarse desde cualquier equipo: con Docker la API llega desde fuera del contenedor.
-- CONTRASEÑA DE DESARROLLO: debe ser la misma de MYSQL_PASSWORD en el archivo .env.
-- En un servidor real se cambia aquí y en el .env.
CREATE USER 'jb_api_gastronomia'@'%' IDENTIFIED BY 'JbApiGastro_2026';

-- Solo puede consultar, insertar, actualizar y eliminar filas de las tablas de bd_gastronomia
GRANT SELECT, INSERT, UPDATE, DELETE ON bd_gastronomia.* TO 'jb_api_gastronomia'@'%';

-- Muestra los permisos que quedaron (evidencia para el anexo)
SHOW GRANTS FOR 'jb_api_gastronomia'@'%';
