@echo off
REM =============================================================================
REM SETUP.BAT - SCRIPT DE INSTALACIÓN AUTOMÁTICA PARA WINDOWS
REM =============================================================================
REM Este script automatiza la instalación y configuración del proyecto Django
REM Ejecuta: setup.bat
REM =============================================================================

echo ========================================
echo   INSTALACIÓN DEL PROYECTO DJANGO
echo   Sistema de Gestión de Juegos
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Por favor, instala Python 3.8 o superior desde https://python.org
    pause
    exit /b 1
)

echo [1/6] Python detectado correctamente
echo.

REM Crear entorno virtual
echo [2/6] Creando entorno virtual...
python -m venv venv
if errorlevel 1 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)

REM Activar entorno virtual
echo [3/6] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo [4/6] Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

REM Ejecutar migraciones
echo [5/6] Configurando base de datos...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo ERROR: No se pudieron ejecutar las migraciones
    pause
    exit /b 1
)

REM Crear superusuario (opcional)
echo [6/6] ¿Deseas crear un superusuario? (s/n)
set /p create_super="Ingresa tu respuesta: "
if /i "%create_super%"=="s" (
    echo Creando superusuario...
    python manage.py createsuperuser
)

echo.
echo ========================================
echo    ¡INSTALACIÓN COMPLETADA!
echo ========================================
echo.
echo Para ejecutar el servidor:
echo   1. Activa el entorno virtual: venv\Scripts\activate
echo   2. Ejecuta el servidor: python manage.py runserver
echo   3. Abre tu navegador en: http://127.0.0.1:8000
echo.
echo ¿Deseas ejecutar el servidor ahora? (s/n)
set /p run_server="Ingresa tu respuesta: "
if /i "%run_server%"=="s" (
    echo Iniciando servidor de desarrollo...
    python manage.py runserver
)

pause
