from backend.db_connection import get_db_connection, close_connection
from mysql.connector import Error
from backend.logs import registrar_log
from backend.validaciones import (
    tiene_sancion_activa,
    excede_reservas_semanales,
    excede_horas_diarias,
    sala_ocupada,
    excede_capacidad,
    validar_tipo_sala,
    fecha_valida
)

#ABM de RESERVAS (creacion, eliminacion, modificacion)--------------------------------

def crear_reserva(ci_participante, nombre_sala, id_turno, fecha, cantidad_participantes, estado = "activa"):
    accion = "Crear reserva"
    
    if not fecha_valida(fecha):
        registrar_log(ci_participante, accion, "error", "Fecha inválida")
        return "La fecha seleccionada no es válida."
    
    if tiene_sancion_activa(ci_participante):
        registrar_log(ci_participante, accion, "error", "Sanción activa")
        return "El participante tiene una sanción activa."

    if excede_reservas_semanales(ci_participante):
        registrar_log(ci_participante, accion, "error", "Excede reservas semanales")
        return "El participante ha excedido el límite de reservas semanales."

    if excede_horas_diarias(ci_participante, fecha):
        registrar_log(ci_participante, accion, "error", "Excede horas diarias")
        return "El participante ha excedido el límite de horas diarias."

    if sala_ocupada(nombre_sala, id_turno, fecha):
        registrar_log(ci_participante, accion, "error", "Sala ocupada")
        return "La sala está ocupada en el turno y fecha seleccionados."

    if excede_capacidad(nombre_sala, cantidad_participantes):
        registrar_log(ci_participante, accion, "error", "Excede capacidad")
        return "La cantidad de personas excede la capacidad de la sala."

    if not validar_tipo_sala(nombre_sala, ci_participante):
        registrar_log(ci_participante, accion, "error", "Tipo de sala no autorizado")
        return "El participante no está autorizado para reservar este tipo de sala."

    # Si pasa todas las validaciones, proceder a crear la reserva
    # Implementación de manejo de errores

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado)
            VALUES (
                %s,
                (SELECT edificio FROM sala WHERE nombre_sala = %s),
                %s, 
                %s, 
                %s);
        """
        # Para el edificio se hace un subquery, ya que no es un input del usuario
        cursor.execute(query, (nombre_sala, nombre_sala, fecha, id_turno, estado))
        id_reserva = cursor.lastrowid # Guarda el id de la reserva recién creada

        # Ahora insertto al participante en la tabla reserva_participante
        query_participante = """
            INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia)
            VALUES (%s, %s, CURDATE(), NULL);
        """
        cursor.execute(query_participante, (ci_participante, id_reserva))        
        conn.commit() # confirma y guarda la reserva y el participante
        conn.close()  #cierra la conexion a la base de datos
        registrar_log(ci_participante, accion, "éxito", f"Reserva creada (ID {id_reserva})")
        return {"id_reserva": id_reserva, "mensaje": "Reserva creada exitosamente."}
    
    except Exception as e:
        # Si hay un error, hago rollback y registro el log
        if conn:
            conn.rollback()
        registrar_log(ci_participante, accion, "error", f"Error SQL: {e}")
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
            registrar_log(None, "eliminar_reserva", "exito", f"Reserda {id_reserva} cancelada correctamente")
            return f"Reserva {id_reserva} cancelada correctamente."
        else: 
            registrar_log(None, "eliminar_reserva", "error", f"No se encontro la reserva {id_reserva}")
            return f"No se encontro la reserva con ID {id_reserva}."
        
    except Error as e:
        registrar_log("eliminar reserva", "error", f"Error al cancelar reserva {id_reserva}")
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
            registrar_log("modificar_reserva", "error", f"No se proporcionaron campos a modificar para reserva {id_reserva}")
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

        registrar_log(None, "modificar_reserva", "exito", f"Reserva {id_reserva} modificada con exito.")
        return f"Reserva {id_reserva} modificada correctamente."
    
    except Error as e:
        registrar_log(None, "modificar_reserva", "error", f"Error al modificar la reserva {id_reserva}.")
        return f"Error al modificar la reserva {e}."
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


#ABM de PERSONAS (creacion, eliminacion, modificacion)--------------------------------
def crear_persona(ci_participante, nombre, apellido, email):
    accion = "crear_persona" #sirve para el log
    connection = None # para garantizar el cierre de conexion
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        # sql = query
        sql = """
            INSERT INTO participante (ci_participante, nombre, apellido, email)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (ci_participante, nombre, apellido, email)) # ejecuta la query con las variables indicadas
        connection.commit() # confirma y guarda los cambios

        registrar_log(ci_participante, accion, "exito", f"Persona {ci_participante} creada correctamente")
        # es exitosa porque esta dentro del try, si hubiera un error saltaria al except
        return {"ci_participante": ci_participante, "mensaje": "Persona creada correctamente."}
    except Error as e:
        if connection:
            connection.rollback() #revierte los cambios durante la transaccion (ctrl + z si detecta error)
        registrar_log(ci_participante, accion, "error", f"Error al crear persona: {e}")
        return f"Error al crear la persona: {e}" #nos indica que fallo debido a la libreria Error
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def eliminar_persona(ci_participante):
    accion = "eliminar_persona"  # se utilizara mas tarde para el log
    connection = None
    try:
        connection = get_db_connection() #importa credenciales desde db_connection.py
        cursor = connection.cursor()

        # sql = query
        sql = "DELETE FROM participante WHERE ci_participante = %s"
        cursor.execute(sql, (ci_participante,))
        connection.commit()  # confirma y guarda los cambios

        #uso rowcount, el cual abarca el DELETE, UPDATE y INSERT
        if cursor.rowcount > 0: # porque pueden NO haber coincidencias en el where
            registrar_log(ci_participante, accion, "exito", f"Persona {ci_participante} eliminada correctamente")
            return f"Persona {ci_participante} eliminada correctamente."
        else:
            registrar_log(ci_participante, accion, "error", f"No se encontró persona {ci_participante}")
            return f"No se encontró persona con CI {ci_participante}."
    except Error as e:
        if connection:
            connection.rollback()  # revierte los cambios si falla
        registrar_log(ci_participante, accion, "error", f"Error al eliminar persona: {e}")
        return f"Error al eliminar persona: {e}"
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close() #cierro conexion


