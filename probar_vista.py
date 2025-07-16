#!/usr/bin/env python
"""
Script para probar la vista tareas sin ejecutar el servidor
"""
import os
import sys
import django
from django.test import RequestFactory

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Djangocrud.settings')
django.setup()

from Tareas.views import tareas

def probar_vista():
    print("🧪 Probando la vista tareas...")
    print("=" * 50)
    
    # Crear una request falsa
    factory = RequestFactory()
    request = factory.get('/tareas/')
    
    try:
        # Llamar a la vista
        response = tareas(request)
        
        print(f"✅ Vista ejecutada exitosamente")
        print(f"📄 Status code: {response.status_code}")
        print(f"📝 Template utilizado: {response.template_name if hasattr(response, 'template_name') else 'tareas.html'}")
        
        # Verificar contexto
        if hasattr(response, 'context_data'):
            context = response.context_data
        else:
            # Para TemplateResponse, obtener el contexto del renderer
            context = response.context_data if hasattr(response, 'context_data') else {}
        
        print(f"🔍 Variables en el contexto:")
        if hasattr(response, 'context_data'):
            for key in response.context_data.keys():
                print(f"  - {key}")
        
        print("=" * 50)
        print("✅ La vista parece estar funcionando correctamente!")
        
    except Exception as e:
        print(f"❌ Error al ejecutar la vista: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    probar_vista()
