from backend.db_connection import get_db_connection, close_connection

def registrar_log(ci_participante, accion, estado, detalle=None):
    """Guarda una acción del usuario en la tabla log_acciones."""
    conn = get_db_connection()
    cursor = conn.cursor()

    if ci_participante is None:
        ci_participante = 0
        # Esto lo hago, para que la administracion pueda hacer cambios solo con el id_reserva
        # y no precise el documento, y que aun asi, se pueda hacer un registro del cambio

    query = """
        INSERT INTO log_acciones (ci_participante, accion, estado, detalle)
        VALUES (%s, %s, %s, %s);
    """
    cursor.execute(query, (ci_participante, accion, estado, detalle))
    conn.commit()
    cursor.close()
    close_connection(conn)
