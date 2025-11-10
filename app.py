from flask import Flask, request, jsonify, send_from_directory
from backend.logica import crear_reserva, crear_persona, eliminar_persona, modificar_persona
from backend.logica import crear_sancion, modificar_sancion, eliminar_sancion, levantar_sancion
from backend import reportes
from flask_cors import CORS
from backend.db_connection import get_db_connection, close_connection
import os
import inspect

app = Flask(__name__)
CORS(app)

@app.route("/api-status")
def index():
    return "Sistema de Reserva de Salas UCU - API activa"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT correo, contraseña, rol FROM login WHERE correo = %s AND contraseña = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        rol = user[2]
        return jsonify({"success": True, "rol": rol})
    else:
        return jsonify({"success": False, "message": "Credenciales incorrectas"}), 401

@app.route("/crear_reserva", methods=["POST"])
def api_crear_reserva():
    data = request.get_json()
    ci_participante = data.get("ci_participante")
    nombre_sala = data.get("nombre_sala")
    id_turno = data.get("id_turno")
    fecha = data.get("fecha")
    cantidad_participantes = data.get("cantidad_participantes")

    resultado = crear_reserva(ci_participante, nombre_sala, id_turno, fecha, cantidad_participantes)
    return jsonify({"resultado": resultado})

@app.route("/api/reportes", methods=["GET"])
def listar_reportes():
    try:
        # Nombres reales → nombres legibles
        nombres_reportes = {
            "salas_mas_reservadas": "Salas más reservadas",
            "turnos_mas_demandados": "Turnos más demandados",
            "promedio_participantes_por_sala": "Promedio de participantes por sala",
            "reservas_por_carrera_y_facultad": "Reservas por carrera y facultad",
            "porcentaje_ocupacion_por_edificio": "Porcentaje de ocupación por edificio",
            "reservas_y_asistencias_por_tipo_y_rol": "Reservas y asistencias por tipo y rol",
            "sanciones_por_tipo_y_rol": "Sanciones por tipo y rol",
            "porcentaje_reservas_utilizadas": "Porcentaje de reservas utilizadas"
        }

        # Tomar solo las funciones que estén en ese diccionario
        reportes_validos = [
            {"nombre": key, "titulo": value}
            for key, value in nombres_reportes.items()
            if hasattr(reportes, key)
        ]

        return jsonify({"reportes": reportes_validos})
    except Exception as e:
        return jsonify({"error": "Error al listar reportes", "details": str(e)}), 500
    
    
@app.route("/reportes/<nombre>", methods=["GET"])
def api_reportes(nombre):
    funcion = getattr(reportes, nombre, None)
    if not funcion:
        return jsonify({"error": "Reporte no encontrado"}), 404
    try:
        cols, rows = funcion()
        return jsonify({"columnas": cols, "filas": rows})
    except Exception as e:
        return jsonify({"error": "Error al generar el reporte", "details": str(e)}), 500

