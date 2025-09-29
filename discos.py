# Módulo para la gestión de discos y particiones en el sistema.
# Proporciona funciones para mostrar información, montar/desmontar, formatear y verificar sistemas de archivos.

from colores import *
import subprocess
import os

# Función para mostrar información detallada de discos y particiones
def mostrar_info_discos():
    print(f"{COLOR_AMARILLO}Información de discos y particiones:{COLOR_RESET}")
    try:
        # Ejecuta lsblk para obtener información de dispositivos de bloque
        resultado = subprocess.run(["lsblk", "-o", "NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT"], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(resultado.stdout)
        else:
            print(f"{COLOR_ROJO}Error al obtener información: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        # Maneja errores de ejecución del comando
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

# Función para mostrar el espacio utilizado en disco
def mostrar_espacio_disco():
    print(f"{COLOR_AMARILLO}Espacio en disco:{COLOR_RESET}")
    try:
        # Ejecuta df -h para mostrar uso de disco en formato legible
        resultado = subprocess.run(["df", "-h"], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(resultado.stdout)
        else:
            print(f"{COLOR_ROJO}Error al obtener espacio: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        # Maneja errores de ejecución
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

# Función para montar una partición en un punto de montaje
def montar_particion():
    # Solicita el dispositivo y punto de montaje
    dispositivo = input(f"{COLOR_NARANJA}Introduce el dispositivo a montar (ej. /dev/sdb1): {COLOR_RESET}")
    punto_montaje = input(f"{COLOR_NARANJA}Introduce el punto de montaje (ej. /mnt): {COLOR_RESET}")
    # Verifica si el punto de montaje existe, si no, ofrece crearlo
    if not os.path.exists(punto_montaje):
        crear = input(f"{COLOR_AMARILLO}El punto de montaje no existe. ¿Crear directorio? (s/n): {COLOR_RESET}")
        if crear.lower() == 's':
            try:
                os.makedirs(punto_montaje)
                print(f"{COLOR_VERDE}Directorio creado.{COLOR_RESET}")
            except Exception as e:
                print(f"{COLOR_ROJO}Error al crear directorio: {e}{COLOR_RESET}")
                return
        else:
            return
    print(f"{COLOR_AMARILLO}Montando {dispositivo} en {punto_montaje}...{COLOR_RESET}")
    try:
        # Ejecuta mount con sudo para montar la partición
        resultado = subprocess.run(["sudo", "mount", dispositivo, punto_montaje], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Partición montada correctamente.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error al montar: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

# Función para desmontar una partición
def desmontar_particion():
    # Solicita el punto de montaje a desmontar
    punto_montaje = input(f"{COLOR_NARANJA}Introduce el punto de montaje a desmontar (ej. /mnt): {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Desmontando {punto_montaje}...{COLOR_RESET}")
    try:
        # Ejecuta umount con sudo para desmontar
        resultado = subprocess.run(["sudo", "umount", punto_montaje], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Partición desmontada correctamente.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error al desmontar: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

# Función para formatear una partición con un sistema de archivos específico
def formatear_particion():
    # Solicita dispositivo y tipo de sistema de archivos
    dispositivo = input(f"{COLOR_NARANJA}Introduce el dispositivo a formatear (ej. /dev/sdb1): {COLOR_RESET}")
    tipo_fs = input(f"{COLOR_NARANJA}Introduce el tipo de sistema de archivos (ext4, ntfs, fat32, etc.): {COLOR_RESET}")
    # Confirmación de seguridad ya que borra todos los datos
    confirmacion = input(f"{COLOR_ROJO}¡ATENCIÓN! Esto borrará todos los datos en {dispositivo}. ¿Confirmar? (sí/no): {COLOR_RESET}")
    if confirmacion.lower() != 'sí':
        print(f"{COLOR_AMARILLO}Operación cancelada.{COLOR_RESET}")
        return
    print(f"{COLOR_AMARILLO}Formateando {dispositivo} como {tipo_fs}...{COLOR_RESET}")
    try:
        # Selecciona el comando apropiado según el tipo de FS
        if tipo_fs == 'ext4':
            cmd = ["sudo", "mkfs.ext4", dispositivo]
        elif tipo_fs == 'ntfs':
            cmd = ["sudo", "mkfs.ntfs", dispositivo]
        elif tipo_fs == 'fat32':
            cmd = ["sudo", "mkfs.vfat", "-F", "32", dispositivo]
        else:
            cmd = ["sudo", "mkfs", "-t", tipo_fs, dispositivo]
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Partición formateada correctamente.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error al formatear: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

# Función para verificar la integridad del sistema de archivos
def verificar_fs():
    # Solicita el dispositivo a verificar
    dispositivo = input(f"{COLOR_NARANJA}Introduce el dispositivo a verificar (ej. /dev/sdb1): {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Verificando sistema de archivos en {dispositivo}...{COLOR_RESET}")
    try:
        # Ejecuta fsck con sudo para verificar y reparar errores
        resultado = subprocess.run(["sudo", "fsck", dispositivo], capture_output=True, text=True)
        print(f"{COLOR_VERDE}Resultado de la verificación:{COLOR_RESET}")
        print(resultado.stdout)
        if resultado.stderr:
            print(f"{COLOR_ROJO}Errores encontrados: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

# Función principal de gestión de discos
def main_menu():
    while True:
        print(f"{COLOR_CIAN}{TEXTO_NEGRITA}\n--- GESTIÓN DE DISCOS Y PARTICIONES ---{COLOR_RESET}")
        print(f"{COLOR_VERDE}1. Mostrar información de discos y particiones{COLOR_RESET}")
        print(f"{COLOR_VERDE}2. Mostrar espacio en disco{COLOR_RESET}")
        print(f"{COLOR_VERDE}3. Montar partición{COLOR_RESET}")
        print(f"{COLOR_VERDE}4. Desmontar partición{COLOR_RESET}")
        print(f"{COLOR_VERDE}5. Formatear partición{COLOR_RESET}")
        print(f"{COLOR_VERDE}6. Verificar sistema de archivos{COLOR_RESET}")
        print(f"{COLOR_ROJO}7. Volver al menú principal{COLOR_RESET}")
        opcion = input(f"{COLOR_NARANJA}Selecciona una opción: {COLOR_RESET}")
        if opcion == "1":
            mostrar_info_discos()
        elif opcion == "2":
            mostrar_espacio_disco()
        elif opcion == "3":
            montar_particion()
        elif opcion == "4":
            desmontar_particion()
        elif opcion == "5":
            formatear_particion()
        elif opcion == "6":
            verificar_fs()
        elif opcion == "7":
            break
        else:
            print(f"{COLOR_ROJO}Opción no válida. Inténtalo de nuevo.{COLOR_RESET}")

# Bloque principal
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        # Maneja la interrupción del usuario (Ctrl+C)
        print(f"\n{COLOR_ROJO}Programa cerrado por el usuario (Ctrl+C).{COLOR_RESET}")