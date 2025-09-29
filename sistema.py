"""
Módulo de sistema: Herramientas para monitoreo y obtención de información del sistema.

Este módulo proporciona funciones para mostrar información detallada del sistema operativo,
hardware (CPU, memoria, discos, batería, USB, gráfica), procesos en ejecución,
estadísticas de red, y monitoreo en tiempo real. Utiliza bibliotecas como psutil,
platform, subprocess y comandos del sistema para recopilar datos.
"""

import subprocess
import os
import psutil
import shutil
import platform
import getpass
import socket
# Importar los colores desde el archivo colores.py
from colores import (
    COLOR_RESET, COLOR_VERDE, COLOR_AMARILLO, COLOR_ROJO, COLOR_CIAN, COLOR_NARANJA,
    TEXTO_NEGRITA, TEXTO_SUBRAYADO
)

def mostrar_equipos_red():
    """   
    Solicita el rango de red (ej. 192.168.1.0/24) y ejecuta un escaneo completo con nmap
    incluyendo detección de OS, puertos y servicios. Muestra el resultado del escaneo.
    Manejo de errores: Captura excepciones y muestra errores.
    """
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Equipos conectados en la red local:{COLOR_RESET}")
    try:
        red = input(f"{COLOR_NARANJA}Introduce el rango de red a escanear (ejemplo: 192.168.1.0/24): {COLOR_RESET}")
        print(f"{COLOR_AMARILLO}Escaneando la red con nmap, esto puede tardar unos segundos...{COLOR_RESET}")
        resultado = subprocess.run(["sudo", "nmap", "-O", "-sS", "-sU", "-p-", "-T4", "-v", "-A", red], capture_output=True, text=True)
        print(f"{COLOR_VERDE}Resultado del escaneo:{COLOR_RESET}")
        print(resultado.stdout)
    except Exception as e:
        print(f"{COLOR_ROJO}Error al detectar equipos en la red: {e}{COLOR_RESET}")

def mostrar_info_bateria():
    """    
    Obtiene porcentaje de carga, tiempo restante y estado de carga.
    Si no hay batería, informa al usuario.
    Manejo de errores: Captura excepciones al acceder a sensores.
    """
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Información de la batería:{COLOR_RESET}")
    try:
        bateria = psutil.sensors_battery()
        if bateria:
            print(f"Porcentaje: {bateria.percent}%")
            print(f"Tiempo restante: {bateria.secsleft // 60} minutos" if bateria.secsleft != psutil.POWER_TIME_UNLIMITED else "Tiempo restante: ilimitado")
            print(f"¿Cargando?: {'Sí' if bateria.power_plugged else 'No'}")
        else:
            print(f"{COLOR_AMARILLO}No se detectó batería en este sistema.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al obtener información de la batería: {e}{COLOR_RESET}")

def mostrar_info_usb():
    """    
    Ejecuta lsusb para listar todos los dispositivos USB conectados.
    Manejo de errores: Captura excepciones y muestra errores.
    """
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Dispositivos USB conectados:{COLOR_RESET}")
    try:
        os.system("lsusb")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al obtener información de los dispositivos USB: {e}{COLOR_RESET}")

