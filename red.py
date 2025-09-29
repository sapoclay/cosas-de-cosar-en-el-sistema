# Módulo para herramientas de red y conectividad en Linux.
# Incluye escaneos con nmap, detección de dispositivos, análisis de vulnerabilidades, y gestión de red.

from colores import *
import psutil
import subprocess

# Mostrar estadísticas básicas de red usando psutil
def mostrar_info_red():
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Información de la red:{COLOR_RESET}")
    estadisticas = psutil.net_io_counters()
    print(f"Bytes enviados: {estadisticas.bytes_sent}")
    print(f"Bytes recibidos: {estadisticas.bytes_recv}")

# Función para detectar equipos conectados en la red local usando nmap
def mostrar_equipos_red():
    import sys
    import re
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Para buscar equipos conectados en la red local:{COLOR_RESET}")
    try:
        red = input(f"{COLOR_NARANJA}Introduce el rango de red a escanear (ejemplo: 192.168.1.0/24): {COLOR_RESET}")
        print(f"{COLOR_AMARILLO}Escaneando la red con nmap, esto puede tardar unos segundos...{COLOR_RESET}")
        comando = ["sudo", "nmap", "-sn", red]
        with subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1) as proc:
            ip_actual = None
            if proc.stdout:
                for linea in proc.stdout:
                    # Detectar IP activa
                    if linea.startswith("Nmap scan report for"):
                        ip_actual = linea.strip().split()[-1]
                    elif "Host is up" in linea and ip_actual:
                        print(f"{COLOR_VERDE}{TEXTO_NEGRITA}Dispositivo activo: {ip_actual}{COLOR_RESET}")
                        ip_actual = None
                    # Feedback visual: barra de progreso (si nmap lo muestra)
                    elif "% done" in linea or "Scan Timing:" in linea or "remaining" in linea:
                        porcentaje = re.search(r"([0-9.]+)% done", linea)
                        if porcentaje:
                            prog = float(porcentaje.group(1))
                            barra = int(prog // 2)
                            print(f"\r{COLOR_AMARILLO}[{'#'*barra}{'.'*(50-barra)}] {prog:.2f}%{COLOR_RESET}", end='')
                        else:
                            print(f"\r{COLOR_AMARILLO}{linea.strip()}{COLOR_RESET}", end='')
                    sys.stdout.flush()
                print()  # salto de línea al terminar
            else:
                print(f"{COLOR_ROJO}No se pudo obtener la salida de nmap.{COLOR_RESET}")
    except KeyboardInterrupt:
        print(f"\n{COLOR_NARANJA}Escaneo cancelado por el usuario.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al detectar equipos en la red: {e}{COLOR_RESET}")

# Escanear puertos abiertos en una IP específica
def escanear_puertos_ip():
    import sys
    import re
    ip = input(f"{COLOR_NARANJA}Introduce la IP a escanear: {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Escaneando puertos abiertos en {ip}...{COLOR_RESET}")
    comando = ["sudo", "nmap", "-Pn", "-p-", ip]
    puertos_abiertos = []
    try:
        with subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1) as proc:
            if proc.stdout:
                for linea in proc.stdout:
                    # Barra de progreso
                    if "% done" in linea or "Scan Timing:" in linea or "remaining" in linea:
                        porcentaje = re.search(r"([0-9.]+)% done", linea)
                        if porcentaje:
                            prog = float(porcentaje.group(1))
                            barra = int(prog // 2)
                            print(f"\r{COLOR_AMARILLO}[{'#'*barra}{'.'*(50-barra)}] {prog:.2f}%{COLOR_RESET}", end='')
                        else:
                            print(f"\r{COLOR_AMARILLO}{linea.strip()}{COLOR_RESET}", end='')
                    # Detectar puertos abiertos
                    elif re.search(r"^[0-9]+/tcp +open", linea):
                        puertos_abiertos.append(linea.strip())
                    elif "Nmap scan report for" in linea:
                        print(f"\n{COLOR_CIAN}{TEXTO_NEGRITA}{linea.strip()}{COLOR_RESET}")
                    sys.stdout.flush()
                print()  # salto de línea al terminar
                # Mostrar resultado final
                if puertos_abiertos:
                    print(f"{COLOR_VERDE}{TEXTO_NEGRITA}Puertos abiertos encontrados:{COLOR_RESET}")
                    for puerto in puertos_abiertos:
                        print(f"{COLOR_VERDE}{puerto}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ROJO}No se encontraron puertos abiertos en la IP indicada.{COLOR_RESET}")
            else:
                print(f"{COLOR_ROJO}No se pudo obtener la salida de nmap.{COLOR_RESET}")
    except KeyboardInterrupt:
        print(f"\n{COLOR_NARANJA}Escaneo cancelado por el usuario.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al escanear la IP: {e}{COLOR_RESET}")

# Función para detectar el sistema operativo remoto usando nmap
def detectar_so_remoto():
    import sys
    ip = input(f"{COLOR_NARANJA}Introduce la IP a analizar: {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Detectando sistema operativo remoto en {ip}...{COLOR_RESET}")
    comando = ["sudo", "nmap", "-O", ip]
    try:
        with subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1) as proc:
            if proc.stdout:
                so_detectado = False
                for linea in proc.stdout:
                    if "OS details" in linea or "Running:" in linea:
                        print(f"{COLOR_VERDE}{TEXTO_NEGRITA}{linea.strip()}{COLOR_RESET}")
                        so_detectado = True
                    elif "Aggressive OS guesses" in linea:
                        print(f"{COLOR_CIAN}{linea.strip()}{COLOR_RESET}")
                    elif "% done" in linea or "Scan Timing:" in linea or "remaining" in linea:
                        import re
                        porcentaje = re.search(r"([0-9.]+)% done", linea)
                        if porcentaje:
                            prog = float(porcentaje.group(1))
                            barra = int(prog // 2)
                            print(f"\r{COLOR_AMARILLO}[{'#'*barra}{'.'*(50-barra)}] {prog:.2f}%{COLOR_RESET}", end='')
                        else:
                            print(f"\r{COLOR_AMARILLO}{linea.strip()}{COLOR_RESET}", end='')
                    sys.stdout.flush()
                print()
                if not so_detectado:
                    print(f"{COLOR_ROJO}No se pudo detectar el sistema operativo remoto.{COLOR_RESET}")
            else:
                print(f"{COLOR_ROJO}No se pudo obtener la salida de nmap.{COLOR_RESET}")
    except KeyboardInterrupt:
        print(f"\n{COLOR_NARANJA}Detección cancelada por el usuario.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al detectar el sistema operativo: {e}{COLOR_RESET}")

# Escanear servicios específicos en puertos comunes
def escanear_servicios_especificos():
    import sys
    ip = input(f"{COLOR_NARANJA}Introduce la IP a escanear: {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Escaneando servicios comunes en {ip}...{COLOR_RESET}")
    # Puertos comunes: 22(SSH), 80(HTTP), 443(HTTPS), 21(FTP), 25(SMTP), 53(DNS), 3306(MySQL), 8080(Web)
    puertos = "22,80,443,21,25,53,3306,8080"
    comando = ["sudo", "nmap", "-Pn", "-p", puertos, ip]
    servicios = {
        "22": "SSH",
        "80": "HTTP",
        "443": "HTTPS",
        "21": "FTP",
        "25": "SMTP",
        "53": "DNS",
        "3306": "MySQL",
        "8080": "Web alternativo"
    }
    try:
        with subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1) as proc:
            if proc.stdout:
                abiertos = []
                for linea in proc.stdout:
                    import re
                    match = re.match(r"^([0-9]+)/tcp +open", linea)
                    if match:
                        puerto = match.group(1)
                        nombre = servicios.get(puerto, "Desconocido")
                        abiertos.append(f"{puerto}/tcp ({nombre})")
                    elif "Nmap scan report for" in linea:
                        print(f"\n{COLOR_CIAN}{TEXTO_NEGRITA}{linea.strip()}{COLOR_RESET}")
                    elif "% done" in linea or "Scan Timing:" in linea or "remaining" in linea:
                        porcentaje = re.search(r"([0-9.]+)% done", linea)
                        if porcentaje:
                            prog = float(porcentaje.group(1))
                            barra = int(prog // 2)
                            print(f"\r{COLOR_AMARILLO}[{'#'*barra}{'.'*(50-barra)}] {prog:.2f}%{COLOR_RESET}", end='')
                        else:
                            print(f"\r{COLOR_AMARILLO}{linea.strip()}{COLOR_RESET}", end='')
                    sys.stdout.flush()
                print()
                if abiertos:
                    print(f"{COLOR_VERDE}{TEXTO_NEGRITA}Servicios abiertos encontrados:{COLOR_RESET}")
                    for s in abiertos:
                        print(f"{COLOR_VERDE}{s}{COLOR_RESET}")
                else:
                    print(f"{COLOR_ROJO}No se encontraron servicios abiertos en la IP indicada.{COLOR_RESET}")
            else:
                print(f"{COLOR_ROJO}No se pudo obtener la salida de nmap.{COLOR_RESET}")
    except KeyboardInterrupt:
        print(f"\n{COLOR_NARANJA}Escaneo cancelado por el usuario.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al escanear servicios: {e}{COLOR_RESET}")

# Función para exportar resultados de escaneo a un archivo
def exportar_resultados():
    ip = input(f"{COLOR_NARANJA}Introduce la IP o rango a escanear para exportar resultados: {COLOR_RESET}")
    archivo = input(f"{COLOR_NARANJA}Nombre del archivo donde guardar el resultado (ejemplo: resultado.txt): {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Escaneando y exportando resultados a {archivo}...{COLOR_RESET}")
    comando = ["sudo", "nmap", "-Pn", "-p-", ip]
    try:
        with subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) as proc:
            resultado = proc.stdout.read() if proc.stdout else ""
        with open(archivo, "w") as f:
            f.write(resultado)
        print(f"{COLOR_VERDE}Resultado exportado correctamente a {archivo}{COLOR_RESET}")
    except KeyboardInterrupt:
        print(f"\n{COLOR_NARANJA}Exportación cancelada por el usuario.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al exportar resultados: {e}{COLOR_RESET}")

