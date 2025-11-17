from db_connection import get_db_connection, close_connection
import mysql.connector
from mysql.connector import Error
from validaciones import (
    tiene_sancion_activa,
    excede_reservas_semanales,
    excede_horas_diarias,
    sala_ocupada,
    excede_capacidad,
    validar_tipo_sala,
    fecha_valida
)
import random
import string

def generar_contraseña_aleatoria(longitud=8):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

#ABM de RESERVAS (creacion, eliminacion, modificacion)--------------------------------

def crear_reserva(ci_participante, nombre_sala, edificio, id_turno, fecha, cantidad_participantes, estado="activa"):
    
    if not fecha_valida(fecha):
        return "La fecha seleccionada no es válida."
    
    if tiene_sancion_activa(ci_participante):
        return "El participante tiene una sanción activa."

    if excede_reservas_semanales(ci_participante):
        return "El participante ha excedido el límite de reservas semanales."

    if excede_horas_diarias(ci_participante, fecha):
        return "El participante ha excedido el límite de horas diarias."

    if sala_ocupada(nombre_sala, edificio, id_turno, fecha):
        return "La sala está ocupada en el turno y fecha seleccionados."

    if excede_capacidad(nombre_sala, edificio, cantidad_participantes):
        return "La cantidad de personas excede la capacidad de la sala."

    if not validar_tipo_sala(nombre_sala, edificio, ci_participante):
        return "El participante no está autorizado para reservar este tipo de sala."

    # Si pasa todas las validaciones, proceder a crear la reserva
    # Implementación de manejo de errores

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado)
            VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(query, (nombre_sala, edificio, fecha, id_turno, estado))
        id_reserva = cursor.lastrowid # Guarda el id de la reserva recién creada

        # Ahora insertto al participante en la tabla reserva_participante
        query_participante = """
            INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia)
            VALUES (%s, %s, CURDATE(), NULL);
        """
        cursor.execute(query_participante, (ci_participante, id_reserva))        
        conn.commit() # confirma y guarda la reserva y el participante
        return {"id_reserva": id_reserva, "mensaje": "Reserva creada exitosamente."}
    
    except Exception as e:
        # Si hay un error, hago rollback
        if conn:
            conn.rollback()
        print("Error MySQL:", e)
        return "Ocurrió un error al crear la reserva. Intente nuevamente más tarde."
    
    finally: # este paso lo hace is o si
        if conn and conn.is_connected():
            close_connection(conn)

def eliminar_reserva(id_reserva):
    try : 
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = "UPDATE reserva SET estado = 'cancelada' WHERE id_reserva = %s"
        cursor.execute(sql, (id_reserva,))
        # LA coma va porque cursor.execute espera valores en forma de tupla
        connection.commit()

        if cursor.rowcount > 0:
        # Esto indica la cantidad de filas afectadas por la instruccion
            return f"Reserva {id_reserva} cancelada correctamente."
        else: 
            return f"No se encontro la reserva con ID {id_reserva}."
        
    except Error as e:
        return f"Error al cancelar la reserva: {e}"
        # Con el {e} muestro el error que ocurre (lo hace el conector)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            # Por ultimo verifico la conexion y la cierro para salir

# para modificar la reserva siempre tengo que indicar el id_reserva, y el/los campos a modificar con su nuevo valor
def modificar_reserva(id_reserva, nombre_sala = None, fecha = None, id_turno = None, estado = None):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        campos = []
        #nombres de las columnas a modificar
        valores = []
        #valores reales que reemplazarán los %s en orden

        if nombre_sala: # vas a cambiar de sala
            campos.append("nombre_sala = %s") #agrego el campo a modificar
            valores.append(nombre_sala) # agrega el valor que reemplazara %s
            #tambien tengo que cambiar el edificio, lo puedo hacer con una consulta simple
            campos.append("edificio = (SELECT edificio FROM sala WHERE nombre_sala = %s)")
            valores.append(nombre_sala)
        if fecha:
            campos.append("fecha = %s")
            valores.append(fecha)
        if id_turno:
            campos.append("id_turno = %s")
            valores.append(id_turno)
        if estado:
            campos.append("estado = %s")
            valores.append(estado)
        if not campos:
            return "No se proporcionaron datos para modificar"
        
        #En caso que todo salio bien
        valores.append(id_reserva)
        sql = f"UPDATE reserva SET {', '.join(campos)} WHERE id_reserva = %s"
        # El método .join() une todos los elementos de una lista en una sola cadena de texto, 
        # separándolos con lo que esta entre comillas.
        # lo que hago con el join es pasarle todos los campos modificados separados por comas
        # ejemplo: UPDATE reserva SET fecha = %s, estado = %s WHERE id_reserva = %s
        cursor.execute(sql, valores)
        connection.commit()

        return f"Reserva {id_reserva} modificada correctamente."
    
    except Error as e:
        return f"Error al modificar la reserva {e}."
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


