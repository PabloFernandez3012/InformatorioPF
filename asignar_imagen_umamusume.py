#!/usr/bin/env python
"""
Script para asignar la imagen umamusume.png al juego UmaMusume
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
    print("🏇 Asignando imagen umamusume.png al juego UmaMusume...")
    
    try:
        # Buscar el juego UmaMusume
        juego = Juego.objects.get(nombre__icontains='umamusume')
        print(f"✅ Juego encontrado: {juego.nombre}")
        print(f"📁 Imagen actual: '{juego.imagen}'")
        
        # Cambiar la imagen
        juego.imagen = 'Tareas/img/games/umamusume.png'
        juego.save()
        
        print(f"🎯 Imagen actualizada a: '{juego.imagen}'")
        print(f"✅ ¡Cambio realizado con éxito!")
        
    except Juego.DoesNotExist:
        print("❌ No se encontró ningún juego con 'umamusume' en el nombre")
    except Exception as e:
        print(f"❌ Error: {e}")
