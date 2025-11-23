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
    (78901234, 'Valentina', 'Lopez', 'valentina.lopez@ucu.edu.uy'),
    (11223344, 'Diego', 'Silva', 'diego.silva@ucu.edu.uy'),
    (22334455, 'Sofia', 'Ramirez', 'sofia.ramirez@ucu.edu.uy'),
    (33445566, 'Lucas', 'Mendez', 'lucas.mendez@ucu.edu.uy'),
    (44556677, 'Camila', 'Torres', 'camila.torres@ucu.edu.uy'),
    (55667788, 'Mateo', 'Vargas', 'mateo.vargas@ucu.edu.uy'),
    (66778899, 'Isabella', 'Castro', 'isabella.castro@ucu.edu.uy'),
    (77889900, 'Santiago', 'Morales', 'santiago.morales@ucu.edu.uy'),
    (88990011, 'Martina', 'Rojas', 'martina.rojas@ucu.edu.uy'),
    (99001122, 'Benjamin', 'Ortiz', 'benjamin.ortiz@ucu.edu.uy'),
    (10112233, 'Lucia', 'Herrera', 'lucia.herrera@ucu.edu.uy'),
    (21223344, 'Emiliano', 'Navarro', 'emiliano.navarro@ucu.edu.uy'),
    (32334455, 'Catalina', 'Suarez', 'catalina.suarez@ucu.edu.uy'),
    (43445566, 'Tomas', 'Ramos', 'tomas.ramos@ucu.edu.uy'),
    (54556677, 'Renata', 'Vega', 'renata.vega@ucu.edu.uy'),
    (65667788, 'Nicolas', 'Blanco', 'nicolas.blanco@ucu.edu.uy'),
    (76778899, 'Emma', 'Aguirre', 'emma.aguirre@ucu.edu.uy'),
    (87889900, 'Felipe', 'Mendoza', 'felipe.mendoza@ucu.edu.uy'),
    (98990011, 'Julia', 'Sosa', 'julia.sosa@ucu.edu.uy'),
    (10203040, 'Gabriel', 'Duarte', 'gabriel.duarte@ucu.edu.uy'),
    (20304050, 'Victoria', 'Acosta', 'victoria.acosta@ucu.edu.uy');

-- Login 
-- Contraseñas genéricas para pruebas (sin hashear):
--   - Usuario ADMIN: facundo.gonzales@ucu.edu.uy / contraseña: admin123
--   - Usuario NORMAL: ana.perez@ucu.edu.uy / contraseña: usuario123