# Escanear vulnerabilidades básicas usando scripts de nmap
def escaneo_vulnerabilidades():
    import sys
    ip = input(f"{COLOR_NARANJA}Introduce la IP o rango a analizar: {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Escaneando vulnerabilidades básicas en {ip}...{COLOR_RESET}")
    comando = ["sudo", "nmap", "-Pn", "--script", "vuln", ip]
    try:
        with subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1) as proc:
            if proc.stdout:
                vulnerabilidades = []
                for linea in proc.stdout:
                    if "VULNERABLE:" in linea:
                        vulnerabilidades.append(linea.strip())
                        print(f"{COLOR_ROJO}{TEXTO_NEGRITA}{linea.strip()}{COLOR_RESET}")
                    elif "Nmap scan report for" in linea:
                        print(f"\n{COLOR_CIAN}{TEXTO_NEGRITA}{linea.strip()}{COLOR_RESET}")
                    elif "% done" in linea or "Scan Timing:" in linea or "remaining" in linea:
                        import re
                        porcentaje = re.search(r"([0-9.]+)% done", linea)
                        if porcentaje:
                            prog = float(porcentaje.group(1))
                            barra = int(prog // 2)
                            print(f"\r{COLOR_AMARILLO}[{'#'*barra}{'.'*(50-barra)}] {prog:.2f}%{COLOR_RESET}", end='')
                        else:
                            print(f"\r{COLOR_AMARILLO}{linea.strip()}{COLOR_RESET}", end='')
                    sys.stdout.flush()
                print()
                if not vulnerabilidades:
                    print(f"{COLOR_VERDE}No se detectaron vulnerabilidades conocidas en el objetivo.{COLOR_RESET}")
            else:
                print(f"{COLOR_ROJO}No se pudo obtener la salida de nmap.{COLOR_RESET}")
    except KeyboardInterrupt:
        print(f"\n{COLOR_NARANJA}Escaneo cancelado por el usuario.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al escanear vulnerabilidades: {e}{COLOR_RESET}")

# Función para enviar paquete Wake-on-LAN a una dirección MAC
def wake_on_lan():
    import sys
    import socket
    mac = input(f"{COLOR_NARANJA}Introduce la dirección MAC del equipo a encender (formato: XX:XX:XX:XX:XX:XX): {COLOR_RESET}")
    print(f"{COLOR_AMARILLO}Enviando paquete Wake-on-LAN a {mac}...{COLOR_RESET}")
    try:
        # Convertir MAC a bytes
        mac_bytes = bytes.fromhex(mac.replace(':', ''))
        if len(mac_bytes) != 6:
            print(f"{COLOR_ROJO}MAC inválida.{COLOR_RESET}")
            return
        # Crear paquete mágico
        paquete = b'\xff' * 6 + mac_bytes * 16
        # Enviar por UDP broadcast
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.sendto(paquete, ('<broadcast>', 9))
        print(f"{COLOR_VERDE}Paquete Wake-on-LAN enviado correctamente.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al enviar Wake-on-LAN: {e}{COLOR_RESET}")

# Monitorizar cambios en la red (dispositivos conectados/desconectados)
def monitorizar_cambios_red():
    import time
    import sys
    rango = input(f"{COLOR_NARANJA}Introduce el rango de red a monitorizar (ejemplo: 192.168.1.0/24): {COLOR_RESET}")
    intervalo = input(f"{COLOR_NARANJA}Intervalo de escaneo en segundos (ejemplo: 10): {COLOR_RESET}")
    try:
        intervalo = int(intervalo)
    except:
        intervalo = 10
    print(f"{COLOR_AMARILLO}Monitorizando cambios en la red... Pulsa Ctrl+C para detener.{COLOR_RESET}")
    anteriores = set()
    try:
        while True:
            comando = ["sudo", "nmap", "-sn", rango]
            actuales = set()
            with subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) as proc:
                ip_actual = None
                if proc.stdout:
                    for linea in proc.stdout:
                        if linea.startswith("Nmap scan report for"):
                            ip_actual = linea.strip().split()[-1]
                        elif "Host is up" in linea and ip_actual:
                            actuales.add(ip_actual)
                            ip_actual = None
            nuevos = actuales - anteriores
            desaparecidos = anteriores - actuales
            if nuevos:
                print(f"{COLOR_VERDE}Nuevos dispositivos conectados: {', '.join(nuevos)}{COLOR_RESET}")
            if desaparecidos:
                print(f"{COLOR_ROJO}Dispositivos desconectados: {', '.join(desaparecidos)}{COLOR_RESET}")
            if not nuevos and not desaparecidos:
                print(f"{COLOR_CIAN}Sin cambios en la red.{COLOR_RESET}")
            anteriores = actuales
            time.sleep(intervalo)
    except KeyboardInterrupt:
        print(f"\n{COLOR_NARANJA}Monitorización detenida por el usuario.{COLOR_RESET}")

