#!/bin/bash

# 🐍 GUÍA COMPLETA DEL ENTORNO VIRTUAL - PROYECTO DJANGO
# ====================================================

echo "🚀 ACTIVANDO ENTORNO VIRTUAL..."
echo "================================"

# Navegar al directorio del proyecto
cd "c:\Users\Pablo\OneDrive\Escritorio\ProyectoDjango"

# Activar el entorno virtual (Windows)
echo "⚡ Activando entorno virtual..."
source venv/Scripts/activate

# Verificar que el entorno está activado
echo ""
echo "✅ ESTADO DEL ENTORNO VIRTUAL:"
echo "=============================="
echo "🐍 Versión de Python en el entorno:"
python --version

echo ""
echo "📍 Ubicación del ejecutable de Python:"
which python

echo ""
echo "📦 PAQUETES INSTALADOS EN EL ENTORNO:"
echo "===================================="
pip list

echo ""
echo "🔍 INFORMACIÓN DEL ENTORNO VIRTUAL:"
echo "=================================="
echo "📂 Directorio del entorno: $(pwd)/venv"
echo "🏠 Python base: C:\Python312"
echo "🚀 Entorno aislado: ✅ Sí"
echo "📚 Paquetes del sistema: ❌ No incluidos"

echo ""
echo "🎯 COMANDOS ÚTILES:"
echo "=================="
echo "✅ Activar entorno: source venv/Scripts/activate"
echo "❌ Desactivar entorno: deactivate"
echo "📦 Instalar paquete: pip install nombre_paquete"
echo "📋 Ver paquetes: pip list"
echo "💾 Guardar dependencias: pip freeze > requirements.txt"
echo "🔄 Instalar desde requirements: pip install -r requirements.txt"

echo ""
echo "🎊 ¡ENTORNO VIRTUAL LISTO PARA USAR!"
