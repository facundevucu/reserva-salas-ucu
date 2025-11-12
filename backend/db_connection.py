# backend/db_connection.py
import os
import mysql.connector
from mysql.connector import Error

# Lee variables de entorno si existen; usa defaults útiles en local
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD","Manya1906")
DB_NAME = os.getenv("DB_NAME", "reserva_salas_ucu_db")

def get_db_connection():
    """
    Devuelve SIEMPRE una conexión válida o levanta una excepción clara.
    NUNCA retorna None.
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            autocommit=False,
            auth_plugin="mysql_native_password",  # útil en Windows/WAMP/XAMPP
        )
        if not conn.is_connected():
            raise Error("Conexión creada pero no conectada (is_connected=False)")
        return conn
    except Exception as e:
        # Re-lanzar con contexto; app.py lo capturará y devolverá JSON
        raise RuntimeError(
            f"Error conectando a MySQL ({DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}): {e}"
        )

def close_connection(conn):
    try:
        if conn and conn.is_connected():
            conn.close()
    except Exception:
        pass
