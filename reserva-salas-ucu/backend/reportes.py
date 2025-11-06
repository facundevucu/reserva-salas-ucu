from backend.db_connection import get_db_connection, close_connection

def ejecutar_consulta(sql):
    conn = get_db_connection()
    if not conn:
        print("No se pudo conectar a la base de datos.")
        return [], []
    
    cursor = conn.cursor()
    cursor.execute(sql)
    resultados = cursor.fetchall()
    nombres_columnas = [desc[0] for desc in cursor.description]
    # Con esto obtengo los nombres de las columnas
    cursor.close()
    close_connection(conn)
    return nombres_columnas, resultados

def mostrar_resultados(nombre_reporte, columnas, resultados):
    # Imprime los resultados en consola de forma legible. 
    print(f"\n📊 {nombre_reporte}")
    print("=" * (len(nombre_reporte) + 4))
    if not resultados:
        print("Sin resultados.")
        return
    print(" | ".join(columnas))
    print("-" * 80)
    for fila in resultados:
        print(" | ".join(str(x) for x in fila))

# Ahora escribo funciones específicas para cada reporte, los cuales estan en db/consultas.sql
def salas_mas_reservadas():
    sql = """
        SELECT nombre_sala,
               COUNT(*) AS total_reservas
        FROM reserva
        GROUP BY nombre_sala
        ORDER BY total_reservas DESC;
    """
    cols, rows = ejecutar_consulta(sql)
    mostrar_resultados("Salas más reservadas", cols, rows)

def turnos_mas_demandados():
    sql = """
        SELECT t.id_turno, t.hora_inicio, t.hora_fin,
               COUNT(r.id_reserva) AS total_reservas
        FROM turno t
        LEFT JOIN reserva r ON t.id_turno = r.id_turno
        GROUP BY t.id_turno, t.hora_inicio, t.hora_fin
        ORDER BY total_reservas DESC;
    """
    cols, rows = ejecutar_consulta(sql)
    mostrar_resultados("Turnos más demandados", cols, rows)

def promedio_participantes_por_sala():
    sql = """
        SELECT r.nombre_sala,
            COUNT(rp.ci_participante) / COUNT(DISTINCT r.id_reserva) AS promedio_participantes
        FROM reserva r
        JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
        GROUP BY r.nombre_sala;
    """
    cols, rows = ejecutar_consulta(sql)
    mostrar_resultados("Promedio de participantes por sala", cols, rows)

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

if __name__ == "__main__":
    salas_mas_reservadas()
    turnos_mas_demandados()
    promedio_participantes_por_sala()
    reservas_por_carrera_y_facultad()
    porcentaje_ocupacion_por_edificio()
    reservas_y_asistencias_por_tipo_y_rol()
    sanciones_por_tipo_y_rol()
    porcentaje_reservas_utilizadas()
# Bloque de prueba, ejecuta todos los reportes