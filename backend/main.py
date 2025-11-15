import os
from logica import *
from validaciones import *
from reportes import *

def limpiar_pantalla():
    os.system('clear')


# ================== AUTENTICACIÓN ==================

def pantalla_login():

    while True:
        limpiar_pantalla()
        print("\n" + "="*50)
        print("SISTEMA DE GESTIÓN DE SALAS Y RESERVAS")
        print("="*50)
        print("Por favor, inicia sesión\n")
        
        correo = input("Correo: ").strip()
        contrasena = input("Contraseña: ").strip()
        
        usuario = autenticar_usuario(correo, contrasena)
        
        if not usuario:
            print("\n Credenciales incorrectas. Intenta nuevamente.")
            input("Presiona Enter para continuar...")
            continue
        
        # Verificar si debe cambiar contraseña
        if verificar_debe_cambiar_contraseña(correo):
            print("\n  Debes cambiar tu contraseña antes de continuar.")
            if not forzar_cambio_contraseña(correo, contrasena):
                print(" No se pudo cambiar la contraseña. Intenta nuevamente.")
                input("Presiona Enter para continuar...")
                continue
        
        # Si es usuario normal, obtener su CI
        ci = None
        if usuario["rol"] == "usuario":
            ci = obtener_ci_por_correo(correo)
            if not ci:
                print(" No se encontró participante asociado al correo.")
                return None
            return {'rol': 'usuario', 'correo': correo, 'ci': ci}
        
        return {'rol': 'admin', 'correo': correo, 'ci': None}


def forzar_cambio_contraseña(correo, contraseña_actual):

    print("\n" + "-"*50)
    print("CAMBIO DE CONTRASEÑA OBLIGATORIO")
    print("-"*50)
    
    while True:
        nueva_contraseña = input("Nueva contraseña (mínimo 8 caracteres): ").strip()
        
        if len(nueva_contraseña) < 8:
            print(" La contraseña debe tener al menos 8 caracteres.")
            continue
        
        confirmar = input("Confirma la nueva contraseña: ").strip()
        
        if nueva_contraseña != confirmar:
            print(" Las contraseñas no coinciden. Intenta nuevamente.")
            continue
        
        resultado = cambiar_contraseña(correo, contraseña_actual, nueva_contraseña)
        
        if resultado is True:
            print(" Contraseña cambiada exitosamente.")
            input("Presiona Enter para continuar...")
            return True
        else:
            print(f"{resultado}")
            respuesta = input("¿Deseas intentar nuevamente? (s/N): ").strip().lower()
            if respuesta != 's':
                return False


def cambiar_mi_contraseña_menu(correo):

    limpiar_pantalla()
    print("--- CAMBIAR MI CONTRASEÑA ---")
    
    contraseña_actual = input("Contraseña actual: ").strip()
    
    while True:
        nueva_contraseña = input("Nueva contraseña (mínimo 8 caracteres): ").strip()
        
        if len(nueva_contraseña) < 8:
            print(" La contraseña debe tener al menos 8 caracteres.")
            continue
        
        confirmar = input("Confirma la nueva contraseña: ").strip()
        
        if nueva_contraseña != confirmar:
            print(" Las contraseñas no coinciden. Intenta nuevamente.")
            continue
        
        break
    
    resultado = cambiar_contraseña(correo, contraseña_actual, nueva_contraseña)
    
    if resultado is True:
        print(" Contraseña cambiada exitosamente.")
    else:
        print(f"{resultado}")
    
    input("Presiona Enter para continuar...")


def mostrar_menu_usuario():
    print("\n" + "="*50)
    print("MENÚ USUARIO - MIS RESERVAS Y SANCIONES")
    print("="*50)
    print("1. Crear reserva")
    print("2. Mis reservas")
    print("3. Modificar mi reserva")
    print("4. Cancelar mi reserva")
    print("5. Consultar mis sanciones")
    print("6. Cambiar mi contraseña")
    print("7. Salir")
    print("="*50)


