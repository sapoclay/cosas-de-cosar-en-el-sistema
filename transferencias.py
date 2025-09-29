# transferencias.py
from colores import *
import subprocess

def ejecutar_comando_remoto():
    host = input(f"{COLOR_NARANJA}Introduce la IP o hostname del servidor remoto: {COLOR_RESET}")
    usuario = input(f"{COLOR_NARANJA}Introduce el usuario remoto: {COLOR_RESET}")
    comando = input(f"{COLOR_NARANJA}Introduce el comando a ejecutar remotamente: {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Ejecutando '{comando}' en {usuario}@{host}...{COLOR_RESET}")
    try:
        resultado = subprocess.run(["ssh", f"{usuario}@{host}", comando], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Resultado:{COLOR_RESET}")
            print(resultado.stdout)
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al ejecutar comando remoto: {e}{COLOR_RESET}")

def transferir_archivo_scp():
    origen = input(f"{COLOR_NARANJA}Ruta del archivo origen (local o remoto, ej. usuario@host:/ruta): {COLOR_RESET}")
    destino = input(f"{COLOR_NARANJA}Ruta del destino (local o remoto, ej. usuario@host:/ruta): {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Transfiriendo de {origen} a {destino}...{COLOR_RESET}")
    try:
        resultado = subprocess.run(["scp", origen, destino], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Transferencia completada.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error en la transferencia: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

def sincronizar_directorios_rsync():
    origen = input(f"{COLOR_NARANJA}Directorio origen (local o remoto, ej. usuario@host:/ruta): {COLOR_RESET}")
    destino = input(f"{COLOR_NARANJA}Directorio destino (local o remoto, ej. usuario@host:/ruta): {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Sincronizando {origen} con {destino}...{COLOR_RESET}")
    try:
        resultado = subprocess.run(["rsync", "-avz", origen, destino], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Sincronización completada.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error en la sincronización: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

def main_menu():
    while True:
        print(f"{COLOR_CIAN}{TEXTO_NEGRITA}\n--- HERRAMIENTAS DE REDIRECCIÓN Y TRANSFERENCIA ---{COLOR_RESET}")
        print(f"{COLOR_VERDE}1. Ejecutar comando remoto via SSH{COLOR_RESET}")
        print(f"{COLOR_VERDE}2. Transferir archivo con SCP{COLOR_RESET}")
        print(f"{COLOR_VERDE}3. Sincronizar directorios con rsync{COLOR_RESET}")
        print(f"{COLOR_ROJO}4. Volver al menú principal{COLOR_RESET}")
        opcion = input(f"{COLOR_NARANJA}Selecciona una opción: {COLOR_RESET}")
        if opcion == "1":
            ejecutar_comando_remoto()
        elif opcion == "2":
            transferir_archivo_scp()
        elif opcion == "3":
            sincronizar_directorios_rsync()
        elif opcion == "4":
            break
        else:
            print(f"{COLOR_ROJO}Opción no válida. Inténtalo de nuevo.{COLOR_RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{COLOR_ROJO}Programa cerrado por el usuario (Ctrl+C).{COLOR_RESET}")