#ABM de PERSONAS (creacion, eliminacion, modificacion)--------------------------------
def crear_persona(ci_participante, nombre, apellido, email):
    conn = get_db_connection()
    if not conn:
        return "Error de conexión a la base de datos"
    
    try:
        cursor = conn.cursor()
        
        # Insertar participante
        query_participante = """
            INSERT INTO participante (ci, nombre, apellido, email)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query_participante, (ci_participante, nombre, apellido, email))
        
        # Generar contraseña automática
        contraseña_generada = generar_contraseña_aleatoria()
        
        # Insertar en tabla login con rol usuario por defecto
        query_login = """
            INSERT INTO login (correo, contraseña, rol, ci_participante, debe_cambiar_contraseña)
            VALUES (%s, %s, 'usuario', %s, TRUE)
        """
        cursor.execute(query_login, (email, contraseña_generada, ci_participante))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return {
            'mensaje': f"Participante creado correctamente. Contraseña generada: {contraseña_generada}",
            'contraseña': contraseña_generada
        }
    
    except mysql.connector.Error as err:
        if conn:
            conn.rollback()
            conn.close()
        return f" Error al crear participante: {err}"

def eliminar_persona(ci_participante):
    connection = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Verificar si tiene reservas asociadas
        cursor.execute("SELECT 1 FROM reserva_participante WHERE ci_participante = %s LIMIT 1", (ci_participante,))
        if cursor.fetchone():
            return "No se puede eliminar porque tiene reservas asociadas."

        # Cambiar estado a 'inactivo'
        sql = "UPDATE participante SET estado = 'inactivo' WHERE ci = %s"
        cursor.execute(sql, (ci_participante,))
        connection.commit()

        if cursor.rowcount > 0:
            return f"Persona {ci_participante} desactivada correctamente."
        else:
            return f"No se encontró persona con CI {ci_participante}."
    except Error as e:
        if connection:
            connection.rollback()
        return f"Error al desactivar persona: {e}"
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


# aca se repite la estructura de modificar_reserva pero adaptada a persona
# para modificar la persona siempre tengo que indicar la ci_participante, y el/los campos a modificar con su nuevo valor
def modificar_persona(ci_participante, nombre=None, apellido=None, email=None):
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        campos = []   # columnas a modificar
        valores = []  # valores nuevos que reemplazan los %s

        if nombre:
            campos.append("nombre = %s")
            valores.append(nombre)
        if apellido:
            campos.append("apellido = %s")
            valores.append(apellido)
        if email:
            campos.append("email = %s")
            valores.append(email)

        if not campos:
            return "No se proporcionaron datos para modificar."

        valores.append(ci_participante)
        sql = f"UPDATE participante SET {', '.join(campos)} WHERE ci = %s"
        # Cambié ci_participante por ci en el WHERE
        cursor.execute(sql, valores)
        connection.commit()

        return f"Persona {ci_participante} modificada correctamente."
    except Error as e:
        if connection:
            connection.rollback()
        return f"Error al modificar persona: {e}"
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()




#ABM de SALAS (creacion, eliminacion, modificacion)--------------------------------
def crear_sala(nombre_sala, edificio, capacidad, tipo_sala):
    connection = None

    if not isinstance(capacidad, int) or capacidad <= 0:
        return "La capacidad debe ser un número entero positivo."

    # verificar si la sala ya existe antes de insertarla
    conn = get_db_connection()
    cursor = conn.cursor()
    # hago una consulta para ver si ya existe la sala con ese nombre y edificio
    cursor.execute("SELECT 1 FROM sala WHERE nombre_sala = %s AND edificio = %s", (nombre_sala, edificio))
    if cursor.fetchone():
        close_connection(conn)
        return f"La sala '{nombre_sala}' ya existe en el edificio '{edificio}'."
    close_connection(conn)

    # ahora si paso a crear la sala
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = """
            INSERT INTO sala (nombre_sala, edificio, capacidad, tipo_sala)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre_sala, edificio, capacidad, tipo_sala))
        connection.commit()

        return f"Sala '{nombre_sala}' creada correctamente en el edificio '{edificio}'."
    except Error as e:
        if connection:
            connection.rollback()
        return f"Error al crear sala: {e}"
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()



