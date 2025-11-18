# aca dejo todo modularizado y limpio
# en modulos dejo todo el codigo de cada funcionalidad
from modulos import pantalla_login, main_admin, main_usuario

def main():
    sesion = pantalla_login()
    if not sesion:
        print("No se pudo iniciar sesión.")
        input("Presiona Enter para salir...")
        return

    if sesion["rol"] == "admin":
        main_admin()
    elif sesion["rol"] == "usuario":
        if sesion.get("ci"):
            main_usuario(sesion["ci"], sesion["correo"])
        else:
            print("No se pudo cargar información del usuario.")
            input("Presiona Enter para salir...")


if __name__ == "__main__":
    main()