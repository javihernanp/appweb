CREATE DATABASE tienda;
SET time_zone = "+00:00";
USE tienda;
CREATE TABLE `tienda`.`clientes` ( `id` INT(11) NOT NULL AUTO_INCREMENT , `nombre` VARCHAR(25) NOT NULL , `apellido` VARCHAR(25) NOT NULL , `dni` VARCHAR(9) NOT NULL , `direccion` VARCHAR(50) NOT NULL , `telefono` VARCHAR(12) NOT NULL , `email` VARCHAR(25) NOT NULL , `password` VARCHAR(25) NOT NULL , PRIMARY KEY (`email`), UNIQUE (`id`));
CREATE TABLE `tienda`.`productos` ( `id` INT(11) NOT NULL AUTO_INCREMENT , `nombre` VARCHAR(25) NOT NULL , `precio` INT(11) NOT NULL , `tipo` VARCHAR(25) NOT NULL , `descripcion` VARCHAR(100) NOT NULL , `cantidad` INT(11) NOT NULL , PRIMARY KEY (`nombre`), UNIQUE (`id`));
CREATE TABLE `tienda`.`pedidos` ( `id` INT(11) NOT NULL AUTO_INCREMENT, `emailcliente` VARCHAR(25) NOT NULL, `idproducto` INT(11) NOT NULL , `nombre_producto` VARCHAR(25) NOT NULL,`fechapedido` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (`id`),FOREIGN KEY (emailcliente) REFERENCES clientes (email) ON DELETE CASCADE ON UPDATE CASCADE, FOREIGN KEY (nombre_producto) REFERENCES productos (nombre) ON DELETE CASCADE ON UPDATE CASCADE);
CREATE VIEW monitor as select * from productos where tipo='monitor';
CREATE VIEW teclado as select * from productos where tipo='teclado';
CREATE VIEW raton as select * from productos where tipo='raton';
insert into clientes values (NULL,'admin','admin','12345678Z','admin','123456789','admin@correo.com','123456');


