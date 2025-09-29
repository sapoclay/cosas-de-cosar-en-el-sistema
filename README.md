# COSAS DE COSAR EN EL SISTEMA

Este es un toolkit modular interactivo que escribí hace un par de años para la administración de sistemas Linux (concretamente Ubuntu), diseñado para facilitar tareas comunes de gestión del sistema a través de una interfaz de menú intuitiva.

## Descripción

Este programa proporciona una colección de herramientas organizadas en módulos independientes para gestionar diversos aspectos de un sistema Linux. Cada módulo ofrece funcionalidades específicas con menús interactivos, colores para una mejor experiencia visual y manejo de errores.

## Requisitos

- **Sistema operativo**: Linux (probado en distribuciones basadas en Debian/Ubuntu)
- **Python**: Versión 3.6 o superior
- **Dependencias del sistema**:
  - `psutil` (para información del sistema)
  - `nmap` (para escaneo de red)
  - `rsync` (para sincronización de archivos)
  - `ufw` (para gestión del firewall)
  - `cups` (para gestión de impresoras)
  - `md5sum` (para verificación de integridad)
  - Herramientas estándar de Linux: `lsblk`, `df`, `mount`, `umount`, `chmod`, `chown`, `systemctl`, etc.

## Instalación

1. Clona o descarga los archivos en un directorio de tu sistema.
2. Asegúrate de tener Python 3 instalado.
3. Ejecuta el programa con permisos de administrador (sudo) para operaciones que lo requieran:

```bash
python3 menu.py
```

## Uso

Ejecuta el archivo principal `menu.py` para acceder al menú principal. Navega por las opciones numéricas para acceder a cada módulo. Cada módulo tiene su propio submenú con opciones específicas.

### Módulos Disponibles

#### 1. Gestión de conceptos
- **Funcionalidad**: Gestión de conceptos y definiciones técnicas.
- **Opciones**:
  - Agregar concepto
  - Ver conceptos
  - Buscar concepto
  - Eliminar concepto
  - Importar/exportar conceptos

#### 2. Información del sistema
- **Funcionalidad**: Monitorización y obtención de información detallada del sistema.
- **Opciones**:
  - Información básica del sistema
  - Información de CPU, memoria y disco
  - Información de GPU y batería
  - Información de USB y uptime
  - Procesos del sistema
  - Información del sistema de archivos
  - Monitoreo en tiempo real de recursos

#### 3. Gestión de software
- **Funcionalidad**: Administración de paquetes y repositorios.
- **Opciones**:
  - Gestionar repositorios
  - Instalar/actualizar/eliminar paquetes
  - Buscar paquetes
  - Limpiar caché de paquetes
  - Exportar lista de paquetes instalados

#### 4. Gestión de usuarios
- **Funcionalidad**: Administración de cuentas de usuario.
- **Opciones**:
  - Crear usuario
  - Eliminar usuario
  - Modificar usuario
  - Cambiar contraseña
  - Ver usuarios activos

#### 5. Gestión de servicios
- **Funcionalidad**: Control de servicios del sistema.
- **Opciones**:
  - Listar servicios
  - Iniciar servicio
  - Detener servicio
  - Reiniciar servicio
  - Ver estado del servicio

#### 6. Gestión de archivos
- **Funcionalidad**: Operaciones básicas con archivos y directorios.
- **Opciones**:
  - Navegar por directorios
  - Copiar archivos/directorios
  - Mover archivos/directorios
  - Eliminar archivos/directorios
  - Buscar archivos

#### 7. Gestión de red
- **Funcionalidad**: Herramientas de red y conectividad.
- **Opciones**:
  - Información de red
  - Detección de dispositivos
  - Escaneo de puertos
  - Detección de OS
  - Escaneo de servicios
  - Verificación de vulnerabilidades
  - Wake-on-LAN
  - Monitoreo de cambios en red
  - Información de interfaces
  - Escaneo WiFi
  - Pruebas de velocidad
  - Gestión del firewall

#### 8. Gestión de logs del sistema
- **Funcionalidad**: Visualización y gestión de archivos de log.
- **Opciones**:
  - Ver logs del sistema
  - Buscar en logs (con filtros de fecha)
  - Rotar logs

#### 9. Herramientas de redirección y transferencia
- **Funcionalidad**: Transferencia de archivos y ejecución remota.
- **Opciones**:
  - Ejecutar comando remoto via SSH
  - Transferir archivo con SCP
  - Sincronizar directorios con rsync

#### 10. Gestión de discos y particiones
- **Funcionalidad**: Administración de almacenamiento.
- **Opciones**:
  - Mostrar información de discos y particiones
  - Mostrar espacio en disco
  - Montar partición
  - Desmontar partición
  - Formatear partición
  - Verificar sistema de archivos

#### 11. Herramientas de seguridad básica
- **Funcionalidad**: Utilidades básicas de seguridad del sistema.
- **Opciones**:
  - Gestionar permisos de archivos (chmod)
  - Cambiar propietario de archivos (chown)
  - Configurar firewall (ufw)
  - Verificar integridad de archivos (MD5)
  - Gestionar configuración SSH
  - Verificar usuarios con permisos sudo

#### 12. Gestión de impresoras
- **Funcionalidad**: Administración de impresoras y trabajos de impresión.
- **Opciones**:
  - Listar impresoras instaladas
  - Agregar impresora
  - Eliminar impresora
  - Configurar impresora por defecto
  - Ver cola de impresión
  - Cancelar trabajos de impresión
  - Gestionar servicio CUPS

## Estructura de Archivos

```
listado-comandos/
├── menu.py              # Menú principal del programa
├── colores.py           # Definiciones de colores ANSI
├── conceptos.py         # Módulo de gestión de conceptos
├── sistema.py           # Módulo de información del sistema
├── software.py          # Módulo de gestión de software
├── usuarios.py          # Módulo de gestión de usuarios
├── servicios.py         # Módulo de gestión de servicios
├── archivos.py          # Módulo de gestión de archivos
├── red.py               # Módulo de gestión de red
├── logs.py              # Módulo de gestión de logs
├── transferencias.py    # Módulo de transferencias
├── discos.py            # Módulo de gestión de discos
├── seguridad.py         # Módulo de seguridad básica
├── impresoras.py        # Módulo de gestión de impresoras
└── README.md            # Este archivo
```

## Características

- **Interfaz intuitiva**: Menús coloreados y navegación sencilla
- **Manejo de errores**: Captura de excepciones y mensajes informativos
- **Operaciones seguras**: Confirmaciones para acciones destructivas
- **Modularidad**: Cada funcionalidad en su propio módulo
- **Colores ANSI**: Salida visualmente atractiva
- **Interrupción segura**: Manejo de Ctrl+C para salir limpiamente

## Contribución

Si deseas contribuir al proyecto:

1. Haz un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

## Autor

entreunosyceros

## Notas de seguridad

- Algunas operaciones requieren permisos de administrador (sudo)
- Usa las herramientas con precaución, especialmente las de formateo y eliminación
- Verifica siempre las rutas y comandos antes de ejecutar
- Este programa es una herramienta educativa. Que cada cual la utilice bajo su propia responsabilidad