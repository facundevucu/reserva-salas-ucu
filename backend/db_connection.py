import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT", 3306) 
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
