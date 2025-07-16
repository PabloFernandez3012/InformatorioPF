from django.contrib import admin
from .models import Juego, Resena, Categoria, Noticia

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
    Configuración optimizada del admin para el modelo Categoria.
    """
    list_display = ['get_nombre_display']
    ordering = ['nombre']
    search_fields = ['nombre']

class ResenaAdmin(admin.ModelAdmin):
    """
    Configuración optimizada del admin para el modelo Resena.
    """
    list_display = ['juego', 'usuario', 'puntuacion', 'fecha_creacion']
    list_filter = ['puntuacion', 'fecha_creacion']
    search_fields = ['juego__nombre', 'usuario__username', 'comentario']
    ordering = ['-fecha_creacion']

class NoticiaAdmin(admin.ModelAdmin):
    """
    Configuración optimizada del admin para el modelo Noticia.
    """
    list_display = ['titulo', 'fuente', 'destacada', 'activa', 'fecha_publicacion']
    list_filter = ['destacada', 'activa', 'fuente', 'fecha_publicacion']
    search_fields = ['titulo', 'descripcion', 'fuente']
    ordering = ['-fecha_publicacion']
    readonly_fields = ['fecha_publicacion', 'fecha_actualizacion']

admin.site.register(Juego, JuegoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Resena, ResenaAdmin)
admin.site.register(Noticia, NoticiaAdmin)

