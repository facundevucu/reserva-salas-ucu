import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Establece y retorna una conexión a la base de datos MySQL."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', "localhost"),
            user=os.getenv('DB_USER', "root"),
            password=os.getenv('DB_PASSWORD', "rootpassword"),
            database=os.getenv('DB_NAME', "reserva_salas_ucu_db"),
            port=int(os.getenv('DB_PORT', 3306)),
            auth_plugin='mysql_native_password'  # 👈 fuerza el plugin correcto
        )
        if connection.is_connected():
            print("✅ Conexión exitosa a la base de datos MySQL")
            return connection
    except Error as e:
        print(f"❌ Error al conectar con MySQL: {e}")
        return None
    
def close_connection(connection):
    """Cierra la conexión con la base de datos si está abierta."""
    if connection and connection.is_connected():
        connection.close()

if __name__ == "__main__":
    conn = get_db_connection()
    if conn:
        print("Conexión verificada correctamente.")
        close_connection(conn)
    else:
        print("No se pudo establecer la conexión.")