# Mostrar información detallada de interfaces de red
def info_interfaces_red():
    import psutil
    import socket
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Información de interfaces de red:{COLOR_RESET}")
    interfaces = psutil.net_if_addrs()
    stats = psutil.net_if_stats()
    for nombre, direcciones in interfaces.items():
        print(f"{COLOR_VERDE}{TEXTO_NEGRITA}Interfaz: {nombre}{COLOR_RESET}")
        for dir in direcciones:
            if dir.family == socket.AF_INET:
                print(f"  IP: {dir.address}")
            elif dir.family == psutil.AF_LINK:
                print(f"  MAC: {dir.address}")
        if nombre in stats:
            st = stats[nombre]
            print(f"  Estado: {'UP' if st.isup else 'DOWN'}")
            print(f"  Velocidad: {st.speed} Mbps")
        print()

# Escanear redes WiFi cercanas usando iwlist
def escaneo_wifi():
    import subprocess
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Escaneando redes WiFi cercanas...{COLOR_RESET}")
    interfaz = input(f"{COLOR_NARANJA}Introduce la interfaz WiFi (ejemplo: wlan0): {COLOR_RESET}")
    comando = ["sudo", "iwlist", interfaz, "scan"]
    try:
        with subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) as proc:
            redes = set()
            ssid = None
            calidad = None
            if proc.stdout:
                for linea in proc.stdout:
                    linea = linea.strip()
                    if "ESSID:" in linea:
                        ssid = linea.split('ESSID:')[1].strip('"')
                    if "Quality=" in linea:
                        calidad = linea.split('Quality=')[1].split()[0]
                    if ssid:
                        print(f"{COLOR_VERDE}SSID: {ssid} | Calidad: {calidad if calidad else 'N/A'}{COLOR_RESET}")
                        redes.add(ssid)
                        ssid = None
                        calidad = None
                if not redes:
                    print(f"{COLOR_ROJO}No se detectaron redes WiFi cercanas o la interfaz no es válida.{COLOR_RESET}")
            else:
                print(f"{COLOR_ROJO}No se pudo obtener la salida del escaneo WiFi. Verifica la interfaz y permisos.{COLOR_RESET}")
    except KeyboardInterrupt:
        print(f"\n{COLOR_NARANJA}Escaneo cancelado por el usuario.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error al escanear WiFi: {e}{COLOR_RESET}")

