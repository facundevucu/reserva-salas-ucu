import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database= "reserva_salas_ucu_db",
            port= 3306,
            auth_plugin='mysql_native_password'  
        )
        if connection.is_connected():
            # print(" Conexión exitosa a la base de datos MySQL")  # Comentado para evitar spam
            return connection
    except Error as e:
        print(f" Error al conectar con MySQL: {e}")
        return None
    
def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()

if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        print("Conexión verificada correctamente.")
        close_connection(conn)
    else:
        print("No se pudo establecer la conexión.")
