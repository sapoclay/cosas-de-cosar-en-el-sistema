# Importar los colores desde el archivo colores.py
from colores import (
    COLOR_RESET, COLOR_VERDE, COLOR_AMARILLO, COLOR_ROJO, COLOR_CIAN, COLOR_NARANJA,
    TEXTO_NEGRITA, TEXTO_SUBRAYADO
)
# Menú principal para navegar entre archivos

import sys

# Importar los módulos como funciones
import conceptos
import sistema
import software
import usuarios
import servicios
import archivos
import red
import logs
import transferencias
import discos
import seguridad
import impresoras

def menu_principal():
    while True:
        print(f"{COLOR_AMARILLO}{TEXTO_NEGRITA}\n----------------------------{COLOR_RESET}")
        print(f"{COLOR_AMARILLO}{TEXTO_NEGRITA}COSAS DE COSAR EN EL SISTEMA{COLOR_RESET}")
        print(f"{COLOR_CIAN}{TEXTO_NEGRITA}\n--- MENÚ PRINCIPAL ---{COLOR_RESET}")
        print(f"{COLOR_VERDE}1. Ir a gestión de conceptos{COLOR_RESET}")
        print(f"{COLOR_VERDE}2. Ir a información del sistema{COLOR_RESET}")
        print(f"{COLOR_VERDE}3. Ir a gestión de software{COLOR_RESET}")
        print(f"{COLOR_VERDE}4. Ir a gestión de usuarios{COLOR_RESET}")
        print(f"{COLOR_VERDE}5. Ir a gestión de servicios{COLOR_RESET}")
        print(f"{COLOR_VERDE}6. Ir a gestión de archivos{COLOR_RESET}")
        print(f"{COLOR_VERDE}7. Ir a gestión de red{COLOR_RESET}")
        print(f"{COLOR_VERDE}8. Ir a gestión de logs del sistema{COLOR_RESET}")
        print(f"{COLOR_VERDE}9. Ir a herramientas de redirección y transferencia{COLOR_RESET}")
        print(f"{COLOR_VERDE}10. Ir a gestión de discos y particiones{COLOR_RESET}")
        print(f"{COLOR_VERDE}11. Ir a herramientas de seguridad básica{COLOR_RESET}")
        print(f"{COLOR_VERDE}12. Ir a gestión de impresoras{COLOR_RESET}")
        print(f"{COLOR_ROJO}13. Salir{COLOR_RESET}")
        opcion = input(f"{COLOR_NARANJA}Selecciona una opción: {COLOR_RESET}")
        if opcion == "1":
            conceptos.main_menu()
        elif opcion == "2":
            sistema.main_menu()
        elif opcion == "3":
            software.main_menu()
        elif opcion == "4":
            usuarios.main_menu()
        elif opcion == "5":
            servicios.main_menu()
        elif opcion == "6":
            archivos.main_menu()
        elif opcion == "7":
            red.main_menu()
        elif opcion == "8":
            logs.main_menu()
        elif opcion == "9":
            transferencias.main_menu()
        elif opcion == "10":
            discos.main_menu()
        elif opcion == "11":
            seguridad.main_menu()
        elif opcion == "12":
            impresoras.main_menu()
        elif opcion == "13":
            print(f"{COLOR_AMARILLO}¡Hasta luego!{COLOR_RESET}")
            sys.exit(0)
        else:
            print(f"{COLOR_ROJO}Opción no válida. Inténtalo de nuevo.{COLOR_RESET}")

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print(f"\n{COLOR_ROJO}Programa cerrado por el usuario (Ctrl+C).{COLOR_RESET}")
