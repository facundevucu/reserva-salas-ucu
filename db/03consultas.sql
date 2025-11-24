-- Salas más reservadas
select nombre_sala,
       COUNT(*) as total_reservas
from reserva
group by nombre_sala
order by total_reservas DESC;

-- TOP 3 Turnos más demandados
SELECT
  t.id_turno,
  t.hora_inicio,
  t.hora_fin,
  COUNT(r.id_reserva) AS total_reservas
FROM turno t
INNER JOIN reserva r
  ON t.id_turno = r.id_turno
GROUP BY t.id_turno, t.hora_inicio, t.hora_fin
ORDER BY total_reservas DESC
LIMIT 3;

-- Promedio de participantes por sala
select r.nombre_sala,
    COUNT(rp.ci_participante) / COUNT(DISTINCT r.id_reserva) as promedio_participantes
from reserva r
join reserva_participante rp on r.id_reserva = rp.id_reserva
group by r.nombre_sala;

-- Cantidad de reservas por carrera y facultad
-- Debo llegar desde "reserva_parcicipante.ci_participante" hasta "facultad"
select f.nombre as facultad, pa.nombre_programa as carrera,
       COUNT(DISTINCT rp.id_reserva) as total_reservas
from reserva_participante rp
join participante_programa_academico ppa on rp.ci_participante = ppa.ci_participante
join programa_academico pa on ppa.nombre_programa = pa.nombre_programa
join facultad f on pa.id_facultad = f.id_facultad
group by f.nombre, pa.nombre_programa
order by total_reservas DESC;

-- Porcentaje de ocupación de salas por edificio
-- Calculo la ocupación se las salas segun el edificio, distribuyendo el 100% de la ocupacion en los n edificios
select e.nombre_edificio,
       ROUND((COUNT(r.id_reserva) * 100) / (select COUNT(*) from reserva), 2) as porcentaje
from edificio e
join sala s on e.nombre_edificio = s.edificio
join reserva r on s.nombre_sala = r.nombre_sala
group by e.nombre_edificio
order by porcentaje DESC;

-- Cantidad de reservas y asistencias de profesores y alumnos (grado y posgrado)
-- Necesito llegar de reserva_participante.ci_ participante a participante_programa_academico.ci_participante
-- y de participante_programa_academico.nombre_programa a programa_academico.nombre_programa
select pa.tipo as tipo_programa,
       ppa.rol as rol_participante,
       COUNT(rp.id_reserva) as total_reservas,
       SUM(CASE WHEN rp.asistencia = 'true' THEN 1 ELSE 0 END) AS total_asistencias
from reserva_participante rp
join participante_programa_academico ppa on rp.ci_participante = ppa.ci_participante
join programa_academico pa on ppa.nombre_programa = pa.nombre_programa
group by pa.tipo, ppa.rol
order by pa.tipo, ppa.rol;

-- Cantidad de sanciones para profesores y alumnos (grado y posgrado)
select pa.tipo as tipo_programa,
       ppa.rol as rol_participante,
       COUNT(sp.ci_participante) as total_sanciones
from sancion_participante sp
join participante_programa_academico ppa on sp.ci_participante = ppa.ci_participante
join programa_academico pa on ppa.nombre_programa = pa.nombre_programa
group by pa.tipo, ppa.rol
order by pa.tipo, ppa.rol;

-- Porcentaje de reservas efectivamente utilizadas vs. canceladas/no asistidas
-- puedo usar case???!?=
select
    CASE
        WHEN estado IN ('activa', 'finalizada') then 'Utilizadas'
        WHEN estado IN ('cancelada', 'sin_asistencia') then 'No utilizadas'
    END AS estado_reserva,
    COUNT(*) as cantidad,
    ROUND((COUNT(*) * 100) / (select COUNT(*) FROM reserva), 2) as porcentaje
from reserva
group by estado_reserva;

-- Consultas adicionales

-- Horarios fantasma: salas que nunca se reservan en ciertos turnos
SELECT 
    s.nombre_sala,
    t.hora_inicio,
    t.hora_fin,
    e.nombre_edificio,
    s.capacidad
FROM sala s
CROSS JOIN turno t
JOIN edificio e ON s.edificio = e.nombre_edificio
WHERE NOT EXISTS (
    SELECT 1 
    FROM reserva r 
    WHERE r.nombre_sala = s.nombre_sala 
    AND r.id_turno = t.id_turno
)
ORDER BY s.nombre_sala, t.hora_inicio;

