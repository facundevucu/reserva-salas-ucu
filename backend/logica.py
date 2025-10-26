from backend.db_connection import get_db_connection, close_connection
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



def crear_reserva(ci_participante, nombre_sala, id_turno, fecha, cantidad_participantes):
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
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado)
        VALUES (
            %s,
            (SELECT edificio FROM sala WHERE nombre_sala = %s),
            %s, 
            %s, 
            'activa');
    """
    # Para el edificio se hace un subquery, ya que no es un input del usuario
    cursor.execute(query, (nombre_sala, nombre_sala, fecha, id_turno))
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
    return "Reserva creada exitosamente."