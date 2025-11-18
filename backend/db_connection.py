import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

def get_db_connection(role: str = "user"):
    try:
        # Elegir credenciales según rol, con fallback a DB_USER/DB_PASSWORD
        host = os.getenv("DB_HOST", "mysql")
        database = os.getenv("DB_NAME")
        port = int(os.getenv("DB_PORT", 3306))

        if role == "admin":
            user = os.getenv("DB_USER_ADMIN") or os.getenv("DB_USER")
            password = os.getenv("DB_PASS_ADMIN") or os.getenv("DB_PASSWORD")
        else:
            user = os.getenv("DB_USER_USER") or os.getenv("DB_USER")
            password = os.getenv("DB_PASS_USER") or os.getenv("DB_PASSWORD")

        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            charset='utf8mb4', #para los tildes y ñ       
            collation='utf8mb4_unicode_ci',  # para los tildes tambien
            use_unicode=True
        )

        if connection.is_connected():
            # Activar roles y configurar encoding para cada sesión
            try:
                cur = connection.cursor()
                cur.execute("SET ROLE DEFAULT")  # Activa los roles asignados
                cur.execute("SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci")  # Fix encoding
                cur.close()
            except Exception:
                pass  # Ignorar errores si el usuario no tiene roles
            
            # print(" Conexión exitosa a la base de datos MySQL")  # Comentado para evitar spam
            return connection
    except Error as e:
        print(f" Error al conectar con MySQL: {e}")
        return None
    
def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()

def get_db_connection_user():
    return get_db_connection("user")


def get_db_connection_admin():
    return get_db_connection("admin")


if __name__ == "__main__":
    conn = get_db_connection_user()
    if conn:
        print("Conexión verificada correctamente.")
        close_connection(conn)
    else:
        print("No se pudo establecer la conexión.")
