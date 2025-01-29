[app]

# Nombre de la aplicación
title = TransportApp

# Nombre del paquete (debe ser único)
package.name = transportapp

# Dominio del paquete (usualmente se usa el dominio inverso de tu organización)
package.domain = org.example

# Ruta del código fuente
source.dir = .

# Archivos y extensiones a incluir en el paquete
source.include_exts = py,png,jpg,kv,ttf,db

# Versión de la aplicación
version = 1.0

# Requisitos de Python y librerías
requirements = python3,kivy==2.1.0,android,pandas,openpyxl,sqlite3

# Orientación de la pantalla
orientation = portrait

# Versión de Python para compilación
python.version = 3

# Versión de Kivy
# (No es necesario si ya se especificó en requirements)
# osx.kivy_version = 2.1.0

# Pantalla completa (0 = no, 1 = sí)
fullscreen = 0

# Permisos de Android
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# API de Android (recomendado 30 o superior)
android.api = 30

# Versión del NDK (recomendado 19b o superior)
android.ndk = 25b

# Mantener la pantalla activa
android.wakelock = True

# Icono de la aplicación (debe estar en la carpeta source.dir)
# icon.filename = %(source.dir)s/icon.png

# Logotipo de la aplicación (opcional)
# presplash.filename = %(source.dir)s/presplash.png

# Configuración de la consola (0 = sin consola, 1 = con consola)
android.console = 0

# Habilitar el almacenamiento externo para Android 10+
android.allow_backup = True
android.archs = armeabi-v7a, arm64-v8a

# Configuración de Buildozer
[buildozer]

# Nivel de log (0 = mínimo, 1 = normal, 2 = detallado)
log_level = 2

# Directorio de salida para los archivos generados
bin_dir = ./bin