def mostrar_info_uptime():
    """  
    Lee el archivo /proc/uptime, calcula horas y minutos de uptime y los muestra.
    Manejo de errores: Captura excepciones al leer el archivo.
    """
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Tiempo de actividad del sistema:{COLOR_RESET}")
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            horas = int(uptime_seconds // 3600)
            minutos = int((uptime_seconds % 3600) // 60)
            print(f"El sistema lleva encendido: {horas} horas y {minutos} minutos.")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al obtener el tiempo de actividad: {e}{COLOR_RESET}")

def mostrar_info_sistema():
    """    
    Utiliza platform para obtener nombre del sistema, OS, versión; getpass para usuario;
    socket para FQDN; psutil para uso de CPU y memoria.
    No requiere parámetros, muestra directamente la información.
    """
    print("--- Información del sistema ---")
    print("Nombre del sistema: ", platform.node())
    print("Sistema operativo: ", platform.system())
    print("Versión del sistema operativo: ", platform.release())
    print("Nombre del usuario activo: ", getpass.getuser())
    print("Grupo de trabajo: ", socket.getfqdn())
    print("CPU: ", psutil.cpu_percent(interval=1), "%")
    print("Memoria RAM: ", psutil.virtual_memory().percent, "%")

def sizeof_fmt(num, suffix='B'):
    """
    Función auxiliar para formatear tamaños en bytes a unidades legibles (KB, MB, GB, etc.).
    
    Parámetros: num (número en bytes), suffix (sufijo, por defecto 'B').
    Itera dividiendo por 1024 hasta encontrar la unidad apropiada.
    Retorna string formateado con 1 decimal.
    """
    # Función auxiliar para formatear tamaños en bytes a una representación más legible
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Y', suffix)

def mostrar_info_discos():
    """
    Función para mostrar información de los discos duros usando psutil.
    
    Lista todas las particiones, sistema de archivos, y espacio total/usado/libre.
    Utiliza sizeof_fmt para formatear los tamaños.
    """
    print("--- Información del disco duro ---")
    discos = psutil.disk_partitions()
    for disco in discos:
        print("Disco: ", disco.device)
        print("Sistema de archivos: ", disco.fstype)
        
        # Obtener el tamaño total, usado y libre del disco
        espacio_total = psutil.disk_usage(disco.mountpoint).total
        espacio_usado = psutil.disk_usage(disco.mountpoint).used
        espacio_libre = psutil.disk_usage(disco.mountpoint).free
        
        # Formatear los tamaños para una mejor legibilidad
        espacio_total_fmt = sizeof_fmt(espacio_total)
        espacio_usado_fmt = sizeof_fmt(espacio_usado)
        espacio_libre_fmt = sizeof_fmt(espacio_libre)
        
        print("Espacio total: ", espacio_total_fmt)
        print("Espacio usado: ", espacio_usado_fmt)
        print("Espacio libre: ", espacio_libre_fmt)

def mostrar_info_memoria():
    """
    Función para mostrar información de la memoria RAM usando psutil.
    
    Muestra total, disponible, usada en GB y porcentaje utilizado.
    """
    print("--- Información de la memoria RAM ---")
    memoria = psutil.virtual_memory()
    print("Total: ", memoria.total / (1024**3), "GB")
    print("Disponible: ", memoria.available / (1024**3), "GB")
    print("Usada: ", memoria.used / (1024**3), "GB")
    print("Porcentaje utilizado: ", memoria.percent, "%")

def mostrar_info_cpu():
    """
    Función para mostrar información de la CPU usando psutil.
    
    Muestra porcentaje de uso por núcleo y promedio general.
    """
    print("--- Información de la CPU ---")
    # Mostrar porcentaje de uso de la CPU por núcleo
    for i, porcentaje in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
        print("CPU", i, ": ", porcentaje, "%")
    # Mostrar porcentaje promedio de uso de la CPU
    print("Promedio de uso de la CPU: ", psutil.cpu_percent(interval=1), "%")

def mostrar_info_red():
    """
    Función para mostrar estadísticas de red usando psutil.
    
    Muestra bytes enviados y recibidos desde el inicio del sistema.
    """
    print("--- Información de la red ---")
    # Obtener estadísticas de la red
    estadisticas = psutil.net_io_counters()
    print("Bytes enviados: ", estadisticas.bytes_sent)
    print("Bytes recibidos: ", estadisticas.bytes_recv)

def mostrar_info_procesos():
    """    
    Lista nombre, PID, uso de CPU y memoria de cada proceso.
    Manejo de errores: Ignora procesos no accesibles.
    """
    print("--- Información de los procesos en ejecución ---")
    # Obtener una lista de procesos
    procesos = psutil.process_iter()
    for proceso in procesos:
        try:
            nombre = proceso.name()
            pid = proceso.pid
            uso_cpu = proceso.cpu_percent(interval=0.1)
            uso_memoria = proceso.memory_percent()
            print("Proceso: ", nombre)
            print("PID: ", pid)
            print("Uso de CPU: ", uso_cpu, "%")
            print("Uso de memoria: ", uso_memoria, "%")
            print("--------------------")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def mostrar_info_sistema_archivos():
    """    
    Lista todas las particiones con dispositivo, punto de montaje, tipo FS, opciones,
    y espacio total/usado/libre en GB.
    Manejo de errores: Ignora particiones sin permisos.
    """
    print("--- Información del sistema de archivos ---")
    particiones = psutil.disk_partitions(all=True)
    for particion in particiones:
        print("Dispositivo: ", particion.device)
        print("Punto de montaje: ", particion.mountpoint)
        print("Tipo de sistema de archivos: ", particion.fstype)
        print("Opciones de montaje: ", particion.opts)
        try:
            total, usado, libre = shutil.disk_usage(particion.mountpoint)
            print("Espacio total: ", total / (1024**3), "GB")
            print("Espacio usado: ", usado / (1024**3), "GB")
            print("Espacio libre: ", libre / (1024**3), "GB")
        except PermissionError:
            print("No se puede acceder a la información del espacio en disco.")
        print("--------------------")

def matar_proceso():
    """
    Función para terminar un proceso por su PID usando psutil.
    
    Solicita el PID al usuario, obtiene el proceso y lo mata.
    """
    pid = input("Escribe el PID del proceso a matar: ")
    try:
        proceso = psutil.Process(int(pid))
        proceso.kill()
        print("Proceso con PID", pid, "eliminado.")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        print("No se pudo eliminar el proceso.")

# Función principal del programa
def mostrar_info_tarjeta_grafica():
    """
    Función para mostrar información de la tarjeta gráfica usando lspci.
    
    Ejecuta lspci -nnk y filtra líneas con controladores VGA o 3D.

    """
    print("--- Información de la tarjeta gráfica ---")
    try:
        resultado = subprocess.check_output(["lspci", "-nnk"], universal_newlines=True)
        graficas = [line for line in resultado.split('\n') if 'VGA compatible controller' in line or '3D controller' in line]
        if graficas:
            for grafica in graficas:
                print(grafica)
        else:
            print("No se encontró información de tarjeta gráfica.")
    except Exception as e:
        print("Error al obtener la información de la tarjeta gráfica:", e)

def monitoreo_recursos_tiempo_real():
    """   
    Muestra uso de CPU, memoria y disco cada 2 segundos en un bucle.
    Limpia pantalla cada actualización. Se detiene con Ctrl+C.
    Manejo de interrupción: Captura KeyboardInterrupt.
    """
    import time
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Monitoreo de recursos en tiempo real (presiona Ctrl+C para detener):{COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Actualizando cada 2 segundos...{COLOR_RESET}")
    try:
        while True:
            # Limpiar pantalla para actualizar
            os.system('clear')
            print(f"{COLOR_CIAN}{TEXTO_NEGRITA}--- MONITOREO EN TIEMPO REAL ---{COLOR_RESET}")
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            print(f"{COLOR_VERDE}CPU: {cpu_percent}%{COLOR_RESET}")
            # Memoria
            mem = psutil.virtual_memory()
            print(f"{COLOR_VERDE}Memoria: {mem.percent}% (Usada: {mem.used / (1024**3):.1f} GB / Total: {mem.total / (1024**3):.1f} GB){COLOR_RESET}")
            # Disco
            disk = psutil.disk_usage('/')
            print(f"{COLOR_VERDE}Disco (/): {disk.percent}% (Usado: {disk.used / (1024**3):.1f} GB / Total: {disk.total / (1024**3):.1f} GB){COLOR_RESET}")
            print(f"{COLOR_AMARILLO}Presiona Ctrl+C para detener...{COLOR_RESET}")
            time.sleep(2)
    except KeyboardInterrupt:
        print(f"\n{COLOR_NARANJA}Monitoreo detenido por el usuario.{COLOR_RESET}")

def main_menu():
    """   
    Muestra menú con opciones para todas las funciones de monitoreo e información.
    """
    while True:
        print(f"{COLOR_CIAN}{TEXTO_NEGRITA}\n--- MENÚ DE INFORMACIÓN DEL SISTEMA ---{COLOR_RESET}")
        print(f"{COLOR_VERDE}1. Mostrar información del sistema{COLOR_RESET}")
        print(f"{COLOR_VERDE}2. Mostrar información del disco duro{COLOR_RESET}")
        print(f"{COLOR_VERDE}3. Mostrar información de la memoria RAM{COLOR_RESET}")
        print(f"{COLOR_VERDE}4. Mostrar información de la CPU{COLOR_RESET}")
        print(f"{COLOR_VERDE}5. Mostrar información de los procesos en ejecución{COLOR_RESET}")
        print(f"{COLOR_VERDE}6. Matar proceso en ejecución{COLOR_RESET}")
        print(f"{COLOR_VERDE}7. Mostrar información del sistema de archivos{COLOR_RESET}")
        print(f"{COLOR_VERDE}8. Mostrar información de la tarjeta gráfica{COLOR_RESET}")
        print(f"{COLOR_VERDE}9. Mostrar información de la batería{COLOR_RESET}")
        print(f"{COLOR_VERDE}10. Mostrar dispositivos USB conectados{COLOR_RESET}")
        print(f"{COLOR_VERDE}11. Mostrar tiempo de actividad del sistema{COLOR_RESET}")
        print(f"{COLOR_VERDE}12. Monitoreo de recursos en tiempo real{COLOR_RESET}")
        print(f"{COLOR_ROJO}13. Volver al menú principal{COLOR_RESET}")
        opcion = input(f"{COLOR_NARANJA}Selecciona una opción: {COLOR_RESET}")

        if opcion == "1":
            mostrar_info_sistema()
        elif opcion == "2":
            mostrar_info_discos()
        elif opcion == "3":
            mostrar_info_memoria()
        elif opcion == "4":
            mostrar_info_cpu()
        elif opcion == "5":
            mostrar_info_procesos()
        elif opcion == "6":
            matar_proceso()
        elif opcion == "7":
            mostrar_info_sistema_archivos()
        elif opcion == "8":
            mostrar_info_tarjeta_grafica()
        elif opcion == "9":
            mostrar_info_bateria()
        elif opcion == "10":
            mostrar_info_usb()
        elif opcion == "11":
            mostrar_info_uptime()
        elif opcion == "12":
            monitoreo_recursos_tiempo_real()
        elif opcion == "13":
            break
        else:
            print(f"{COLOR_ROJO}Opción no válida. Inténtalo de nuevo.{COLOR_RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{COLOR_ROJO}Programa cerrado por el usuario (Ctrl+C).{COLOR_RESET}")