# Función para realizar test de velocidad de red (descarga y subida)
def test_velocidad_red():
    import shutil
    import time
    import tempfile
    import os
    print(f"{COLOR_CIAN}{TEXTO_NEGRITA}Test de velocidad de red (descarga y subida):{COLOR_RESET}")
    url_descarga = "https://speed.cloudflare.com/__down?bytes=10485760"  # 10MB de Cloudflare
    url_subida = "https://httpbin.org/post"
    tamano_subida = 10485760  # 10MB en bytes
    
    # Test de bajada
    print(f"{COLOR_AMARILLO}Test de bajada: Descargando 10MB desde Cloudflare{COLOR_RESET}")
    try:
        if shutil.which("curl"):
            inicio = time.time()
            resultado = subprocess.run(["curl", "-o", "/dev/null", url_descarga], capture_output=True, text=True)
            fin = time.time()
            if resultado.returncode == 0:
                segundos = fin - inicio
                velocidad_bajada = 10 / segundos  # MB/s
                print(f"{COLOR_VERDE}Bajada: {velocidad_bajada*8:.2f} Mbps (Tiempo: {segundos:.2f} s){COLOR_RESET}")
            else:
                print(f"{COLOR_ROJO}Error en la descarga:{COLOR_RESET}")
                print(resultado.stderr)
        else:
            print(f"{COLOR_ROJO}curl no está disponible.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error en test de bajada: {e}{COLOR_RESET}")
    
    # Test de subida
    print(f"{COLOR_AMARILLO}Test de subida: Enviando 10MB a httpbin.org{COLOR_RESET}")
    try:
        if shutil.which("curl"):
            # Crear archivo temporal con 10MB de datos
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(b'\x00' * tamano_subida)
                temp_path = temp_file.name
            inicio = time.time()
            resultado = subprocess.run([
                "curl", "-X", "POST", "--upload-file", temp_path, url_subida
            ], capture_output=True, text=True)
            fin = time.time()
            # Eliminar archivo temporal
            os.unlink(temp_path)
            if resultado.returncode == 0:
                segundos = fin - inicio
                velocidad_subida = 10 / segundos  # MB/s
                print(f"{COLOR_VERDE}Subida: {velocidad_subida*8:.2f} Mbps (Tiempo: {segundos:.2f} s){COLOR_RESET}")
            else:
                print(f"{COLOR_ROJO}Error en la subida:{COLOR_RESET}")
                print(resultado.stderr)
        else:
            print(f"{COLOR_ROJO}curl no está disponible.{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_ROJO}Error en test de subida: {e}{COLOR_RESET}")



