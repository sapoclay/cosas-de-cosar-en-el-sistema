import os
import webbrowser
import platform

# Guardamos el sistema operativo sobre el que está funcionando el scritp
sistema_operativo = platform.system()


# Importar los colores desde el archivo colores.py
from colores import (
    COLOR_RESET, COLOR_VERDE, COLOR_AMARILLO, COLOR_ROJO, COLOR_CIAN, COLOR_NARANJA,
    TEXTO_NEGRITA, TEXTO_SUBRAYADO
)

def buscar_en_google():
    # Solicita al usuario el término de búsqueda
    busqueda = input(f"{COLOR_NARANJA}Escribe el término de búsqueda: {COLOR_RESET}")
    # Crea la URL de búsqueda en Google con el término ingresado
    url = f"https://www.google.com/search?q={busqueda}"
    # Abre la URL en el navegador web predeterminado
    webbrowser.open(url)
    print(f"{COLOR_AMARILLO}------------------------------------------{COLOR_RESET}")
    print(f"{COLOR_AMARILLO}| Búsqueda realizada en Google con éxito |{COLOR_RESET}")
    print(f"{COLOR_AMARILLO}------------------------------------------{COLOR_RESET}")

def borrar_pantalla():
    # Limpia la pantalla según el sistema operativo
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{COLOR_VERDE}---------------------------------{COLOR_RESET}")
    print(f"{COLOR_VERDE}| Pantalla borrada exitosamente |{COLOR_RESET}")
    print(f"{COLOR_VERDE}---------------------------------{COLOR_RESET}")


def guardar_concepto():
    comando = input(f"{COLOR_NARANJA}-> Escribe el concepto: {COLOR_RESET}")
    if not os.path.exists("conceptos.txt"):
        with open("conceptos.txt", "w") as archivo:
            archivo.write("")
    with open("conceptos.txt", "r") as archivo:
        comandos_existentes = [line.split("\t")[0] for line in archivo]
        if comando in comandos_existentes:
            print(f"{COLOR_ROJO}------------------------------------------------{COLOR_RESET}")
            print(f"{COLOR_ROJO}| El concepto ya existe. Modifica su definición |{COLOR_RESET}")
            print(f"{COLOR_ROJO}------------------------------------------------{COLOR_RESET}")
            return
    definicion = input(f"{COLOR_NARANJA}-> Escribe la definición del concepto: {COLOR_RESET}")
    categoria = input(f"{COLOR_NARANJA}-> Escribe la categoría del concepto (opcional): {COLOR_RESET}")
    with open("conceptos.txt", "a") as archivo:
        archivo.write(comando + "\t" + definicion + "\t" + categoria + "\n")
    print(f"{COLOR_VERDE}--------------------------------{COLOR_RESET}")
    print(f"{COLOR_VERDE}| Concepto guardado con éxito!! |{COLOR_RESET}")
    print(f"{COLOR_VERDE}--------------------------------{COLOR_RESET}")


def consultar_conceptos():
    with open("conceptos.txt", "r") as archivo:
        comandos = archivo.readlines()
        if comandos:
            print(f"{COLOR_CIAN}-----------------------{COLOR_RESET}")
            print(f"{COLOR_CIAN}| Conceptos guardados: |{COLOR_RESET}")
            print(f"{COLOR_CIAN}-----------------------{COLOR_RESET}")
            for i, comando in enumerate(comandos):
                comando = comando.strip()
                comando_info = comando.split("\t")
                if len(comando_info) >= 2:
                    nombre = comando_info[0]
                    definicion = comando_info[1]
                    categoria = comando_info[2] if len(comando_info) > 2 else ""
                    print(f"{TEXTO_NEGRITA}{i+1}. Concepto:{COLOR_RESET} {nombre}")
                    print(f"{TEXTO_NEGRITA}   Definición: {COLOR_RESET}{definicion}")
                    print(f"{TEXTO_NEGRITA}   Categoría: {COLOR_RESET}{categoria}")
                    print("-" * 40)
                else:
                    print(f"{COLOR_ROJO}-------------------------------------------------------------------{COLOR_RESET}")
                    print(f"{COLOR_ROJO}El concepto en la línea {i+1} no tiene un formato válido: {comando}{COLOR_RESET}")
                    print(f"{COLOR_ROJO}-------------------------------------------------------------------{COLOR_RESET}")
        else:
            print(f"{COLOR_ROJO}------------------------------------{COLOR_RESET}")
            print(f"{COLOR_ROJO}| ¡¡ No hay conceptos guardados !! |{COLOR_RESET}")
            print(f"{COLOR_ROJO}------------------------------------{COLOR_RESET}")
