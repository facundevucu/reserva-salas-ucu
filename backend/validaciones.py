from backend.db_connection import get_db_connection as get_connection

# Verificar si el usuario tiene una sanción activa
def tiene_sancion_activa(ci_participante):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT 1
        FROM sancion_participante
        where ci_participante = %s 
        AND CURDATE() BETWEEN fecha_inicio AND fecha_fin;
    """
    # El %s es el input del usuario
    cursor.execute(query, (ci_participante,))
    result = cursor.fetchone()
    cursor.close()
    return result is not None 

# No más de 3 reservas activas por semana
def excede_reservas_semanales(ci_participante):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT COUNT(*)
        FROM reserva_participante rp
        JOIN reserva r on rp.id_reserva = r.id_reserva
        WHERE rp.ci_participante = %s
        AND r.estado = 'activa'
        AND YEARWEEK(r.fecha) = YEARWEEK(CURDATE());
    """
    cursor.execute(query, (ci_participante,))
    count = cursor.fetchone()[0] # Me devuelve el primer resultado de la tupla count
    conn.close()
    return count >= 3

# No más de 2 horas diarias por sala
def excede_horas_diarias(ci_participante, fecha):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT SUM(TIMESTAMPDIFF(HOUR, t.hora_inicio, t.hora_fin))
        FROM reserva r
        JOIN turno t ON r.id_turno = t.id_turno
        JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
        WHERE rp.ci_participante = %s
        AND r.fecha = %s
    """
    
    cursor.execute(query, (ci_participante, fecha))
    resultado = cursor.fetchone()
    total_horas = resultado[0] if resultado and resultado[0] is not None else 0 # Si es none, son 0 horas, sirve para el return
    # aca le agregue una validacion porque si no daba salida la orden, se rompia el codigo, entonces ahora si no da salida, le establezco 0, como valor definido
    conn.close()
    return total_horas >= 2

# Verificar si la sala está disponible
def sala_ocupada(nombre_sala, id_turno, fecha):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT 1
        FROM reserva r
        WHERE nombre_sala = %s
        AND id_turno = %s
        AND r.fecha = %s
        AND r.estado = 'activa';
    """
    cursor.execute(query, (nombre_sala, id_turno, fecha))
    result = cursor.fetchone()
    # Si habia una fila : result = (1,)
    cursor.close()
    return result is not None
    # Devuelvo el opuesto, osea si hay una fila, la sala está ocupada

# Verificar capacidad de la sala
def excede_capacidad(nombre_sala, cantidad_participantes):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT capacidad
        FROM sala
        WHERE nombre_sala = %s;
    """
    cursor.execute(query, (nombre_sala,))
    capacidad = cursor.fetchone()[0]
    cursor.close()
    return cantidad_participantes > capacidad

# Restriccion por tipo de sala
def validar_tipo_sala(ci_participante, nombre_sala):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT s.tipo_sala, pa.tipo AS tipo_programa, pp.rol
        FROM participante_programa_academico pp
        JOIN programa_academico pa on pa.nombre_programa = pp.nombre_programa
        JOIN participante p ON p.ci = pp.ci_participante
        JOIN sala s on s.nombre_sala = %s
        WHERE p.ci = %s;
        LIMIT 1;
    """
    cursor.execute(query, (ci_participante, nombre_sala))
    result = cursor.fetchone()
    conn.close()
    # Mi result va a ser una tupla (tipo_sala, tipo_participante, rol) 
    # Ahora comparo que los 3 sean iguales, para validar el tipo de sala
    
    if result is None:
        return False  # No hay relación entre participante y sala
    
    tipo_sala, tipo_participante, rol = result

    if tipo_sala == "libre":
        return True
    
    if tipo_sala == "posgrado" and tipo_participante == "posgrado":
        return True
    
    
    if tipo_sala == "docente" and rol == "docente":
        return True
    
    return False

# Validar si la fecha a reservar es futura
def fecha_valida(fecha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT %s >= CURDATE();", (fecha,))
    # No uso query porque es una consulta simple
    valido = cursor.fetchone()[0]
    conn.close()
    return bool(valido)
