from flask import Flask, request, jsonify
from backend.logica import crear_reserva
from backend import reportes
from flask_cors import CORS
from backend.db_connection import get_db_connection

app = Flask(__name__)
CORS(app)

@app.route("/")
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

@app.route("/reportes/<nombre>", methods=["GET"])
def api_reportes(nombre):
    if nombre == "salas_mas_reservadas":
        resultado = reportes.salas_mas_reservadas()
    elif nombre == "turnos_mas_demandados":
        resultado = reportes.turnos_mas_demandados()
    elif nombre == "promedio_participantes_por_sala":
        resultado = reportes.promedio_participantes_por_sala()
    elif nombre == "reservas_por_carrera_y_facultad":
        resultado = reportes.reservas_por_carrera_y_facultad()
    elif nombre == "porcentaje_ocupacion_por_edificio":
        resultado = reportes.porcentaje_ocupacion_por_edificio()
    elif nombre == "reservas_y_asistencias_por_tipo_y_rol":
        resultado = reportes.reservas_y_asistencias_por_tipo_y_rol()
    elif nombre == "sanciones_por_tipo_y_rol":
        resultado = reportes.sanciones_por_tipo_y_rol()
    elif nombre == "porcentaje_reservas_utilizadas":
        resultado = reportes.porcentaje_reservas_utilizadas()
    else:
        return jsonify({"error": "Reporte no encontrado"}), 404

    return jsonify({"resultado": resultado})

if __name__ == "__main__":
    app.run(debug=True)