def buscar_por_categoria():
    categoria = input(f"{COLOR_NARANJA}Introduce la categoría a buscar: {COLOR_RESET}")
    with open("conceptos.txt", "r") as archivo:
        comandos = archivo.readlines()
        encontrados = False
        for i, comando in enumerate(comandos):
            comando_info = comando.strip().split("\t")
            if len(comando_info) >= 3 and categoria.lower() == comando_info[2].lower():
                print(f"{TEXTO_NEGRITA}{i+1}. Concepto:{COLOR_RESET} {comando_info[0]}")
                print(f"{TEXTO_NEGRITA}   Definición: {COLOR_RESET}{comando_info[1]}")
                print(f"{TEXTO_NEGRITA}   Categoría: {COLOR_RESET}{comando_info[2]}")
                print("-" * 40)
                encontrados = True
        if not encontrados:
            print(f"{COLOR_ROJO}No se encontraron conceptos en la categoría '{categoria}'.{COLOR_RESET}")
def exportar_conceptos():
    archivo_destino = input(f"{COLOR_NARANJA}Introduce el nombre del archivo para exportar los conceptos: {COLOR_RESET}")
    try:
        with open("conceptos.txt", "r") as archivo_origen:
            conceptos = archivo_origen.read()
        with open(archivo_destino, "w") as archivo_destino_f:
            archivo_destino_f.write(conceptos)
        print(f"{COLOR_VERDE}Conceptos exportados correctamente a {archivo_destino}.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al exportar conceptos: {e}{COLOR_RESET}")

def importar_conceptos():
    archivo_origen = input(f"{COLOR_NARANJA}Introduce el nombre del archivo para importar los conceptos: {COLOR_RESET}")
    try:
        with open(archivo_origen, "r") as archivo_origen_f:
            conceptos = archivo_origen_f.read()
        with open("conceptos.txt", "a") as archivo_destino:
            archivo_destino.write(conceptos)
        print(f"{COLOR_VERDE}Conceptos importados correctamente desde {archivo_origen}.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al importar conceptos: {e}{COLOR_RESET}")


