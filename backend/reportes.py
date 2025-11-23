from db_connection import get_db_connection, close_connection

def ejecutar_consulta(sql):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    resultados = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    cursor.close()
    close_connection(conn)
    return columnas, resultados


def mostrar_resultados(nombre_reporte, columnas, resultados):
    print(f"\n {nombre_reporte}")
    if not resultados:
        print("Sin resultados.")
        return
    print(" | ".join(columnas))
    for fila in resultados:
        print(" | ".join(str(x) for x in fila))

# Ahora escribo funciones específicas para cada reporte, los cuales estan en db/consultas.sql
def salas_mas_reservadas():
    sql = """
        SELECT r.nombre_sala, s.edificio, COUNT(*) AS total_reservas
        FROM reserva r
        JOIN sala s ON r.nombre_sala = s.nombre_sala
        GROUP BY r.nombre_sala, s.edificio
        ORDER BY total_reservas DESC;
    """
    cols, rows = ejecutar_consulta(sql)

    # Armo el nombre completo en Python (nombre_sala + edificio)
    filas_formateadas = []
    for fila in rows:
        nombre_sala = f"{fila[0]} ({fila[1]})"
        total_reservas = fila[2]
        filas_formateadas.append((nombre_sala, total_reservas))

    columnas = ["nombre_sala", "total_reservas"]

    mostrar_resultados("Salas más reservadas", columnas, filas_formateadas)
    return columnas, filas_formateadas

def turnos_mas_demandados():
    sql = """
        SELECT t.id_turno, t.hora_inicio, t.hora_fin,
               COUNT(r.id_reserva) AS total_reservas
        FROM turno t
        JOIN reserva r ON t.id_turno = r.id_turno
        GROUP BY t.id_turno, t.hora_inicio, t.hora_fin
        ORDER BY total_reservas DESC;
    """
    cols, rows = ejecutar_consulta(sql)
    rows = convertir_tiempos(rows)  #  convierto las horas a texto
    mostrar_resultados("Turnos más demandados", cols, rows)
    return cols, rows

def promedio_participantes_por_sala():
    sql = """
        SELECT r.nombre_sala, s.edificio,
               COUNT(rp.ci_participante) / COUNT(DISTINCT r.id_reserva) AS promedio_participantes
        FROM reserva r
        JOIN sala s ON r.nombre_sala = s.nombre_sala
        JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
        WHERE r.nombre_sala != 'cancelada'
        GROUP BY r.nombre_sala, s.edificio;
    """
    cols, rows = ejecutar_consulta(sql)

    filas_formateadas = []
    for fila in rows:
        nombre_sala = f"{fila[0]} ({fila[1]})"
        promedio_participantes = fila[2]
        filas_formateadas.append((nombre_sala, promedio_participantes))

    columnas = ["nombre_sala", "promedio_participantes"]

    mostrar_resultados("Promedio de participantes por sala", columnas, filas_formateadas)
    return columnas, filas_formateadas

def reservas_por_carrera_y_facultad():
    sql = """
        SELECT f.nombre AS facultad, pa.nombre_programa AS carrera,
               COUNT(DISTINCT rp.id_reserva) AS total_reservas
        FROM reserva_participante rp
        JOIN participante_programa_academico ppa ON rp.ci_participante = ppa.ci_participante
        JOIN programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
        JOIN facultad f ON pa.id_facultad = f.id_facultad
        GROUP BY f.nombre, pa.nombre_programa
        ORDER BY total_reservas DESC;
    """
    cols, rows = ejecutar_consulta(sql)
    mostrar_resultados("Reservas por carrera y facultad", cols, rows)
    return cols, rows

def porcentaje_ocupacion_por_edificio():
    sql = """
        SELECT e.nombre_edificio,
               ROUND((COUNT(r.id_reserva) * 100) / (SELECT COUNT(*) FROM reserva), 2) AS porcentaje
        FROM edificio e
        JOIN sala s ON e.nombre_edificio = s.edificio
        JOIN reserva r ON s.nombre_sala = r.nombre_sala
        GROUP BY e.nombre_edificio
        ORDER BY porcentaje DESC;
    """
    cols, rows = ejecutar_consulta(sql)
    mostrar_resultados("Porcentaje de ocupación por edificio", cols, rows)
    return cols, rows

