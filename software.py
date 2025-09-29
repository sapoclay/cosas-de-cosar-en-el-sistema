"""
Módulo de software: Herramientas para gestión de paquetes y repositorios en sistemas Debian/Ubuntu.

Este módulo permite actualizar repositorios, instalar/buscar/eliminar paquetes,
gestionar repositorios, actualizar el sistema, limpiar paquetes innecesarios
y exportar listas de paquetes. Utiliza comandos apt y dpkg para la gestión.
Todas las operaciones que requieren privilegios usan sudo.
"""

from colores import (
    COLOR_RESET, COLOR_VERDE, COLOR_AMARILLO, COLOR_ROJO, COLOR_CIAN, COLOR_NARANJA,
    TEXTO_NEGRITA, TEXTO_SUBRAYADO
)
import subprocess
import sys

def actualizar_repositorios():
    """    
    Ejecuta 'sudo apt update' para sincronizar la lista de paquetes.
    Muestra mensaje de éxito si se actualiza correctamente.
    Manejo de errores: Captura excepciones y muestra errores.
    """
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Actualizando listado de repositorios...{COLOR_RESET}")
    try:
        subprocess.run(["sudo", "apt", "update"], check=True)
        print(f"{COLOR_VERDE}Repositorios actualizados correctamente.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al actualizar repositorios: {e}{COLOR_RESET}")

def agregar_repositorio():
    """   
    Solicita la URL o PPA del repositorio y ejecuta 'sudo add-apt-repository'.
    Manejo de errores: Captura excepciones y muestra errores.
    """
    repo = input(f"{COLOR_NARANJA}Introduce el repositorio a añadir (ej: ppa:nombre/ppa): {COLOR_RESET}")
    try:
        subprocess.run(["sudo", "add-apt-repository", repo], check=True)
        print(f"{COLOR_VERDE}Repositorio añadido correctamente.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al añadir el repositorio: {e}{COLOR_RESET}")

def instalar_paquete():
    """   
    Solicita el nombre del paquete y ejecuta 'sudo apt install -y'.
    El flag -y confirma automáticamente la instalación.
    Manejo de errores: Captura excepciones y muestra errores.
    """
    paquete = input(f"{COLOR_NARANJA}Introduce el nombre del paquete a instalar: {COLOR_RESET}")
    try:
        subprocess.run(["sudo", "apt", "install", paquete, "-y"], check=True)
        print(f"{COLOR_VERDE}Paquete '{paquete}' instalado correctamente.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al instalar el paquete: {e}{COLOR_RESET}")

def buscar_paquete():
    """   
    Solicita el nombre del paquete y ejecuta 'apt search' para mostrar resultados.
    Manejo de errores: Captura excepciones y muestra errores.
    """
    paquete = input(f"{COLOR_NARANJA}Introduce el nombre del paquete a buscar: {COLOR_RESET}")
    try:
        subprocess.run(["apt", "search", paquete], check=True)
    except Exception as e:
        print(f"{COLOR_ROJO}Error al buscar el paquete: {e}{COLOR_RESET}")


def consultar_repositorios():
    """
    Muestra líneas deb de /etc/apt/sources.list y lista archivos en sources.list.d.
    Manejo de errores: Captura excepciones y muestra errores.
    """
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Repositorios instalados en el sistema:{COLOR_RESET}")
    try:
        subprocess.run(["grep", "^deb", "/etc/apt/sources.list"], check=False)
        subprocess.run(["ls", "/etc/apt/sources.list.d/"], check=False)
    except Exception as e:
        print(f"{COLOR_ROJO}Error al consultar los repositorios: {e}{COLOR_RESET}")