def editar_concepto():
    # Solicita al usuario el número del concepto a editar y resta 1 para obtener el índice correspondiente
    numero_comando = int(input(f"{COLOR_NARANJA}-> Escribe el número del concepto a editar: {COLOR_RESET}")) - 1
    # Abre el archivo "conceptos.txt" en modo de lectura (read)
    with open("conceptos.txt", "r") as archivo:
        # Lee todas las líneas del archivo y las guarda en la variable "comandos" como una lista de strings
        comandos = archivo.readlines()
    if numero_comando >= 0 and numero_comando < len(comandos):
        # Verifica si el número de comando es válido
        comando_actual = comandos[numero_comando].strip()
        # Divide el comando en sus componentes (concepto y definición) utilizando el tabulador "\t" como separador
        comando_info = comando_actual.split("\t")
        if len(comando_info) >= 2:
            # Si el comando tiene un formato válido (concepto y definición), extrae el concepto y su definición
            comando = comando_info[0]
            definicion = "\t".join(comando_info[1:])
            # Imprime el comando actual y su definición
            print(f"-> Concepto actual: {comando}")
            print(f"-> Definición actual: {definicion}")
            # Solicita al usuario escribir el nuevo concepto (o pulsar Intro para mantener el actual)
            nuevo_comando = input(f"{COLOR_NARANJA}* Teclea el nuevo concepto (o pulsa Intro para mantener el actual): {COLOR_RESET}")
            # Solicita al usuario escribir la nueva definición (o pulsar Intro para mantener la actual)
            nueva_definicion = input(f"{COLOR_NARANJA}* Escribe la nueva definición (o pulsa Intro para mantener la actual): {COLOR_RESET}")
            if nuevo_comando == "":
                nuevo_comando = comando  # Si no se escribe un nuevo comando, se mantiene el actual
            if nueva_definicion == "":
                nueva_definicion = definicion  # Si no se escribe una nueva definición, se mantiene la actual
            # Actualiza el concepto en la lista de comandos con el nuevo concepto y la nueva definición
            comandos[numero_comando] = nuevo_comando + "\t" + nueva_definicion + "\n"
            # Abre el archivo "conceptos.txt" en modo de escritura (write)
            with open("conceptos.txt", "w") as archivo:
                # Escribe las líneas actualizadas en el archivo
                archivo.writelines(comandos)
            print(f"{COLOR_VERDE}----------------------------------{COLOR_RESET}")
            print(f"{COLOR_VERDE}| Concepto editado correctamente |{COLOR_RESET}")
            print(f"{COLOR_VERDE}----------------------------------{COLOR_RESET}")
        else:
            print(
                f"{COLOR_ROJO}-----------------------------------------------------------------------------------------{COLOR_RESET}")
            print(
                f"{COLOR_ROJO}El concepto en la línea {numero_comando + 1} no tiene un formato válido: {comando_actual}{COLOR_RESET}")
            print(
                f"{COLOR_ROJO}-----------------------------------------------------------------------------------------{COLOR_RESET}")
    else:
        print(f"{COLOR_ROJO}--------------------------------------------------------------------------------{COLOR_RESET}")
        print(f"{COLOR_ROJO}| Número de concepto inválido. ¡¡ Fíjate un poco y escribe un número válido !! |{COLOR_RESET}")
        print(f"{COLOR_ROJO}--------------------------------------------------------------------------------{COLOR_RESET}")


def buscar_concepto():
    # Solicita al usuario que seleccione una opción de búsqueda (por definición o por nombre)
    opcion = input(
        f"{TEXTO_NEGRITA}1. Buscar por definición\n2. Buscar por nombre\nSelecciona una opción: {COLOR_RESET}")
    if opcion == "1":
        # Si la opción seleccionada es 1 (buscar por definición)
        definicion = input(f"{COLOR_NARANJA}Escribe la definición a buscar: {COLOR_RESET}")
        # Abre el archivo "conceptos.txt" en modo de lectura (read)
        with open("conceptos.txt", "r") as archivo:
            # Lee todas las líneas del archivo y las guarda en la variable "comandos" como una lista de strings
            comandos = archivo.readlines()
            # Variable para rastrear si se encontraron conceptos con la definición buscada
            encontrados = False
            # Itera sobre cada concepto en la lista con su índice correspondiente
            for i, comando in enumerate(comandos):
                # Verifica si la definición buscada se encuentra en el concepto actual (ignorando mayúsculas y minúsculas)
                if definicion.lower() in comando.lower():
                    # Divide el comando en sus componentes (concepto y definición) utilizando el tabulador "\t" como separador
                    comando, definicion = comando.strip().split("\t")
                    # Imprime el número del concepto, el nombre del concepto y su definición
                    print(f"{i+1}. Concepto: {comando}")
                    print(f"   Definición: {definicion}")
                    # Imprime una línea de separación para cada concepto encontrado
                    print("-" * 40)
                    # Actualiza la variable "encontrados" para indicar que se encontraron conceptos
                    encontrados = True
            # Si no se encontraron conceptos con la definición buscada, imprime un mensaje
            if not encontrados:
                print(f"{COLOR_ROJO}--------------------------------------------------{COLOR_RESET}")
                print(f"{COLOR_ROJO}| No se encontraron conceptos con esa definición |{COLOR_RESET}")
                print(f"{COLOR_ROJO}--------------------------------------------------{COLOR_RESET}")
    elif opcion == "2":
        # La opción seleccionada es 2 buscar por nombre
        nombre = input(f"{COLOR_NARANJA}-> Escribe el nombre a buscar: {COLOR_RESET}")
        # Abre el archivo "conceptos.txt" en modo de lectura (read)
        with open("conceptos.txt", "r") as archivo:
            # Lee todas las líneas del archivo y las guarda en la variable "comandos" como una lista de strings
            comandos = archivo.readlines()
            # Variable para rastrear si se encontraron conceptos con el nombre buscado
            encontrados = False
            # Itera sobre cada concepto en la lista con su índice correspondiente
            for i, comando in enumerate(comandos):
                # Verifica si el nombre buscado se encuentra en el primer elemento del concepto actual (ignorando mayúsculas y minúsculas)
                if nombre.lower() in comando.lower().split('\t')[0]:
                    # Divide el comando en sus componentes (concepto y definición) utilizando el tabulador "\t" como separador
                    comando, definicion = comando.strip().split("\t")
                    # Imprime el número de concepto, el nombre del concepto y su definición
                    print(f"{i+1}. Concepto: {comando}")
                    print(f"   Definición: {definicion}")
                    print("-" * 40)
                    encontrados = True
            if not encontrados:
                print(f"{COLOR_ROJO}----------------------------------------------{COLOR_RESET}")
                print(f"{COLOR_ROJO}| No se encontraron conceptos con ese nombre |{COLOR_RESET}")
                print(f"{COLOR_ROJO}----------------------------------------------{COLOR_RESET}")
    else:
        print(f"{COLOR_ROJO}------------------------------------------------------------------------{COLOR_RESET}")
        print(f"{COLOR_ROJO}| ¡¡ Opción inválida !! No seas cabezón y selecciona una opción válida |{COLOR_RESET}")
        print(f"{COLOR_ROJO}------------------------------------------------------------------------{COLOR_RESET}")