-- Contraseñas hasheadas con SHA-256 (para el resto de usuarios):
-- pass1234 -> bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f
-- pass2345 -> 13bb2e1f5eab8fd7f85d0a71622888b03c6de50ca5b739250185fd875b8cdbe8
-- pass3456 -> 3943e10f0b6889b6ae1560c1e6ae99615ee68170f8cf24dde5ae59aed76ba2c2
-- pass4567 -> ced75643425df8422f6b947248904aad4b0a471da94c6618be2819b8fb455e77
-- pass5678 -> e8fa823a76f3aaf7068fd2068ba81d1fcb3b680bd854276ddc42d6139754240b
-- pass6789 -> 202681d5a66574ea64184a3083fb6bb4101f5d4c0f0afe35c8a5071bedb7a267
-- pass7890 -> 62ebdc70c80e642c82c9ed71670791a99309fbab6fe0be4850b34d0e5b054d49
INSERT INTO login (correo, contrasena, rol, ci_participante) VALUES
    ('facundo.gonzales@ucu.edu.uy', 'admin123', 'admin', 12345678),
    ('ana.perez@ucu.edu.uy', 'usuario123', 'usuario', 23456789),
    ('maria.gonzalez@ucu.edu.uy', '3943e10f0b6889b6ae1560c1e6ae99615ee68170f8cf24dde5ae59aed76ba2c2', 'usuario', 34567890),
    ('carlos.rodriguez@ucu.edu.uy', 'ced75643425df8422f6b947248904aad4b0a471da94c6618be2819b8fb455e77', 'usuario', 45678901),
    ('laura.martinez@ucu.edu.uy', 'e8fa823a76f3aaf7068fd2068ba81d1fcb3b680bd854276ddc42d6139754240b', 'usuario', 56789012),
    ('javier.fernandez@ucu.edu.uy', '202681d5a66574ea64184a3083fb6bb4101f5d4c0f0afe35c8a5071bedb7a267', 'usuario', 67890123),
    ('valentina.lopez@ucu.edu.uy', '62ebdc70c80e642c82c9ed71670791a99309fbab6fe0be4850b34d0e5b054d49', 'usuario', 78901234),
    ('diego.silva@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 11223344),
    ('sofia.ramirez@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 22334455),
    ('lucas.mendez@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 33445566),
    ('camila.torres@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 44556677),
    ('mateo.vargas@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 55667788),
    ('isabella.castro@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 66778899),
    ('santiago.morales@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 77889900),
    ('martina.rojas@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 88990011),
    ('benjamin.ortiz@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 99001122),
    ('lucia.herrera@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 10112233),
    ('emiliano.navarro@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 21223344),
    ('catalina.suarez@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 32334455),
    ('tomas.ramos@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 43445566),
    ('renata.vega@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 54556677),
    ('nicolas.blanco@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 65667788),
    ('emma.aguirre@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 76778899),
    ('felipe.mendoza@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 87889900),
    ('julia.sosa@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 98990011),
    ('gabriel.duarte@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 10203040),
    ('victoria.acosta@ucu.edu.uy', 'bd94dcda26fccb4e68d6a31f9b5aac0b571ae266d822620e901ef7ebe3a11d4f', 'usuario', 20304050);

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
('Sala E1', 'Edificio Madre Marta', '2025-10-28', 6, 'activa'),      -- turno 13:00–14:00
('Sala A1', 'Edificio Sacre Coeur', '2025-11-01', 1, 'finalizada'),  -- turno 08:00–09:00
('Sala A1', 'Edificio Sacre Coeur', '2025-11-01', 3, 'finalizada'),  -- turno 10:00–11:00
('Sala A2', 'Edificio Sacre Coeur', '2025-11-02', 5, 'activa'),      -- turno 12:00–13:00
('Sala B1', 'Edificio San Ignacio', '2025-11-02', 7, 'finalizada'),  -- turno 14:00–15:00
('Sala B2', 'Edificio San Ignacio', '2025-11-03', 2, 'cancelada'),   -- turno 09:00–10:00
('Sala C1', 'Edificio Semprun', '2025-11-04', 4, 'finalizada'),      -- turno 11:00–12:00
('Sala C2', 'Edificio Semprun', '2025-11-05', 6, 'activa'),          -- turno 13:00–14:00
('Sala D1', 'Edificio Mullin', '2025-11-06', 8, 'finalizada'),       -- turno 15:00–16:00
('Sala E1', 'Edificio Madre Marta', '2025-11-07', 1, 'activa'),      -- turno 08:00–09:00
('Sala A1', 'Edificio Sacre Coeur', '2025-11-08', 9, 'finalizada'),  -- turno 16:00–17:00
('Sala A2', 'Edificio Sacre Coeur', '2025-11-09', 3, 'cancelada'),   -- turno 10:00–11:00
('Sala B1', 'Edificio San Ignacio', '2025-11-10', 5, 'finalizada'),  -- turno 12:00–13:00
('Sala C1', 'Edificio Semprun', '2025-11-11', 7, 'activa'),          -- turno 14:00–15:00
('Sala D1', 'Edificio Mullin', '2025-11-12', 2, 'finalizada'),       -- turno 09:00–10:00
('Sala E1', 'Edificio Madre Marta', '2025-11-13', 4, 'activa'),      -- turno 11:00–12:00
('Sala A1', 'Edificio Sacre Coeur', '2025-11-14', 6, 'finalizada'),  -- turno 13:00–14:00
('Sala B2', 'Edificio San Ignacio', '2025-11-15', 8, 'activa'),      -- turno 15:00–16:00
('Sala C2', 'Edificio Semprun', '2025-11-16', 1, 'cancelada'),       -- turno 08:00–09:00
('Sala A2', 'Edificio Sacre Coeur', '2025-11-17', 10, 'finalizada'), -- turno 17:00–18:00
('Sala B1', 'Edificio San Ignacio', '2025-11-18', 3, 'activa'),      -- turno 10:00–11:00
('Sala C1', 'Edificio Semprun', '2025-11-19', 5, 'finalizada'),      -- turno 12:00–13:00
('Sala D1', 'Edificio Mullin', '2025-11-20', 7, 'activa'),           -- turno 14:00–15:00
('Sala E1', 'Edificio Madre Marta', '2025-11-21', 2, 'finalizada'),  -- turno 09:00–10:00
('Sala A1', 'Edificio Sacre Coeur', '2025-11-22', 4, 'activa'),      -- turno 11:00–12:00
('Sala A2', 'Edificio Sacre Coeur', '2025-11-23', 6, 'activa'),      -- turno 13:00–14:00
('Sala B1', 'Edificio San Ignacio', '2025-11-24', 8, 'activa'),      -- turno 15:00–16:00
('Sala C2', 'Edificio Semprun', '2025-11-25', 1, 'activa'),          -- turno 08:00–09:00
('Sala D1', 'Edificio Mullin', '2025-11-26', 3, 'activa'),           -- turno 10:00–11:00
('Sala E1', 'Edificio Madre Marta', '2025-11-27', 5, 'activa'),      -- turno 12:00–13:00
('Sala A1', 'Edificio Sacre Coeur', '2025-11-28', 7, 'activa'),      -- turno 14:00–15:00
('Sala B2', 'Edificio San Ignacio', '2025-11-29', 2, 'activa'),      -- turno 09:00–10:00
('Sala C1', 'Edificio Semprun', '2025-11-30', 4, 'activa'),          -- turno 11:00–12:00
('Sala A2', 'Edificio Sacre Coeur', '2025-12-01', 6, 'activa'),      -- turno 13:00–14:00
('Sala D1', 'Edificio Mullin', '2025-12-02', 8, 'activa');           -- turno 15:00–16:00

-- Reserva-Participantes
INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia) VALUES
(12345678, 1, '2025-10-20', 'presente'),   -- Facundo - Sala A1
(23456789, 2, '2025-10-21', 'presente'),  -- Ana - Sala A2
(34567890, 3, '2025-10-21', 'ausente'), -- María - Sala B1
(45678901, 4, '2025-10-22', 'presente'),  -- Carlos - Sala C1
(56789012, 5, '2025-10-23', 'ausente'), -- Laura - Sala D1
(67890123, 6, '2025-10-24', 'justificado'),  -- Javier - Sala E1
(11223344, 7, '2025-10-28', 'presente'),  -- Diego - Sala A1
(22334455, 8, '2025-10-29', 'presente'),  -- Sofia - Sala A1
(33445566, 9, '2025-10-30', 'presente'),  -- Lucas - Sala A2
(44556677, 10, '2025-10-31', 'presente'), -- Camila - Sala B1
(55667788, 11, '2025-11-01', 'ausente'),  -- Mateo - Sala B2
(66778899, 12, '2025-11-02', 'presente'), -- Isabella - Sala C1
(77889900, 13, '2025-11-03', 'presente'), -- Santiago - Sala C2
(88990011, 14, '2025-11-04', 'presente'), -- Martina - Sala D1
(99001122, 15, '2025-11-05', 'presente'), -- Benjamin - Sala E1
(10112233, 16, '2025-11-06', 'presente'), -- Lucia - Sala A1
(21223344, 17, '2025-11-07', 'ausente'),  -- Emiliano - Sala A2
(32334455, 18, '2025-11-08', 'presente'), -- Catalina - Sala B1
(43445566, 19, '2025-11-09', 'presente'), -- Tomas - Sala C1
(54556677, 20, '2025-11-10', 'presente'), -- Renata - Sala D1
(65667788, 21, '2025-11-11', 'presente'), -- Nicolas - Sala E1
(76778899, 22, '2025-11-12', 'presente'), -- Emma - Sala A1
(87889900, 23, '2025-11-13', 'presente'), -- Felipe - Sala B2
(98990011, 24, '2025-11-14', 'ausente'),  -- Julia - Sala C2
(10203040, 25, '2025-11-15', 'presente'), -- Gabriel - Sala A2
(20304050, 26, '2025-11-16', 'presente'), -- Victoria - Sala B1
(12345678, 27, '2025-11-17', 'presente'), -- Facundo - Sala C1
(23456789, 28, '2025-11-18', 'presente'), -- Ana - Sala D1
(34567890, 29, '2025-11-19', 'justificado'), -- María - Sala E1
(45678901, 30, '2025-11-20', 'presente'), -- Carlos - Sala A1
(56789012, 31, '2025-11-21', 'presente'), -- Laura - Sala A2
(67890123, 32, '2025-11-22', 'presente'), -- Javier - Sala B1
(11223344, 33, '2025-11-23', 'presente'), -- Diego - Sala C2
(22334455, 34, '2025-11-24', 'presente'), -- Sofia - Sala D1
(33445566, 35, '2025-11-25', 'presente'), -- Lucas - Sala E1
(44556677, 36, '2025-11-26', 'presente'), -- Camila - Sala A1
(55667788, 37, '2025-11-27', 'presente'), -- Mateo - Sala B2
(66778899, 38, '2025-11-28', 'presente'), -- Isabella - Sala C1
(77889900, 39, '2025-11-29', 'presente'), -- Santiago - Sala A2
(88990011, 40, '2025-11-30', 'presente'); -- Martina - Sala D1

-- Sanciones con respecto a las reservas anteriores
INSERT INTO sancion_participante (ci_participante, motivo, fecha_inicio, fecha_fin) VALUES
(56789012, 'Incumplimiento de normas del aula', '2025-10-22', '2025-12-22'),
(67890123, 'Llegadas tardias reiteradas', '2025-10-22', '2025-12-22'),
(34567890, 'Uso indebido de la sala reservada', '2025-10-23', '2025-12-23'),
(55667788, 'Ausencia sin justificacion', '2025-11-02', '2025-12-02'),
(21223344, 'No cancelacion de reserva', '2025-11-08', '2025-12-08'),
(98990011, 'Dano a equipamiento de la sala', '2025-11-15', '2026-01-15');

-- Participantes Programas Academicos
INSERT INTO participante_programa_academico (ci_participante, nombre_programa, rol) VALUES
(12345678, 'Ingenieria en Informatica', 'alumno'),
(23456789, 'Licenciatura en Direccion de Empresas', 'alumno'),
(34567890, 'Licenciatura en Comunicacion Social', 'alumno'),
(45678901, 'Licenciatura en Psicologia', 'alumno'),
(56789012, 'Licenciatura en Fonoaudiologia', 'alumno'),
(67890123, 'MBA - Maestria en Direccion de Empresas', 'docente'),
(78901234, 'Licenciatura en Nutricion', 'alumno'),
(11223344, 'Ingenieria en Informatica', 'alumno'),
(22334455, 'Licenciatura en Finanzas', 'alumno'),
(33445566, 'Ingenieria Electronica', 'alumno'),
(44556677, 'Licenciatura en Nutricion', 'alumno'),
(55667788, 'Ingenieria en Informatica', 'alumno'),
(66778899, 'Licenciatura en Psicologia', 'alumno'),
(77889900, 'Abogacia', 'alumno'),
(88990011, 'Licenciatura en Comunicacion Social', 'alumno'),
(99001122, 'Ingenieria Electronica', 'alumno'),
(10112233, 'Licenciatura en Direccion de Empresas', 'alumno'),
(21223344, 'Notariado', 'alumno'),
(32334455, 'Licenciatura en Fonoaudiologia', 'alumno'),
(43445566, 'Licenciatura en Finanzas', 'alumno'),
(54556677, 'Licenciatura en Psicologia', 'alumno'),
(65667788, 'Maestria en Gerencia de Tecnologia de la Informacion', 'docente'),
(76778899, 'Licenciatura en Comunicacion Social', 'alumno'),
(87889900, 'Ingenieria en Informatica', 'docente'),
(98990011, 'Abogacia', 'alumno'),
(10203040, 'Ingenieria Electronica', 'alumno'),
(20304050, 'Licenciatura en Nutricion', 'alumno');