def mostrar_menu_admin():
    print("\n" + "="*50)
    print("MENÚ ADMINISTRADOR")
    print("="*50)
    print("1. Gestionar Participantes")
    print("2. Gestionar Salas")
    print("3. Gestionar Reservas")
    print("4. Gestionar Sanciones")
    print("5. Ver Reportes")
    print("6. Salir")
    print("="*50)

# ================== UTILIDADES DE SELECCIÓN ==================

def _imprimir_lista(titulo, opciones, fmt):
    print(f"\n{titulo}")
    print("-" * max(10, len(titulo)))
    if not opciones:
        print("No hay opciones disponibles.")
        return
    for idx, item in enumerate(opciones, start=1):
        texto = fmt(item)
        print(f"{idx}. {texto}")
    print("0. Volver")


def seleccionar_opcion(titulo, opciones, fmt=lambda x: str(x)):

    while True:
        limpiar_pantalla()
        _imprimir_lista(titulo, opciones, fmt)
        if not opciones:
            input("Presiona Enter para continuar...")
            return None
        eleccion = input("Elige una opción: ").strip()
        if eleccion == "0":
            return None
        if eleccion.isdigit():
            idx = int(eleccion)
            if 1 <= idx <= len(opciones):
                return opciones[idx - 1]
        print("Opción no válida.")
        input("Presiona Enter para intentar de nuevo...")

# ================== MENU PARTICIPANTES ==================

def menu_participantes():
    while True:
        limpiar_pantalla()
        print("\n--- PARTICIPANTES ---")
        print("1. Crear participante")
        print("2. Eliminar participante")
        print("3. Modificar participante")
        print("4. Volver al menú principal")
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            crear_participante_menu()
        elif opcion == "2":
            eliminar_participante_menu()
        elif opcion == "3":
            modificar_participante_menu()
        elif opcion == "4":
            break
        else:
            print("Opción no válida")
            input("Presiona Enter para continuar...")

def crear_participante_menu():
    limpiar_pantalla()
    print("--- CREAR PARTICIPANTE ---")
    ci = input("Ingresa la cédula: ").strip()
    nombre = input("Ingresa el nombre: ").strip()
    apellido = input("Ingresa el apellido: ").strip()
    email = input("Ingresa el email: ").strip()
    
    if not participante_valido(ci, nombre, apellido, email):
        print(" Datos inválidos. Verifica los campos.")
    else:
        resultado = crear_persona(ci, nombre, apellido, email)
        if isinstance(resultado, dict):
            print(f"\n {resultado['mensaje']}")
            print(f"\n  IMPORTANTE: Guarda esta contraseña temporal:")
            print(f"   Contraseña: {resultado['contraseña']}")
            print(f"\n   El usuario deberá cambiarla en su primer login.")
        else:
            print(f" {resultado}")
    input("\nPresiona Enter para continuar...")

def eliminar_participante_menu():
    participantes = listar_participantes_activos()
    seleccionado = seleccionar_opcion(
        "Participantes activos (elige uno para eliminar)",
        participantes,
        fmt=lambda p: f"{p['ci']} - {p['apellido']}, {p['nombre']} ({p['email']})",
    )
    if not seleccionado:
        return
    resultado = eliminar_persona(seleccionado["ci"])
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presiona Enter para continuar...")

def modificar_participante_menu():
    participantes = listar_participantes_activos()
    seleccionado = seleccionar_opcion(
        "Participantes activos (elige uno para modificar)",
        participantes,
        fmt=lambda p: f"{p['ci']} - {p['apellido']}, {p['nombre']} ({p['email']})",
    )
    if not seleccionado:
        return
    ci = str(seleccionado["ci"])  # usar como string para inputs
    
    print("Deja en blanco lo que no deseas modificar")
    nombre = input("Nuevo nombre (opcional): ").strip() or None
    apellido = input("Nuevo apellido (opcional): ").strip() or None
    email = input("Nuevo email (opcional): ").strip() or None
    
    resultado = modificar_persona(ci, nombre, apellido, email)
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presiona Enter para continuar...")

# ================== MENU SALAS ==================