# aca se repite la estructura de modificar_reserva pero adaptada a persona
# para modificar la persona siempre tengo que indicar la ci_participante, y el/los campos a modificar con su nuevo valor
def modificar_persona(ci_participante, nombre=None, apellido=None, email=None):
    accion = "modificar_persona"
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
            registrar_log(ci_participante, accion, "error", f"No se proporcionaron campos a modificar para {ci_participante}")
            return "No se proporcionaron datos para modificar."

        valores.append(ci_participante)
        sql = f"UPDATE participante SET {', '.join(campos)} WHERE ci_participante = %s"
        # lo mismo que antes pero con la cedula, antes era con el id
        cursor.execute(sql, valores)
        connection.commit()

        registrar_log(ci_participante, accion, "exito", f"Persona {ci_participante} modificada correctamente")
        return f"Persona {ci_participante} modificada correctamente."
    except Error as e:
        if connection:
            connection.rollback()
        registrar_log(ci_participante, accion, "error", f"Error al modificar persona: {e}")
        return f"Error al modificar persona: {e}"
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()




#ABM de SALAS (creacion, eliminacion, modificacion)--------------------------------
def crear_sala(nombre_sala, edificio, capacidad, tipo_sala):
    accion = "crear_sala" # sirve para el log
    connection = None # verifica que no se quede abierta la conexion en caso de error

    if not isinstance(capacidad, int) or capacidad <= 0:
        registrar_log(None, accion, "error", f"Capacidad inválida para sala '{nombre_sala}'")
        return "La capacidad debe ser un número entero positivo."
    # verifico que la capacidad sea correcta, si no lo es retorno el error desde ya

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = """
            INSERT INTO sala (nombre_sala, edificio, capacidad, tipo_sala)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre_sala, edificio, capacidad, tipo_sala))
        connection.commit()  # guarda los cambios

        # es none porque la sala no tiene identificasdor unico como la cedula o el id_reserva
        # esto porque el log necesita un id, la accion, el estado y el detalle
        registrar_log(None, accion, "exito", f"Sala '{nombre_sala}' en edificio '{edificio}' creada correctamente.")
        return f"Sala '{nombre_sala}' creada correctamente en el edificio '{edificio}'."
    except Error as e:
        if connection:
            connection.rollback()  # deshace si algo falla
        # igual que arriba
        registrar_log(None, accion, "error", f"Error al crear sala: {e}")
        return f"Error al crear sala: {e}"
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()



def eliminar_sala(nombre_sala, edificio):
    accion = "eliminar_sala" # sirve para el log
    connection = None # verifica que no se quede abierta la conexion en caso de error
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # sql = query
        sql = "DELETE FROM sala WHERE nombre_sala = %s AND edificio = %s"
        cursor.execute(sql, (nombre_sala, edificio))
        connection.commit() # confirma y guarda los cambios

        if cursor.rowcount > 0: # esto indica la cantidad de filas afectadas por la instruccion
            # otra vez none porque la sala no tiene id unico, rellena el campo de id en el log
            registrar_log(None, accion, "exito", f"Sala '{nombre_sala}' del edificio '{edificio}' eliminada correctamente.")
            return f"Sala '{nombre_sala}' del edificio '{edificio}' eliminada correctamente."
        else:
            # none para el id tambien
            registrar_log(None, accion, "error", f"No se encontró la sala '{nombre_sala}' en el edificio '{edificio}'.")
            return f"No se encontró la sala '{nombre_sala}' en el edificio '{edificio}'."
    except Error as e:
        if connection:
            connection.rollback() # vuelve al estado anterior si falla(ctrl + z)
        #otra vez none para el id
        registrar_log(None, accion, "error", f"Error al eliminar sala: {e}")
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
        registrar_log(None, "modificar_sala", "error", f"Capacidad inválida: {capacidad}")
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
            registrar_log(None, accion, "error", f"No se proporcionaron campos a modificar para sala '{nombre_sala}'")
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
            registrar_log(None, accion, "exito", f"Sala '{nombre_sala}' modificada correctamente.")
            return f"Sala '{nombre_sala}' modificada correctamente."
        else:
            registrar_log(None, accion, "error", f"No se encontró la sala '{nombre_sala}' en el edificio '{edificio}'.")
            return f"No se encontró la sala '{nombre_sala}' en el edificio '{edificio}'."
    
    except Error as e:
        if connection:
            connection.rollback() # vuelve al estado anterior si falla(ctrl + z)
        registrar_log(None, accion, "error", f"Error al modificar sala: {e}")
        return f"Error al modificar sala: {e}"
    
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            


# ABM de SANCIONES (creación, baja, odificación) -----------------------


from backend.db_connection import get_db_connection, close_connection
from mysql.connector import Error
from backend.logs import registrar_log
from backend.validaciones import (
    tiene_sancion_activa,
    fecha_valida
)

def crear_sancion(ci_participante, motivo, fecha_inicio, fecha_fin=None, estado="activa"):
    """
    Crea una sanción para un participante.
    - Valida fechas, orden cronológico y que no exista una sanción activa simultánea.
    - Por defecto crea en estado 'activa'.
    """
    accion = "crear_sancion"
    conn = None

    # Validaciones de negocio
    if not fecha_valida(fecha_inicio) or (fecha_fin and not fecha_valida(fecha_fin)):
        registrar_log(ci_participante, accion, "error", "Fecha(s) inválida(s)")
        return "Alguna de las fechas indicadas no es válida."

    if fecha_fin and fecha_fin < fecha_inicio:
        registrar_log(ci_participante, accion, "error", "Rango de fechas inválido")
        return "La fecha de fin no puede ser anterior a la fecha de inicio."

    if tiene_sancion_activa(ci_participante):
        registrar_log(ci_participante, accion, "error", "Sanción ya activa")
        return "El participante ya tiene una sanción activa."

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO sancion (ci_participante, motivo, fecha_inicio, fecha_fin, estado)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (ci_participante, motivo, fecha_inicio, fecha_fin, estado))
        conn.commit()
        id_sancion = cursor.lastrowid

        registrar_log(ci_participante, accion, "éxito", f"Sanción creada (ID {id_sancion})")
        return {"id_sancion": id_sancion, "mensaje": "Sanción creada correctamente."}

    except Exception as e:
        if conn:
            conn.rollback()
        registrar_log(ci_participante, accion, "error", f"Error SQL: {e}")
        return f"Ocurrió un error al crear la sanción: {e}"

    finally:
        if conn and conn.is_connected():
            close_connection(conn)


def levantar_sancion(id_sancion):
    """
    Levanta (finaliza) una sanción: pasa a 'inactiva' y fija fecha_fin = CURDATE().
    No borra el registro para conservar trazabilidad.
    """
    accion = "levantar_sancion"
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = """
            UPDATE sancion
            SET estado = 'inactiva', fecha_fin = CURDATE()
            WHERE id_sancion = %s AND estado = 'activa'
        """
        cursor.execute(sql, (id_sancion,))
        connection.commit()

        if cursor.rowcount > 0:
            registrar_log(None, accion, "éxito", f"Sanción {id_sancion} levantada")
            return f"Sanción {id_sancion} levantada correctamente."
        else:
            registrar_log(None, accion, "error", f"No se pudo levantar sanción {id_sancion}")
            return "No se encontró una sanción activa con ese ID."

    except Error as e:
        if connection:
            connection.rollback()
        registrar_log(None, accion, "error", f"Error al levantar sanción {id_sancion}: {e}")
        return f"Error al levantar la sanción: {e}"

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def eliminar_sancion(id_sancion):
    """
    Baja lógica de la sanción (marca 'anulada'). Si preferís borrado físico, cambia por DELETE.
    """
    accion = "eliminar_sancion"
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql = "UPDATE sancion SET estado = 'anulada' WHERE id_sancion = %s"
        cursor.execute(sql, (id_sancion,))
        connection.commit()

        if cursor.rowcount > 0:
            registrar_log(None, accion, "éxito", f"Sanción {id_sancion} anulada")
            return f"Sanción {id_sancion} anulada correctamente."
        else:
            registrar_log(None, accion, "error", f"No existe sanción {id_sancion}")
            return f"No se encontró sanción con ID {id_sancion}."

    except Error as e:
        if connection:
            connection.rollback()
        registrar_log(None, accion, "error", f"Error al anular sanción {id_sancion}: {e}")
        return f"Error al anular la sanción: {e}"

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def modificar_sancion(id_sancion, motivo=None, fecha_inicio=None, fecha_fin=None, estado=None):
    """
    Modifica campos de la sanción. Valida fechas si se pasan y orden cronológico.
    """
    accion = "modificar_sancion"
    connection = None

    # Validaciones simples de fechas si vienen informadas
    if fecha_inicio and not fecha_valida(fecha_inicio):
        registrar_log(None, accion, "error", f"fecha_inicio inválida para sanción {id_sancion}")
        return "La fecha de inicio no es válida."
    if fecha_fin and not fecha_valida(fecha_fin):
        registrar_log(None, accion, "error", f"fecha_fin inválida para sanción {id_sancion}")
        return "La fecha de fin no es válida."
    if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
        registrar_log(None, accion, "error", f"Rango de fechas inválido en sanción {id_sancion}")
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
            # Validar estados permitidos si querés: activa/inactiva/anulada
            campos.append("estado = %s")
            valores.append(estado)

        if not campos:
            registrar_log(None, accion, "error", f"Sin campos a modificar en sanción {id_sancion}")
            return "No se proporcionaron datos para modificar."

        valores.append(id_sancion)
        sql = f"UPDATE sancion SET {', '.join(campos)} WHERE id_sancion = %s"
        cursor.execute(sql, valores)
        connection.commit()

        registrar_log(None, accion, "éxito", f"Sanción {id_sancion} modificada")
        return f"Sanción {id_sancion} modificada correctamente."

    except Error as e:
        if connection:
            connection.rollback()
        registrar_log(None, accion, "error", f"Error al modificar sanción {id_sancion}: {e}")
        return f"Error al modificar la sanción: {e}"

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()






