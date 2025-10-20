create database reserva_salas_ucu_db;
use reserva_salas_ucu_db;

-- Primero creo el login ya que es independiente

create table login (
    correo VARCHAR(30),
    contraseña VARCHAR(30),
    PRIMARY KEY (correo)
);

-- Se organiza de mayor a menor tamaño de la organización/objeto
create table facultad (
    id_facultad INT AUTO_INCREMENT,
    nombre VARCHAR(50),
    PRIMARY KEY(id_facultad)
);

create table programa_academico (
    nombre_programa VARCHAR(50),
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
    PRIMARY KEY(ci)
);

create table participante_programa_academico (
    id_alumno_programa INT AUTO_INCREMENT,
    ci_participante INT,
    nombre_programa VARCHAR(50),
    rol ENUM('alumno', 'docente'),
    PRIMARY KEY (id_alumno_programa),
    FOREIGN KEY (ci_participante) REFERENCES participante(ci),
    FOREIGN KEY (nombre_programa) REFERENCES programa_academico(nombre_programa)
);

create table edificio (
    nombre_edificio VARCHAR(50),
    direccion VARCHAR(50),
    departamento VARCHAR(50),
    PRIMARY KEY (nombre_edificio)
);

create table sala (
    nombre_sala VARCHAR(50),
    edificio VARCHAR(50),
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
    edificio VARCHAR(50),
    fecha DATE NOT NULL,
    id_turno INT NOT NULL,
    estado ENUM('activa', 'cancelada', 'sin asistencia', 'finalizada'),
    PRIMARY KEY (id_reserva),
    FOREIGN KEY (nombre_sala) REFERENCES sala(nombre_sala),
    FOREIGN KEY (edificio) REFERENCES edificio(nombre_edificio),
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
    ci_participante INT,
    fecha_inicio DATE,
    fecha_fin DATE,
    PRIMARY KEY (ci_participante, fecha_inicio, fecha_fin),
    FOREIGN KEY (ci_participante) REFERENCES participante(ci)
)