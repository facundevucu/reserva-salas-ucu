from flask import Flask, request, jsonify, send_from_directory
# ------------------- IMPORTACIONES -------------------
from backend.logica import (
    crear_reserva, 
    crear_persona, 
    eliminar_persona, 
    modificar_persona, 
    crear_sancion, 
    modificar_sancion, 
    eliminar_sancion, 
)
from backend.validaciones import (
    login_valido,
    autenticar_usuario,
    obtener_estadisticas_dashboard,
    obtener_edificios,
    obtener_salas,
    obtener_participantes,
    ci_valido,
    participante_valido,
    obtener_sanciones,
    sancion_valida,
)

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


# ------------------- AUTENTICACIÓN -------------------
# a partir de aqui se trabaja con la autenticación de usuarios
# se establece la ruta para el login de usuarios
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Validación del input
    if not login_valido(email, password):
        return jsonify("Datos de login inválidos")

    # Autenticación en base de datos
    rol = autenticar_usuario(email, password)
    if rol:
        return jsonify({"success": True, "rol": rol})
    else:
        return jsonify("Credenciales incorrectas")



# ------------------- DISEÑO DE INTERFAZ -------------------
# a partir de aqui se trabaja con las secciones de reportes y dashboard del frontend
# se establecen las rutas para los reportes y el dashboard

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
        return jsonify("Error al listar reportes.")
    
    
@app.route("/reportes/<nombre>", methods=["GET"])
def api_reportes(nombre):
    funcion = getattr(reportes, nombre, None)
    if not funcion:
        return jsonify("Reporte no encontrado")
    try:
        cols, rows = funcion()
        return jsonify({"columnas": cols, "filas": rows})
    except Exception as e:
        return jsonify("Error al generar el reporte")


@app.route("/api/dashboard", methods=["GET"])
def dashboard_stats():
    try:
        result = obtener_estadisticas_dashboard()
        return jsonify(result)
    except Exception as e:
        return jsonify("Error al obtener estadísticas.")
    

# ---------------------------------------------------------------------------------------------------------------------------
# bloque de codigo especial del frontend, sirve para que Flask muestre mi web en el navegador
# cuando alguien entra a la app, flask busca el archivo del frontend en /out y lo muestra
# si no lo encuentra muestra index.html que es la pagina principal
# y si alguien entra a una ruta que empieza con /api le tira un error 404 porque esas rutas son para la API solamente
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_static_files(path):
    if path.startswith("api"):
        return jsonify("Not Found")
    root_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(root_dir, "frontend/out")
    if path != "" and os.path.exists(os.path.join(build_dir, path)):
        return send_from_directory(build_dir, path)
    else:
        return send_from_directory(build_dir, "index.html")
# ---------------------------------------------------------------------------------------------------------------------------


# ------------------- EDIFICIOS Y SALAS -------------------
# a partir de aqui se trabaja con los edificios y las salas
# se establecen las rutas para listar edificios y salas
@app.route("/api/edificios", methods=["GET"])
def api_obtener_edificios():
    try:
        edificios = obtener_edificios()
        return jsonify(edificios)
    except Exception as e:
        return jsonify("Error al obtener edificios.")


@app.route("/api/salas", methods=["GET"])
def api_obtener_salas():
    try:
        salas = obtener_salas()
        return jsonify(salas)
    except Exception as e:
        return jsonify("Error al obtener salas.")


# ------------------- PARTICIPANTES -------------------
# a partir de aqui se trabaja con los participantes
# se establecen las rutas para listar, crear, modificar y eliminar participantes


@app.route("/api/participantes", methods=["GET"])
def api_obtener_participantes():
    try:
        participantes = obtener_participantes()
        return jsonify(participantes)
    except Exception as e:
        return jsonify("Error al obtener participantes.")


@app.route("/api/participantes", methods=["POST"])
def api_crear_participante():
    data = request.get_json()
    ci = data.get("ci")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")

    if not participante_valido(ci, nombre, apellido, email):
        return jsonify("Datos de participante inválidos")

    resultado = crear_persona(ci, nombre, apellido, email)

    if "correctamente" in resultado:
        return jsonify({"mensaje": resultado})
    else:
        return jsonify({"error": resultado})
    

@app.route("/api/participantes/<int:ci>", methods=["DELETE"])
def api_eliminar_participante(ci):
    if not ci_valido(ci):
        return jsonify("CI inválido")

    resultado = eliminar_persona(ci)

    if "correctamente" in resultado:
        return jsonify({"mensaje": resultado})
    elif "No se encontró" in resultado:
        return jsonify("No se encontró participante.")
    else:
        return jsonify("Error al eliminar participante.")



# ------------------- SANCIONES -------------------
# a partir de aqui se trabaja con las sanciones
# se establecen las rutas para listar, crear, modificar y eliminar sanciones

@app.route("/api/sanciones", methods=["GET"])
def api_listar_sanciones():
    try:
        sanciones = obtener_sanciones()
        return jsonify(sanciones)
    except Exception as e:
        return jsonify("Error al obtener sanciones.")


@app.route("/api/sanciones", methods=["POST"])
def api_crear_sancion():
    data = request.get_json()
    ci = data.get("ci_participante")
    motivo = data.get("motivo")
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")

    if not sancion_valida(ci, fecha_inicio, fecha_fin):
        return jsonify("Datos de sanción inválidos")

    resultado = crear_sancion(ci, motivo, fecha_inicio, fecha_fin)

    if "correctamente" in resultado:
        return jsonify({"mensaje": resultado})
    else:
        return jsonify("Error al crear sanción.")


@app.route("/api/sanciones/<int:ci>", methods=["PUT"])
def api_modificar_sancion(ci):
    data = request.get_json()
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")

    if not sancion_valida(ci, fecha_inicio, fecha_fin, verificar_solapamiento=False):
        return jsonify("Fechas inválidas")

    resultado = modificar_sancion(ci, fecha_inicio, fecha_fin)

    if "correctamente" in resultado:
        return jsonify({"mensaje": resultado})
    elif "No se encontró" in resultado:
        return jsonify("No se encontró sanción.")
    else:
        return jsonify("Error al modificar sanción.")


@app.route("/api/sanciones/<int:ci>", methods=["DELETE"])
def api_eliminar_sancion(ci):
    
    if not ci_valido(ci):
        return jsonify("CI inválido")

    resultado = eliminar_sancion(ci)

    if "correctamente" in resultado:
        return jsonify({"mensaje": resultado})
    elif "No se encontró" in resultado:
        return jsonify("No se encontró sanción.")
    else:
        return jsonify("Error al eliminar sanción.")



if __name__ == "__main__":
    app.run(debug=True)
