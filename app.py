from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# ---------- IMPORTS PROPIOS (tus módulos) ----------
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
    obtener_participantes,
    ci_valido,
    participante_valido,
    obtener_sanciones,
    sancion_valida,
)
from backend import reportes
from backend.db_connection import get_db_connection, close_connection

# ---------- APP ----------
app = Flask(__name__)
CORS(app)

@app.route("/api-status")
def index():
    return "Sistema de Reserva de Salas UCU - API activa"

# ===========================================================
#                      AUTENTICACIÓN
#   Tabla real: login(correo, contraseña, rol)
# ===========================================================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    password = (data.get("password") or "").strip()

    if not email or not password:
        return jsonify({"success": False, "error": "Faltan email o contraseña."}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "No se pudo abrir conexión a BD."}), 500

    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT rol
            FROM login
            WHERE correo = %s AND `contraseña` = %s
            LIMIT 1
        """, (email, password))
        row = cur.fetchone()

        if row:
            return jsonify({"success": True, "rol": row["rol"]}), 200

        return jsonify({"success": False, "error": "Credenciales incorrectas"}), 401

    except Exception as e:
        print("ERROR /login:", e)
        return jsonify({"success": False, "error": "Error interno en el login"}), 500
    finally:
        close_connection(conn)

# ---------- REGISTRO DE USUARIOS (PERSISTENTE) ----------
@app.route("/register", methods=["POST"])
def register():
    """
    Crea una cuenta en la tabla login (correo, contraseña, rol).
    Rol por defecto: 'usuario'.
    """
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip()
    password = (data.get("password") or "").strip()
    nombre = (data.get("nombre") or "").strip()   # hoy no lo usamos en BD, pero lo recibimos

    if not email or not password:
        return jsonify({"success": False, "error": "Faltan email o contraseña."}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"success": False, "error": "No se pudo abrir conexión a BD."}), 500

    try:
        cur = conn.cursor(dictionary=True)
        # ¿ya existe?
        cur.execute("SELECT 1 FROM login WHERE correo=%s LIMIT 1", (email,))
        if cur.fetchone():
            return jsonify({"success": False, "error": "El correo ya está registrado."}), 409

        # Inserta el usuario (texto plano como tu esquema actual)
        cur.execute("""
            INSERT INTO login (correo, `contraseña`, rol)
            VALUES (%s, %s, 'usuario')
        """, (email, password))
        conn.commit()

        return jsonify({"success": True, "rol": "usuario"}), 201

    except Exception as e:
        print("ERROR /register:", e)
        conn.rollback()
        return jsonify({"success": False, "error": "Error registrando usuario."}), 500
    finally:
        close_connection(conn)

# ===========================================================
#                   REPORTES / DASHBOARD
# ===========================================================
@app.route("/crear_reserva", methods=["POST"])
def api_crear_reserva_legacy():
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
        reportes_validos = [{"nombre": k, "titulo": v} for k, v in nombres_reportes.items() if hasattr(reportes, k)]
        return jsonify({"reportes": reportes_validos})
    except Exception as e:
        print("listar_reportes:", e)
        return jsonify({"error": "Error al listar reportes."}), 500

@app.route("/reportes/<nombre>", methods=["GET"])
def api_reportes(nombre):
    funcion = getattr(reportes, nombre, None)
    if not funcion:
        return jsonify({"error": "Reporte no encontrado"}), 404
    try:
        cols, rows = funcion()
        return jsonify({"columnas": cols, "filas": rows})
    except Exception as e:
        print("api_reportes:", e)
        return jsonify({"error": "Error al generar el reporte"}), 500

@app.route("/api/dashboard", methods=["GET"])
def dashboard_stats():
    try:
        return jsonify(obtener_estadisticas_dashboard())
    except Exception as e:
        print("dashboard_stats:", e)
        return jsonify({"error": "Error al obtener estadísticas."}), 500

# ===========================================================
#                      SERVIR FRONTEND BUILD
# ===========================================================
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

# ===========================================================
#                   EDIFICIOS / SALAS
# ===========================================================
@app.route("/api/edificios", methods=["GET"])
def api_obtener_edificios():
    try:
        return jsonify(obtener_edificios())
    except Exception as e:
        print("api_obtener_edificios:", e)
        return jsonify({"error": "Error al obtener edificios."}), 500

@app.route("/api/salas", methods=["GET"])
def api_obtener_salas():
    from backend.db_connection import get_db_connection, close_connection
    conn = get_db_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT nombre_sala, edificio, capacidad, tipo_sala
            FROM sala
            ORDER BY edificio, nombre_sala
        """)
        rows = cur.fetchall()
        out = [{
            "id": f"{r['nombre_sala']}|{r['edificio']}",
            "nombre": f"{r['nombre_sala']} ({r['edificio']})",
            "capacidad": r["capacidad"],
            "tipo": r["tipo_sala"],
            "nombre_sala": r["nombre_sala"],
            "edificio": r["edificio"],
        } for r in rows]
        return jsonify(out)
    except Exception as e:
        print("api_obtener_salas:", e)
        return jsonify({"error": "Error al obtener salas."}), 500
    finally:
        close_connection(conn)

