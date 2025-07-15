from django.contrib import admin

from .models import Juego, Resena, Categoria

class JuegoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Juego.
    Permite seleccionar múltiples categorías fácilmente.
    """
    list_display = ['nombre', 'estudio', 'fecha_publicacion', 'importante', 'categorias_texto']
    list_filter = ['importante', 'categorias', 'estudio']
    search_fields = ['nombre', 'estudio', 'descripcion']
    filter_horizontal = ['categorias']  # Interface amigable para seleccionar categorías

class CategoriaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Categoria.
    """
    list_display = ['get_nombre_display']
    ordering = ['nombre']

class ResenaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Resena.
    """
    list_display = ['juego', 'usuario', 'puntuacion', 'fecha_creacion']
    list_filter = ['puntuacion', 'fecha_creacion']
    search_fields = ['juego__nombre', 'usuario__username', 'comentario']

admin.site.register(Juego, JuegoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Resena, ResenaAdmin)

