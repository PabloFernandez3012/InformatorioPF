#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append('c:\\Users\\Pablo\\OneDrive\\Escritorio\\ProyectoDjango')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Djangocrud.settings')
django.setup()

from Tareas.models import Juego

print("🔍 DIAGNÓSTICO DE ESTRELLAS EN MENÚ DE JUEGOS")
print("=" * 60)

# Obtener todos los juegos
juegos = Juego.objects.all()

for juego in juegos:
    promedio = juego.promedio_puntuacion()
    estrellas_llenas = int(promedio) if promedio > 0 else 0
    total_resenas = juego.resenas.count()
    
    print(f"\n🎮 {juego.nombre}")
    print(f"   Estudio: {juego.estudio}")
    print(f"   Promedio: {promedio}")
    print(f"   Estrellas llenas: {estrellas_llenas}")
    print(f"   Total reseñas: {total_resenas}")
    
    # Simular la lógica de estrellas
    estrellas_display = ""
    for i in range(1, 6):  # 1 a 5
        if i <= estrellas_llenas:
            estrellas_display += "★"  # Estrella dorada
        else:
            estrellas_display += "☆"  # Estrella gris
    
    print(f"   Estrellas: {estrellas_display}")
    print(f"   HTML: {promedio} ({total_resenas})")

print("\n" + "=" * 60)
print("✅ VERIFICACIÓN COMPLETA")

# Verificar que la lógica sea correcta
print("\n🧮 VERIFICACIÓN DE LÓGICA:")
print("Battlefield 1942 (promedio 2.5) debería mostrar: ★★☆☆☆")
print("Black Myth (promedio 5.0) debería mostrar: ★★★★★")
print("UmaMusume (promedio 5.0) debería mostrar: ★★★★★")