# ===========================================================
#                   PARTICIPANTES
# ===========================================================
@app.route("/api/participantes", methods=["GET"])
def api_obtener_participantes():
    try:
        return jsonify(obtener_participantes())
    except Exception as e:
        print("api_obtener_participantes:", e)
        return jsonify({"error": "Error al obtener participantes."}), 500

@app.route("/api/participantes", methods=["POST"])
def api_crear_participante():
    data = request.get_json()
    ci = data.get("ci")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")
    if not participante_valido(ci, nombre, apellido, email):
        return jsonify({"error": "Datos de participante inválidos"}), 400
    resultado = crear_persona(ci, nombre, apellido, email)
    if "correctamente" in resultado:
        return jsonify({"mensaje": resultado})
    return jsonify({"error": resultado}), 400

@app.route("/api/participantes/<int:ci>", methods=["DELETE"])
def api_eliminar_participante(ci):
    if not ci_valido(ci):
        return jsonify({"error": "CI inválido"}), 400
    resultado = eliminar_persona(ci)
    if "correctamente" in resultado:
        return jsonify({"mensaje": resultado})
    elif "No se encontró" in resultado:
        return jsonify({"error": "No se encontró participante."}), 404
    return jsonify({"error": "Error al eliminar participante."}), 500

# ===========================================================
#                        SANCIONES
# ===========================================================
@app.route("/api/sanciones", methods=["GET"])
def api_listar_sanciones():
    try:
        return jsonify(obtener_sanciones())
    except Exception as e:
        print("api_listar_sanciones:", e)
        return jsonify({"error": "Error al obtener sanciones."}), 500

@app.route("/api/sanciones", methods=["POST"])
def api_crear_sancion():
    data = request.get_json()
    ci = data.get("ci_participante")
    motivo = data.get("motivo")
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")
    if not sancion_valida(ci, fecha_inicio, fecha_fin):
        return jsonify({"error": "Datos de sanción inválidos"}), 400
    resultado = crear_sancion(ci, motivo, fecha_inicio, fecha_fin)
    if "correctamente" in resultado:
        return jsonify({"mensaje": resultado})
    return jsonify({"error": "Error al crear sanción."}), 500

@app.route("/api/sanciones/<int:ci>", methods=["PUT"])
def api_modificar_sancion(ci):
    data = request.get_json()
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")
    if not sancion_valida(ci, fecha_inicio, fecha_fin, verificar_solapamiento=False):
        return jsonify({"error": "Fechas inválidas"}), 400
    resultado = modificar_sancion(ci, fecha_inicio, fecha_fin)
    if "correctamente" in resultado:
        return jsonify({"mensaje": resultado})
    elif "No se encontró" in resultado:
        return jsonify({"error": "No se encontró sanción."}), 404
    return jsonify({"error": "Error al modificar sanción."}), 500

@app.route("/api/sanciones/<int:ci>", methods=["DELETE"])
def api_eliminar_sancion(ci):
    if not ci_valido(ci):
        return jsonify({"error": "CI inválido"}), 400
    resultado = eliminar_sancion(ci)
    if "correctamente" in resultado:
        return jsonify({"mensaje": resultado})
    elif "No se encontró" in resultado:
        return jsonify({"error": "No se encontró sanción."}), 404
    return jsonify({"error": "Error al eliminar sanción."}), 500

# ===========================================================
#                       RESERVAS (ABM)
# ===========================================================
@app.route("/api/reservas", methods=["GET"])
def api_listar_reservas():
    fecha = request.args.get("fecha")
    conn = get_db_connection()
    try:
        cur = conn.cursor(dictionary=True)
        base_sql = """
            SELECT
                r.id_reserva AS id,
                r.nombre_sala,
                r.edificio,
                r.fecha,
                TIME_FORMAT(t.hora_inicio, '%%H:%%i') AS hora_inicio,
                TIME_FORMAT(t.hora_fin, '%%H:%%i')   AS hora_fin,
                r.estado,
                COALESCE(COUNT(rp.ci_participante), 0) AS cantidad,
                COALESCE(GROUP_CONCAT(CONCAT(p.nombre, ' ', p.apellido) SEPARATOR ', '), '') AS participantes
            FROM reserva r
            JOIN turno t  ON t.id_turno = r.id_turno
            LEFT JOIN reserva_participante rp ON rp.id_reserva = r.id_reserva
            LEFT JOIN participante p ON p.ci = rp.ci_participante
        """
        params = []
        if fecha:
            base_sql += " WHERE r.fecha = %s"
            params.append(fecha)
        base_sql += " GROUP BY r.id_reserva ORDER BY r.fecha DESC, t.hora_inicio ASC"

        cur.execute(base_sql, tuple(params))
        rows = cur.fetchall()

        out = []
        for r in rows:
            out.append({
                "id": r["id"],
                "ci_participante": "",
                "participante": r["participantes"],
                "sala_id": f"{r['nombre_sala']}|{r['edificio']}",
                "sala_nombre": f"{r['nombre_sala']} ({r['edificio']})",
                "fecha": r["fecha"].isoformat() if hasattr(r["fecha"], "isoformat") else str(r["fecha"]),
                "hora_inicio": r["hora_inicio"],
                "hora_fin": r["hora_fin"],
                "cantidad": int(r["cantidad"] or 0),
                "estado": r["estado"] or "activa",
                "observaciones": ""
            })
        return jsonify(out)
    except Exception as e:
        print("api_listar_reservas:", e)
        return jsonify({"error": "Error al obtener reservas."}), 500
    finally:
        close_connection(conn)