def menu_salas():
    while True:
        limpiar_pantalla()
        print("\n--- SALAS ---")
        print("1. Crear sala")
        print("2. Eliminar sala")
        print("3. Modificar sala")
        print("4. Ver todas las salas")
        print("5. Volver al menú principal")
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            crear_sala_menu()
        elif opcion == "2":
            eliminar_sala_menu()
        elif opcion == "3":
            modificar_sala_menu()
        elif opcion == "4":
            ver_salas_menu()
        elif opcion == "5":
            break
        else:
            print("Opción no válida")
            input("Presiona Enter para continuar...")

def crear_sala_menu():
    limpiar_pantalla()
    print("--- CREAR SALA ---")
    nombre_sala = input("Nombre de la sala: ").strip()
    edificios = listar_edificios()
    edificio_sel = seleccionar_opcion(
        "Elige un edificio",
        edificios,
        fmt=lambda e: e["nombre_edificio"],
    )
    if not edificio_sel:
        return
    edificio = edificio_sel["nombre_edificio"]
    try:
        capacidad = int(input("Capacidad: "))
    except ValueError:
        print(" La capacidad debe ser un número")
        input("Presiona Enter para continuar...")
        return
    tipos = ["libre", "posgrado", "docente"]
    tipo_sel = seleccionar_opcion(
        "Tipo de sala",
        tipos,
        fmt=lambda t: t,
    )
    if not tipo_sel:
        return
    tipo_sala = tipo_sel
    
    resultado = crear_sala(nombre_sala, edificio, capacidad, tipo_sala)
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presiona Enter para continuar...")

def eliminar_sala_menu():
    edificios = listar_edificios()
    edificio_sel = seleccionar_opcion(
        "Elige un edificio",
        edificios,
        fmt=lambda e: e["nombre_edificio"],
    )
    if not edificio_sel:
        return
    salas = listar_salas(edificio_sel["nombre_edificio"])
    sala_sel = seleccionar_opcion(
        f"Salas en {edificio_sel['nombre_edificio']}",
        salas,
        fmt=lambda s: f"{s['nombre']} (cap {s['capacidad']}, {s['tipo_sala']})",
    )
    if not sala_sel:
        return
    resultado = eliminar_sala(sala_sel["nombre"], sala_sel["edificio"])
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presiona Enter para continuar...")

def modificar_sala_menu():
    edificios = listar_edificios()
    edificio_sel = seleccionar_opcion(
        "Elige un edificio",
        edificios,
        fmt=lambda e: e["nombre_edificio"],
    )
    if not edificio_sel:
        return
    salas = listar_salas(edificio_sel["nombre_edificio"])
    sala_sel = seleccionar_opcion(
        f"Salas en {edificio_sel['nombre_edificio']}",
        salas,
        fmt=lambda s: f"{s['nombre']} (cap {s['capacidad']}, {s['tipo_sala']})",
    )
    if not sala_sel:
        return
    nombre_sala = sala_sel["nombre"]
    edificio = sala_sel["edificio"]
    
    print("Deja en blanco lo que no deseas modificar")
    try:
        capacidad_input = input("Nueva capacidad (opcional): ").strip()
        capacidad = int(capacidad_input) if capacidad_input else None
    except ValueError:
        capacidad = None
    
    tipo_sala = None
    elegir_tipo = input("¿Cambiar tipo de sala? (s/N): ").strip().lower()
    if elegir_tipo == 's':
        tipo_sel = seleccionar_opcion("Nuevo tipo de sala", ["libre", "posgrado", "docente"], fmt=lambda t: t)
        if not tipo_sel:
            tipo_sala = None
        else:
            tipo_sala = tipo_sel
    
    resultado = modificar_sala(nombre_sala, edificio, capacidad, tipo_sala)
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presiona Enter para continuar...")

def ver_salas_menu():
    limpiar_pantalla()
    print("--- LISTA DE SALAS ---")
    salas = listar_salas()
    if not salas:
        print("No hay salas registradas")
    else:
        for sala in salas:
            print(f"  • {sala['nombre']} - {sala['edificio']} (Cap: {sala['capacidad']}, {sala['tipo_sala']})")
    input("Presiona Enter para continuar...")

