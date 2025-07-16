#!/usr/bin/env python
"""
Script para verificar si hay juegos en la base de datos
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Djangocrud.settings')
django.setup()

from Tareas.models import Juego, Categoria

def verificar_datos():
    print("🔍 Verificando datos en la base de datos...")
    print("=" * 50)
    
    # Contar juegos
    total_juegos = Juego.objects.count()
    print(f"📊 Total de juegos en la base de datos: {total_juegos}")
    
    if total_juegos > 0:
        print("\n🎮 Primeros 5 juegos:")
        for juego in Juego.objects.all()[:5]:
            print(f"  - {juego.nombre} ({juego.estudio}) - {juego.fecha_publicacion}")
    else:
        print("\n❌ No hay juegos en la base de datos")
        print("\n💡 Sugerencias:")
        print("1. Acceder al admin de Django para agregar juegos")
        print("2. Verificar que las migraciones se hayan aplicado correctamente")
    
    # Contar categorías
    total_categorias = Categoria.objects.count()
    print(f"\n📂 Total de categorías: {total_categorias}")
    
    if total_categorias > 0:
        print("📂 Categorías disponibles:")
        for categoria in Categoria.objects.all():
            print(f"  - {categoria.nombre}")
    
    print("=" * 50)

if __name__ == "__main__":
    verificar_datos()
