#!/usr/bin/env python
"""
Script para verificar las reseñas y sus puntuaciones
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Djangocrud.settings')
django.setup()

from Tareas.models import Juego, Resena

def verificar_resenas():
    print("🔍 Verificando reseñas en la base de datos...")
    print("=" * 60)
    
    # Contar reseñas
    total_resenas = Resena.objects.count()
    print(f"📊 Total de reseñas: {total_resenas}")
    
    if total_resenas > 0:
        print("\n📝 Reseñas encontradas:")
        for resena in Resena.objects.all():
            print(f"  - {resena.juego.nombre} por {resena.usuario.username}")
            print(f"    Puntuación: {resena.puntuacion}/5")
            print(f"    Comentario: {resena.comentario[:50]}...")
            print()
    else:
        print("\n❌ No hay reseñas en la base de datos")
        print("\n💡 Sugerencias:")
        print("1. Crear algunas reseñas desde la interfaz web")
        print("2. Verificar que los usuarios puedan acceder al formulario de reseñas")
    
    # Verificar promedios de puntuación
    print("\n🎮 Promedios de puntuación por juego:")
    for juego in Juego.objects.all():
        promedio = juego.promedio_puntuacion()
        total_resenas_juego = juego.total_resenas()
        print(f"  - {juego.nombre}: {promedio:.1f}/5 ({total_resenas_juego} reseñas)")
    
    print("=" * 60)

if __name__ == "__main__":
    verificar_resenas()