# ================== MENU RESERVAS ==================

def menu_reservas():
    while True:
        limpiar_pantalla()
        print("\n--- RESERVAS ---")
        print("1. Crear reserva")
        print("2. Cancelar reserva")
        print("3. Modificar reserva")
        print("4. Volver al menú principal")
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            crear_reserva_menu()
        elif opcion == "2":
            cancelar_reserva_menu()
        elif opcion == "3":
            modificar_reserva_menu()
        elif opcion == "4":
            break
        else:
            print("Opción no válida")
            input("Presiona Enter para continuar...")

def crear_reserva_menu():
    limpiar_pantalla()
    print("--- CREAR RESERVA ---")
    # Participante (ingreso manual de CI)
    ci = input("Cédula del participante: ").strip()
    if not existe_participante(ci):
        print(" El participante no existe")
        input("Presiona Enter para continuar...")
        return

    # Edificio -> Sala
    edificios = listar_edificios()
    edificio_sel = seleccionar_opcion(
        "Elige un edificio",
        edificios,
        fmt=lambda e: e["nombre_edificio"],
    )
    if not edificio_sel:
        return
    edificio = edificio_sel["nombre_edificio"]
    salas = listar_salas(edificio)
    sala_sel = seleccionar_opcion(
        f"Elige una sala en {edificio}",
        salas,
        fmt=lambda s: f"{s['nombre']} (cap {s['capacidad']}, {s['tipo_sala']})",
    )
    if not sala_sel:
        return
    nombre_sala = sala_sel["nombre"]

    # Fecha
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    
    # Mostrar disponibilidad de turnos para esa sala y fecha
    disponibilidad = obtener_disponibilidad_turnos(nombre_sala, edificio, fecha)
    
    if not disponibilidad:
        print(" No hay turnos disponibles para esta fecha/sala o la fecha es pasada.")
        input("Presiona Enter para continuar...")
        return
    
    # Turno con indicador de disponibilidad
    turno_sel = seleccionar_opcion(
        f"Turnos para {nombre_sala} el {fecha}",
        disponibilidad,
        fmt=lambda t: f"{t['hora_inicio'][:5]} - {t['hora_fin'][:5]} {' DISPONIBLE' if t['disponible'] else ' OCUPADO'}",
    )
    if not turno_sel:
        return
    
    if not turno_sel['disponible']:
        print(" Este turno ya está ocupado. Elige otro.")
        input("Presiona Enter para continuar...")
        return
    
    id_turno = int(turno_sel["id_turno"])

    # Cantidad de horas
    print("\n¿Cuántas horas deseas reservar?")
    print("1. Una hora")
    print("2. Dos horas consecutivas")
    while True:
        opcion_horas = input("Elige (1 o 2): ").strip()
        if opcion_horas in ['1', '2']:
            cantidad_horas = int(opcion_horas)
            break
        print(" Opción no válida. Elige 1 o 2.")

    # Cantidad de participantes
    try:
        cantidad = int(input("Cantidad de participantes: "))
    except ValueError:
        print(" La cantidad debe ser un número")
        input("Presiona Enter para continuar...")
        return

    resultado = crear_reserva_multiple(ci, nombre_sala, edificio, id_turno, fecha, cantidad, cantidad_horas)
    if isinstance(resultado, dict):
        print(f" {resultado['mensaje']}")
        print(f"   IDs de reserva: {', '.join(map(str, resultado['ids_reserva']))}")
    else:
        print(f" {resultado}")
    input("Presiona Enter para continuar...")

def cancelar_reserva_menu():
    reservas = listar_reservas(estado="activa")
    sel = seleccionar_opcion(
        "Reservas activas (elige una para cancelar)",
        reservas,
        fmt=lambda r: f"{r['id_reserva']} - {r['fecha']} {r['hora_inicio']}-{r['hora_fin']} | {r['nombre_sala']} ({r['edificio']})",
    )
    if not sel:
        return
    resultado = eliminar_reserva(sel["id_reserva"])
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presiona Enter para continuar...")

