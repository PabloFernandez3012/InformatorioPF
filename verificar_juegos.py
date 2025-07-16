#!/usr/bin/env python
"""
Script para verificar el estado de las imágenes de los juegos
"""

import os
import sys
import django

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Djangocrud.settings')
django.setup()

# Importar modelos
from Tareas.models import Juego

if __name__ == "__main__":
    print("🎮 Verificando estado de imágenes de juegos...")
    
    juegos = Juego.objects.all()
    print(f"\n📊 Total de juegos en la base de datos: {juegos.count()}")
    
    for i, juego in enumerate(juegos, 1):
        imagen_status = "✅ CON IMAGEN" if juego.imagen else "❌ SIN IMAGEN"
        print(f"  {i}. {juego.nombre} - {imagen_status}")
        if juego.imagen:
            print(f"     📁 Imagen: '{juego.imagen}'")
    
    print(f"\n🔍 Juegos con imagen: {juegos.exclude(imagen='').count()}")
    print(f"🔍 Juegos sin imagen: {juegos.filter(imagen='').count()}")
    
    # Verificar si algún juego tiene la imagen umamusume
    juegos_umamusume = juegos.filter(imagen__icontains='umamusume')
    if juegos_umamusume.exists():
        print(f"\n🏇 Juegos con imagen umamusume: {juegos_umamusume.count()}")
        for juego in juegos_umamusume:
            print(f"   - {juego.nombre}: '{juego.imagen}'")
    else:
        print(f"\n🏇 No hay juegos con imagen umamusume asignada")
