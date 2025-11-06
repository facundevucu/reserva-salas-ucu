Sistema de Gestión de Reserva de Salas de Estudio – UCU
Descripción del Proyecto
Este proyecto implementa un sistema de información para la gestión de salas de estudio de la Universidad Católica del Uruguay. Su objetivo principal es reemplazar el método manual de registro (actualmente realizado en planillas de papel) por una aplicación centralizada que permita la reserva, el control de asistencia y la generación de reportes para la gestión académica y la toma de decisiones.
El sistema está diseñado para facilitar las tareas de los funcionarios administrativos, docentes y estudiantes, asegurando un uso equitativo y trazable de las salas en todos los edificios de la universidad.
Funcionalidades Principales
Gestión de participantes: alta, baja y modificación de estudiantes y docentes.
Gestión de salas: registro de salas con información de edificio, capacidad y tipo (libre, posgrado o docente).
Gestión de reservas: creación, modificación y cancelación de reservas, respetando las restricciones definidas (bloques horarios, límite de horas por día y número máximo de reservas semanales).
Control de asistencia: registro de asistencia por participante y aplicación automática de sanciones por inasistencia.
Reportes y consultas: generación de métricas para el área de BI, incluyendo:
Salas más reservadas y turnos más demandados.
Promedio de participantes por sala y ocupación por edificio.
Cantidad de reservas, asistencias y sanciones por tipo de usuario.
Consultas adicionales definidas por el equipo de desarrollo.
Tecnologías Utilizadas
Backend: Python (sin ORM, con MySQL Connector)
Base de datos: MySQL
Frontend: framework libre (en desarrollo / según versión del proyecto)
Control de versiones: Git y GitHub
Contenedorización: Docker y Docker Compose
Estado Actual del Proyecto
El proyecto cuenta con:
Modelo relacional diseñado y validado.
Scripts SQL completos para creación y carga de datos maestros.
Módulos de backend implementados para operaciones CRUD, validaciones y manejo de errores.
Registro de acciones mediante un módulo de logs, para trazabilidad y depuración.
Documentación básica e instructivo de ejecución local.
Próximos pasos:
Integrar la interfaz web para interacción con el usuario.
Mejorar la gestión de reportes con visualizaciones dinámicas.
Implementar autenticación y control de roles.
Optimizar la estructura Docker y agregar pruebas automatizadas.