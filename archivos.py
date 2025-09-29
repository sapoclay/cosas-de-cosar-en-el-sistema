# archivos.py
from colores import *
import os
import shutil

def navegar_directorio():
    ruta = input(f"{COLOR_NARANJA}Introduce la ruta del directorio a navegar: {COLOR_RESET}")
    try:
        archivos = os.listdir(ruta)
        print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Contenido de {ruta}:{COLOR_RESET}")
        for archivo in archivos:
            print(archivo)
    except Exception as e:
        print(f"{COLOR_ROJO}Error al navegar el directorio: {e}{COLOR_RESET}")

def copiar_archivo():
    origen = input(f"{COLOR_NARANJA}Ruta del archivo/carpeta origen: {COLOR_RESET}")
    destino = input(f"{COLOR_NARANJA}Ruta de destino: {COLOR_RESET}")
    try:
        if os.path.isdir(origen):
            shutil.copytree(origen, destino)
        else:
            shutil.copy2(origen, destino)
        print(f"{COLOR_VERDE}Copiado correctamente.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al copiar: {e}{COLOR_RESET}")

def mover_archivo():
    origen = input(f"{COLOR_NARANJA}Ruta del archivo/carpeta origen: {COLOR_RESET}")
    destino = input(f"{COLOR_NARANJA}Ruta de destino: {COLOR_RESET}")
    try:
        shutil.move(origen, destino)
        print(f"{COLOR_VERDE}Movido correctamente.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al mover: {e}{COLOR_RESET}")

def eliminar_archivo():
    ruta = input(f"{COLOR_NARANJA}Ruta del archivo/carpeta a eliminar: {COLOR_RESET}")
    try:
        if os.path.isdir(ruta):
            shutil.rmtree(ruta)
        else:
            os.remove(ruta)
        print(f"{COLOR_VERDE}Eliminado correctamente.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al eliminar: {e}{COLOR_RESET}")

def buscar_archivo():
    nombre = input(f"{COLOR_NARANJA}Nombre del archivo a buscar: {COLOR_RESET}")
    ruta = input(f"{COLOR_NARANJA}Ruta base para buscar: {COLOR_RESET}")
    encontrados = []
    for root, dirs, files in os.walk(ruta):
        for file in files:
            if nombre.lower() in file.lower():
                encontrados.append(os.path.join(root, file))
    if encontrados:
        print(f"{COLOR_VERDE}Archivos encontrados:{COLOR_RESET}")
        for f in encontrados:
            print(f)
    else:
        print(f"{COLOR_ROJO}No se encontraron archivos con ese nombre.{COLOR_RESET}")

def main_menu():
    while True:
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

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{COLOR_ROJO}Programa cerrado por el usuario (Ctrl+C).{COLOR_RESET}")
