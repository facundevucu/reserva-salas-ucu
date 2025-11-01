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