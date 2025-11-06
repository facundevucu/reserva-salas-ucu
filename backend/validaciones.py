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
        AND r.estado = 'activa'
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
    resultado = cursor.fetchone()
    #esta parte se modifico para que si alguien pasa un nombre de sala que no existe, no tire error
    if not resultado:
        conn.close()
        return False  # si la sala no existe, no excede capacidad
    capacidad = resultado[0]
    conn.close()
    return cantidad_participantes > capacidad # devuelvo si la cantidad de participantes excede la capacidad

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
        WHERE p.ci = %s
        LIMIT 1;
    """
    cursor.execute(query, (nombre_sala, ci_participante))
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

# Luego de armadas las ABM, el equipo se dio cuenta de que podiamos
# ahorrarnos mucho trabajo si crearamos las validaciones para evitar
# tener que definir manejo de errores en cada ABM.

# Asi que todas las funciones de validacion van aca, y las ABM's las llaman
# antes de hacer cualquier operacion en la base de datos.

def existe_participante(ci_participante):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT 1 FROM participante WHERE ci = %s;"
    cursor.execute(query, (ci_participante,))
    existe = cursor.fetchone()
    conn.close()
    return existe is not None

def existe_sala(nombre_sala):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT 1 FROM sala WHERE nombre_sala = %s;"
    cursor.execute(query, (nombre_sala,))
    existe = cursor.fetchone()
    conn.close()
    return existe is not None

def turno_valido(id_turno):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        sELECT hora_inicio, hora_fin
        FROM turno
        WHERE id_turno = %s;"""
    cursor.execute(query, (id_turno,))
    valido = cursor.fetchone()
    conn.close()

    if not valido:
        return False
    hora_inicio, hora_fin = valido # valido es una tupla con hora_inicio y hora_fin
    #por ultimo verifico que la hora de inicio sea menor a la de fin
    return hora_inicio < hora_fin

def sancion_valida(ci_participante, fecha_inicio, fecha_fin):
    # fechas coherentes
    if fecha_fin < fecha_inicio:
        return False

    conn = get_connection()
    cursor = conn.cursor()
    # hago una query para ver si hay alguna sancion que se solape con el rango dado
    query = """
        SELECT 1
        FROM sancion_participante
        WHERE ci_participante = %s
        AND (
            (fecha_inicio <= %s AND fecha_fin >= %s)
            OR (fecha_inicio <= %s AND fecha_fin >= %s)
        );
    """
    cursor.execute(query, (ci_participante, fecha_inicio, fecha_inicio, fecha_fin, fecha_fin))
    solapada = cursor.fetchone()
    conn.close()

    # No debe haber solapamiento
    # si fetchone devuelve algo, es que hay solapamiento
    return solapada is None

def reserva_existente(id_reserva):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT 1 FROM reserva WHERE id_reserva = %s;"
    cursor.execute(query, (id_reserva,))
    existe = cursor.fetchone()
    conn.close()
    return existe is not None

def estado_valido(estado, tabla):
    # creo un diccionario de estados permitidos
    # una especie de catalogo
    estados_permitidos = {
        "reserva": ["activa", "cancelada", "sin_asistencia", "finalizada"],
        "sancion": ["activa", "inactiva", "anulada"]
    }
    # con esta funcion me aseguro que cuando modifique o cree una reserva
    # o sancion, el estado sea uno de los permitidos
    # me va a servir para las sanciones, que segun el profe son automaticas
    # si la persona no esta a la hora marcada en la sala
    if tabla not in estados_permitidos:
        return False
    return estado in estados_permitidos[tabla]

def participante_activo(ci_participante):
    conn = get_connection()
    cursor = conn.cursor()
    # como es corta la consulta, no uso query
    cursor.execute("SELECT activo FROM participante WHERE ci = %s;", (ci_participante,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == 1
