# usuarios.py
from colores import *
import subprocess

def crear_usuario():
    usuario = input(f"{COLOR_NARANJA}Introduce el nombre de usuario a crear: {COLOR_RESET}")
    try:
        subprocess.run(["sudo", "adduser", usuario], check=True)
        print(f"{COLOR_VERDE}Usuario '{usuario}' creado correctamente.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al crear usuario: {e}{COLOR_RESET}")

def eliminar_usuario():
    usuario = input(f"{COLOR_NARANJA}Introduce el nombre de usuario a eliminar: {COLOR_RESET}")
    try:
        subprocess.run(["sudo", "deluser", usuario], check=True)
        print(f"{COLOR_VERDE}Usuario '{usuario}' eliminado correctamente.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al eliminar usuario: {e}{COLOR_RESET}")

def modificar_usuario():
    usuario = input(f"{COLOR_NARANJA}Introduce el nombre de usuario a modificar: {COLOR_RESET}")
    nuevo_nombre = input(f"{COLOR_NARANJA}Introduce el nuevo nombre de usuario: {COLOR_RESET}")
    try:
        subprocess.run(["sudo", "usermod", "-l", nuevo_nombre, usuario], check=True)
        print(f"{COLOR_VERDE}Usuario modificado correctamente.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al modificar usuario: {e}{COLOR_RESET}")

def cambiar_contrasena():
    usuario = input(f"{COLOR_NARANJA}Introduce el nombre de usuario para cambiar la contraseña: {COLOR_RESET}")
    try:
        subprocess.run(["sudo", "passwd", usuario], check=True)
        print(f"{COLOR_VERDE}Contraseña cambiada correctamente.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al cambiar la contraseña: {e}{COLOR_RESET}")

def mostrar_usuarios_activos():
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Usuarios activos en el sistema:{COLOR_RESET}")
    try:
        subprocess.run(["who"], check=True)
    except Exception as e:
        print(f"{COLOR_ROJO}Error al mostrar usuarios activos: {e}{COLOR_RESET}")

def main_menu():
    while True:
        print(f"{COLOR_CIAN}{TEXTO_NEGRITA}\n--- MENÚ DE GESTIÓN DE USUARIOS ---{COLOR_RESET}")
        print(f"{COLOR_VERDE}1. Crear usuario{COLOR_RESET}")
        print(f"{COLOR_VERDE}2. Eliminar usuario{COLOR_RESET}")
        print(f"{COLOR_VERDE}3. Modificar usuario{COLOR_RESET}")
        print(f"{COLOR_VERDE}4. Cambiar contraseña{COLOR_RESET}")
        print(f"{COLOR_VERDE}5. Mostrar usuarios activos{COLOR_RESET}")
        print(f"{COLOR_ROJO}6. Volver al menú principal{COLOR_RESET}")
        opcion = input(f"{COLOR_NARANJA}Selecciona una opción: {COLOR_RESET}")
        if opcion == "1":
            crear_usuario()
        elif opcion == "2":
            eliminar_usuario()
        elif opcion == "3":
            modificar_usuario()
        elif opcion == "4":
            cambiar_contrasena()
        elif opcion == "5":
            mostrar_usuarios_activos()
        elif opcion == "6":
            break
        else:
            print(f"{COLOR_ROJO}Opción no válida. Inténtalo de nuevo.{COLOR_RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{COLOR_ROJO}Programa cerrado por el usuario (Ctrl+C).{COLOR_RESET}")
