#!/usr/bin/env python
"""
Script de prueba para verificar la función obtener_imagenes_juegos
"""

import os
import sys
import django

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Djangocrud.settings')
django.setup()

# Importar la función
from Tareas.models import obtener_imagenes_juegos

if __name__ == "__main__":
    print("🔍 Probando función obtener_imagenes_juegos...")
    choices = obtener_imagenes_juegos()
    
    print(f"\n📋 Choices encontradas ({len(choices)} opciones):")
    for i, (valor, texto) in enumerate(choices):
        print(f"  {i+1}. '{valor}' -> '{texto}'")
    
    print(f"\n✅ Función ejecutada correctamente")
    print(f"📁 Imágenes disponibles: {len(choices) - 1}")  # -1 porque incluye 'Sin imagen'