def modificar_reserva_menu():
    reservas = listar_reservas()
    sel = seleccionar_opcion(
        "Elige una reserva a modificar",
        reservas,
        fmt=lambda r: f"{r['id_reserva']} - {r['fecha']} {r['hora_inicio']}-{r['hora_fin']} | {r['nombre_sala']} ({r['edificio']}) [{r['estado']}]",
    )
    if not sel:
        return
    id_reserva = sel["id_reserva"]

    # Nuevo edificio->sala (opcional)
    nombre_sala = None
    if input("¿Cambiar sala? (s/N): ").strip().lower() == 's':
        edif = seleccionar_opcion("Elige edificio", listar_edificios(), fmt=lambda e: e['nombre_edificio'])
        if not edif:
            nombre_sala = None
        else:
            salas = listar_salas(edif["nombre_edificio"])
            sala_sel = seleccionar_opcion(
                f"Salas en {edif['nombre_edificio']}",
                salas,
                fmt=lambda s: f"{s['nombre']} (cap {s['capacidad']}, {s['tipo_sala']})",
            )
            if sala_sel:
                nombre_sala = sala_sel["nombre"]

    # Nueva fecha (opcional)
    fecha = input("Nueva fecha (opcional, YYYY-MM-DD, Enter para omitir): ").strip() or None

    # Nuevo turno (opcional)
    id_turno = None
    if input("¿Cambiar turno? (s/N): ").strip().lower() == 's':
        turnos = listar_turnos()
        turno_sel = seleccionar_opcion("Elige turno", turnos, fmt=lambda t: f"{t['id_turno']} - {t['hora_inicio']} a {t['hora_fin']}")
        if turno_sel:
            id_turno = int(turno_sel["id_turno"]) 

    # Nuevo estado (opcional)
    estado = None
    if input("¿Cambiar estado? (s/N): ").strip().lower() == 's':
        estado_sel = seleccionar_opcion("Estado", ["activa", "cancelada", "sin_asistencia", "finalizada"], fmt=lambda e: e)
        estado = estado_sel if estado_sel else None

    resultado = modificar_reserva(id_reserva, nombre_sala, fecha, id_turno, estado)
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presiona Enter para continuar...")

# ================== MENU SANCIONES ==================

def menu_sanciones():
    while True:
        limpiar_pantalla()
        print("\n--- SANCIONES ---")
        print("1. Crear sanción")
        print("2. Anular sanción")
        print("3. Levantar sanción")
        print("4. Modificar sanción")
        print("5. Ver sanciones activas")
        print("6. Volver al menú principal")
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            crear_sancion_menu()
        elif opcion == "2":
            eliminar_sancion_menu()
        elif opcion == "3":
            levantar_sancion_menu()
        elif opcion == "4":
            modificar_sancion_menu()
        elif opcion == "5":
            ver_sanciones_menu()
        elif opcion == "6":
            break
        else:
            print("Opción no válida")
            input("Presiona Enter para continuar...")

def crear_sancion_menu():
    limpiar_pantalla()
    print("--- CREAR SANCIÓN ---")
    # Participante (ingreso manual de CI)
    ci = input("Cédula del participante: ").strip()
    if not existe_participante(ci):
        print(" El participante no existe")
        input("Presiona Enter para continuar...")
        return

    motivo = input("Motivo de la sanción: ").strip()
    fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ").strip()
    fecha_fin = input("Fecha de fin (YYYY-MM-DD, Enter si no aplica): ").strip() or None
    
    resultado = crear_sancion(ci, motivo, fecha_inicio, fecha_fin)
    if isinstance(resultado, dict):
        print(f" {resultado['mensaje']} (ID: {resultado['id_sancion']})")
    else:
        print(f" {resultado}")
    input("Presiona Enter para continuar...")

