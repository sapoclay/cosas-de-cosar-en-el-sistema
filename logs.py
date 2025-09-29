# logs.py
from colores import *
import subprocess

def ver_logs_principales():
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Logs principales del sistema:{COLOR_RESET}")
    logs = [
        ("Syslog", "/var/log/syslog"),
        ("Auth log", "/var/log/auth.log"),
        ("Kernel log", "/var/log/kern.log"),
        ("Daemon log", "/var/log/daemon.log")
    ]
    for nombre, ruta in logs:
        print(f"{COLOR_VERDE}{TEXTO_NEGRITA}{nombre} ({ruta}):{COLOR_RESET}")
        try:
            resultado = subprocess.run(["sudo", "tail", "-20", ruta], capture_output=True, text=True)
            if resultado.returncode == 0:
                print(resultado.stdout)
            else:
                print(f"{COLOR_ROJO}Error al leer {ruta}: {resultado.stderr}{COLOR_RESET}")
        except Exception as e:
            print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")
        print()

def buscar_en_logs():
    patron = input(f"{COLOR_NARANJA}Introduce el patrón a buscar en los logs: {COLOR_RESET}")
    usar_fecha = input(f"{COLOR_NARANJA}¿Quieres filtrar por fecha? (s/n): {COLOR_RESET}").lower() == 's'
    fecha_desde = ""
    fecha_hasta = ""
    if usar_fecha:
        fecha_desde = input(f"{COLOR_NARANJA}Fecha desde (formato YYYY-MM-DD HH:MM:SS, o vacío para no limitar): {COLOR_RESET}")
        fecha_hasta = input(f"{COLOR_NARANJA}Fecha hasta (formato YYYY-MM-DD HH:MM:SS, o vacío para no limitar): {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Buscando '{patron}' en logs del sistema...{COLOR_RESET}")
    try:
        comando = ["sudo", "journalctl", "-g", patron, "--no-pager"]
        if fecha_desde:
            comando.extend(["--since", fecha_desde])
        if fecha_hasta:
            comando.extend(["--until", fecha_hasta])
        resultado = subprocess.run(comando, capture_output=True, text=True)
        if resultado.returncode == 0 and resultado.stdout.strip():
            print(f"{COLOR_VERDE}Resultados encontrados:{COLOR_RESET}")
            print(resultado.stdout)
        else:
            print(f"{COLOR_ROJO}No se encontraron resultados o error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error en la búsqueda: {e}{COLOR_RESET}")

def limpiar_logs_antiguos():
    print(f"{COLOR_AMARILLO}Rotando logs antiguos...{COLOR_RESET}")
    print(f"{COLOR_CIAN}Esto archivará los logs actuales en archivos comprimidos (ej. syslog.1.gz),")
    print(f"creará nuevos logs vacíos y eliminará los más antiguos según la configuración del sistema.")
    print(f"Esto ayuda a mantener el espacio en disco y mejora el rendimiento.{COLOR_RESET}")
    try:
        # Usar logrotate para rotar logs
        resultado = subprocess.run(["sudo", "logrotate", "-f", "/etc/logrotate.conf"], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Logs rotados correctamente. Los logs antiguos han sido archivados y comprimidos.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error al rotar logs: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

def main_menu():
    while True:
        print(f"{COLOR_CIAN}{TEXTO_NEGRITA}\n--- GESTIÓN DE LOGS DEL SISTEMA ---{COLOR_RESET}")
        print(f"{COLOR_VERDE}1. Ver logs principales{COLOR_RESET}")
        print(f"{COLOR_VERDE}2. Buscar en logs{COLOR_RESET}")
        print(f"{COLOR_VERDE}3. Limpiar/rotar logs antiguos{COLOR_RESET}")
        print(f"{COLOR_ROJO}4. Volver al menú principal{COLOR_RESET}")
        opcion = input(f"{COLOR_NARANJA}Selecciona una opción: {COLOR_RESET}")
        if opcion == "1":
            ver_logs_principales()
        elif opcion == "2":
            buscar_en_logs()
        elif opcion == "3":
            limpiar_logs_antiguos()
        elif opcion == "4":
            break
        else:
            print(f"{COLOR_ROJO}Opción no válida. Inténtalo de nuevo.{COLOR_RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{COLOR_ROJO}Programa cerrado por el usuario (Ctrl+C).{COLOR_RESET}")