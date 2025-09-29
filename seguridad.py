"""
Módulo de seguridad: Herramientas básicas para gestión de seguridad en Linux.

Este módulo proporciona funciones para gestionar permisos de archivos, propietarios,
configuración de firewall (ufw), verificación de integridad de archivos mediante hashes MD5,
gestión de configuración SSH y verificación de usuarios con permisos sudo.
Todas las funciones incluyen manejo de errores y solicitan confirmación para operaciones sensibles.
"""

from colores import *
import subprocess
import os

def gestionar_permisos():
    """
    Función para gestionar permisos de archivos y directorios usando el comando chmod.
    
    Solicita al usuario la ruta del archivo/directorio y los permisos deseados (ej. 755, u+x).
    Ejecuta el comando chmod con subprocess y muestra el resultado de la operación.
    Manejo de errores: Captura excepciones generales y muestra mensajes de error en rojo.
    """
    archivo = input(f"{COLOR_NARANJA}Introduce la ruta del archivo/directorio: {COLOR_RESET}")
    permisos = input(f"{COLOR_NARANJA}Introduce los permisos (ej. 755, u+x, etc.): {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Cambiando permisos de {archivo} a {permisos}...{COLOR_RESET}")
    try:
        resultado = subprocess.run(["chmod", permisos, archivo], capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Permisos cambiados correctamente.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

def cambiar_propietario():
    """
    Función para cambiar el propietario y grupo de archivos o directorios usando chown.
    
    Solicita la ruta del archivo, el nuevo propietario y opcionalmente el grupo.
    Construye el comando chown según si se especifica grupo o no.
    Ejecuta el comando y muestra el resultado.
    Manejo de errores: Captura excepciones y muestra errores.
    """
    archivo = input(f"{COLOR_NARANJA}Introduce la ruta del archivo/directorio: {COLOR_RESET}")
    usuario = input(f"{COLOR_NARANJA}Introduce el nuevo propietario: {COLOR_RESET}")
    grupo = input(f"{COLOR_NARANJA}Introduce el nuevo grupo (opcional, presiona Enter para omitir): {COLOR_RESET}")
    if grupo:
        cmd = ["chown", f"{usuario}:{grupo}", archivo]
    else:
        cmd = ["chown", usuario, archivo]
    print(f"{COLOR_AMARILLO}Cambiando propietario de {archivo}...{COLOR_RESET}")
    try:
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Propietario cambiado correctamente.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

def configurar_firewall():
    """
    Función para configurar el firewall usando ufw (Uncomplicated Firewall).
    
    Muestra el estado actual del firewall, luego permite habilitar/deshabilitar,
    permitir/denegar reglas, o recargar la configuración.
    Para allow/deny, solicita la regla específica (ej. 22/tcp).
    Ejecuta comandos sudo ufw y muestra resultados.
    Manejo de errores: Captura excepciones al obtener estado o ejecutar comandos.
    """
    print(f"{COLOR_AMARILLO}Estado actual del firewall (ufw):{COLOR_RESET}")
    try:
        resultado = subprocess.run(["sudo", "ufw", "status"], capture_output=True, text=True)
        print(resultado.stdout)
    except Exception as e:
        print(f"{COLOR_ROJO}Error al obtener estado: {e}{COLOR_RESET}")
        return

    accion = input(f"{COLOR_NARANJA}¿Qué deseas hacer? (enable/disable/allow/deny/reload): {COLOR_RESET}")
    if accion in ["enable", "disable", "reload"]:
        cmd = ["sudo", "ufw", accion]
    elif accion in ["allow", "deny"]:
        regla = input(f"{COLOR_NARANJA}Introduce la regla (ej. 22/tcp, 80): {COLOR_RESET}")
        cmd = ["sudo", "ufw", accion, regla]
    else:
        print(f"{COLOR_ROJO}Acción no válida.{COLOR_RESET}")
        return

    print(f"{COLOR_AMARILLO}Ejecutando: {' '.join(cmd)}{COLOR_RESET}")
    try:
        resultado = subprocess.run(cmd, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"{COLOR_VERDE}Comando ejecutado correctamente.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

def verificar_integridad():
    """
    Función para verificar la integridad de archivos calculando y comparando hashes MD5.
    
    Solicita la ruta del archivo y opcionalmente el hash MD5 original.
    Calcula el hash usando md5sum y lo compara si se proporciona el original.
    Muestra el hash calculado y el resultado de la comparación.
    Manejo de errores: Captura excepciones y errores de comando.
    """
    archivo = input(f"{COLOR_NARANJA}Introduce la ruta del archivo a verificar: {COLOR_RESET}")
    hash_original = input(f"{COLOR_NARANJA}Introduce el hash MD5 original (opcional, presiona Enter para calcular): {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Calculando hash MD5 de {archivo}...{COLOR_RESET}")
    try:
        resultado = subprocess.run(["md5sum", archivo], capture_output=True, text=True)
        if resultado.returncode == 0:
            hash_calculado = resultado.stdout.split()[0]
            print(f"{COLOR_VERDE}Hash MD5 calculado: {hash_calculado}{COLOR_RESET}")
            if hash_original:
                if hash_calculado == hash_original:
                    print(f"{COLOR_VERDE}¡Integridad verificada! Los hashes coinciden.{COLOR_RESET}")
                else:
                    print(f"{COLOR_ROJO}¡Alerta! Los hashes no coinciden. El archivo puede estar corrupto o modificado.{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

def gestionar_ssh():
    """
    Función para gestionar la configuración básica de SSH (sshd_config).
    
    Muestra configuración actual del puerto y PermitRootLogin.
    Permite cambiar el puerto SSH o la política de login de root.
    Usa sed para modificar el archivo de configuración y recuerda reiniciar SSH.
    Manejo de errores: Captura excepciones al leer/escribir archivo o ejecutar comandos.
    """
    print(f"{COLOR_AMARILLO}Configuración actual de SSH:{COLOR_RESET}")
    try:
        with open("/etc/ssh/sshd_config", "r") as f:
            for linea in f:
                if linea.startswith("Port ") or linea.startswith("PermitRootLogin"):
                    print(linea.strip())
    except Exception as e:
        print(f"{COLOR_ROJO}Error al leer configuración SSH: {e}{COLOR_RESET}")
        return

    opcion = input(f"{COLOR_NARANJA}¿Qué deseas cambiar? (puerto/root): {COLOR_RESET}")
    if opcion == "puerto":
        nuevo_puerto = input(f"{COLOR_NARANJA}Introduce el nuevo puerto SSH: {COLOR_RESET}")
        print(f"{COLOR_AMARILLO}Cambiando puerto SSH a {nuevo_puerto}...{COLOR_RESET}")
        try:
            resultado = subprocess.run(["sudo", "sed", "-i", f"s/^Port .*/Port {nuevo_puerto}/", "/etc/ssh/sshd_config"], capture_output=True, text=True)
            if resultado.returncode == 0:
                print(f"{COLOR_VERDE}Puerto cambiado. Recuerda reiniciar SSH: sudo systemctl restart ssh{COLOR_RESET}")
            else:
                print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
        except Exception as e:
            print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")
    elif opcion == "root":
        permitir = input(f"{COLOR_NARANJA}¿Permitir login de root? (yes/no): {COLOR_RESET}")
        print(f"{COLOR_AMARILLO}Cambiando PermitRootLogin a {permitir}...{COLOR_RESET}")
        try:
            resultado = subprocess.run(["sudo", "sed", "-i", f"s/^PermitRootLogin .*/PermitRootLogin {permitir}/", "/etc/ssh/sshd_config"], capture_output=True, text=True)
            if resultado.returncode == 0:
                print(f"{COLOR_VERDE}Configuración cambiada. Recuerda reiniciar SSH: sudo systemctl restart ssh{COLOR_RESET}")
            else:
                print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
        except Exception as e:
            print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")
    else:
        print(f"{COLOR_ROJO}Opción no válida.{COLOR_RESET}")

def verificar_usuarios_sudo():
    """
    Función para verificar y listar usuarios con permisos sudo.
    
    Obtiene los miembros del grupo 'sudo' usando getent group sudo.
    Lista los usuarios encontrados.
    Manejo de errores: Captura excepciones y errores de comando.
    """
    print(f"{COLOR_AMARILLO}Usuarios con permisos sudo:{COLOR_RESET}")
    try:
        resultado = subprocess.run(["getent", "group", "sudo"], capture_output=True, text=True)
        if resultado.returncode == 0:
            grupo = resultado.stdout.split(":")[-1].strip()
            usuarios = grupo.split(",")
            for usuario in usuarios:
                if usuario:
                    print(f"- {usuario}")
        else:
            print(f"{COLOR_ROJO}Error: {resultado.stderr}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error: {e}{COLOR_RESET}")

def main_menu():
    """
    Función del menú principal para herramientas de seguridad.

    """
    while True:
        print(f"{COLOR_CIAN}{TEXTO_NEGRITA}\n--- HERRAMIENTAS DE SEGURIDAD BÁSICA ---{COLOR_RESET}")
        print(f"{COLOR_VERDE}1. Gestionar permisos de archivos (chmod){COLOR_RESET}")
        print(f"{COLOR_VERDE}2. Cambiar propietario de archivos (chown){COLOR_RESET}")
        print(f"{COLOR_VERDE}3. Configurar firewall (ufw){COLOR_RESET}")
        print(f"{COLOR_VERDE}4. Verificar integridad de archivos (MD5){COLOR_RESET}")
        print(f"{COLOR_VERDE}5. Gestionar configuración SSH{COLOR_RESET}")
        print(f"{COLOR_VERDE}6. Verificar usuarios con permisos sudo{COLOR_RESET}")
        print(f"{COLOR_ROJO}7. Volver al menú principal{COLOR_RESET}")
        opcion = input(f"{COLOR_NARANJA}Selecciona una opción: {COLOR_RESET}")
        if opcion == "1":
            gestionar_permisos()
        elif opcion == "2":
            cambiar_propietario()
        elif opcion == "3":
            configurar_firewall()
        elif opcion == "4":
            verificar_integridad()
        elif opcion == "5":
            gestionar_ssh()
        elif opcion == "6":
            verificar_usuarios_sudo()
        elif opcion == "7":
            break
        else:
            print(f"{COLOR_ROJO}Opción no válida. Inténtalo de nuevo.{COLOR_RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{COLOR_ROJO}Programa cerrado por el usuario (Ctrl+C).{COLOR_RESET}")