#!/bin/bash
# =============================================================================
# SETUP.SH - SCRIPT DE INSTALACIÓN AUTOMÁTICA PARA LINUX/MACOS
# =============================================================================
# Este script automatiza la instalación y configuración del proyecto Django
# Ejecuta: bash setup.sh
# =============================================================================

echo "========================================"
echo "  INSTALACIÓN DEL PROYECTO DJANGO"
echo "  Sistema de Gestión de Juegos"
echo "========================================"
echo

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    echo "Por favor, instala Python 3.8 o superior"
    exit 1
fi

echo "[1/6] Python detectado correctamente"
echo

# Crear entorno virtual
echo "[2/6] Creando entorno virtual..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo crear el entorno virtual"
    exit 1
fi

# Activar entorno virtual
echo "[3/6] Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "[4/6] Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi

# Ejecutar migraciones
echo "[5/6] Configurando base de datos..."
python manage.py makemigrations
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron ejecutar las migraciones"
    exit 1
fi

# Crear superusuario (opcional)
echo "[6/6] ¿Deseas crear un superusuario? (s/n)"
read -p "Ingresa tu respuesta: " create_super
if [[ $create_super == "s" || $create_super == "S" ]]; then
    echo "Creando superusuario..."
    python manage.py createsuperuser
fi

echo
echo "========================================"
echo "   ¡INSTALACIÓN COMPLETADA!"
echo "========================================"
echo
echo "Para ejecutar el servidor:"
echo "  1. Activa el entorno virtual: source venv/bin/activate"
echo "  2. Ejecuta el servidor: python manage.py runserver"
echo "  3. Abre tu navegador en: http://127.0.0.1:8000"
echo

echo "¿Deseas ejecutar el servidor ahora? (s/n)"
read -p "Ingresa tu respuesta: " run_server
if [[ $run_server == "s" || $run_server == "S" ]]; then
    echo "Iniciando servidor de desarrollo..."
    python manage.py runserver
fi