@app.route("/api/dashboard", methods=["GET"])
def dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) AS total FROM sala")
        total_salas = cursor.fetchone()["total"]
        cursor.execute("SELECT COUNT(*) AS total FROM reserva WHERE estado = 'activa'")
        reservas_activas = cursor.fetchone()["total"]
        cursor.execute("SELECT COUNT(*) AS total FROM participante")
        total_participantes = cursor.fetchone()["total"]
        cursor.execute("SELECT COUNT(*) AS total FROM sancion_participante WHERE fecha_fin >= CURDATE()")
        sanciones_activas = cursor.fetchone()["total"]
        result = {
            "total_salas": total_salas,
            "reservas_activas": reservas_activas,
            "total_participantes": total_participantes,
            "sanciones_activas": sanciones_activas
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Error al obtener estadísticas", "details": str(e)}), 500
    finally:
        cursor.close()
        close_connection(conn)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_static_files(path):
    if path.startswith("api"):
        return jsonify({"error": "Not Found"}), 404
    root_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(root_dir, "frontend/out")
    if path != "" and os.path.exists(os.path.join(build_dir, path)):
        return send_from_directory(build_dir, path)
    else:
        return send_from_directory(build_dir, "index.html")
    
@app.route("/api/edificios", methods=["GET"])
def obtener_edificios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre_edificio FROM edificio")
    edificios = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(edificios)

@app.route("/api/salas", methods=["GET"])
def obtener_salas():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre_sala, edificio, capacidad FROM sala")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    salas = [{"nombre": row[0], "edificio": row[1], "capacidad": row[2]} for row in data]
    return jsonify(salas)

@app.route("/api/participantes", methods=["GET"])
def obtener_participantes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ci, nombre, apellido, email FROM participante")
        data = cursor.fetchall()
        cursor.close()
        close_connection(conn)
        participantes = [{"ci": row[0], "nombre": row[1], "apellido": row[2], "email": row[3]} for row in data]
        return jsonify(participantes)
    except Exception as e:
        return jsonify({"error": "Error al obtener participantes", "details": str(e)}), 500

@app.route("/api/participantes", methods=["POST"])
def crear_participante():
    data = request.get_json()
    try:
        ci = data.get("ci")
        nombre = data.get("nombre")
        apellido = data.get("apellido")
        email = data.get("email")
        resultado = crear_persona(ci, nombre, apellido, email)
        return jsonify({"resultado": resultado})
    except Exception as e:
        return jsonify({"error": "Error al crear participante", "details": str(e)}), 400

@app.route("/api/participantes/<int:ci>", methods=["PUT"])
def modificar_participante(ci):
    data = request.get_json()
    try:
        nombre = data.get("nombre")
        apellido = data.get("apellido")
        email = data.get("email")
        resultado = modificar_persona(ci, nombre, apellido, email)
        return jsonify({"resultado": resultado})
    except Exception as e:
        return jsonify({"error": "Error al modificar participante", "details": str(e)}), 400

@app.route("/api/participantes/<int:ci>", methods=["DELETE"])
def eliminar_participante(ci):
    try:
        resultado = eliminar_persona(ci)
        return jsonify({"resultado": resultado})
    except Exception as e:
        return jsonify({"error": "Error al eliminar participante", "details": str(e)}), 400

# ------------------- SANCIONES -------------------

@app.route("/api/sanciones", methods=["GET"])
def listar_sanciones():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                s.ci_participante,
                p.nombre,
                p.apellido,
                DATE_FORMAT(s.fecha_inicio, '%Y-%m-%d') AS fecha_inicio,
                DATE_FORMAT(s.fecha_fin, '%Y-%m-%d') AS fecha_fin
            FROM sancion_participante s
            JOIN participante p ON s.ci_participante = p.ci
        """)
        sanciones = cursor.fetchall()
        close_connection(conn)
        return jsonify(sanciones), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/sanciones", methods=["POST"])
def crear_sancion_api():
    data = request.get_json()
    ci = data.get("ci_participante")
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")

    if not all([ci, fecha_inicio, fecha_fin]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    resultado = crear_sancion(ci, fecha_inicio, fecha_fin)
    if "correctamente" in resultado or isinstance(resultado, dict):
        return jsonify({"mensaje": resultado}), 201
    return jsonify({"error": resultado}), 400


@app.route("/api/sanciones/<int:ci>", methods=["PUT"])
def modificar_sancion_api(ci):
    data = request.get_json()
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")

    resultado = modificar_sancion(ci, fecha_inicio, fecha_fin)
    if "correctamente" in resultado:
        return jsonify({"mensaje": resultado}), 200
    return jsonify({"error": resultado}), 400


@app.route("/api/sanciones/<int:ci>", methods=["DELETE"])
def eliminar_sancion_api(ci):
    resultado = eliminar_sancion(ci)
    if "correctamente" in resultado:
        return jsonify({"mensaje": resultado}), 200
    return jsonify({"error": resultado}), 400




if __name__ == "__main__":
    app.run(debug=True)
