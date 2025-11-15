from db_connection import get_db_connection, close_connection
from mysql.connector import Error

def registrar_log(ci_participante, accion, detalle, estado="exitoso"):
    """Registra una acción en el log."""
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO log (ci_participante, accion, estado, detalle)
            VALUES (%s, %s, %s, %s)
        """
        # Si ci_participante no es numérico o es None, usar NULL
        ci_value = None
        if ci_participante:
            try:
                ci_value = int(ci_participante)
            except (ValueError, TypeError):
                ci_value = None
        
        cursor.execute(query, (ci_value, accion, estado, detalle))
        conn.commit()
        cursor.close()
        conn.close()
    except Error as err:
        print(f"Error al registrar log: {err}")
        if conn:
            conn.close()
