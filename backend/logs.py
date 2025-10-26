from backend.db_connection import get_db_connection, close_connection

def registrar_log(ci_participante, accion, estado, detalle=None):
    """Guarda una acción del usuario en la tabla log_acciones."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO log_acciones (ci_participante, accion, estado, detalle)
        VALUES (%s, %s, %s, %s);
    """
    cursor.execute(query, (ci_participante, accion, estado, detalle))
    conn.commit()
    close_connection(conn)