@app.route("/api/reservas", methods=["POST"])
def api_crear_reserva_rest():
    data = request.get_json(silent=True) or {}
    nombre_sala = data.get("nombre_sala")
    edificio = data.get("edificio")
    id_turno = data.get("id_turno")
    fecha = data.get("fecha")
    estado = data.get("estado", "activa")
    participantes = data.get("participantes") or []
    if not participantes and data.get("ci_participante"):
        participantes = [data.get("ci_participante")]

    if not (nombre_sala and edificio and id_turno and fecha):
        return jsonify({"ok": False, "error": "Faltan campos requeridos"}), 400

    conn = get_db_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT 1 FROM reserva
            WHERE nombre_sala = %s AND edificio = %s AND fecha = %s AND id_turno = %s
            LIMIT 1
        """, (nombre_sala, edificio, fecha, id_turno))
        if cur.fetchone():
            return jsonify({"ok": False, "error": "La sala ya está reservada en ese horario."}), 400

        cur.execute("""
            INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre_sala, edificio, fecha, id_turno, estado))
        id_reserva = cur.lastrowid

        if participantes:
            for ci in participantes:
                cur.execute("""
                    INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia)
                    VALUES (%s, %s, CURDATE(), 'false')
                """, (ci, id_reserva))

        conn.commit()
        return jsonify({"ok": True, "id": id_reserva})
    except Exception as e:
        print("api_crear_reserva_rest:", e)
        conn.rollback()
        return jsonify({"ok": False, "error": "Error al crear reserva."}), 500
    finally:
        close_connection(conn)

@app.route("/api/reservas/<int:id_reserva>", methods=["PUT"])
def api_actualizar_reserva(id_reserva):
    data = request.get_json(silent=True) or {}
    campos = []
    valores = []

    mapeo = {
        "nombre_sala": "nombre_sala",
        "edificio": "edificio",
        "fecha": "fecha",
        "id_turno": "id_turno",
        "estado": "estado",
    }
    for k, col in mapeo.items():
        if k in data:
            campos.append(f"{col} = %s")
            valores.append(data[k])

    conn = get_db_connection()
    try:
        cur = conn.cursor()

        if campos:
            cur.execute(f"UPDATE reserva SET {', '.join(campos)} WHERE id_reserva = %s", (*valores, id_reserva))

        if "participantes" in data and isinstance(data["participantes"], list):
            cur.execute("DELETE FROM reserva_participante WHERE id_reserva = %s", (id_reserva,))
            for ci in data["participantes"]:
                cur.execute("""
                    INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia)
                    VALUES (%s, %s, CURDATE(), 'false')
                """, (ci, id_reserva))

        conn.commit()
        return jsonify({"ok": True})
    except Exception as e:
        print("api_actualizar_reserva:", e)
        conn.rollback()
        return jsonify({"ok": False, "error": "Error al actualizar reserva."}), 500
    finally:
        close_connection(conn)

@app.route("/api/reservas/<int:id_reserva>", methods=["DELETE"])
def api_eliminar_reserva(id_reserva):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM reserva_participante WHERE id_reserva = %s", (id_reserva,))
        cur.execute("DELETE FROM reserva WHERE id_reserva = %s", (id_reserva,))
        conn.commit()
        return jsonify({"ok": True})
    except Exception as e:
        print("api_eliminar_reserva:", e)
        conn.rollback()
        return jsonify({"ok": False, "error": "Error al eliminar reserva."}), 500
    finally:
        close_connection(conn)

@app.route("/api/reservas/<int:id_reserva>/estado", methods=["PUT"])
def api_cambiar_estado_reserva(id_reserva):
    data = request.get_json(silent=True) or {}
    estado = data.get("estado")
    if estado not in ("activa", "cancelada", "sin_asistencia", "finalizada"):
        return jsonify({"ok": False, "error": "Estado inválido"}), 400
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("UPDATE reserva SET estado = %s WHERE id_reserva = %s", (estado, id_reserva))
        conn.commit()
        return jsonify({"ok": True})
    except Exception as e:
        print("api_cambiar_estado_reserva:", e)
        conn.rollback()
        return jsonify({"ok": False, "error": "Error al cambiar estado."}), 500
    finally:
        close_connection(conn)

# ===========================================================
#                         MAIN
# ===========================================================
if __name__ == "__main__":
    app.run(debug=True)
