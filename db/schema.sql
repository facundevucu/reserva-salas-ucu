create database if not exists reserva_salas_ucu_db;
use reserva_salas_ucu_db;
-- Primero creo el login ya que es independiente

create table login (
    correo VARCHAR(100) PRIMARY KEY,
    contraseña VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'usuario') NOT NULL DEFAULT 'usuario',
    ci_participante INT,
    debe_cambiar_contraseña BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (ci_participante) REFERENCES participante(ci) ON DELETE CASCADE
);

-- Se organiza de mayor a menor tamaño de la organización/objeto
create table facultad (
    id_facultad INT AUTO_INCREMENT,
    nombre VARCHAR(100),
    PRIMARY KEY(id_facultad)
);

create table programa_academico (
    nombre_programa VARCHAR(100),
    id_facultad INT NOT NULL,
    tipo ENUM('grado', 'posgrado') NOT NULL,
    FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad),
    PRIMARY KEY(nombre_programa)
);

create table participante (
    ci INT,
    nombre VARCHAR(20),
    apellido VARCHAR(20),
    email VARCHAR(30),
    estado ENUM('activo', 'inactivo') DEFAULT 'activo',
    PRIMARY KEY(ci)
);

create table participante_programa_academico (
    id_alumno_programa INT AUTO_INCREMENT,
    ci_participante INT,
    nombre_programa VARCHAR(100),
    rol ENUM('alumno', 'docente'),
    PRIMARY KEY (id_alumno_programa),
    FOREIGN KEY (ci_participante) REFERENCES participante(ci),
    FOREIGN KEY (nombre_programa) REFERENCES programa_academico(nombre_programa)
);

create table edificio (
    nombre_edificio VARCHAR(100),
    direccion VARCHAR(100),
    departamento VARCHAR(100),
    PRIMARY KEY (nombre_edificio)
);

create table sala (
    nombre_sala VARCHAR(50),
    edificio VARCHAR(100),
    capacidad INT,
    tipo_sala ENUM('libre', 'posgrado', 'docente'),
    PRIMARY KEY (nombre_sala, edificio),
    FOREIGN KEY (edificio) REFERENCES edificio(nombre_edificio)
);

create table turno (
    id_turno INT AUTO_INCREMENT,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    PRIMARY KEY (id_turno)
);

create table reserva (
    id_reserva INT AUTO_INCREMENT,
    nombre_sala VARCHAR(50),
    edificio VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    id_turno INT NOT NULL,
    estado ENUM('activa', 'cancelada', 'sin_asistencia', 'finalizada'),
    PRIMARY KEY (id_reserva),
    FOREIGN KEY (nombre_sala, edificio) REFERENCES sala(nombre_sala, edificio),
    FOREIGN KEY (id_turno) REFERENCES turno(id_turno)
);

create table reserva_participante (
    ci_participante INT,
    id_reserva INT NOT NULL,
    fecha_solicitud_reserva DATE,
    asistencia ENUM('true', 'false'),
    PRIMARY KEY (ci_participante, id_reserva),
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

create table sancion_participante (
    id_sancion INT AUTO_INCREMENT not null,
    ci_participante INT not null,
    motivo VARCHAR(200),
    estado ENUM('activa', 'inactiva', 'anulada') DEFAULT 'activa',
    fecha_inicio DATE,
    fecha_fin DATE,
    PRIMARY KEY (id_sancion),
    FOREIGN KEY (ci_participante) REFERENCES participante(ci)
);

CREATE TABLE IF NOT EXISTS log_acciones (
    id_log INT AUTO_INCREMENT,
    ci_participante INT NULL,
    accion VARCHAR(200),
    estado VARCHAR(50),
    fecha_hora TIMESTAMP DEFAULT NOW(),
    detalle VARCHAR(100),
    PRIMARY KEY (id_log)
    -- no le hago FK de ci
)
-- log de acciones