def eliminar_sancion_menu():
    sanciones = listar_sanciones_activas()
    sel = seleccionar_opcion(
        "Sanciones activas (elige una para anular)",
        sanciones,
        fmt=lambda s: f"{s['id_sancion']} - {s['ci_participante']} {s['apellido']}, {s['nombre']} ({s['fecha_inicio']} -> {s['fecha_fin']})",
    )
    if not sel:
        return
    resultado = eliminar_sancion(sel["id_sancion"])
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presiona Enter para continuar...")

def levantar_sancion_menu():
    sanciones = listar_sanciones_activas()
    sel = seleccionar_opcion(
        "Sanciones activas (elige una para levantar)",
        sanciones,
        fmt=lambda s: f"{s['id_sancion']} - {s['ci_participante']} {s['apellido']}, {s['nombre']} ({s['fecha_inicio']} -> {s['fecha_fin']})",
    )
    if not sel:
        return
    resultado = levantar_sancion(sel["id_sancion"])
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presiona Enter para continuar...")

def modificar_sancion_menu():
    sanciones = listar_sanciones_activas()
    sel = seleccionar_opcion(
        "Elige una sanción a modificar",
        sanciones,
        fmt=lambda s: f"{s['id_sancion']} - {s['ci_participante']} {s['apellido']}, {s['nombre']} ({s['fecha_inicio']} -> {s['fecha_fin']})",
    )
    if not sel:
        return
    id_sancion = sel["id_sancion"]
    
    print("Deja en blanco lo que no deseas modificar")
    motivo = input("Nuevo motivo (opcional): ").strip() or None
    fecha_inicio = input("Nueva fecha de inicio (opcional, YYYY-MM-DD): ").strip() or None
    fecha_fin = input("Nueva fecha de fin (opcional, YYYY-MM-DD): ").strip() or None
    estado = None
    if input("¿Cambiar estado? (s/N): ").strip().lower() == 's':
        estado_sel = seleccionar_opcion("Estado", ["activa", "inactiva", "anulada"], fmt=lambda e: e)
        estado = estado_sel if estado_sel else None
    
    resultado = modificar_sancion(id_sancion, motivo, fecha_inicio, fecha_fin, estado)
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presiona Enter para continuar...")

def ver_sanciones_menu():
    limpiar_pantalla()
    print("--- SANCIONES ACTIVAS ---")
    sanciones = listar_sanciones_activas()
    if not sanciones:
        print("No hay sanciones activas")
    else:
        for sancion in sanciones:
            print(f"    ID: {sancion['id_sancion']} | CI: {sancion['ci_participante']} - {sancion['nombre']} {sancion['apellido']}")
            print(f"    Desde: {sancion['fecha_inicio']} Hasta: {sancion['fecha_fin']}")
    input("Presiona Enter para continuar...")

# ================== MENU USUARIO (ESTUDIANTE) ==================

