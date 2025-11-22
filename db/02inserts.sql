USE obligatorio_bdd;

-- FAcultades
INSERT INTO facultad (nombre) VALUES
    ('Ciencias Empresariales'),
    ('Ingenieria y Tecnologias'),
    ('Ciencias de la Salud'),
    ('Humanidades y Artes Liberales'),
    ('Derecho y Ciencias Sociales');

-- Programas Academicos
INSERT INTO programa_academico (nombre_programa, id_facultad, tipo) VALUES
    ('Licenciatura en Direccion de Empresas', 1, 'grado'),
    ('Licenciatura en Finanzas', 1, 'grado'),
    ('Ingenieria en Informatica', 2, 'grado'),
    ('Ingenieria Electronica', 2, 'grado'),
    ('Licenciatura en Nutricion', 3, 'grado'),
    ('Licenciatura en Fonoaudiologia', 3, 'grado'),
    ('Licenciatura en Psicologia', 4, 'grado'),
    ('Licenciatura en Comunicacion Social', 4, 'grado'),
    ('Abogacia', 5, 'grado'),
    ('Notariado', 5, 'grado'),
    ('MBA - Maestria en Direccion de Empresas', 1, 'posgrado'),
    ('Maestria en Gerencia de Tecnologia de la Informacion', 2, 'posgrado');

-- Edificios
INSERT INTO edificio (nombre_edificio, direccion, departamento) VALUES
    ('Edificio Sacre Coeur', 'Av. 8 de Octubre 2738', 'Montevideo'),
    ('Edificio San Ignacio', 'Cornelio Cantera 2733', 'Montevideo'),
    ('Edificio Semprun', 'Estero Bellaco 2771', 'Montevideo'),
    ('Edificio Mullin', 'Comandante Braga 2715', 'Montevideo'),
    ('Edificio Madre Marta', 'Av. Garibaldi 2831', 'Montevideo');

-- Salas
INSERT INTO sala (nombre_sala, edificio, capacidad, tipo_sala) VALUES
    ('Sala A1', 'Edificio Sacre Coeur', 30, 'libre'),
    ('Sala A2', 'Edificio Sacre Coeur', 25, 'docente'),
    ('Sala B1', 'Edificio San Ignacio', 20, 'libre'),
    ('Sala B2', 'Edificio San Ignacio', 15, 'posgrado'),
    ('Sala C1', 'Edificio Semprun', 40, 'libre'),
    ('Sala C2', 'Edificio Semprun', 30, 'docente'),
    ('Sala D1', 'Edificio Mullin', 10, 'posgrado'),
    ('Sala E1', 'Edificio Madre Marta', 35, 'libre');

-- Participantes
INSERT INTO participante (ci, nombre, apellido, email) VALUES
    (12345678, 'Facundo', 'Gonzales', 'facundo.gonzales@ucu.edu.uy'),
    (23456789, 'Ana', 'Perez', 'ana.perez@ucu.edu.uy'),
    (34567890, 'Maria', 'Gonzalez', 'maria.gonzalez@ucu.edu.uy'),
    (45678901, 'Carlos', 'Rodriguez', 'carlos.rodriguez@ucu.edu.uy'),
    (56789012, 'Laura', 'Martinez', 'laura.martinez@ucu.edu.uy'),
    (67890123, 'Javier', 'Fernandez', 'javier.fernandez@ucu.edu.uy'),
    (78901234, 'Valentina', 'Lopez', 'valentina.lopez@ucu.edu.uy');