def reservas_y_asistencias_por_tipo_y_rol():
    sql = """
        SELECT pa.tipo AS tipo_programa,
               ppa.rol AS rol_participante,
               COUNT(rp.id_reserva) AS total_reservas,
               SUM(CASE WHEN rp.asistencia = 'true' THEN 1 ELSE 0 END) AS total_asistencias
        FROM reserva_participante rp
        JOIN participante_programa_academico ppa ON rp.ci_participante = ppa.ci_participante
        JOIN programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
        GROUP BY pa.tipo, ppa.rol
        ORDER BY pa.tipo, ppa.rol;
    """
    cols, rows = ejecutar_consulta(sql)
    mostrar_resultados("Reservas y asistencias por tipo y rol", cols, rows)
    return cols, rows

def sanciones_por_tipo_y_rol():
    sql = """
        SELECT pa.tipo AS tipo_programa,
               ppa.rol AS rol_participante,
               COUNT(sp.ci_participante) AS total_sanciones
        FROM sancion_participante sp
        JOIN participante_programa_academico ppa ON sp.ci_participante = ppa.ci_participante
        JOIN programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
        GROUP BY pa.tipo, ppa.rol
        ORDER BY pa.tipo, ppa.rol;
    """
    cols, rows = ejecutar_consulta(sql)
    mostrar_resultados("Sanciones por tipo y rol", cols, rows)
    return cols, rows

def porcentaje_reservas_utilizadas():
    sql = """
        SELECT
            CASE
                WHEN estado IN ('activa', 'finalizada') THEN 'Utilizadas'
                WHEN estado IN ('cancelada', 'sin_asistencia') THEN 'No utilizadas'
            END AS estado_reserva,
            COUNT(*) AS cantidad,
            ROUND((COUNT(*) * 100) / (SELECT COUNT(*) FROM reserva), 2) AS porcentaje
        FROM reserva
        GROUP BY estado_reserva;
    """
    cols, rows = ejecutar_consulta(sql)
    mostrar_resultados("Porcentaje de reservas utilizadas vs no utilizadas", cols, rows)
    return cols, rows

def horarios_fantasma():
    sql = """
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
    """
    cols, rows = ejecutar_consulta(sql)
    rows = convertir_tiempos(rows)
    mostrar_resultados(" Horarios Fantasma - Salas nunca reservadas en ciertos turnos", cols, rows)
    return cols, rows

def sala_camaleon():
    sql = """
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
    """
    cols, rows = ejecutar_consulta(sql)
    mostrar_resultados(" Sala Camaleón - Salas con mayor diversidad de facultades", cols, rows)
    return cols, rows

def patrones_uso_por_franja_horaria():
    sql = """
        SELECT 
            CASE 
                WHEN t.hora_inicio < '09:00' THEN ' Madrugadores (antes 9am)'
                WHEN t.hora_inicio < '13:00' THEN ' Mañana (9am-1pm)'
                WHEN t.hora_inicio < '17:00' THEN ' Tarde (1pm-5pm)'
                ELSE ' Noche (después 5pm)'
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
    """
    cols, rows = ejecutar_consulta(sql)
    mostrar_resultados(" Patrones de uso por franja horaria", cols, rows)
    return cols, rows

# Convierte objetos timedelta en texto legible (ej: '08:00:00')
def convertir_tiempos(resultados):
    nuevos_resultados = []
    for fila in resultados:
        nueva_fila = []
        for valor in fila:
            # Si el valor es de tipo timedelta, lo paso a texto
            if str(type(valor)) == "<class 'datetime.timedelta'>":
                segundos = valor.total_seconds()
                horas = int(segundos // 3600)
                minutos = int((segundos % 3600) // 60)
                nueva_fila.append(f"{horas:02d}:{minutos:02d}:00")
            else:
                nueva_fila.append(valor)
        nuevos_resultados.append(tuple(nueva_fila))
    return nuevos_resultados

if __name__ == "__main__":
    salas_mas_reservadas()
    turnos_mas_demandados()
    promedio_participantes_por_sala()
    reservas_por_carrera_y_facultad()
    porcentaje_ocupacion_por_edificio()
    reservas_y_asistencias_por_tipo_y_rol()
    sanciones_por_tipo_y_rol()
    porcentaje_reservas_utilizadas()
    horarios_fantasma()
    sala_camaleon()
    patrones_uso_por_franja_horaria()
# Bloque de prueba, ejecuta todos los reportes
