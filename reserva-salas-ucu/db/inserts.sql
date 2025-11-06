USE reserva_salas_ucu_db;

-- FAcultades
INSERT INTO facultad (nombre) VALUES
    ('Ciencias Empresariales'),
    ('Ingeniería y Tecnologías'),
    ('Ciencias de la Salud'),
    ('Humanidades y Artes Liberales'),
    ('Derecho y Ciencias Sociales');

-- Programas Academicos
INSERT INTO programa_academico (nombre_programa, id_facultad, tipo) VALUES
    ('Licenciatura en Dirección de Empresas', 1, 'grado'),
    ('Licenciatura en Finanzas', 1, 'grado'),
    ('Ingeniería en Informática', 2, 'grado'),
    ('Ingeniería Electrónica', 2, 'grado'),
    ('Licenciatura en Nutrición', 3, 'grado'),
    ('Licenciatura en Fonoaudiología', 3, 'grado'),
    ('Licenciatura en Psicología', 4, 'grado'),
    ('Licenciatura en Comunicación Social', 4, 'grado'),
    ('Abogacía', 5, 'grado'),
    ('Notariado', 5, 'grado'),
    ('MBA - Maestría en Dirección de Empresas', 1, 'posgrado'),
    ('Maestría en Gerencia de Tecnología de la Información', 2, 'posgrado');

-- Edificios
INSERT INTO edificio (nombre_edificio, direccion, departamento) VALUES
    ('Edificio Sacré Coeur', 'Av. 8 de Octubre 2738', 'Montevideo'),
    ('Edificio San Ignacio', 'Cornelio Cantera 2733', 'Montevideo'),
    ('Edificio Semprún', 'Estero Bellaco 2771', 'Montevideo'),
    ('Edificio Mullin', 'Comandante Braga 2715', 'Montevideo'),
    ('Edificio Madre Marta', 'Av. Garibaldi 2831', 'Montevideo');

-- Salas
INSERT INTO sala (nombre_sala, edificio, capacidad, tipo_sala) VALUES
    ('Sala A1', 'Edificio Sacré Coeur', 30, 'libre'),
    ('Sala A2', 'Edificio Sacré Coeur', 25, 'docente'),
    ('Sala B1', 'Edificio San Ignacio', 20, 'libre'),
    ('Sala B2', 'Edificio San Ignacio', 15, 'posgrado'),
    ('Sala C1', 'Edificio Semprún', 40, 'libre'),
    ('Sala C2', 'Edificio Semprún', 30, 'docente'),
    ('Sala D1', 'Edificio Mullin', 10, 'posgrado'),
    ('Sala E1', 'Edificio Madre Marta', 35, 'libre');

-- Participantes
INSERT INTO participante (ci, nombre, apellido, email) VALUES
    (12345678, 'Facundo', 'Gonzales', 'facundo.gonzales@ucu.edu.uy'),
    (23456789, 'Ana', 'Pérez', 'ana.perez@ucu.edu.uy'),
    (34567890, 'María', 'González', 'maria.gonzalez@ucu.edu.uy'),
    (45678901, 'Carlos', 'Rodríguez', 'carlos.rodriguez@ucu.edu.uy'),
    (56789012, 'Laura', 'Martínez', 'laura.martinez@ucu.edu.uy'),
    (67890123, 'Javier', 'Fernández', 'javier.fernandez@ucu.edu.uy'),
    (78901234, 'Valentina', 'López', 'valentina.lopez@ucu.edu.uy');

-- Login
INSERT INTO login (correo, contraseña) VALUES
    ('facundo.gonzales@ucu.edu.uy', 'pass1234'),
    ('ana.perez@ucu.edu.uy', 'pass2345'),
    ('maria.gonzalez@ucu.edu.uy', 'pass3456'),
    ('carlos.rodriguez@ucu.edu.uy', 'pass4567'),
    ('laura.martinez@ucu.edu.uy', 'pass5678'),
    ('javier.fernandez@ucu.edu.uy', 'pass6789'),
    ('valentina.lopez@ucu.edu.uy', 'pass7890');

-- Turnos
INSERT INTO turno (hora_inicio, hora_fin) VALUES
    ('08:00:00', '09:00:00'),
    ('09:00:00', '10:00:00'),
    ('10:00:00', '11:00:00'),
    ('11:00:00', '12:00:00'),
    ('12:00:00', '13:00:00'),
    ('13:00:00', '14:00:00'),
    ('14:00:00', '15:00:00'),
    ('15:00:00', '16:00:00'),
    ('16:00:00', '17:00:00'),
    ('17:00:00', '18:00:00'),
    ('18:00:00', '19:00:00'),
    ('19:00:00', '20:00:00'),
    ('20:00:00', '21:00:00'),
    ('21:00:00', '22:00:00'),
    ('22:00:00', '23:00:00');

-- REservas
INSERT INTO reserva (nombre_sala, fecha, id_turno, estado) VALUES
    ('Sala A1', '2025-08-20', 1, 'activa'),
    ('Sala A2', '2025-08-20', 2, 'activa'),
    ('Sala B1', '2025-08-21', 3, 'cancelada'),
    ('Sala B2', '2025-09-21', 4, 'sin_asistencia'),
    ('Sala C1', '2025-09-22', 5, 'finalizada'),
    ('Sala C2', '2025-09-22', 6, 'activa'),
    ('Sala D1', '2025-09-23', 7, 'activa'),
    ('Sala E1', '2025-09-23', 8, 'activa'),
    ('Sala A1', '2025-09-24', 9, 'finalizada'),
    ('Sala A2', '2025-10-24', 10, 'activa'),
    ('Sala B1', '2025-10-25', 11, 'sin_asistencia'),
    ('Sala B2', '2025-10-25', 12, 'activa'),
    ('Sala C1', '2025-10-26', 13, 'finalizada'),
    ('Sala C2', '2025-10-26', 14, 'activa'),
    ('Sala D1', '2025-10-27', 15, 'cancelada');

-- Reserva-Participantes
INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia) VALUES
    (12345678, 1, '2025-10-15', 'true'),
    (34567890, 2, '2025-10-18', 'true'),
    (56789012, 3, '2025-10-19', 'false'),
    (67890123, 4, '2025-10-19', 'false'),
    (78901234, 5, '2025-10-19', 'true'),
    (12345678, 6, '2025-10-20', 'true'),
    (23456789, 7, '2025-10-20', 'true'),
    (34567890, 8, '2025-10-20', 'true'),
    (45678901, 9, '2025-10-21', 'true'),
    (56789012, 10, '2025-10-21', 'true'),
    (67890123, 11, '2025-10-21', 'false'),
    (78901234, 12, '2025-10-21', 'true'),
    (12345670, 13, '2025-10-21', 'true');

-- Sanciones con respecto a las reservas anteriores
INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin) VALUES
(56789012, '2025-10-22', '2025-12-22'),
(67890123, '2025-10-22', '2025-12-22'),
(34567890, '2025-10-23', '2025-12-23');

-- Participantes Programas Academicos
INSERT INTO participante_programa_academico (ci_participante, nombre_programa, rol) VALUES
(12345678, 'Ingeniería en Informática', 'alumno'),
(23456789, 'Licenciatura en Dirección de Empresas', 'alumno'),
(34567890, 'Licenciatura en Comunicación Social', 'alumno'),
(45678901, 'Licenciatura en Psicología', 'alumno'),
(56789012, 'Licenciatura en Fonoaudiología', 'alumno'),
(67890123, 'MBA - Maestría en Dirección de Empresas', 'docente'),
(78901234, 'Licenciatura en Nutrición', 'alumno');
