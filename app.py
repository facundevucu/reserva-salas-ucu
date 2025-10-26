from backend.logica import crear_reserva

def mostrar_menu():
    print("\n=== Sistema de Reserva de Salas UCU ===")
    print("1. Crear nueva reserva")
    print("2. Salir")

def main():
    while True:
        mostrar_menu()
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
            print("Saliendo del sistema. ¡Hasta luego!")
            break

        else:
            print("Opción no válida. Por favor, intente nuevamente.")

if __name__ == "__main__":
    main()