def eliminar_sala(nombre_sala, edificio):
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = "DELETE FROM sala WHERE nombre_sala = %s AND edificio = %s"
        cursor.execute(sql, (nombre_sala, edificio))
        connection.commit()

        if cursor.rowcount > 0:
            return f"Sala '{nombre_sala}' del edificio '{edificio}' eliminada correctamente."
        else:
            return f"No se encontró la sala '{nombre_sala}' en el edificio '{edificio}'."
    except Error as e:
        if "1451" in str(e):
            return "No se puede eliminar la sala porque tiene reservas asociadas."
        
        if connection:
            connection.rollback()
        return f"Error al eliminar sala: {e}"
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

# para modificar la sala siempre tengo que indicar el nombre_sala y edificio, y el/los campos a modificar con su nuevo valor
# se repite como en los dos anteriores (persona y reserva)
# el none es porque son las posibles modificaciones, no es obligatorio cambiar todo
def modificar_sala(nombre_sala, edificio, capacidad=None, tipo_sala=None):
    accion = "modificar_sala" # sirve para el log
    connection = None # verifica que no se quede abierta la conexion en caso de error

    if capacidad and (not isinstance(capacidad, int) or capacidad <= 0):
        # si la capacidad existe (o sea, se quiere cambiar) y no es un entero positivo
        return "La capacidad debe ser un número entero positivo."
    # de entrada verifico que la capacidad sea correcta, si no lo es retorno el error desde ya
    # no utilizo los recursos del try si ya se que va a fallar

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        campos = []   # columnas a cambiar
        valores = []  # valores nuevos

        # esto seria como un IF CAPACIDAD:
        if capacidad: # variable ya verificada arriba
            campos.append("capacidad = %s")
            valores.append(capacidad)
        if tipo_sala:
            campos.append("tipo_sala = %s")
            valores.append(tipo_sala)

        # no incluyo cambiar nombre_sala o edificio porque son las primary key
        # las unica solucion que se nos ocurre es eliminar y crear una nueva sala o renonmbrar la sala con una funcion aparte

        if not campos: # el usuario no paso ningun campo a modificar, es bobo
            return "No se proporcionaron datos para modificar."

        valores.append(nombre_sala) # para el WHERE
        valores.append(edificio) # para el WHERE

        sql = f"UPDATE sala SET {', '.join(campos)} WHERE nombre_sala = %s AND edificio = %s"
        # El método .join() une todos los elementos de una lista en una sola cadena de texto,
        # separándolos con lo que esta entre comillas.
        # lo que hago con el join es pasarle todos los campos modificados separados por comas
        cursor.execute(sql, valores)
        connection.commit()

        if cursor.rowcount > 0: # esto indica la cantidad de filas afectadas por la instruccion
            return f"Sala '{nombre_sala}' modificada correctamente."
        else:
            return f"No se encontró la sala '{nombre_sala}' en el edificio '{edificio}'."
    
    except Error as e:
        if connection:
            connection.rollback() # vuelve al estado anterior si falla(ctrl + z)
        return f"Error al modificar sala: {e}"
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            


# ABM de SANCIONES (creación, baja, odificación) -----------------------
from validaciones import (
    tiene_sancion_activa,
    fecha_valida
)

