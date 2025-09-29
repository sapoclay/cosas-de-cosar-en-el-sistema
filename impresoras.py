# impresoras.py
from colores import *
import subprocess

def listar_impresoras():
    print(f"{COLOR_AMARILLO}Impresoras instaladas:{COLOR_RESET}")
    try:
        resultado = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(resultado.stdout)
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

def agregar_impresora():
    nombre = input(f"{COLOR_NARANJA}Introduce el nombre de la impresora: {COLOR_RESET}")
    uri = input(f"{COLOR_NARANJA}Introduce la URI de la impresora (ej. usb://HP/Deskjet?serial=123): {COLOR_RESET}")
    driver = input(f"{COLOR_NARANJA}Introduce el driver PPD (opcional, presiona Enter para omitir): {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Agregando impresora {nombre}...{COLOR_RESET}")
    try:
        cmd = ["lpadmin", "-p", nombre, "-E", "-v", uri]
        if driver:
            cmd.extend(["-P", driver])
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Impresora agregada correctamente.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

def eliminar_impresora():
    nombre = input(f"{COLOR_NARANJA}Introduce el nombre de la impresora a eliminar: {COLOR_RESET}")
    confirmacion = input(f"{COLOR_ROJO}¿Confirmar eliminación de {nombre}? (s/n): {COLOR_RESET}")
    if confirmacion.lower() != 's':
        print(f"{COLOR_AMARILLO}Operación cancelada.{COLOR_RESET}")
        return
    print(f"{COLOR_AMARILLO}Eliminando impresora {nombre}...{COLOR_RESET}")
    try:
        resultado = subprocess.run(["lpadmin", "-x", nombre], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Impresora eliminada correctamente.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

def configurar_impresora_defecto():
    nombre = input(f"{COLOR_NARANJA}Introduce el nombre de la impresora por defecto: {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Configurando {nombre} como impresora por defecto...{COLOR_RESET}")
    try:
        resultado = subprocess.run(["lpadmin", "-d", nombre], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Impresora por defecto configurada.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

def ver_cola_impresion():
    nombre = input(f"{COLOR_NARANJA}Introduce el nombre de la impresora (opcional, presiona Enter para todas): {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Cola de impresión:{COLOR_RESET}")
    try:
        if nombre:
            cmd = ["lpq", "-P", nombre]
        else:
            cmd = ["lpq"]
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        print(resultado.stdout)
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

def cancelar_trabajo():
    nombre = input(f"{COLOR_NARANJA}Introduce el nombre de la impresora: {COLOR_RESET}")
    trabajo = input(f"{COLOR_NARANJA}Introduce el ID del trabajo a cancelar (opcional, presiona Enter para todos): {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Cancelando trabajos...{COLOR_RESET}")
    try:
        if trabajo:
            cmd = ["lprm", "-P", nombre, trabajo]
        else:
            cmd = ["lprm", "-P", nombre, "-"]
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Trabajos cancelados.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

def gestionar_servicio_cups():
    print(f"{COLOR_AMARILLO}Estado del servicio CUPS:{COLOR_RESET}")
    try:
        resultado = subprocess.run(["systemctl", "status", "cups"], capture_output=True, text=True)
        print(resultado.stdout)
    except Exception as e:
        print(f"{COLOR_ROJO}Error al obtener estado: {e}{COLOR_RESET}")
        return

    accion = input(f"{COLOR_NARANJA}¿Qué deseas hacer? (start/stop/restart/enable/disable): {COLOR_RESET}")
    if accion in ["start", "stop", "restart", "enable", "disable"]:
        print(f"{COLOR_AMARILLO}Ejecutando: sudo systemctl {accion} cups{COLOR_RESET}")
        try:
            resultado = subprocess.run(["sudo", "systemctl", accion, "cups"], capture_output=True, text=True)
            if resultado.returncode == 0:
                print(f"{COLOR_VERDE}Comando ejecutado correctamente.{COLOR_RESET}")
            else:
                print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
        except Exception as e:
            print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")
    else:
        print(f"{COLOR_ROJO}Acción no válida.{COLOR_RESET}")

def main_menu():
    while True:
        print(f"{COLOR_CIAN}{TEXTO_NEGRITA}\n--- GESTIÓN DE IMPRESORAS ---{COLOR_RESET}")
        print(f"{COLOR_VERDE}1. Listar impresoras instaladas{COLOR_RESET}")
        print(f"{COLOR_VERDE}2. Agregar impresora{COLOR_RESET}")
        print(f"{COLOR_VERDE}3. Eliminar impresora{COLOR_RESET}")
        print(f"{COLOR_VERDE}4. Configurar impresora por defecto{COLOR_RESET}")
        print(f"{COLOR_VERDE}5. Ver cola de impresión{COLOR_RESET}")
        print(f"{COLOR_VERDE}6. Cancelar trabajos de impresión{COLOR_RESET}")
        print(f"{COLOR_VERDE}7. Gestionar servicio CUPS{COLOR_RESET}")
        print(f"{COLOR_ROJO}8. Volver al menú principal{COLOR_RESET}")
        opcion = input(f"{COLOR_NARANJA}Selecciona una opción: {COLOR_RESET}")
        if opcion == "1":
            listar_impresoras()
        elif opcion == "2":
            agregar_impresora()
        elif opcion == "3":
            eliminar_impresora()
        elif opcion == "4":
            configurar_impresora_defecto()
        elif opcion == "5":
            ver_cola_impresion()
        elif opcion == "6":
            cancelar_trabajo()
        elif opcion == "7":
            gestionar_servicio_cups()
        elif opcion == "8":
            break
        else:
            print(f"{COLOR_ROJO}Opción no válida. Inténtalo de nuevo.{COLOR_RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{COLOR_ROJO}Programa cerrado por el usuario (Ctrl+C).{COLOR_RESET}")