def eliminar_concepto():
    # Abre el archivo "conceptos.txt" en modo de lectura (read)
    with open("conceptos.txt", "r") as archivo:
        # Lee todas las líneas del archivo y las guarda en la variable "comandos" como una lista de strings
        comandos = archivo.readlines()
    if comandos:
        # Si existen conceptos en la lista
        print(f"{COLOR_AMARILLO}----------------------------------------{COLOR_RESET}")
        print(f"{COLOR_AMARILLO}| Conceptos disponibles para eliminar: |{COLOR_RESET}")
        print(f"{COLOR_AMARILLO}----------------------------------------{COLOR_RESET}")
        # Itera sobre cada concepto en la lista con su índice correspondiente
        for i, comando in enumerate(comandos):
            # Elimina los espacios en blanco al principio y al final del comando
            comando = comando.strip()
            # Divide el comando en sus componentes (concepto y definición) utilizando el tabulador "\t" como separador
            comando_info = comando.split("\t")
            if len(comando_info) >= 2:
                # Si el concepto tiene un formato válido (concepto y definición), extrae el concepto y su definición
                comando = comando_info[0]
                definicion = "\t".join(comando_info[1:])
                # Imprime el número del concepto, el nombre del concepto y su definición
                print(f"{i+1}. Concepto: {comando}")
                print(f"   Definición: {definicion}")
                # Imprime una línea de separación para cada concepto
                print("-" * 40)
            else:
                # Si el concepto no tiene un formato válido, imprime un mensaje de error
                print(f"{COLOR_ROJO}-------------------------------------------------------------------{COLOR_RESET}")
                print(f"{COLOR_ROJO}El concepto en la línea {i+1} no tiene un formato válido: {comando}{COLOR_RESET}")
                print(f"{COLOR_ROJO}-------------------------------------------------------------------{COLOR_RESET}")
        # Solicita al usuario seleccionar el número del concepto que quiere eliminar
        seleccion = input(f"{COLOR_NARANJA}-> Selecciona el número del concepto que quieras eliminar (o '0' para cancelar): {COLOR_RESET}")
        if seleccion == "0":
            return  # Si la selección es 0, se cancela la eliminación
        try:
            seleccion = int(seleccion)
            if seleccion >= 1 and seleccion <= len(comandos):
                # Si la selección es un número válido, elimina el concepto correspondiente de la lista de conceptos
                del comandos[seleccion-1]
                # Abre el archivo "conceptos.txt" en modo de escritura (write)
                with open("conceptos.txt", "w") as archivo:
                    # Escribe las líneas actualizadas de conceptos en el archivo
                    archivo.writelines(comandos)
                print(f"{COLOR_VERDE}-----------------------------------------{COLOR_RESET}")
                print(f"{COLOR_VERDE}| ¡¡ Concepto eliminado exitosamente !! |{COLOR_RESET}")
                print(f"{COLOR_VERDE}-----------------------------------------{COLOR_RESET}")
            else:
                print(f"{COLOR_ROJO}----------------------------{COLOR_RESET}")
                print(f"{COLOR_ROJO}| ¡¡ Selección inválida !! |{COLOR_RESET}")
                print(f"{COLOR_ROJO}----------------------------{COLOR_RESET}")
        except ValueError:
            print(f"{COLOR_ROJO}----------------------------{COLOR_RESET}")
            print(f"{COLOR_ROJO}| ¡¡ Selección inválida !! |{COLOR_RESET}")
            print(f"{COLOR_ROJO}----------------------------{COLOR_RESET}")
    else:
        print(f"{COLOR_AMARILLO}------------------------------{COLOR_RESET}")
        print(f"{COLOR_AMARILLO}| No hay conceptos guardados |{COLOR_RESET}")
        print(f"{COLOR_AMARILLO}------------------------------{COLOR_RESET}")