def crear_sancion(ci_participante, motivo, fecha_inicio, fecha_fin=None, estado="activa"):
    accion = "crear_sancion"
    conn = None

    # Validaciones de fechas con las funciones del módulo validaciones
    if not fecha_valida(fecha_inicio) or (fecha_fin and not fecha_valida(fecha_fin)):
        #por las dudas si no tiene fecha_fin no la valido
        return "Alguna de las fechas indicadas no es válida."

    if fecha_fin and fecha_fin < fecha_inicio:
        # mas validaciones para posible errores de input de ususario
        return "La fecha de fin no puede ser anterior a la fecha de inicio."

    if tiene_sancion_activa(ci_participante):
        #si ya tiene sancion no dejo crear otra
        return "El participante ya tiene una sanción activa."

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO sancion_participante (ci_participante, motivo, fecha_inicio, fecha_fin, estado)
            VALUES (%s, %s, %s, %s, %s)
        """
        # hay que agregar estos alores a la db
        cursor.execute(sql, (ci_participante, motivo, fecha_inicio, fecha_fin, estado))
        conn.commit()
        id_sancion = cursor.lastrowid

        return {"id_sancion": id_sancion, "mensaje": "Sanción creada correctamente."}

    except Exception as e:
        if conn:
            conn.rollback() # revierte los cambios si hay error
        return f"Ocurrió un error al crear la sanción: {e}"

    finally:
        if conn and conn.is_connected():
            close_connection(conn)


def levantar_sancion(id_sancion):
    accion = "levantar_sancion"
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = """
            UPDATE sancion_participante
            SET estado = 'inactiva', fecha_fin = CURDATE()
            WHERE id_sancion = %s AND estado = 'activa'
        """
        # cambio el estado a inactiva y pongo la fecha_fin como hoy
        cursor.execute(sql, (id_sancion,))
        connection.commit()

        if cursor.rowcount > 0:
            return f"Sanción {id_sancion} levantada correctamente."
        else:
            return "No se encontró una sanción activa con ese ID."

    except Error as e:
        if connection:
            connection.rollback()
        return f"Error al levantar la sanción: {e}"

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def eliminar_sancion(id_sancion):
    # la marco como anulada en vez de borrarla fisicamente
    accion = "eliminar_sancion"
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "UPDATE sancion_participante SET estado = 'anulada' WHERE id_sancion = %s"
        cursor.execute(sql, (id_sancion,)) # en forma de tupla
        connection.commit()

        if cursor.rowcount > 0:
            return f"Sanción {id_sancion} anulada correctamente."
        else:
            return f"No se encontró sanción con ID {id_sancion}."

    except Error as e:
        if connection:
            connection.rollback()
        return f"Error al anular la sanción: {e}"

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def modificar_sancion(id_sancion, motivo=None, fecha_inicio=None, fecha_fin=None, estado=None):
    accion = "modificar_sancion"
    connection = None

    # validaciones simples de fechas si vienen informadas
    if fecha_inicio and not fecha_valida(fecha_inicio):
        return "La fecha de inicio no es válida."
    
    if fecha_fin and not fecha_valida(fecha_fin):
        return "La fecha de fin no es válida."
    
    if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
        return "La fecha de fin no puede ser anterior a la fecha de inicio."

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        campos = []
        valores = []

        if motivo:
            campos.append("motivo = %s")
            valores.append(motivo)
        if fecha_inicio:
            campos.append("fecha_inicio = %s")
            valores.append(fecha_inicio)
        if fecha_fin is not None:  # permitir setear a NULL
            campos.append("fecha_fin = %s")
            valores.append(fecha_fin)
        if estado:
            # validar estados permitidos si querés: activa/inactiva/anulada
            campos.append("estado = %s")
            valores.append(estado)

        if not campos:
            return "No se proporcionaron datos para modificar."

        valores.append(id_sancion)
        sql = f"UPDATE sancion_participante SET {', '.join(campos)} WHERE id_sancion = %s"
        cursor.execute(sql, valores)
        connection.commit()
        # repito la estructura de los otros ABM de modificacion

        return f"Sanción {id_sancion} modificada correctamente."

    except Error as e:
        if connection:
            connection.rollback()
        return f"Error al modificar la sanción: {e}"

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()






# ================== LISTADOS / CONSULTAS DE APOYO PARA MENÚS ==================

def listar_edificios():

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT nombre_edificio FROM edificio ORDER BY nombre_edificio")
        rows = cur.fetchall()
        return [{"nombre_edificio": r[0]} for r in rows]
    except Exception as e:
        return []
    finally:
        if conn and conn.is_connected():
            cur.close()
            close_connection(conn)


def listar_salas(edificio=None):

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if edificio:
            cur.execute(
                """
                SELECT nombre_sala, edificio, capacidad, tipo_sala
                FROM sala
                WHERE edificio = %s
                ORDER BY nombre_sala
                """,
                (edificio,)
            )
        else:
            cur.execute(
                """
                SELECT nombre_sala, edificio, capacidad, tipo_sala
                FROM sala
                ORDER BY edificio, nombre_sala
                """
            )
        rows = cur.fetchall()
        return [
            {
                "nombre": r[0],
                "edificio": r[1],
                "capacidad": r[2],
                "tipo_sala": r[3],
            }
            for r in rows
        ]
    except Exception:
        return []
    finally:
        if conn and conn.is_connected():
            cur.close()
            close_connection(conn)


def listar_turnos():

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id_turno, hora_inicio, hora_fin FROM turno ORDER BY hora_inicio"
        )
        rows = cur.fetchall()
        return [
            {
                "id_turno": r[0],
                "hora_inicio": str(r[1]),
                "hora_fin": str(r[2]),
            }
            for r in rows
        ]
    except Exception:
        return []
    finally:
        if conn and conn.is_connected():
            cur.close()
            close_connection(conn)


def listar_participantes_activos():

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT ci, nombre, apellido, email
            FROM participante
            WHERE estado = 'activo'
            ORDER BY apellido, nombre
            """
        )
        rows = cur.fetchall()
        return [
            {"ci": r[0], "nombre": r[1], "apellido": r[2], "email": r[3]}
            for r in rows
        ]
    except Exception:
        return []
    finally:
        if conn and conn.is_connected():
            cur.close()
            close_connection(conn)


