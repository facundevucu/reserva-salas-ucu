Guía para ejecutar el sistema de gestión de salas y reservas

Este proyecto utiliza Python y MySQL, ejecutados mediante Docker para
asegurar que funcione igual en cualquier computadora. A continuación se
detallan los pasos para instalar y ejecutar el sistema tanto en macOS
como en Windows.

1.  Requisitos previos Antes de comenzar, es necesario tener instalado
    Docker Desktop. Está disponible para macOS y Windows en:
    https://www.docker.com/products/docker-desktop.

2.  Clonar el repositorio:
    Abrir una terminal (macOS) o PowerShell/CMD (Windows) y ejecutar: 
    - git clone https://github.com/facundevucu/reserva-salas-ucu.git 
    - cd reserva-salas-ucu 

3.  Construir y levantar los contenedores:
    Desde la carpeta raíz del proyecto ejecutar: 
    - docker compose up --build

4.  Ejecutar el programa Ingresar al contenedor: 
    En otra ventana
    - docker exec -it python_app bash 
    Luego iniciar la aplicación: 
    - python backend/main.py

5.  Usuarios iniciales para pruebas:
    
    **Administrador:**
    - Correo: facundo.gonzales@ucu.edu.uy
    - Contraseña: pass1234 
    - Rol: admin
    
    **Usuario regular:**
    - Correo: ana.perez@ucu.edu.uy
    - Contraseña: pass2345
    - Rol: usuario
    
    **Nota de Seguridad:** Todas las contraseñas están hasheadas con SHA-256 en la base de datos.


6.  Detener los contenedores:
    - docker compose down

7.  Notas adicionales: 
    La base de datos persiste gracias al volumen definido en docker-compose.yml. 
    Si se desea resetear completamente, debe eliminarse el volumen mysql_data.
