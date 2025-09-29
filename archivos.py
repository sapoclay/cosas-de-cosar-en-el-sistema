# Módulo para la gestión de archivos y directorios en el sistema.
# Proporciona funciones para navegar, copiar, mover, eliminar y buscar archivos.

from colores import *
import os
import shutil

# Función para navegar por un directorio y listar su contenido
def navegar_directorio():
    # Solicita al usuario la ruta del directorio a explorar
    ruta = input(f"{COLOR_NARANJA}Introduce la ruta del directorio a navegar: {COLOR_RESET}")
    try:
        # Obtiene la lista de archivos y directorios en la ruta especificada
        archivos = os.listdir(ruta)
        print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Contenido de {ruta}:{COLOR_RESET}")
        # Imprime cada elemento encontrado
        for archivo in archivos:
            print(archivo)
    except Exception as e:
        # Maneja errores como rutas inexistentes o permisos insuficientes
        print(f"{COLOR_ROJO}Error al navegar el directorio: {e}{COLOR_RESET}")

# Función para copiar archivos o directorios
def copiar_archivo():
    # Solicita las rutas de origen y destino
    origen = input(f"{COLOR_NARANJA}Ruta del archivo/carpeta origen: {COLOR_RESET}")
    destino = input(f"{COLOR_NARANJA}Ruta de destino: {COLOR_RESET}")
    try:
        # Verifica si el origen es un directorio para usar copytree, sino copy2
        if os.path.isdir(origen):
            shutil.copytree(origen, destino)
        else:
            shutil.copy2(origen, destino)
        print(f"{COLOR_VERDE}Copiado correctamente.{COLOR_RESET}")
    except Exception as e:
        # Maneja errores como archivos inexistentes o permisos
        print(f"{COLOR_ROJO}Error al copiar: {e}{COLOR_RESET}")

# Función para mover archivos o directorios
def mover_archivo():
    # Solicita las rutas de origen y destino
    origen = input(f"{COLOR_NARANJA}Ruta del archivo/carpeta origen: {COLOR_RESET}")
    destino = input(f"{COLOR_NARANJA}Ruta de destino: {COLOR_RESET}")
    try:
        # Mueve el archivo/directorio usando shutil.move
        shutil.move(origen, destino)
        print(f"{COLOR_VERDE}Movido correctamente.{COLOR_RESET}")
    except Exception as e:
        # Maneja errores de movimiento
        print(f"{COLOR_ROJO}Error al mover: {e}{COLOR_RESET}")

# Función para eliminar archivos o directorios
def eliminar_archivo():
    # Solicita la ruta del elemento a eliminar
    ruta = input(f"{COLOR_NARANJA}Ruta del archivo/carpeta a eliminar: {COLOR_RESET}")
    try:
        # Verifica si es directorio para usar rmtree, sino remove
        if os.path.isdir(ruta):
            shutil.rmtree(ruta)
        else:
            os.remove(ruta)
        print(f"{COLOR_VERDE}Eliminado correctamente.{COLOR_RESET}")
    except Exception as e:
        # Maneja errores de eliminación
        print(f"{COLOR_ROJO}Error al eliminar: {e}{COLOR_RESET}")

# Función para buscar archivos por nombre en un directorio y subdirectorios
def buscar_archivo():
    # Solicita el nombre a buscar y la ruta base
    nombre = input(f"{COLOR_NARANJA}Nombre del archivo a buscar: {COLOR_RESET}")
    ruta = input(f"{COLOR_NARANJA}Ruta base para buscar: {COLOR_RESET}")
    encontrados = []
    # Recorre recursivamente el directorio usando os.walk
    for root, dirs, files in os.walk(ruta):
        for file in files:
            # Busca coincidencias ignorando mayúsculas/minúsculas
            if nombre.lower() in file.lower():
                encontrados.append(os.path.join(root, file))
    if encontrados:
        print(f"{COLOR_VERDE}Archivos encontrados:{COLOR_RESET}")
        # Imprime cada archivo encontrado
        for f in encontrados:
            print(f)
    else:
        print(f"{COLOR_ROJO}No se encontraron archivos con ese nombre.{COLOR_RESET}")

# Función principal del menú de gestión de archivos
def main_menu():
    while True:
        # Muestra el menú de opciones
        print(f"{COLOR_CIAN}{TEXTO_NEGRITA}\n--- MENÚ DE GESTIÓN DE ARCHIVOS ---{COLOR_RESET}")
        print(f"{COLOR_VERDE}1. Navegar por el sistema de archivos{COLOR_RESET}")
        print(f"{COLOR_VERDE}2. Copiar archivo/carpeta{COLOR_RESET}")
        print(f"{COLOR_VERDE}3. Mover archivo/carpeta{COLOR_RESET}")
        print(f"{COLOR_VERDE}4. Eliminar archivo/carpeta{COLOR_RESET}")
        print(f"{COLOR_VERDE}5. Buscar archivo por nombre{COLOR_RESET}")
        print(f"{COLOR_ROJO}6. Volver al menú principal{COLOR_RESET}")
        opcion = input(f"{COLOR_NARANJA}Selecciona una opción: {COLOR_RESET}")
        if opcion == "1":
            navegar_directorio()
        elif opcion == "2":
            copiar_archivo()
        elif opcion == "3":
            mover_archivo()
        elif opcion == "4":
            eliminar_archivo()
        elif opcion == "5":
            buscar_archivo()
        elif opcion == "6":
            break
        else:
            print(f"{COLOR_ROJO}Opción no válida. Inténtalo de nuevo.{COLOR_RESET}")

# Bloque principal para ejecutar el menú si el archivo se ejecuta directamente
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        # Maneja la interrupción del usuario (Ctrl+C)
        print(f"\n{COLOR_ROJO}Programa cerrado por el usuario (Ctrl+C).{COLOR_RESET}")