-- Login (contraseñas hasheadas con SHA-256)
-- pass1234 -> bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f
-- pass2345 -> 13bb2e1f5eab8fd7f85d0a71622888b03c6de50ca5b739250185fd875b8cdbe8
-- pass3456 -> 3943e10f0b6889b6ae1560c1e6ae99615ee68170f8cf24dde5ae59aed76ba2c2
-- pass4567 -> ced75643425df8422f6b947248904aad4b0a471da94c6618be2819b8fb455e77
-- pass5678 -> e8fa823a76f3aaf7068fd2068ba81d1fcb3b680bd854276ddc42d6139754240b
-- pass6789 -> 202681d5a66574ea64184a3083fb6bb4101f5d4c0f0afe35c8a5071bedb7a267
-- pass7890 -> 62ebdc70c80e642c82c9ed71670791a99309fbab6fe0be4850b34d0e5b054d49
INSERT INTO login (correo, contrasena, rol, ci_participante) VALUES
    ('facundo.gonzales@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'admin', 12345678),
    ('ana.perez@ucu.edu.uy', '13bb2e1f5eab8fd7f85d0a71622888b03c6de50ca5b739250185fd875b8cdbe8', 'usuario', 23456789),
    ('maria.gonzalez@ucu.edu.uy', '3943e10f0b6889b6ae1560c1e6ae99615ee68170f8cf24dde5ae59aed76ba2c2', 'usuario', 34567890),
    ('carlos.rodriguez@ucu.edu.uy', 'ced75643425df8422f6b947248904aad4b0a471da94c6618be2819b8fb455e77', 'usuario', 45678901),
    ('laura.martinez@ucu.edu.uy', 'e8fa823a76f3aaf7068fd2068ba81d1fcb3b680bd854276ddc42d6139754240b', 'usuario', 56789012),
    ('javier.fernandez@ucu.edu.uy', '202681d5a66574ea64184a3083fb6bb4101f5d4c0f0afe35c8a5071bedb7a267', 'usuario', 67890123),
    ('valentina.lopez@ucu.edu.uy', '62ebdc70c80e642c82c9ed71670791a99309fbab6fe0be4850b34d0e5b054d49', 'usuario', 78901234);

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
INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado) VALUES
('Sala A1', 'Edificio Sacre Coeur', '2025-10-25', 1, 'activa'),      -- turno 08:00–09:00
('Sala A2', 'Edificio Sacre Coeur', '2025-10-25', 2, 'activa'),      -- turno 09:00–10:00
('Sala B1', 'Edificio San Ignacio', '2025-10-26', 3, 'finalizada'),  -- turno 10:00–11:00
('Sala C1', 'Edificio Semprun', '2025-10-26', 4, 'activa'),          -- turno 11:00–12:00
('Sala D1', 'Edificio Mullin', '2025-10-27', 5, 'cancelada'),        -- turno 12:00–13:00
('Sala E1', 'Edificio Madre Marta', '2025-10-28', 6, 'activa');      -- turno 13:00–14:00

-- Reserva-Participantes
INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia) VALUES
(12345678, 1, '2025-10-20', 'presente'),   -- Facundo - Sala A1
(23456789, 2, '2025-10-21', 'presente'),  -- Ana - Sala A2
(34567890, 3, '2025-10-21', 'ausente'), -- María - Sala B1
(45678901, 4, '2025-10-22', 'presente'),  -- Carlos - Sala C1
(56789012, 5, '2025-10-23', 'ausente'), -- Laura - Sala D1
(67890123, 6, '2025-10-24', 'justificado');  -- Javier - Sala E1

-- Sanciones con respecto a las reservas anteriores
INSERT INTO sancion_participante (ci_participante, motivo, fecha_inicio, fecha_fin) VALUES
(56789012, 'Incumplimiento de normas del aula', '2025-10-22', '2025-12-22'),
(67890123, 'Llegadas tardias reiteradas', '2025-10-22', '2025-12-22'),
(34567890, 'Uso indebido de la sala reservada', '2025-10-23', '2025-12-23');

-- Participantes Programas Academicos
INSERT INTO participante_programa_academico (ci_participante, nombre_programa, rol) VALUES
(12345678, 'Ingenieria en Informatica', 'alumno'),
(23456789, 'Licenciatura en Direccion de Empresas', 'alumno'),
(34567890, 'Licenciatura en Comunicacion Social', 'alumno'),
(45678901, 'Licenciatura en Psicologia', 'alumno'),
(56789012, 'Licenciatura en Fonoaudiologia', 'alumno'),
(67890123, 'MBA - Maestria en Direccion de Empresas', 'docente'),
(78901234, 'Licenciatura en Nutricion', 'alumno');
