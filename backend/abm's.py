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
        conn.commit()
        conn.close()
        registrar_log(ci_participante, accion, "éxito", f"Reserva creada (ID {id_reserva})")
        return {"id_reserva": id_reserva, "mensaje": "Reserva creada exitosamente."}
    
    except Exception as e:
        # Si hay un error, hago rollback y registro el log
        if conn:
            conn.rollback()
        registrar_log(ci_participante, accion, "error", f"Error SQL: {e}")
        print("Error MySQL:", e)
        return "Ocurrió un error al crear la reserva. Intente nuevamente más tarde."
    
    finally:
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

def modificar_reserva(id_reserva, nombre_sala = None, fecha = None, id_turno = None, estado = None):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        campos = []
        #campos a modificar
        valores = []
        #valores a agregar

        if nombre_sala:
            campos.append("nombre_sala = %s")
            valores.append(nombre_sala)
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
        cursor.execute(sql, valores)
        connection.commit()

        registrar_log(None, "modificar_reserva", "exito", f"Reserva {id_reserva} modificada con exito.")
        return f"Reserva {id_reserva} modificada correctamenet."
    
    except Error as e:
        registrar_log(None, "modificar_reserva", "error", f"Error al modificar la reserva {id_reserva}.")
        return f"Error al modificar la reserva {e}."
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()