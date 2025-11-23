-- aca intentamos crear roles para usuarios de la app con permisos limitados
-- al admin le permitimos todo, al usuario le damos permisos mínimos necesarios

USE obligatorio_bdd;

-- Roles
-- un rol es un perfil de permisos
CREATE ROLE IF NOT EXISTS 'rol_app_user';
CREATE ROLE IF NOT EXISTS 'rol_app_admin';

-- Permisos del rol de usuario (mínimos)
-- select es para permisos de lectura
-- insert es para permisos de creación
-- usage es para permisos generales
-- update es para permisos de modificación

GRANT USAGE ON obligatorio_bdd.* TO 'rol_app_user';
-- ejemplo: doy permiso de SELECT sobre la tabla TURNO del schema obligatorio_bdd al rol rol_app_user.
GRANT SELECT ON obligatorio_bdd.turno TO 'rol_app_user';
GRANT SELECT ON obligatorio_bdd.sala TO 'rol_app_user';
GRANT SELECT ON obligatorio_bdd.reserva TO 'rol_app_user';
GRANT SELECT ON obligatorio_bdd.reserva_participante TO 'rol_app_user';
GRANT SELECT ON obligatorio_bdd.participante TO 'rol_app_user';
GRANT SELECT ON obligatorio_bdd.edificio TO 'rol_app_user';
GRANT SELECT ON obligatorio_bdd.sancion_participante TO 'rol_app_user';
GRANT SELECT ON obligatorio_bdd.programa_academico TO 'rol_app_user';
GRANT SELECT ON obligatorio_bdd.participante_programa_academico TO 'rol_app_user';
GRANT SELECT ON obligatorio_bdd.facultad TO 'rol_app_user';
GRANT SELECT, UPDATE ON obligatorio_bdd.login TO 'rol_app_user';
GRANT INSERT, UPDATE ON obligatorio_bdd.reserva TO 'rol_app_user';
GRANT INSERT, UPDATE ON obligatorio_bdd.reserva_participante TO 'rol_app_user';

-- Permisos del rol admin
GRANT SELECT, INSERT, UPDATE, DELETE ON obligatorio_bdd.* TO 'rol_app_admin';

-- USUARIOS (crear y asignar roles)
-- creo los usuarios de la base de datos y les asigno los roles correspondientes
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'app_user_password';
CREATE USER IF NOT EXISTS 'app_admin'@'%' IDENTIFIED BY 'app_admin_password';

-- doy los roles a los usuarios
GRANT 'rol_app_user' TO 'app_user'@'%';
GRANT 'rol_app_admin' TO 'app_admin'@'%';

-- doy el rol por defecto 
SET DEFAULT ROLE 'rol_app_user' TO 'app_user'@'%';
SET DEFAULT ROLE 'rol_app_admin' TO 'app_admin'@'%';

FLUSH PRIVILEGES;