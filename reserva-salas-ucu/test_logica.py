from backend.logica import crear_reserva, modificar_reserva, eliminar_reserva
from backend.db_connection import get_db_connection

def registrar_log_manual(ci_participante, accion, estado, detalle):
    # Inserta un registro válido en log_acciones para evitar error de FK."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO log_acciones (ci_participante, accion, estado, detalle)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (ci_participante, accion, estado, detalle))
    conn.commit()
    conn.close()

def mostrar_reservas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_reserva, nombre_sala, fecha, id_turno, estado FROM reserva ORDER BY id_reserva;")
    reservas = cursor.fetchall()
    conn.close()
    return reservas

def test_abm_reservas():
    print("Ejecutando test de alta/baja/modificacion de reservas")

    ci_participante = 12345678
    nombre_sala = "Sala B1"
    id_turno = 1
    fecha = "2025-11-20"
    cantidad_participantes = 3
    estado = "activa"


    resultado = crear_reserva(ci_participante, nombre_sala, id_turno, fecha, cantidad_participantes, estado)
    print("Resultado:", resultado)
    id_nueva = resultado.get("id_reserva") if isinstance(resultado, dict) else None
    #Si crear_reserva devolvio un diccionario, agarra el valor de id_reserva, sino deja id_nueva como none
    #la funcion isinstance pregunta si resultado es el diccionario
    if not id_nueva:
        print(" No se creo la reserva. Test detenido.")
        return
    registrar_log_manual(ci_participante, "crear_reserva", "exito", f"Reserva {id_nueva} creada en test.")

    #Muestro las reservas actuales para evr si esta la que yo cree
    #muestro los 3 ultimos con [-3:]
    for r in mostrar_reservas()[-3:]:
        print(r)

    #Modifico el estado a cancelada
    resultado_cancelada = modificar_reserva(id_nueva, "cancelada")
    print("Resultado:", resultado_cancelada)
    registrar_log_manual(ci_participante, "modificar_reserva", "exito", f"Reserva {id_nueva} modificada en test.")

    #Verifico que se modifico (la primer reserva tiene que ser la nueva)
    for r in mostrar_reservas():
        if r[0] == id_nueva:
            print("->", r)

    #Elimino la reserva
    resultado_eliminada = eliminar_reserva(id_nueva)
    print("Resultado:", resultado_eliminada)
    registrar_log_manual(ci_participante, "eliminar_reserva", "exito", f"Reserva {id_nueva} eliminada en test.")

    #Verifico eliminacion
    ids_actuales = [r[0] for r in mostrar_reservas()]
    print("el id sigue en la base de datos?:", id_nueva in ids_actuales)

if __name__ == "__main__":
    test_abm_reservas()