def crear_reserva_usuario(ci_sesion):

    limpiar_pantalla()
    print("--- CREAR RESERVA ---")
    # Edificio -> Sala
    edificios = listar_edificios()
    edificio_sel = seleccionar_opcion(
        "Elige un edificio",
        edificios,
        fmt=lambda e: e["nombre_edificio"],
    )
    if not edificio_sel:
        return
    edificio = edificio_sel["nombre_edificio"]
    salas = listar_salas(edificio)
    sala_sel = seleccionar_opcion(
        f"Elige una sala en {edificio}",
        salas,
        fmt=lambda s: f"{s['nombre']} (cap {s['capacidad']}, {s['tipo_sala']})",
    )
    if not sala_sel:
        return
    nombre_sala = sala_sel["nombre"]

    # Fecha
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    
    # Mostrar disponibilidad de turnos para esa sala y fecha
    disponibilidad = obtener_disponibilidad_turnos(nombre_sala, edificio, fecha)
    
    if not disponibilidad:
        print(" No hay turnos disponibles para esta fecha/sala o la fecha es pasada.")
        input("Presiona Enter para continuar...")
        return
    
    # Turno con indicador de disponibilidad
    turno_sel = seleccionar_opcion(
        f"Turnos para {nombre_sala} el {fecha}",
        disponibilidad,
        fmt=lambda t: f"{t['hora_inicio'][:5]} - {t['hora_fin'][:5]} {' DISPONIBLE' if t['disponible'] else ' OCUPADO'}",
    )
    if not turno_sel:
        return
    
    if not turno_sel['disponible']:
        print(" Este turno ya está ocupado. Elige otro.")
        input("Presiona Enter para continuar...")
        return
    
    id_turno = int(turno_sel["id_turno"])

    # Cantidad de horas
    print("\n¿Cuántas horas deseas reservar?")
    print("1. Una hora")
    print("2. Dos horas consecutivas")
    while True:
        opcion_horas = input("Elige (1 o 2): ").strip()
        if opcion_horas in ['1', '2']:
            cantidad_horas = int(opcion_horas)
            break
        print(" Opción no válida. Elige 1 o 2.")

    # Cantidad de participantes
    try:
        cantidad = int(input("Cantidad de participantes: "))
    except ValueError:
        print(" La cantidad debe ser un número")
        input("Presiona Enter para continuar...")
        return

    resultado = crear_reserva_multiple(str(ci_sesion), nombre_sala, edificio, id_turno, fecha, cantidad, cantidad_horas)
    if isinstance(resultado, dict):
        print(f" {resultado['mensaje']}")
        print(f"   IDs de reserva: {', '.join(map(str, resultado['ids_reserva']))}")
    else:
        print(f" {resultado}")
    input("Presiona Enter para continuar...")


def ver_mis_reservas_menu(ci_sesion):

    limpiar_pantalla()
    print("--- MIS RESERVAS ---")
    reservas = listar_reservas_usuario(ci_sesion)
    if not reservas:
        print("No tienes reservas registradas.")
    else:
        for r in reservas:
            print(f"    ID: {r['id_reserva']} | {r['fecha']} {r['hora_inicio']}-{r['hora_fin']}")
            print(f"    Sala: {r['nombre_sala']} ({r['edificio']}) | Estado: {r['estado']}")
    input("Presiona Enter para continuar...")


def modificar_mi_reserva_menu(ci_sesion):

    reservas = listar_reservas_usuario(ci_sesion)
    sel = seleccionar_opcion(
        "Elige una de tus reservas para modificar",
        reservas,
        fmt=lambda r: f"{r['id_reserva']} - {r['fecha']} {r['hora_inicio']}-{r['hora_fin']} | {r['nombre_sala']} ({r['edificio']}) [{r['estado']}]",
    )
    if not sel:
        return
    id_reserva = sel["id_reserva"]

    # Nuevo edificio->sala (opcional)
    nombre_sala = None
    if input("¿Cambiar sala? (s/N): ").strip().lower() == 's':
        edif = seleccionar_opcion("Elige edificio", listar_edificios(), fmt=lambda e: e['nombre_edificio'])
        if edif:
            salas = listar_salas(edif["nombre_edificio"])
            sala_sel = seleccionar_opcion(
                f"Salas en {edif['nombre_edificio']}",
                salas,
                fmt=lambda s: f"{s['nombre']} (cap {s['capacidad']}, {s['tipo_sala']})",
            )
            if sala_sel:
                nombre_sala = sala_sel["nombre"]

    # Nueva fecha (opcional)
    fecha = input("Nueva fecha (opcional, YYYY-MM-DD, Enter para omitir): ").strip() or None

    # Nuevo turno (opcional)
    id_turno = None
    if input("¿Cambiar turno? (s/N): ").strip().lower() == 's':
        turnos = listar_turnos()
        turno_sel = seleccionar_opcion("Elige turno", turnos, fmt=lambda t: f"{t['id_turno']} - {t['hora_inicio']} a {t['hora_fin']}")
        if turno_sel:
            id_turno = int(turno_sel["id_turno"]) 

    resultado = modificar_reserva(id_reserva, nombre_sala, fecha, id_turno, None)
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presiona Enter para continuar...")