def listar_reservas(estado=None):

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        base_sql = (
            """
            SELECT r.id_reserva, r.fecha, r.estado, r.nombre_sala, r.edificio,
                   t.id_turno, t.hora_inicio, t.hora_fin
            FROM reserva r
            JOIN turno t ON r.id_turno = t.id_turno
            {where}
            ORDER BY r.fecha DESC, t.hora_inicio
            """
        )
        where_clause = ""
        params = ()
        if estado:
            where_clause = "WHERE r.estado = %s"
            params = (estado,)
        cur.execute(base_sql.format(where=where_clause), params)
        rows = cur.fetchall()
        return [
            {
                "id_reserva": r[0],
                "fecha": str(r[1]),
                "estado": r[2],
                "nombre_sala": r[3],
                "edificio": r[4],
                "id_turno": r[5],
                "hora_inicio": str(r[6]),
                "hora_fin": str(r[7]),
            }
            for r in rows
        ]
    except Exception:
        return []
    finally:
        if conn and conn.is_connected():
            cur.close()
            close_connection(conn)


def listar_sanciones_activas():

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT s.id_sancion, s.ci_participante, p.nombre, p.apellido, s.fecha_inicio, s.fecha_fin
            FROM sancion_participante s
            JOIN participante p ON p.ci = s.ci_participante
            WHERE s.estado = 'activa'
            ORDER BY s.fecha_inicio DESC
            """
        )
        rows = cur.fetchall()
        return [
            {
                "id_sancion": r[0],
                "ci_participante": r[1],
                "nombre": r[2],
                "apellido": r[3],
                "fecha_inicio": str(r[4]) if r[4] is not None else None,
                "fecha_fin": str(r[5]) if r[5] is not None else None,
            }
            for r in rows
        ]
    except Exception:
        return []
    finally:
        if conn and conn.is_connected():
            cur.close()
            close_connection(conn)


# ================== AUTENTICACIÓN Y ACCESO POR ROL ==================

def autenticar_usuario(correo, contrasena):

    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT rol, correo 
            FROM login 
            WHERE correo = %s AND contraseña = %s
        """
        cursor.execute(query, (correo, contrasena))
        resultado = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if resultado:
            return {
                'rol': resultado['rol'],
                'correo': resultado['correo']
            }
        return None
        
    except mysql.connector.Error as err:
        print(f" Error al autenticar: {err}")
        if conn:
            conn.close()
        return None

