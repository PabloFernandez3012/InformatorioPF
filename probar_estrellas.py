#!/usr/bin/env python
"""
Script para probar que las estrellas se muestren correctamente
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Djangocrud.settings')
django.setup()

from Tareas.models import Juego, Resena

def probar_estrellas():
    print("⭐ Probando el sistema de estrellas...")
    print("=" * 60)
    
    # Probar emojis de estrellas
    print("🧪 Probando emojis de estrellas:")
    for i in range(1, 6):
        print(f"  {i} estrellas: {'⭐' * i}{'☆' * (5-i)}")
    
    print("\n🎮 Probando con datos reales:")
    for juego in Juego.objects.all():
        promedio = juego.promedio_puntuacion()
        total_resenas = juego.total_resenas()
        
        # Generar estrellas basadas en el promedio
        estrellas_llenas = int(promedio)
        estrellas_vacias = 5 - estrellas_llenas
        estrellas_display = '⭐' * estrellas_llenas + '☆' * estrellas_vacias
        
        print(f"\n  📱 {juego.nombre}")
        print(f"    Promedio: {promedio:.1f}/5")
        print(f"    Estrellas: {estrellas_display}")
        print(f"    Reseñas: {total_resenas}")
        
        # Mostrar reseñas individuales
        if total_resenas > 0:
            print("    📝 Reseñas:")
            for resena in juego.resenas.all():
                resena_estrellas = '⭐' * resena.puntuacion + '☆' * (5 - resena.puntuacion)
                print(f"      - {resena.usuario.username}: {resena_estrellas} ({resena.puntuacion}/5)")
    
    print("\n" + "=" * 60)
    print("✅ Las estrellas deberían mostrarse correctamente ahora!")

if __name__ == "__main__":
    probar_estrellas()