def cancelar_mi_reserva_menu(ci_sesion):

    reservas = [r for r in listar_reservas_usuario(ci_sesion) if r["estado"] == "activa"]
    sel = seleccionar_opcion(
        "Tus reservas activas (elige una para cancelar)",
        reservas,
        fmt=lambda r: f"{r['id_reserva']} - {r['fecha']} {r['hora_inicio']}-{r['hora_fin']} | {r['nombre_sala']} ({r['edificio']})",
    )
    if not sel:
        return
    resultado = eliminar_reserva(sel["id_reserva"])
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presiona Enter para continuar...")


def consultar_mis_sanciones_menu(ci_sesion):

    limpiar_pantalla()
    print("--- MIS SANCIONES ---")
    sanciones = consultar_mis_sanciones(ci_sesion)
    if not sanciones:
        print("No tienes sanciones registradas.")
    else:
        for s in sanciones:
            print(f"  • ID: {s['id_sancion']} | Estado: {s['estado']}")
            print(f"    Motivo: {s['motivo']}")
            print(f"    Desde: {s['fecha_inicio']} Hasta: {s['fecha_fin']}")
    input("Presiona Enter para continuar...")


# ================== MENU REPORTES ==================

def menu_reportes():
    while True:
        limpiar_pantalla()
        print("\n--- REPORTES ---")
        print("1. Salas más reservadas")
        print("2. Turnos más demandados")
        print("3. Promedio de participantes por sala")
        print("4. Reservas por carrera y facultad")
        print("5. Ocupación por edificio")
        print("6. Reservas y asistencias por tipo y rol")
        print("7. Sanciones por tipo y rol")
        print("8. Porcentaje de reservas utilizadas")
        print("9. Volver al menú principal")
        opcion = input("Elige una opción: ")
        
        limpiar_pantalla()
        if opcion == "1":
            salas_mas_reservadas()
        elif opcion == "2":
            turnos_mas_demandados()
        elif opcion == "3":
            promedio_participantes_por_sala()
        elif opcion == "4":
            reservas_por_carrera_y_facultad()
        elif opcion == "5":
            porcentaje_ocupacion_por_edificio()
        elif opcion == "6":
            reservas_y_asistencias_por_tipo_y_rol()
        elif opcion == "7":
            sanciones_por_tipo_y_rol()
        elif opcion == "8":
            porcentaje_reservas_utilizadas()
        elif opcion == "9":
            break
        else:
            print("Opción no válida")
            input("Presiona Enter para continuar...")
            continue
        
        input("Presiona Enter para continuar...")

# ================== MENU PRINCIPAL ==================

def main_admin():

    while True:
        limpiar_pantalla()
        mostrar_menu_admin()
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            menu_participantes()
        elif opcion == "2":
            menu_salas()
        elif opcion == "3":
            menu_reservas()
        elif opcion == "4":
            menu_sanciones()
        elif opcion == "5":
            menu_reportes()
        elif opcion == "6":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("Opción no válida")
            input("Presiona Enter para continuar...")


def main_usuario(ci_sesion, correo_sesion):

    while True:
        limpiar_pantalla()
        mostrar_menu_usuario()
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            crear_reserva_usuario(ci_sesion)
        elif opcion == "2":
            ver_mis_reservas_menu(ci_sesion)
        elif opcion == "3":
            modificar_mi_reserva_menu(ci_sesion)
        elif opcion == "4":
            cancelar_mi_reserva_menu(ci_sesion)
        elif opcion == "5":
            consultar_mis_sanciones_menu(ci_sesion)
        elif opcion == "6":
            cambiar_mi_contraseña_menu(correo_sesion)
        elif opcion == "7":
            print(" ¡Hasta luego!")
            break
        else:
            print("Opción no válida")
            input("Presiona Enter para continuar...")


def main():
    sesion = pantalla_login()
    
    if sesion["rol"] == "admin": 
        main_admin()
    elif sesion["rol"] == "usuario":
        if sesion["ci"]:
            main_usuario(sesion["ci"], sesion["correo"])
        else:
            print("No se pudo cargar información del usuario.")
            input("Presiona Enter para salir...")

if __name__ == "__main__":
    main()