def obtener_ci_por_correo(correo):

    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        query = """
            SELECT ci_participante 
            FROM login 
            WHERE correo = %s
        """
        cursor.execute(query, (correo,))
        resultado = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if resultado and resultado['ci_participante']:
            return resultado['ci_participante']
        return None
        
    except mysql.connector.Error as err:
        print(f" Error al obtener CI: {err}")
        if conn:
            conn.close()
        return None

def listar_reservas_usuario(ci):

    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT r.id_reserva, r.fecha, r.estado, r.nombre_sala, r.edificio,
                   t.id_turno, t.hora_inicio, t.hora_fin
            FROM reserva r
            JOIN turno t ON r.id_turno = t.id_turno
            JOIN reserva_participante rp ON rp.id_reserva = r.id_reserva
            WHERE rp.ci_participante = %s
            ORDER BY r.fecha DESC, t.hora_inicio
            """,
            (ci,)
        )
        rows = cur.fetchall()
        return [
            {
                "id_reserva": r[0],
                "fecha": str(r[1]),
                "estado": r[2],
                "nombre_sala": r[3],
                "edificio": r[4],
                "id_turno": r[5],
                "hora_inicio": str(r[6]),
                "hora_fin": str(r[7]),
            }
            for r in rows
        ]
    except Exception:
        return []
    finally:
        if conn and conn.is_connected():
            cur.close()
            close_connection(conn)


def consultar_mis_sanciones(ci):
    """Lista todas las sanciones (activas e inactivas) de un participante.
    Estructura: { 'id_sancion': int, 'motivo': str, 'estado': str, 'fecha_inicio': str, 'fecha_fin': str }
    """
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id_sancion, motivo, estado, fecha_inicio, fecha_fin
            FROM sancion_participante
            WHERE ci_participante = %s
            ORDER BY fecha_inicio DESC
            """,
            (ci,)
        )
        rows = cur.fetchall()
        return [
            {
                "id_sancion": r[0],
                "motivo": r[1],
                "estado": r[2],
                "fecha_inicio": str(r[3]) if r[3] else None,
                "fecha_fin": str(r[4]) if r[4] else None,
            }
            for r in rows
        ]
    except Exception:
        return []
    finally:
        if conn and conn.is_connected():
            cur.close()
            close_connection(conn)


def obtener_disponibilidad_turnos(nombre_sala, edificio, fecha):

    from datetime import datetime, time
    
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Obtener todos los turnos
        query_turnos = "SELECT id_turno, hora_inicio, hora_fin FROM turno ORDER BY hora_inicio"
        cursor.execute(query_turnos)
        turnos = cursor.fetchall()
        
        # Obtener turnos ocupados para esa sala y fecha
        query_ocupados = """
            SELECT id_turno 
            FROM reserva 
            WHERE nombre_sala = %s 
            AND edificio = %s 
            AND fecha = %s 
            AND estado = 'activa'
        """
        cursor.execute(query_ocupados, (nombre_sala, edificio, fecha))
        ocupados = {row['id_turno'] for row in cursor.fetchall()}
        
        cursor.close()
        conn.close()
        
        # Filtrar turnos futuros si la fecha es hoy
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        hoy = datetime.now().date()
        hora_actual = datetime.now().time()
        
        resultado = []
        for turno in turnos:
            # Si es hoy, solo mostrar turnos futuros (al menos 1 hora adelante)
            if fecha_obj == hoy:
                hora_inicio = turno['hora_inicio']
                # Convertir a datetime.time si es necesario
                if isinstance(hora_inicio, str):
                    hora_inicio = datetime.strptime(hora_inicio, '%H:%M:%S').time()
                elif hasattr(hora_inicio, 'total_seconds'):  # timedelta
                    hora_inicio = (datetime.min + hora_inicio).time()
                
                # Calcular hora límite (hora actual + 1 hora)
                hora_limite = datetime.combine(fecha_obj, hora_actual)
                hora_limite = (hora_limite.hour + 1, hora_limite.minute)
                hora_limite_time = time(hora_limite[0] if hora_limite[0] < 24 else 23, hora_limite[1])
                
                if hora_inicio <= hora_limite_time:
                    continue  # Omitir turnos pasados o muy cercanos
            
            resultado.append({
                'id_turno': turno['id_turno'],
                'hora_inicio': str(turno['hora_inicio']),
                'hora_fin': str(turno['hora_fin']),
                'disponible': turno['id_turno'] not in ocupados
            })
        
        return resultado
        
    except mysql.connector.Error as err:
        print(f"Error al obtener disponibilidad: {err}")
        if conn:
            conn.close()
        return []


