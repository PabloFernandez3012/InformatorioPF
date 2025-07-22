from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin

class SuppressAdminMessagesMiddleware(MiddlewareMixin):
    """
    Middleware para suprimir las notificaciones verdes del panel de administrador.
    Elimina todos los mensajes de éxito en las URLs del admin.
    """
    
    def process_response(self, request, response):
        # Solo aplicar en las páginas del admin
        if request.path.startswith('/admin/'):
            # Obtener el storage de mensajes
            storage = messages.get_messages(request)
            
            # Filtrar solo los mensajes que NO son de éxito
            filtered_messages = []
            for message in storage:
                # Mantener solo mensajes de error, warning e info
                # Eliminar mensajes de SUCCESS (25) que son las notificaciones verdes
                if message.level != messages.SUCCESS:
                    filtered_messages.append(message)
            
            # Limpiar todos los mensajes existentes
            storage.used = True
            
            # Re-agregar solo los mensajes filtrados
            for message in filtered_messages:
                messages.add_message(request, message.level, message.message, message.tags)
        
        return response
