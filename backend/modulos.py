import os
from logica import *
from validaciones import *
from reportes import *


def limpiar_pantalla():
    os.system('clear')
    os.system('clear') # doble como el clear clears


# ------------------- AUTENTICACION -------------------

def pantalla_login():

    while True:
        limpiar_pantalla()
        limpiar_pantalla()  # doble como el clear clear
        print("\n" + "="*50)
        print("SISTEMA DE GESTIÓN DE SALAS Y RESERVAS")
        print("="*50)
        print("Por favor, inicia sesión\n")
        
        correo = input("Correo: ").strip()
        contrasena = input("contrasena: ").strip()
        
        usuario = autenticar_usuario(correo, contrasena)
        
        if not usuario:
            print("\n Credenciales incorrectas. Intenta nuevamente.")
            input("Presiona Enter para continuar...")
            continue
        
        # Verificar si debe cambiar contrasena
        if verificar_debe_cambiar_contrasena(correo):
            print("\n  Debes cambiar tu contrasena antes de continuar.")
            if not forzar_cambio_contrasena(correo, contrasena):
                print(" No se pudo cambiar la contrasena. Intenta nuevamente.")
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


def forzar_cambio_contrasena(correo, contrasena_actual):

    print("\n" + "-"*50)
    print("CAMBIO DE contrasena OBLIGATORIO")
    print("-"*50)
    
    while True:
        nueva_contrasena = input("Nueva contrasena (mínimo 8 caracteres): ").strip()
        
        if len(nueva_contrasena) < 8:
            print(" La contrasena debe tener al menos 8 caracteres.")
            continue
        
        confirmar = input("Confirma la nueva contrasena: ").strip()
        
        if nueva_contrasena != confirmar:
            print(" Las contrasenas no coinciden. Intenta nuevamente.")
            continue
        
        resultado = cambiar_contrasena(correo, contrasena_actual, nueva_contrasena)
        
        if resultado is True:
            print(" contrasena cambiada exitosamente.")
            input("Presiona Enter para continuar...")
            return True
        else:
            print(f"{resultado}")
            respuesta = input("¿Deseas intentar nuevamente? (s/N): ").strip().lower()
            if respuesta != 's':
                return False


def cambiar_mi_contrasena_menu(correo):

    limpiar_pantalla()
    print("--- CAMBIAR MI contrasena ---")
    
    contrasena_actual = input("contrasena actual: ").strip()
    
    while True:
        nueva_contrasena = input("Nueva contrasena (mínimo 8 caracteres): ").strip()
        
        if len(nueva_contrasena) < 8:
            print(" La contrasena debe tener al menos 8 caracteres.")
            continue
        
        confirmar = input("Confirma la nueva contrasena: ").strip()
        
        if nueva_contrasena != confirmar:
            print(" Las contrasenas no coinciden. Intenta nuevamente.")
            continue
        
        break
    
    resultado = cambiar_contrasena(correo, contrasena_actual, nueva_contrasena)
    
    if resultado is True:
        print(" contrasena cambiada exitosamente.")
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
    print("5. Registrar mi asistencia")
    print("6. Consultar mis sanciones")
    print("7. Cambiar mi contrasena")
    print("8. Salir")
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

# ------------------- UTILIDADES DE SELECCIÓN -------------------

def _imprimir_lista(titulo, opciones, fmt=None):
    # fmt recibe un elemento y devuelve su representación en string
    print(f"\n{titulo}")
    print("-" * max(10, len(titulo)))
    
    if not opciones:
        print("No hay opciones disponibles.")
    else:
        for i, item in enumerate(opciones, 1):
            if fmt:
                print(f"{i}. {fmt(item)}")
            else:
                print(f"{i}. {item}")
    print("0. Volver")


def seleccionar_opcion(titulo, opciones, fmt=None):

    while True:
        limpiar_pantalla()
        _imprimir_lista(titulo, opciones, fmt)
        if not opciones:
            input("Presiona Enter para continuar...")
            return None
        
        # strip para evitar espacios en blanco al inicio/final
        eleccion = input("Elige una opción: ").strip()
        
        if eleccion == "0":
            return None
        
        if eleccion.isdigit():
            indice = int(eleccion)
            if 1 <= indice <= len(opciones):
                return opciones[indice - 1]
        print("Opción no válida.")
        input("Presiona Enter para intentar de nuevo...")