def crear_reserva_multiple(ci_participante, nombre_sala, edificio, id_turno_inicio, fecha, cantidad_participantes, cantidad_horas):

    if cantidad_horas not in [1, 2]:
        return "Solo se pueden reservar 1 o 2 horas consecutivas"
    
    conn = get_db_connection()
    if not conn:
        return "Error de conexión a la base de datos"
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Obtener turno inicial
        cursor.execute("SELECT hora_inicio, hora_fin FROM turno WHERE id_turno = %s", (id_turno_inicio,))
        turno_inicial = cursor.fetchone()
        if not turno_inicial:
            cursor.close()
            conn.close()
            return "Turno no encontrado"
        
        # Lista de turnos a reservar
        turnos_a_reservar = [id_turno_inicio]
        
        if cantidad_horas == 2:
            # Buscar el turno siguiente
            hora_fin_inicial = turno_inicial['hora_fin']
            cursor.execute(
                "SELECT id_turno FROM turno WHERE hora_inicio = %s",
                (hora_fin_inicial,)
            )
            turno_siguiente = cursor.fetchone()
            
            if not turno_siguiente:
                cursor.close()
                conn.close()
                return "No hay turno consecutivo disponible para reservar 2 horas"
            
            turnos_a_reservar.append(turno_siguiente['id_turno'])
        
        cursor.close()
        conn.close()
        
        # Validar y crear cada reserva
        resultados = []
        for id_turno in turnos_a_reservar:
            # Validar disponibilidad
            if sala_ocupada(nombre_sala, edificio, fecha, id_turno):
                return f"El turno {id_turno} ya está ocupado. No se puede completar la reserva de {cantidad_horas} hora(s)"
            
            # Crear la reserva individual
            resultado = crear_reserva(ci_participante, nombre_sala, edificio, id_turno, fecha, cantidad_participantes)
            
            if isinstance(resultado, str):  # Error
                return f"Error al reservar turno {id_turno}: {resultado}"
            
            resultados.append(resultado)
        
        # Resumen exitoso
        ids_reserva = [r['id_reserva'] for r in resultados]
        return {
            'mensaje': f"Reserva de {cantidad_horas} hora(s) creada exitosamente",
            'ids_reserva': ids_reserva,
            'cantidad_horas': cantidad_horas
        }
        
    except mysql.connector.Error as err:
        print(f"Error al crear reserva múltiple: {err}")
        return f"Error al crear reserva: {err}"

def cambiar_contraseña(correo, contraseña_actual, contraseña_nueva):

    conn = get_db_connection()
    if not conn:
        return "Error de conexión a la base de datos"
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Verificar contraseña actual
        query_verificar = "SELECT contraseña FROM login WHERE correo = %s"
        cursor.execute(query_verificar, (correo,))
        resultado = cursor.fetchone()
        
        if not resultado:
            cursor.close()
            conn.close()
            return "Usuario no encontrado"
        
        if resultado['contraseña'] != contraseña_actual:
            cursor.close()
            conn.close()
            return "Contraseña actual incorrecta"
        
        # Actualizar contraseña y marcar que ya no debe cambiarla
        query_actualizar = """
            UPDATE login 
            SET contraseña = %s, debe_cambiar_contraseña = FALSE 
            WHERE correo = %s
        """
        cursor.execute(query_actualizar, (contraseña_nueva, correo))
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
        
    except mysql.connector.Error as err:
        if conn:
            conn.close()
        return f"Error al cambiar contraseña: {err}"

def verificar_debe_cambiar_contraseña(correo):

    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT debe_cambiar_contraseña FROM login WHERE correo = %s"
        cursor.execute(query, (correo,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if resultado:
            return resultado['debe_cambiar_contraseña']
        return False
        
    except mysql.connector.Error as err:
        if conn:
            conn.close()
        return False






