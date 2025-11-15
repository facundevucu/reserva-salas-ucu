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

# Verificar si el participante está activo
def participante_activo(ci_participante):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT estado FROM partic sipante WHERE ci = %s;", (ci_participante,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == 'activo'

# Validar datos del participante
def participante_valido(ci, nombre, apellido, email):

    if not all([ci, nombre, apellido, email]):
        return False
    if not str(ci).isdigit() or len(str(ci)) < 7:
        return False
    if "@" not in email or "." not in email:
        return False
    return True

# Validar CI
def ci_valido(ci):
    return str(ci).isdigit() and 6 <= len(str(ci)) <= 9

# ---------------- SALAS ----------------

# Verificar si la sala existe
def existe_sala(nombre_sala, edificio):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT 1 FROM sala WHERE nombre_sala = %s AND edificio = %s;"
    cursor.execute(query, (nombre_sala, edificio))
    existe = cursor.fetchone()
    conn.close()
    return existe is not None

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

# Verificar si el turno es válido
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

# Verificar si la reserva existe
def reserva_existente(id_reserva):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT 1 FROM reserva WHERE id_reserva = %s;"
    cursor.execute(query, (id_reserva,))
    existe = cursor.fetchone()
    conn.close()
    return existe is not None

# Validar si la fecha a reservar es futura
def fecha_valida(fecha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT %s >= CURDATE();", (fecha,))
    # No uso query porque es una consulta simple
    valido = cursor.fetchone()[0]
    conn.close()
    return bool(valido)


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

# Validar sanción (fechas y solapamiento)
def sancion_valida(ci_participante=None, fecha_inicio=None, fecha_fin=None, verificar_solapamiento=True):

    if not fecha_inicio or not fecha_fin:
        return False
    if fecha_fin < fecha_inicio:
        return False

    if verificar_solapamiento and ci_participante:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT 1
            FROM sancion_participante
            WHERE ci_participante = %s
            AND (
                (fecha_inicio <= %s AND fecha_fin >= %s)  -- Se solapa por dentro
                OR (fecha_inicio <= %s AND fecha_fin >= %s)  -- Se solapa al final
                OR (%s <= fecha_inicio AND %s >= fecha_fin)  -- Contiene completamente
            )
        """
        cursor.execute(query, (
            ci_participante,
            fecha_fin, fecha_inicio,
            fecha_inicio, fecha_fin,
            fecha_inicio, fecha_fin
        ))
        result = cursor.fetchone()
        cursor.close()
        close_connection(conn)
        
        if result:
            return False

    return True


# ---------------- GENERALES ----------------

# Validar estado para reservas y sanciones
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

# Validar login
def login_valido(email, password):
    if not email or not password:
        return False
    if "@" not in email or "." not in email:
        return False
    if len(password) < 4:
        return False
    return True



# Obtener estadísticas para el dashboard
def obtener_estadisticas_dashboard():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) AS total FROM sala")
        total_salas = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM reserva WHERE estado = 'activa'")
        reservas_activas = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM participante")
        total_participantes = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM sancion_participante WHERE fecha_fin >= CURDATE()")
        sanciones_activas = cursor.fetchone()["total"]

        return {
            "total_salas": total_salas,
            "reservas_activas": reservas_activas,
            "total_participantes": total_participantes,
            "sanciones_activas": sanciones_activas
        }

    except Exception as e:
        # Re-lanzamos el error para manejarlo en app.py
        raise e
    finally:
        cursor.close()
        close_connection(conn)

# ---------------- CONSULTAS AUXILIARES ----------------

# Aca algunas que podrian ir a logica, pero por organizacion las dejamos aca,
# para no confundir con los ABM


def obtener_edificios():

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT nombre_edificio FROM edificio")
        edificios = [row[0] for row in cursor.fetchall()]
        return edificios
    except Exception as e:
        raise e
    finally:
        cursor.close()
        close_connection(conn)

def obtener_salas():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT nombre_sala, edificio, capacidad FROM sala")
        data = cursor.fetchall()
        salas = [
            {"nombre": row[0], "edificio": row[1], "capacidad": row[2]}
            for row in data
        ]
        return salas
    except Exception as e:
        raise e
    finally:
        cursor.close()
        close_connection(conn)

def obtener_participantes():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ci, nombre, apellido, email FROM participante")
        data = cursor.fetchall()
        participantes = [
            {"ci": row[0], "nombre": row[1], "apellido": row[2], "email": row[3]}
            for row in data
        ]
        return participantes
    except Exception as e:
        raise e
    finally:
        cursor.close()
        close_connection(conn)

def obtener_turnos():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_turno, hora_inicio, hora_fin FROM turno ORDER BY hora_inicio")
        return cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        close_connection(conn)

def obtener_turnos_formateados():
    turnos = obtener_turnos()
    lista = []
    for t in turnos:
        id_turno, inicio, fin = t
        lista.append(f"{id_turno} | {inicio.strftime('%H:%M')}–{fin.strftime('%H:%M')}")
    return lista

def seleccionar_opcion(lista, titulo):
    print(f"\n--- {titulo} ---")
    for i, item in enumerate(lista, start=1):
        print(f"{i}. {item}")
    
    while True:
        opcion = input("Elige una opción: ").strip()
        if opcion.isdigit() and 1 <= int(opcion) <= len(lista):
            return lista[int(opcion) - 1]
        print(" Opción inválida, intenta de nuevo.")