def eliminar_repositorio():
    """    
    Lista archivos en /etc/apt/sources.list.d y permite seleccionar uno para eliminar.
    Ejecuta 'sudo rm' en el archivo seleccionado.
    Manejo de errores: Captura excepciones y validaciones de entrada.
    """
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Eliminar repositorio:{COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Archivos de repositorios en /etc/apt/sources.list.d/{COLOR_RESET}")
    try:
        resultado = subprocess.run(["ls", "/etc/apt/sources.list.d/"], capture_output=True, text=True)
        archivos = resultado.stdout.strip().split('\n')
        for i, archivo in enumerate(archivos):
            print(f"{COLOR_VERDE}{i+1}. {archivo}{COLOR_RESET}")
        seleccion = input(f"{COLOR_NARANJA}Selecciona el número del repositorio a eliminar (o 0 para cancelar): {COLOR_RESET}")
        if seleccion == "0":
            return
        try:
            seleccion = int(seleccion)
            if 1 <= seleccion <= len(archivos):
                archivo_a_borrar = archivos[seleccion-1]
                subprocess.run(["sudo", "rm", f"/etc/apt/sources.list.d/{archivo_a_borrar}"], check=True)
                print(f"{COLOR_VERDE}Repositorio eliminado correctamente.{COLOR_RESET}")
            else:
                print(f"{COLOR_ROJO}Selección inválida.{COLOR_RESET}")
        except ValueError:
            print(f"{COLOR_ROJO}Selección inválida.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al eliminar el repositorio: {e}{COLOR_RESET}")


def actualizar_paquetes():
    """    
    Ejecuta 'sudo apt upgrade -y' para actualizar paquetes instalados.
    Manejo de errores: Captura excepciones y muestra errores.
    """
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Actualizando todos los paquetes del sistema...{COLOR_RESET}")
    try:
        subprocess.run(["sudo", "apt", "upgrade", "-y"], check=True)
        print(f"{COLOR_VERDE}Todos los paquetes han sido actualizados correctamente.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al actualizar los paquetes: {e}{COLOR_RESET}")

def info_paquete():
    """   
    Solicita el nombre del paquete y ejecuta 'apt show' para mostrar detalles.
    Manejo de errores: Captura excepciones y muestra errores.
    """
    paquete = input(f"{COLOR_NARANJA}Introduce el nombre del paquete para ver información detallada: {COLOR_RESET}")
    try:
        subprocess.run(["apt", "show", paquete], check=True)
    except Exception as e:
        print(f"{COLOR_ROJO}Error al mostrar la información del paquete: {e}{COLOR_RESET}")

def limpiar_paquetes():
    """    
    Ejecuta 'sudo apt autoremove -y' para eliminar paquetes huérfanos y 'sudo apt clean' para limpiar caché.
    Manejo de errores: Captura excepciones y muestra errores.
    """
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Limpiando paquetes y dependencias no necesarias...{COLOR_RESET}")
    try:
        subprocess.run(["sudo", "apt", "autoremove", "-y"], check=True)
        subprocess.run(["sudo", "apt", "clean"], check=True)
        print(f"{COLOR_VERDE}Sistema limpio de paquetes innecesarios.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al limpiar paquetes: {e}{COLOR_RESET}")

def exportar_paquetes():
    """    
    Solicita el nombre del archivo y usa 'dpkg-query' para obtener la lista de paquetes instalados.
    Escribe la lista en el archivo especificado.
    Manejo de errores: Captura excepciones al escribir archivo.
    """
    archivo = input(f"{COLOR_NARANJA}Introduce el nombre del archivo para exportar la lista de paquetes: {COLOR_RESET}")
    try:
        with open(archivo, "w") as f:
            subprocess.run(["dpkg-query", "-f", "${binary:Package}\n", "-W"], stdout=f, check=True)
        print(f"{COLOR_VERDE}Lista de paquetes exportada correctamente a {archivo}.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al exportar la lista de paquetes: {e}{COLOR_RESET}")

def main_menu():
    """
    Función del menú principal para gestión de software.
    """
    while True:
        print(f"{COLOR_CIAN}{TEXTO_NEGRITA}\n--- MENÚ DE GESTIÓN DE SOFTWARE ---{COLOR_RESET}")
        print(f"{COLOR_VERDE}1. Actualizar listado de repositorios{COLOR_RESET}")
        print(f"{COLOR_VERDE}2. Añadir nuevo repositorio{COLOR_RESET}")
        print(f"{COLOR_VERDE}3. Instalar paquete de repositorio{COLOR_RESET}")
        print(f"{COLOR_VERDE}4. Buscar paquete en repositorios{COLOR_RESET}")
        print(f"{COLOR_VERDE}5. Consultar repositorios instalados{COLOR_RESET}")
        print(f"{COLOR_VERDE}6. Eliminar repositorio instalado{COLOR_RESET}")
        print(f"{COLOR_VERDE}7. Actualizar todos los paquetes del sistema{COLOR_RESET}")
        print(f"{COLOR_VERDE}8. Mostrar información detallada de un paquete{COLOR_RESET}")
        print(f"{COLOR_VERDE}9. Limpiar paquetes y dependencias no necesarias{COLOR_RESET}")
        print(f"{COLOR_VERDE}10. Exportar lista de paquetes instalados{COLOR_RESET}")
        print(f"{COLOR_ROJO}11. Volver al menú principal{COLOR_RESET}")
        opcion = input(f"{COLOR_NARANJA}Selecciona una opción: {COLOR_RESET}")
        if opcion == "1":
            actualizar_repositorios()
        elif opcion == "2":
            agregar_repositorio()
        elif opcion == "3":
            instalar_paquete()
        elif opcion == "4":
            buscar_paquete()
        elif opcion == "5":
            consultar_repositorios()
        elif opcion == "6":
            eliminar_repositorio()
        elif opcion == "7":
            actualizar_paquetes()
        elif opcion == "8":
            info_paquete()
        elif opcion == "9":
            limpiar_paquetes()
        elif opcion == "10":
            exportar_paquetes()
        elif opcion == "11":
            break
        else:
            print(f"{COLOR_ROJO}Opción no válida. Inténtalo de nuevo.{COLOR_RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{COLOR_ROJO}Programa cerrado por el usuario (Ctrl+C).{COLOR_RESET}")