-- Sala camaleon, sala con mayor diversidad de facultades que la usan
SELECT 
    r.nombre_sala,
    COUNT(DISTINCT f.id_facultad) as cantidad_facultades_diferentes,
    GROUP_CONCAT(DISTINCT f.nombre ORDER BY f.nombre SEPARATOR ', ') as facultades_que_la_usan,
    COUNT(DISTINCT r.id_reserva) as total_reservas
FROM reserva r
JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
JOIN participante_programa_academico ppa ON rp.ci_participante = ppa.ci_participante
JOIN programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
JOIN facultad f ON pa.id_facultad = f.id_facultad
GROUP BY r.nombre_sala
HAVING COUNT(DISTINCT f.id_facultad) > 1
ORDER BY cantidad_facultades_diferentes DESC;

-- Patrones de uso por franja horaria
SELECT 
    CASE 
        WHEN t.hora_inicio < '09:00' THEN 'Madrugadores (antes 9am)'
        WHEN t.hora_inicio < '13:00' THEN 'Mañana (9am-1pm)'
        WHEN t.hora_inicio < '17:00' THEN 'Tarde (1pm-5pm)'
        ELSE 'Noche (después 5pm)'
    END AS franja_horaria,
    pa.tipo as tipo_programa,
    ppa.rol as rol,
    COUNT(r.id_reserva) as cantidad_reservas
FROM reserva r
JOIN turno t ON r.id_turno = t.id_turno
JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
JOIN participante_programa_academico ppa ON rp.ci_participante = ppa.ci_participante
JOIN programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
GROUP BY franja_horaria, pa.tipo, ppa.rol
ORDER BY 
    MIN(t.hora_inicio),
    pa.tipo, 
    ppa.rol;

-- ===============================================
-- CONSULTAS ADICIONALES AVANZADAS
-- ===============================================
-- Marcos consulto si podiamos agregar mas consultas y nos dijeron que si

-- Demanda de salas en períodos de examen vs. período lectivo
SELECT CASE
         WHEN MONTH(r.fecha) IN (2, 7, 11) THEN 'Examen'
         ELSE 'Lectivo'
       END AS periodo,
       COUNT(*) AS total_reservas,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reserva), 2) AS porcentaje
FROM reserva r
GROUP BY periodo
ORDER BY total_reservas DESC;



-- Tiempo promedio de antelación de las reservas
SELECT ROUND(AVG(DATEDIFF(r.fecha, rp.fecha_solicitud_reserva)), 2) AS dias_promedio_anticipacion,
       ROUND(AVG(TIMESTAMPDIFF(HOUR, rp.fecha_solicitud_reserva, r.fecha)), 2) AS horas_promedio_anticipacion
FROM reserva_participante rp
JOIN reserva r ON rp.id_reserva = r.id_reserva
WHERE rp.fecha_solicitud_reserva IS NOT NULL;

-- Distribución semanal de uso por edificio
SELECT r.edificio,
       DAYNAME(r.fecha) AS dia_semana,
       COUNT(*) AS total_reservas,
       ROUND(AVG(s.capacidad), 0) AS capacidad_promedio_salas
FROM reserva r
JOIN sala s ON r.nombre_sala = s.nombre_sala
GROUP BY r.edificio, dia_semana
ORDER BY r.edificio, total_reservas DESC;

-- Alumnos sancionados
SELECT p.ci,
       CONCAT(p.nombre, ' ', p.apellido) AS participante,
       pa.nombre_programa,
       s.estado,
       s.motivo,
       s.fecha_inicio,
       s.fecha_fin,
       DATEDIFF(IFNULL(s.fecha_fin, CURDATE()), s.fecha_inicio) AS dias_sancion
FROM sancion_participante s
JOIN participante p ON s.ci_participante = p.ci
LEFT JOIN participante_programa_academico ppa ON ppa.ci_participante = p.ci
LEFT JOIN programa_academico pa ON pa.nombre_programa = ppa.nombre_programa
ORDER BY s.estado DESC, s.fecha_inicio DESC;

-- Usuarios con mayor reincidencia en sanciones
SELECT p.ci,
       CONCAT(p.nombre, ' ', p.apellido) AS participante,
       COUNT(s.id_sancion) AS total_sanciones,
       SUM(CASE WHEN s.estado = 'activa' THEN 1 ELSE 0 END) AS sanciones_activas,
       MAX(s.fecha_inicio) AS ultima_sancion
FROM sancion_participante s
JOIN participante p ON s.ci_participante = p.ci
GROUP BY p.ci, participante
HAVING total_sanciones > 0
ORDER BY total_sanciones DESC, sanciones_activas DESC;