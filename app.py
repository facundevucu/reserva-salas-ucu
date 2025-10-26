from backend.logica import crear_reserva
from backend import reportes  

def mostrar_menu_principal():
    print("\n=== Sistema de Reserva de Salas UCU ===")
    print("1. Crear nueva reserva")
    print("2. Ver reportes")
    print("3. Salir")


def menu_reportes():
    """Muestra el submenú de reportes."""
    while True:
        print("\n=== Reportes disponibles ===")
        print("1. Salas más reservadas")
        print("2. Turnos más demandados")
        print("3. Promedio de participantes por sala")
        print("4. Reservas por carrera y facultad")
        print("5. Porcentaje de ocupación por edificio")
        print("6. Reservas y asistencias por tipo y rol")
        print("7. Sanciones por tipo y rol")
        print("8. Porcentaje de reservas utilizadas vs no utilizadas")
        print("9. Volver al menú principal")

        opcion = input("Seleccione un reporte: ")

        if opcion == "1":
            reportes.salas_mas_reservadas()
        elif opcion == "2":
            reportes.turnos_mas_demandados()
        elif opcion == "3":
            reportes.promedio_participantes_por_sala()
        elif opcion == "4":
            reportes.reservas_por_carrera_y_facultad()
        elif opcion == "5":
            reportes.porcentaje_ocupacion_por_edificio()
        elif opcion == "6":
            reportes.reservas_y_asistencias_por_tipo_y_rol()
        elif opcion == "7":
            reportes.sanciones_por_tipo_y_rol()
        elif opcion == "8":
            reportes.porcentaje_reservas_utilizadas()
        elif opcion == "9":
            break
        else:
            print("Opción no válida. Intente nuevamente.")


def main():
    while True:
        mostrar_menu_principal()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            ci_participante = input("Ingrese su CI de participante: ")
            nombre_sala = input("Ingrese el nombre de la sala: ")
            id_turno = input("Ingrese el ID del turno: ")
            fecha = input("Ingrese la fecha (YYYY-MM-DD): ")
            cantidad_participantes = int(input("Ingrese la cantidad de participantes: "))

            resultado = crear_reserva(ci_participante, nombre_sala, id_turno, fecha, cantidad_participantes)
            print("\n" + resultado)

        elif opcion == '2':
            menu_reportes()

        elif opcion == '3':
            print("Saliendo del sistema. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Por favor, intente nuevamente.")


if __name__ == "__main__":
    main()