# ------------------- ENTRADA DE PARTICIPANTES -------------------

def ingresar_participantes(cantidad, incluidos_iniciales=None, *, nombre_sala=None, edificio=None, id_turno=None, fecha=None):

    if cantidad is None or cantidad <= 0:
        print(" La cantidad de participantes debe ser un entero positivo.")
        return None

    participantes = []
    if incluidos_iniciales:
        participantes = [str(ci) for ci in incluidos_iniciales]

    while len(participantes) < cantidad:
        nro = len(participantes) + 1
        ci_nuevo = input(f"CI del participante #{nro}: ").strip()
        if not ci_nuevo:
            print(" La cédula no puede estar vacía.")
            continue
        if ci_nuevo in participantes:
            print(" Cédula duplicada en la lista.")
            continue
        if not existe_participante(ci_nuevo):
            print(" La cédula no está registrada.")
            continue
        # Validaciones adicionales con el mismo criterio que el creador
        if fecha and tiene_sancion_activa(ci_nuevo):
            print(" Este participante tiene una sanción activa.")
            continue
        if fecha and excede_reservas_semanales(ci_nuevo, nombre_sala, edificio):
            print(" Este participante excede el límite de reservas semanales.")
            continue
        if fecha and excede_horas_diarias(ci_nuevo, fecha, nombre_sala, edificio):
            print(" Este participante excede el límite de horas diarias para esa fecha.")
            continue
        if nombre_sala and edificio and not validar_tipo_sala(nombre_sala, edificio, ci_nuevo):
            print(" Este participante no está autorizado para este tipo de sala.")
            continue
        if fecha and id_turno and participante_ocupado_en_turno(ci_nuevo, fecha, id_turno):
            print(" Este participante ya tiene una reserva activa en ese turno y fecha.")
            continue
        participantes.append(ci_nuevo)

    return participantes

# ------------------- MENU PARTICIPANTES -------------------

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
    # aca voy a usar el strip para evitar espacios al inicio/final (ejemplo: "  Juan  " -> "Juan")
    ci = input("Ingresa la cédula: ").strip()
    nombre = input("Ingresa el nombre: ").strip()
    apellido = input("Ingresa el apellido: ").strip()
    email = input("Ingresa el email: ").strip()
    
    if not participante_valido(ci, nombre, apellido, email):
        print(" Datos inválidos. Verifica los campos.")
        # a implementar: mostrar errores específicos (ejemplo: cedula repetida)
    else:
        resultado = crear_persona(ci, nombre, apellido, email)
        if isinstance(resultado, dict):
            print(f"\n {resultado['mensaje']}")
            print(f"\n  IMPORTANTE: Guarda esta contrasena temporal:")
            print(f"   contrasena: {resultado['contrasena']}")
            print(f"\n   El usuario deberá cambiarla en su primer login.")
        else:
            print(f" {resultado}")
    input("\nPresiona Enter para continuar...")

def eliminar_participante_menu():
    participantes = listar_participantes_activos()
    seleccionado = seleccionar_opcion(
        "Participantes activos (elegí uno para eliminar)",
        participantes,
        fmt=lambda p: f"{p['ci']} - {p['apellido']}, {p['nombre']} ({p['email']})",
    )
    # cree una funcion anonima para formatear los datos de cada participante
    if not seleccionado:
        return
    resultado = eliminar_persona(seleccionado["ci"])
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presiona Enter para continuar...")

def modificar_participante_menu():
    participantes = listar_participantes_activos()
    seleccionado = seleccionar_opcion(
        "Participantes activos (elegí uno para modificar)",
        participantes,
        fmt=lambda p: f"{p['ci']} - {p['apellido']}, {p['nombre']} ({p['email']})",
    )
    # repito la funcion anonima para formatear los datos
    if not seleccionado:
        return
    ci = str(seleccionado["ci"])  # usar como string para inputs
    
    print("Dejá en blanco lo que no deseas modificar")
    # vuelvo a usar strip para evitar espacios en blanco
    # none es una opcion, por si el usuario no quiere cambiar ese campo
    nombre = input("Nuevo nombre (opcional): ").strip() or None
    apellido = input("Nuevo apellido (opcional): ").strip() or None
    email = input("Nuevo email (opcional): ").strip() or None
    
    resultado = modificar_persona(ci, nombre, apellido, email)
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presioná Enter para continuar...")

