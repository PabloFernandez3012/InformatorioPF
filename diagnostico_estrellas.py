#!/usr/bin/env python
"""
Script de diagnóstico para verificar problemas con las estrellas
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Djangocrud.settings')
django.setup()

from Tareas.models import Juego, Resena

def diagnostico_estrellas():
    print("🔍 Diagnóstico del sistema de estrellas")
    print("=" * 60)
    
    print("1. 🎮 Verificando datos de juegos y reseñas:")
    for juego in Juego.objects.all():
        promedio = juego.promedio_puntuacion()
        total_resenas = juego.total_resenas()
        print(f"   📱 {juego.nombre}")
        print(f"      Promedio: {promedio:.1f}/5")
        print(f"      Reseñas: {total_resenas}")
        
        # Simular la lógica del template
        promedio_entero = int(promedio)
        print(f"      Promedio entero (para template): {promedio_entero}")
        print(f"      Estrellas llenas: {promedio_entero}")
        print(f"      Estrellas vacías: {5 - promedio_entero}")
        print()
    
    print("2. 🎨 Probando caracteres de estrellas:")
    caracteres = {
        'Emoji estrella': '⭐',
        'Unicode estrella llena': '★',
        'Unicode estrella vacía': '☆',
        'Unicode estrella media': '☆',
        'Símbolo alternativo': '✦'
    }
    
    for nombre, char in caracteres.items():
        print(f"   {nombre}: {char}")
    
    print("\n3. 🌈 Colores utilizados:")
    colores = {
        'Dorado estrellas llenas': '#eab308',
        'Gris estrellas vacías': '#d1d5db',
        'Amarillo Tailwind': 'text-yellow-500'
    }
    
    for nombre, color in colores.items():
        print(f"   {nombre}: {color}")
    
    print("\n4. 📝 Soluciones implementadas:")
    soluciones = [
        "✅ Cambié de emojis ⭐ a caracteres Unicode ★ y ☆",
        "✅ Agregué CSS inline como respaldo: style='color: #eab308'",
        "✅ Agregué clases CSS personalizadas: .star-filled y .star-empty",
        "✅ Agregué text-shadow para mejor visibilidad",
        "✅ Uso !important en CSS para forzar los estilos"
    ]
    
    for solucion in soluciones:
        print(f"   {solucion}")
    
    print("\n5. 🔧 Si las estrellas aún no tienen color:")
    problemas = [
        "💻 Problema del navegador: Algunos navegadores no renderizan bien ciertos Unicode",
        "🎨 CSS no se aplica: Verificar que Tailwind CSS esté cargando",
        "📱 Sistema operativo: Algunos SO no soportan ciertos emojis/Unicode",
        "🔍 Caché del navegador: Hacer Ctrl+F5 para limpiar caché",
        "⚙️ Configuración del navegador: Verificar que los estilos CSS estén habilitados"
    ]
    
    for problema in problemas:
        print(f"   {problema}")
    
    print("\n6. 🎯 Alternativas probadas:")
    print("   - Página de prueba creada: test_estrellas.html")
    print("   - Múltiples estilos CSS aplicados")
    print("   - Caracteres Unicode más compatibles")
    
    print("=" * 60)

if __name__ == "__main__":
    diagnostico_estrellas()
