from db_connection import get_db_connection as get_connection
from db_connection import close_connection
from db_connection import get_db_connection, close_connection


# ---------------- PARTICIPANTES ----------------

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

# Verificar si el participante existe
def existe_participante(ci_participante):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT 1 FROM participante WHERE ci = %s;"
    cursor.execute(query, (ci_participante,))
    existe = cursor.fetchone()
    conn.close()
    return existe is not None


# Validar datos del participante
def participante_valido(ci, nombre, apellido, email):

    if not all([ci, nombre, apellido, email]):
        return False
    if not str(ci).isdigit() or len(str(ci)) < 7:
        return False
    if "@" not in email or "." not in email:
        return False
    return True


# ---------------- SALAS ----------------

# Verificar si la sala está disponible
def sala_ocupada(nombre_sala, edificio, id_turno, fecha):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT 1
        FROM reserva r
        WHERE r.nombre_sala = %s
        AND r.edificio = %s
        AND r.id_turno = %s
        AND r.fecha = %s
        AND r.estado = 'activa';
    """
    cursor.execute(query, (nombre_sala, edificio, id_turno, fecha))
    result = cursor.fetchone()
    # Si habia una fila : result = (1,)
    cursor.close()
    return result is not None
    # Devuelvo el opuesto, osea si hay una fila, la sala está ocupada

# Verificar capacidad de la sala
def excede_capacidad(nombre_sala, edificio, cantidad_participantes):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT capacidad
        FROM sala
        WHERE nombre_sala = %s AND edificio = %s;
    """
    cursor.execute(query, (nombre_sala, edificio))
    resultado = cursor.fetchone()
    #esta parte se modifico para que si alguien pasa un nombre de sala que no existe, no tire error
    if not resultado:
        conn.close()
        return False  # si la sala no existe, no excede capacidad
    capacidad = resultado[0]
    conn.close()
    return cantidad_participantes > capacidad # devuelvo si la cantidad de participantes excede la capacidad

# Restriccion por tipo de sala
def validar_tipo_sala(nombre_sala, edificio, ci_participante):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT s.tipo_sala, pa.tipo AS tipo_programa, pp.rol
        FROM participante_programa_academico pp
        JOIN programa_academico pa on pa.nombre_programa = pp.nombre_programa
        JOIN participante p ON p.ci = pp.ci_participante
        JOIN sala s ON s.nombre_sala = %s AND s.edificio = %s
        WHERE p.ci = %s
        LIMIT 1;
    """
    cursor.execute(query, (nombre_sala, edificio, ci_participante))
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


# ---------------- RESERVAS ----------------

# No mas de 3 reservas activas por semana
# EXCEPCION: docentes en salas "docente" y posgrado en salas "posgrado" no tienen este límite
def excede_reservas_semanales(ci_participante, nombre_sala=None, edificio=None):
    # Si docente reserva sala docente o posgrado reserva sala posgrado - sin límite
    if nombre_sala and edificio:
        conn = get_connection()
        cursor = conn.cursor()
        query_excepcion = """
            SELECT s.tipo_sala, pa.tipo AS tipo_programa, pp.rol
            FROM participante_programa_academico pp
            JOIN programa_academico pa ON pa.nombre_programa = pp.nombre_programa
            JOIN sala s ON s.nombre_sala = %s AND s.edificio = %s
            WHERE pp.ci_participante = %s
            LIMIT 1;
        """
        cursor.execute(query_excepcion, (nombre_sala, edificio, ci_participante))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            tipo_sala, tipo_programa, rol = result
            # Docentes en salas docente: sin límite
            if tipo_sala == "docente" and rol == "docente":
                return False
            # Posgrado en salas posgrado: sin límite
            if tipo_sala == "posgrado" and tipo_programa == "posgrado":
                return False
    
    # En todos los demás casos, aplicar límite de 3 reservas/semana
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
    count = cursor.fetchone()[0]
    conn.close()
    return count >= 3

# No mas de 2 horas diarias
# EXCEPCION: docentes en salas "docente" y posgrado en salas "posgrado" no tienen este límite
def excede_horas_diarias(ci_participante, fecha, nombre_sala=None, edificio=None):
    # Si docente reserva sala docente o posgrado reserva sala posgrado - sin límite
    if nombre_sala and edificio:
        conn = get_connection()
        cursor = conn.cursor()
        query_excepcion = """
            SELECT s.tipo_sala, pa.tipo AS tipo_programa, pp.rol
            FROM participante_programa_academico pp
            JOIN programa_academico pa ON pa.nombre_programa = pp.nombre_programa
            JOIN sala s ON s.nombre_sala = %s AND s.edificio = %s
            WHERE pp.ci_participante = %s
            LIMIT 1;
        """
        cursor.execute(query_excepcion, (nombre_sala, edificio, ci_participante))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            tipo_sala, tipo_programa, rol = result
            # Docentes en salas docente: sin límite
            if tipo_sala == "docente" and rol == "docente":
                return False
            # Posgrado en salas posgrado: sin límite
            if tipo_sala == "posgrado" and tipo_programa == "posgrado":
                return False
    
    # En todos los demás casos, aplicar límite de 2 horas/día
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT SUM(TIMESTAMPDIFF(HOUR, t.hora_inicio, t.hora_fin))
        FROM reserva r
        JOIN turno t ON r.id_turno = t.id_turno
        JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
        WHERE rp.ci_participante = %s
        AND r.fecha = %s
        AND r.estado = 'activa'
    """
    
    cursor.execute(query, (ci_participante, fecha))
    resultado = cursor.fetchone()
    total_horas = resultado[0] if resultado and resultado[0] is not None else 0
    conn.close()
    return total_horas >= 2

# Validar si la fecha a reservar es futura
def fecha_valida(fecha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT %s >= CURDATE();", (fecha,))
    # No uso query porque es una consulta simple
    valido = cursor.fetchone()[0]
    conn.close()
    return bool(valido)


# Participante tiene otra reserva activa en el mismo turno y fecha
def participante_ocupado_en_turno(ci_participante, fecha, id_turno):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
                SELECT 1
                FROM reserva r
                JOIN reserva_participante rp ON rp.id_reserva = r.id_reserva
                WHERE rp.ci_participante = %s
                    AND r.fecha = %s
                    AND r.id_turno = %s
                    AND r.estado = 'activa'
                LIMIT 1;
        """
        cursor.execute(query, (ci_participante, fecha, id_turno))
        existe = cursor.fetchone()
        conn.close()
        return existe is not None


# ---------------- SANCIONES ----------------

# Obtener sanciones activas
def obtener_sanciones():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT 
                s.id_sancion,
                s.ci_participante,
                p.nombre,
                p.apellido,
                DATE_FORMAT(s.fecha_inicio, '%Y-%m-%dT%H:%i:%sZ') AS fecha_inicio,
                DATE_FORMAT(s.fecha_fin, '%Y-%m-%dT%H:%i:%sZ') AS fecha_fin
            FROM sancion_participante s
            JOIN participante p ON s.ci_participante = p.ci
            WHERE s.estado = 'activa';
        """)
        sanciones = cursor.fetchall()
        return sanciones
    except Exception as e:
        raise e
    finally:
        cursor.close()
        close_connection(conn)