# ------------------- MENU SALAS -------------------

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
            input("Presioná Enter para continuar...")

def crear_sala_menu():
    limpiar_pantalla()
    print("--- CREAR SALA ---")
    nombre_sala = input("Nombre de la sala: ").strip()
    edificios = listar_edificios()
    edificio_sel = seleccionar_opcion(
        "Elegí un edificio",
        edificios,
        fmt=lambda e: e["nombre_edificio"],
    )
    # vuelvo a usar la funcion anonima para formatear los edificios
    if not edificio_sel:
        # si el usuario cancela la seleccion ( con 0 ) , vuelvo para atras
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
    # me creo una funcion anonima "s" para formatear las salas
    if not sala_sel:
        return
    resultado = eliminar_sala(sala_sel["nombre"], sala_sel["edificio"])
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presioná Enter para continuar...")

def modificar_sala_menu():
    edificios = listar_edificios()
    edificio_sel = seleccionar_opcion(
        "Elegí un edificio",
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
    except ValueError:  # si el usuario ingresa algo que no es numero lo agarramos
        capacidad = None
    
    tipo_sala = None
    elegir_tipo = input("¿Cambiar tipo de sala? (s/N): ").strip().lower()
    # defino opciones (sin distinguir mayus) para cambiar el tipo de sala
    if elegir_tipo == 's':
        tipo_sel = seleccionar_opcion("Nuevo tipo de sala", ["libre", "posgrado", "docente"], fmt=lambda t: t)
        if not tipo_sel:
            tipo_sala = None
        else:
            tipo_sala = tipo_sel
    
    resultado = modificar_sala(nombre_sala, edificio, capacidad, tipo_sala)
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presioná Enter para continuar...")

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

# ------------------- MENU RESERVAS -------------------

def menu_reservas():
    while True:
        limpiar_pantalla()
        print("\n--- RESERVAS ---")
        print("1. Crear reserva")
        print("2. Cancelar reserva")
        print("3. Modificar reserva")
        print("4. Registrar asistencia")
        print("5. Procesar reservas vencidas (no-shows)")
        print("6. Volver al menú principal")
        opcion = input("Elegí una opción: ")
        
        if opcion == "1":
            crear_reserva_menu()
        elif opcion == "2":
            cancelar_reserva_menu()
        elif opcion == "3":
            modificar_reserva_menu()
        elif opcion == "4":
            registrar_asistencia_menu()
        elif opcion == "5":
            procesar_no_shows_menu()
        elif opcion == "6":
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

    # Edificio - Sala
    edificios = listar_edificios()
    edificio_sel = seleccionar_opcion(
        "Elegí un edificio",
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
    # vuelvo a usar la funcion anonima para formatear las salas
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
        print(" Este turno ya está ocupado. Elegí otro.")
        input("Presioná Enter para continuar...")
        return
    
    id_turno = int(turno_sel["id_turno"])

    # Cantidad de horas
    print("\n¿Cuántas horas deseás reservar?")
    print("1. Una hora")
    print("2. Dos horas consecutivas")
    while True:
        opcion_horas = input("Elegí (1 o 2): ").strip()
        if opcion_horas in ['1', '2']:
            cantidad_horas = int(opcion_horas)
            break
        print(" Opción no válida. Elegí 1 o 2.")
        # de a poco voy capturando todos los errores
    # Cantidad de participantes y carga de CIs (incluye al creador como 1ro)
    try:
        cantidad = int(input("Cantidad de participantes (total, incluyendo al creador): "))
    except ValueError:
        print(" La cantidad debe ser un número")
        input("Presioná Enter para continuar...")
        return

    participantes = ingresar_participantes(
        cantidad,
        incluidos_iniciales=[ci],
        nombre_sala=nombre_sala,
        edificio=edificio,
        id_turno=id_turno,
        fecha=fecha,
    )
    if not participantes:
        input("Presioná Enter para continuar...")
        return

    resultado = crear_reserva_multiple(ci, nombre_sala, edificio, id_turno, fecha, len(participantes), cantidad_horas)
    if isinstance(resultado, dict):
        print(f" {resultado['mensaje']}")
        print(f"   IDs de reserva: {', '.join(map(str, resultado['ids_reserva']))}")
        # Agregar el resto de los participantes a cada reserva creada
        otros = [p for p in participantes if p != str(ci)]
        if otros:
            agregado = agregar_participantes_a_reservas(resultado['ids_reserva'], otros)
            print(f"   {agregado}")
    # si yo hice una reserava doble, se me guardan dos Ids, con map los convierto en string
    # y con join los junto con comas para luego hacer consultas y que aparezcan juntos
    else:
        print(f" {resultado}")
    input("Presioná Enter para continuar...")

def cancelar_reserva_menu():
    reservas = listar_reservas(estado="activa")
    sel = seleccionar_opcion(
        "Reservas activas (elige una para cancelar)",
        reservas,
        fmt=lambda r: f"{r['id_reserva']} - {r['fecha']} {r['hora_inicio']}-{r['hora_fin']} | {r['nombre_sala']} ({r['edificio']})",
    )
    # vuelvo a usar la funcion anonima para formatear las reservas
    if not sel:
        return
    resultado = eliminar_reserva(sel["id_reserva"])
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presioná Enter para continuar...")

def modificar_reserva_menu():
    reservas = listar_reservas()
    sel = seleccionar_opcion(
        "Elegí una reserva a modificar",
        reservas,
        fmt=lambda r: f"{r['id_reserva']} - {r['fecha']} {r['hora_inicio']}-{r['hora_fin']} | {r['nombre_sala']} ({r['edificio']}) [{r['estado']}]",
    )
    # vuelvo a usar la funcion anonima para formatear las reservas
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
            # vuelvo a usar la funcion anonima para formatear las salas
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

def registrar_asistencia_menu():

    limpiar_pantalla()
    print("--- REGISTRAR ASISTENCIA ---")
    
    reservas_hoy = listar_reservas_hoy()
    
    if not reservas_hoy:
        print("No hay reservas activas para hoy.")
        input("Presiona Enter para continuar...")
        return
    
    reserva_sel = seleccionar_opcion(
        "Reservas activas de hoy (elige una para registrar asistencia)",
        reservas_hoy,
        fmt=lambda r: f"ID {r['id_reserva']} - {r['nombre_sala']} ({r['edificio']}) | {r['hora_inicio'][:5]}-{r['hora_fin'][:5]}"
    )
    
    if not reserva_sel:
        return
    
    id_reserva = reserva_sel['id_reserva']
    
    # Obtener participantes de la reserva
    participantes = listar_participantes_reserva(id_reserva)
    
    if not participantes:
        print("No se encontraron participantes para esta reserva.")
        input("Presiona Enter para continuar...")
        return
    
    limpiar_pantalla()
    print(f"--- ASISTENCIA RESERVA {id_reserva} ---")
    print(f"Sala: {reserva_sel['nombre_sala']} ({reserva_sel['edificio']})")
    print(f"Horario: {reserva_sel['hora_inicio'][:5]} - {reserva_sel['hora_fin'][:5]}")
    print("\nParticipantes:")
    print("-" * 60)
    
    for i, p in enumerate(participantes, 1):
        estado_actual = p['asistencia'] or 'sin registrar'
        print(f"{i}. {p['apellido']}, {p['nombre']} (CI: {p['ci_participante']}) - {estado_actual}")
    
    print("\n" + "=" * 60)
    print("Marca la asistencia de cada participante:")
    print("  P = Presente")
    print("  J = Justificado")
    print("  A = Ausente")
    print("=" * 60)
    
    presentes = []
    justificados = []
    
    for p in participantes:
        while True:
            opcion = input(f"\n{p['apellido']}, {p['nombre']} (CI: {p['ci_participante']}) [P/J/A]: ").strip().upper()
            if opcion in ['P', 'J', 'A']:
                if opcion == 'P':
                    presentes.append(str(p['ci_participante']))
                elif opcion == 'J':
                    justificados.append(str(p['ci_participante']))
                # Si es 'A' no hacemos nada, queda como ausente por defecto
                break
            else:
                print(" Opción inválida. Usa P, J o A.")
    
    # Confirmar antes de guardar
    print("\n" + "-" * 60)
    print("RESUMEN:")
    print(f"  Presentes: {len(presentes)}")
    print(f"  Justificados: {len(justificados)}")
    print(f"  Ausentes: {len(participantes) - len(presentes) - len(justificados)}")
    print("-" * 60)
    
    confirmar = input("\n¿Confirmar registro de asistencia? (S/n): ").strip().lower()
    if confirmar == 'n':
        print("Operación cancelada.")
        input("Presiona Enter para continuar...")
        return
    
    resultado = registrar_asistencia_reserva(id_reserva, presentes, justificados)
    
    if isinstance(resultado, dict):
        print(f"\n {resultado['mensaje']}")
        print(f"   Estado de reserva: {resultado['estado']}")
        print(f"   Presentes: {resultado['presentes']}")
        print(f"   Justificados: {resultado['justificados']}")
        print(f"   Ausentes: {resultado['ausentes']}")
    else:
        print(f" {resultado}")
    
    input("\nPresiona Enter para continuar...")

def procesar_no_shows_menu():

    limpiar_pantalla()
    print("--- PROCESAR RESERVAS VENCIDAS (NO-SHOWS) ---")
    print("\nEsta operación:")
    print("  • Busca reservas pasadas sin asistencia registrada")
    print("  • Marca a participantes ausentes")
    print("  • Aplica sanción de 2 meses a quienes no asistieron")
    print("  • Actualiza el estado de las reservas")
    print("\n" + "=" * 60)
    
    confirmar = input("\n¿Proceder con el procesamiento? (S/n): ").strip().lower()
    if confirmar == 'n':
        print("Operación cancelada.")
        input("Presiona Enter para continuar...")
        return
    
    print("\nProcesando...")
    resultado = procesar_reservas_vencidas_y_sancionar()
    
    if isinstance(resultado, dict):
        print(f"\n {resultado['mensaje']}")
        print(f"   Reservas procesadas: {resultado['reservas_procesadas']}")
        print(f"   Sanciones aplicadas: {resultado['sanciones_aplicadas']}")
    else:
        print(f" {resultado}")
    
    input("\nPresiona Enter para continuar...")

# ------------------- MENU SANCIONES -------------------

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
    # vuelvo a usar la funcion anonima para formatear las sanciones
    if not sel:
        return
    resultado = eliminar_sancion(sel["id_sancion"])
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presioná Enter para continuar...")

def levantar_sancion_menu():
    sanciones = listar_sanciones_activas()
    sel = seleccionar_opcion(
        "Sanciones activas (elige una para levantar)",
        sanciones,
        fmt=lambda s: f"{s['id_sancion']} - {s['ci_participante']} {s['apellido']}, {s['nombre']} ({s['fecha_inicio']} -> {s['fecha_fin']})",
    )
    # vuelvo a usar la funcion anonima para formatear las sanciones
    if not sel:
        return
    resultado = levantar_sancion(sel["id_sancion"])
    print(f" {resultado}" if "correctamente" in resultado else f" {resultado}")
    input("Presioná Enter para continuar...")

def modificar_sancion_menu():
    sanciones = listar_sanciones_activas()
    sel = seleccionar_opcion(
        "Elegí una sanción a modificar",
        sanciones,
        fmt=lambda s: f"{s['id_sancion']} - {s['ci_participante']} {s['apellido']}, {s['nombre']} ({s['fecha_inicio']} -> {s['fecha_fin']})",
    )
    # vuelvo a usar la funcion anonima para formatear las sanciones
    if not sel:
        return
    id_sancion = sel["id_sancion"]
    
    print("Deja en blanco lo que no deseas modificar")
    motivo = input("Nuevo motivo (opcional): ").strip() or None
    # uso el strip para formatear el comentario por si esta mal ingresado
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

# ------------------- MENU USUARIO (ESTUDIANTE) -------------------

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
    # formateo la hora y agarro solo los primeros 5 caracteres (hora y minutos)
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

    # Cantidad de participantes y carga de CIs (incluye al usuario de sesión)
    try:
        cantidad = int(input("Cantidad de participantes (total, incluyéndote): "))
    except ValueError:  # value error por si el usuario ingresa algo que no es numero
        print(" La cantidad debe ser un número")
        input("Presioná Enter para continuar...")
        return

    participantes = ingresar_participantes(
        cantidad,
        incluidos_iniciales=[str(ci_sesion)],
        nombre_sala=nombre_sala,
        edificio=edificio,
        id_turno=id_turno,
        fecha=fecha,
    )
    if not participantes:
        input("Presioná Enter para continuar...")
        return

    resultado = crear_reserva_multiple(str(ci_sesion), nombre_sala, edificio, id_turno, fecha, len(participantes), cantidad_horas)
    if isinstance(resultado, dict):
        # resultado es un diccionario?? osea es una reserva doble??
        print(f" {resultado['mensaje']}")
        print(f"   IDs de reserva: {', '.join(map(str, resultado['ids_reserva']))}")
        otros = [p for p in participantes if p != str(ci_sesion)]
        if otros:
            agregado = agregar_participantes_a_reservas(resultado['ids_reserva'], otros)
            print(f"   {agregado}")
    else:
        print(f" {resultado}")
    input("Presioná Enter para continuar...")


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

    # Nuevo edificio - sala (opcional)
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


def registrar_mi_asistencia_menu(ci_sesion):
 
    limpiar_pantalla()
    print("--- REGISTRAR MI ASISTENCIA ---")
    
    mis_reservas_hoy = listar_reservas_hoy(ci_sesion)
    
    if not mis_reservas_hoy:
        print("No tienes reservas activas para hoy.")
        input("Presiona Enter para continuar...")
        return
    
    reserva_sel = seleccionar_opcion(
        "Tus reservas de hoy (elige una para confirmar asistencia)",
        mis_reservas_hoy,
        fmt=lambda r: f"ID {r['id_reserva']} - {r['nombre_sala']} ({r['edificio']}) | {r['hora_inicio'][:5]}-{r['hora_fin'][:5]}"
    )
    
    if not reserva_sel:
        return
    
    id_reserva = reserva_sel['id_reserva']
    
    # Verificar si ya registró asistencia
    participantes = listar_participantes_reserva(id_reserva)
    mi_registro = next((p for p in participantes if str(p['ci_participante']) == str(ci_sesion)), None)
    
    if mi_registro and mi_registro['asistencia']:
        print(f"\nYa registraste tu asistencia como: {mi_registro['asistencia']}")
        input("Presiona Enter para continuar...")
        return
    
    limpiar_pantalla()
    print(f"--- CONFIRMAR ASISTENCIA ---")
    print(f"Reserva: {reserva_sel['nombre_sala']} ({reserva_sel['edificio']})")
    print(f"Horario: {reserva_sel['hora_inicio'][:5]} - {reserva_sel['hora_fin'][:5]}")
    print("\n¿Confirmas tu asistencia?")
    print("  1. Sí, asistiré/asistí")
    print("  2. No podré asistir (ausencia justificada)")
    print("  0. Cancelar")
    
    opcion = input("\nElige una opción: ").strip()
    
    if opcion == "1":
        resultado = registrar_asistencia_reserva(id_reserva, presentes=[str(ci_sesion)])
        if isinstance(resultado, dict):
            print(f"\n {resultado['mensaje']}")
            print(f"   Tu asistencia ha sido registrada como: PRESENTE")
        else:
            print(f" {resultado}")
    elif opcion == "2":
        resultado = registrar_asistencia_reserva(id_reserva, justificados=[str(ci_sesion)])
        if isinstance(resultado, dict):
            print(f"\n {resultado['mensaje']}")
            print(f"   Tu asistencia ha sido registrada como: JUSTIFICADO")
        else:
            print(f" {resultado}")
    else:
        print("Operación cancelada.")
    
    input("\nPresiona Enter para continuar...")


# ------------------- MENU REPORTES -------------------

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

# ------------------- MENU PRINCIPAL -------------------

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
            print(" Hasta luego!")
            break
        else:
            print("Opción no válida")
            input("Presioná Enter para continuar...")

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
            registrar_mi_asistencia_menu(ci_sesion)
        elif opcion == "6":
            consultar_mis_sanciones_menu(ci_sesion)
        elif opcion == "7":
            cambiar_mi_contrasena_menu(correo_sesion)
        elif opcion == "8":
            print(" ¡Hasta luego!")
            break
        else:
            print("Opción no válida")
            input("Presiona Enter para continuar...")