def main_menu():
    while True:
        print(f"{COLOR_CIAN}-----------------------{COLOR_RESET}")
        print(f"{COLOR_CIAN}| MENÚ - PARA APUNTAR- |{COLOR_RESET}")
        print(f"{COLOR_CIAN}-----------------------{COLOR_RESET}")
        print(f"{TEXTO_SUBRAYADO} Bajo un sistema {sistema_operativo} {COLOR_RESET}")
        print("-----------------------")
        print(f"{TEXTO_NEGRITA}1. Guardar concepto{COLOR_RESET}")
        print(f"{TEXTO_NEGRITA}2. Consultar conceptos{COLOR_RESET}")
        print(f"{TEXTO_NEGRITA}3. Editar concepto{COLOR_RESET}")
        print(f"{TEXTO_NEGRITA}4. Buscar concepto{COLOR_RESET}")
        print(f"{TEXTO_NEGRITA}5. Eliminar concepto{COLOR_RESET}")
        print(f"{TEXTO_NEGRITA}6. Buscar por categoría{COLOR_RESET}")
        print(f"{TEXTO_NEGRITA}7. Exportar conceptos a archivo{COLOR_RESET}")
        print(f"{TEXTO_NEGRITA}8. Importar conceptos desde archivo{COLOR_RESET}")
        print(f"{TEXTO_NEGRITA}9. Buscar en Google{COLOR_RESET}")
        print(f"{TEXTO_NEGRITA}10. Limpiar pantalla{COLOR_RESET}")
        print(f"{TEXTO_NEGRITA}11. Volver al menú principal{COLOR_RESET}")
        opcion = input(f"{COLOR_NARANJA}-> Selecciona una opción: {COLOR_RESET}")
        if opcion == "1":
            guardar_concepto()
        elif opcion == "2":
            consultar_conceptos()
        elif opcion == "3":
            editar_concepto()
        elif opcion == "4":
            buscar_concepto()
        elif opcion == "5":
            eliminar_concepto()
        elif opcion == "6":
            buscar_por_categoria()
        elif opcion == "7":
            exportar_conceptos()
        elif opcion == "8":
            importar_conceptos()
        elif opcion == "9":
            buscar_en_google()
        elif opcion == "10":
            borrar_pantalla()
        elif opcion == "11":
            break
        else:
            print(f"{COLOR_AMARILLO}--------------------------------------------------------------------------{COLOR_RESET}")
            print(f"{COLOR_AMARILLO}| Opción inválida. ¡¡ No seas ocurrente y selecciona una opción válida!! |{COLOR_RESET}")
            print(f"{COLOR_AMARILLO}--------------------------------------------------------------------------{COLOR_RESET}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{COLOR_ROJO}Programa cerrado por el usuario (Ctrl+C).{COLOR_RESET}")