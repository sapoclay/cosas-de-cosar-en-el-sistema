# Módulo para la gestión de impresoras en el sistema Linux.
# Utiliza el sistema de impresión CUPS para administrar impresoras, trabajos y servicios.

from colores import *
import subprocess

# Listar todas las impresoras instaladas en el sistema
def listar_impresoras():
    print(f"{COLOR_AMARILLO}Impresoras instaladas:{COLOR_RESET}")
    try:
        # Ejecuta lpstat -p para obtener la lista de impresoras
        resultado = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(resultado.stdout)
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        # Errores de ejecución del comando
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

# Función para añadir una nueva impresora al sistema
def agregar_impresora():
    # Solicita nombre, URI y driver opcional
    nombre = input(f"{COLOR_NARANJA}Introduce el nombre de la impresora: {COLOR_RESET}")
    uri = input(f"{COLOR_NARANJA}Introduce la URI de la impresora (ej. usb://HP/Deskjet?serial=123): {COLOR_RESET}")
    driver = input(f"{COLOR_NARANJA}Introduce el driver PPD (opcional, presiona Enter para omitir): {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Agregando impresora {nombre}...{COLOR_RESET}")
    try:
        # Construye el comando lpadmin con parámetros básicos
        cmd = ["lpadmin", "-p", nombre, "-E", "-v", uri]
        if driver:
            # Agrega el driver PPD si se especifica
            cmd.extend(["-P", driver])
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Impresora agregada correctamente.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

# Función para eliminar una impresora instalada
def eliminar_impresora():
    # Solicita el nombre de la impresora a eliminar
    nombre = input(f"{COLOR_NARANJA}Introduce el nombre de la impresora a eliminar: {COLOR_RESET}")
    # Confirmación de seguridad
    confirmacion = input(f"{COLOR_ROJO}¿Confirmar eliminación de {nombre}? (s/n): {COLOR_RESET}")
    if confirmacion.lower() != 's':
        print(f"{COLOR_AMARILLO}Operación cancelada.{COLOR_RESET}")
        return
    print(f"{COLOR_AMARILLO}Eliminando impresora {nombre}...{COLOR_RESET}")
    try:
        # Ejecuta lpadmin -x para eliminar la impresora
        resultado = subprocess.run(["lpadmin", "-x", nombre], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Impresora eliminada correctamente.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

# Configurar una impresora como la predeterminada
def configurar_impresora_defecto():
    # Solicita el nombre de la impresora por defecto
    nombre = input(f"{COLOR_NARANJA}Introduce el nombre de la impresora por defecto: {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Configurando {nombre} como impresora por defecto...{COLOR_RESET}")
    try:
        # Ejecuta lpadmin -d para establecer la impresora por defecto
        resultado = subprocess.run(["lpadmin", "-d", nombre], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Impresora por defecto configurada.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

# Ver la cola de impresión de una impresora
def ver_cola_impresion():
    # Solicita el nombre de la impresora (opcional)
    nombre = input(f"{COLOR_NARANJA}Introduce el nombre de la impresora (opcional, presiona Enter para todas): {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Cola de impresión:{COLOR_RESET}")
    try:
        if nombre:
            # Si se especifica nombre, muestra cola de esa impresora
            cmd = ["lpq", "-P", nombre]
        else:
            # Si no, muestra todas las colas
            cmd = ["lpq"]
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        print(resultado.stdout)
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

# Función para cancelar trabajos de impresión
def cancelar_trabajo():
    # Solicita nombre de impresora y ID de trabajo (opcional)
    nombre = input(f"{COLOR_NARANJA}Introduce el nombre de la impresora: {COLOR_RESET}")
    trabajo = input(f"{COLOR_NARANJA}Introduce el ID del trabajo a cancelar (opcional, presiona Enter para todos): {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Cancelando trabajos...{COLOR_RESET}")
    try:
        if trabajo:
            # Cancela un trabajo específico
            cmd = ["lprm", "-P", nombre, trabajo]
        else:
            # Cancela todos los trabajos de la impresora
            cmd = ["lprm", "-P", nombre, "-"]
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Trabajos cancelados.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

# Función para gestionar el servicio CUPS
def gestionar_servicio_cups():
    print(f"{COLOR_AMARILLO}Estado del servicio CUPS:{COLOR_RESET}")
    try:
        # Muestra el estado actual del servicio
        resultado = subprocess.run(["systemctl", "status", "cups"], capture_output=True, text=True)
        print(resultado.stdout)
    except Exception as e:
        print(f"{COLOR_ROJO}Error al obtener estado: {e}{COLOR_RESET}")
        return

    # Solicita la acción a realizar
    accion = input(f"{COLOR_NARANJA}¿Qué deseas hacer? (start/stop/restart/enable/disable): {COLOR_RESET}")
    if accion in ["start", "stop", "restart", "enable", "disable"]:
        print(f"{COLOR_AMARILLO}Ejecutando: sudo systemctl {accion} cups{COLOR_RESET}")
        try:
            # Ejecuta la acción solicitada con sudo
            resultado = subprocess.run(["sudo", "systemctl", accion, "cups"], capture_output=True, text=True)
            if resultado.returncode == 0:
                print(f"{COLOR_VERDE}Comando ejecutado correctamente.{COLOR_RESET}")
            else:
                print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
        except Exception as e:
            print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")
    else:
        print(f"{COLOR_ROJO}Acción no válida.{COLOR_RESET}")

# Función principal del menú de gestión de impresoras
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

# Bloque principal 
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        # Interrupción del usuario (Ctrl+C)
        print(f"\n{COLOR_ROJO}Programa cerrado por el usuario (Ctrl+C).{COLOR_RESET}")