# Función principal del menú de red
def main_menu():
    while True:
        print(f"{COLOR_CIAN}{TEXTO_NEGRITA}\n--- MENÚ DE RED LOCAL ---{COLOR_RESET}")
        print(f"{COLOR_VERDE}1. Mostrar información de la red{COLOR_RESET}")
        print(f"{COLOR_VERDE}2. Detectar equipos conectados en la red local{COLOR_RESET}")
        print(f"{COLOR_VERDE}3. Escanear puertos abiertos en una IP{COLOR_RESET}")
        print(f"{COLOR_VERDE}4. Detección de sistema operativo remoto{COLOR_RESET}")
        print(f"{COLOR_VERDE}5. Escaneo de servicios específicos{COLOR_RESET}")
        print(f"{COLOR_VERDE}6. Exportar resultados de escaneo{COLOR_RESET}")
        print(f"{COLOR_VERDE}7. Escaneo de vulnerabilidades básicas{COLOR_RESET}")
        print(f"{COLOR_VERDE}8. Wake-on-LAN{COLOR_RESET}")
        print(f"{COLOR_VERDE}9. Monitorización de cambios en la red{COLOR_RESET}")
        print(f"{COLOR_VERDE}10. Información de interfaces de red{COLOR_RESET}")
        print(f"{COLOR_VERDE}11. Escaneo de WiFi{COLOR_RESET}")
        print(f"{COLOR_VERDE}12. Test de velocidad de red{COLOR_RESET}")
        print(f"{COLOR_ROJO}13. Volver al menú principal{COLOR_RESET}")
        opcion = input(f"{COLOR_NARANJA}Selecciona una opción: {COLOR_RESET}")
        if opcion == "1":
            mostrar_info_red()
        elif opcion == "2":
            mostrar_equipos_red()
        elif opcion == "3":
            escanear_puertos_ip()
        elif opcion == "4":
            detectar_so_remoto()
        elif opcion == "5":
            escanear_servicios_especificos()
        elif opcion == "6":
            exportar_resultados()
        elif opcion == "7":
            escaneo_vulnerabilidades()
        elif opcion == "8":
            wake_on_lan()
        elif opcion == "9":
            monitorizar_cambios_red()
        elif opcion == "10":
            info_interfaces_red()
        elif opcion == "11":
            escaneo_wifi()
        elif opcion == "12":
            test_velocidad_red()
        elif opcion == "13":
            break
        else:
            print(f"{COLOR_ROJO}Opción no válida. Inténtalo de nuevo.{COLOR_RESET}")

# Bloque principal para ejecutar el menú si el archivo se ejecuta directamente
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        #(Ctrl+C)
        print(f"\n{COLOR_ROJO}Programa cerrado por el usuario (Ctrl+C).{COLOR_RESET}")
