# servicios.py
from colores import *
import subprocess

def listar_servicios():
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Servicios activos/inactivos:{COLOR_RESET}")
    try:
        subprocess.run(["systemctl", "list-units", "--type=service"], check=True)
    except Exception as e:
        print(f"{COLOR_ROJO}Error al listar servicios: {e}{COLOR_RESET}")

def iniciar_servicio():
    servicio = input(f"{COLOR_NARANJA}Introduce el nombre del servicio a iniciar: {COLOR_RESET}")
    try:
        subprocess.run(["sudo", "systemctl", "start", servicio], check=True)
        print(f"{COLOR_VERDE}Servicio '{servicio}' iniciado correctamente.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al iniciar servicio: {e}{COLOR_RESET}")

def detener_servicio():
    servicio = input(f"{COLOR_NARANJA}Introduce el nombre del servicio a detener: {COLOR_RESET}")
    try:
        subprocess.run(["sudo", "systemctl", "stop", servicio], check=True)
        print(f"{COLOR_VERDE}Servicio '{servicio}' detenido correctamente.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al detener servicio: {e}{COLOR_RESET}")

def reiniciar_servicio():
    servicio = input(f"{COLOR_NARANJA}Introduce el nombre del servicio a reiniciar: {COLOR_RESET}")
    try:
        subprocess.run(["sudo", "systemctl", "restart", servicio], check=True)
        print(f"{COLOR_VERDE}Servicio '{servicio}' reiniciado correctamente.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al reiniciar servicio: {e}{COLOR_RESET}")

def estado_servicio():
    servicio = input(f"{COLOR_NARANJA}Introduce el nombre del servicio a consultar: {COLOR_RESET}")
    try:
        subprocess.run(["systemctl", "status", servicio], check=True)
    except Exception as e:
        print(f"{COLOR_ROJO}Error al consultar el estado del servicio: {e}{COLOR_RESET}")

def main_menu():
    while True:
        print(f"{COLOR_CIAN}{TEXTO_NEGRITA}\n--- MENÚ DE GESTIÓN DE SERVICIOS ---{COLOR_RESET}")
        print(f"{COLOR_VERDE}1. Listar servicios activos/inactivos{COLOR_RESET}")
        print(f"{COLOR_VERDE}2. Iniciar servicio{COLOR_RESET}")
        print(f"{COLOR_VERDE}3. Detener servicio{COLOR_RESET}")
        print(f"{COLOR_VERDE}4. Reiniciar servicio{COLOR_RESET}")
        print(f"{COLOR_VERDE}5. Consultar estado de servicio{COLOR_RESET}")
        print(f"{COLOR_ROJO}6. Volver al menú principal{COLOR_RESET}")
        opcion = input(f"{COLOR_NARANJA}Selecciona una opción: {COLOR_RESET}")
        if opcion == "1":
            listar_servicios()
        elif opcion == "2":
            iniciar_servicio()
        elif opcion == "3":
            detener_servicio()
        elif opcion == "4":
            reiniciar_servicio()
        elif opcion == "5":
            estado_servicio()
        elif opcion == "6":
            break
        else:
            print(f"{COLOR_ROJO}Opción no válida. Inténtalo de nuevo.{COLOR_RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{COLOR_ROJO}Programa cerrado por el usuario (Ctrl+C).{COLOR_RESET}")
