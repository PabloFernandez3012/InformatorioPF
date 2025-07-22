from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Juego, Resena, Categoria, Noticia, VotoResena

class CategoriaAdmin(admin.ModelAdmin):
    """
    Configuración avanzada del admin para el modelo Categoria.
    Incluye funcionalidades mejoradas para gestión de categorías.
    """
    list_display = [
        'icono_categoria', 
        'nombre_con_formato', 
        'nombre_interno', 
        'cantidad_juegos',
        'acciones_rapidas'
    ]
    list_display_links = ['nombre_con_formato']
    ordering = ['nombre']
    search_fields = ['nombre']
    list_per_page = 20
    
    fields = ['nombre']
    
    def nombre_con_formato(self, obj):
        """Muestra el nombre formateado"""
        return obj.nombre.title()
    nombre_con_formato.short_description = 'Nombre'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['nombre'].help_text = mark_safe(
            '<strong>💡 Consejos:</strong><br>'
            '• Escribe el nombre de la categoría (ej: Disparos, RPG, Aventura)<br>'
            '• Se normalizará automáticamente con la primera letra en mayúscula<br>'
            '• Ejemplos populares: Disparos, Carrera, Puzzles, RPG, Estrategia, Deportes, etc.'
        )
        form.base_fields['nombre'].widget.attrs.update({
            'placeholder': 'Ej: Disparos, RPG, Aventura...',
            'style': 'font-size: 16px; padding: 12px;'
        })
        return form
    
    def icono_categoria(self, obj):
        """Muestra un ícono representativo para cada categoría"""
        iconos = {
            'disparos': '🔫',
            'carrera': '🏎️',
            'puzzles': '🧩',
            'rpg': '⚔️',
            'estrategia': '🧠',
            'deportes': '⚽',
            'aventura': '🗺️',
            'plataformas': '🏃‍♂️',
            'simulacion': '🎮',
            'mundo abierto': '🌍',
            'terror': '👻',
            'cooperativo': '👥',
            'coop': '👥',
            'metroidvania': '🏰',
            'cartas': '🃏',
            'accion': '💥',
            'indie': '🌟',
            'multijugador': '👫',
            'supervivencia': '🏕️',
            'rol': '⚔️',
            'musica': '🎵',
            'baile': '💃',
        }
        nombre_lower = obj.nombre.lower()
        icono = iconos.get(nombre_lower, '🎯')
        return format_html(
            '<span style="font-size: 20px; margin-right: 8px;">{}</span>',
            icono
        )
    icono_categoria.short_description = '🎨 Ícono'
    
    def nombre_interno(self, obj):
        """Muestra el nombre interno del campo"""
        return format_html(
            '<code style="background: #f8f9fa; padding: 2px 6px; border-radius: 3px; color: #6c757d;">{}</code>',
            obj.nombre
        )
    nombre_interno.short_description = '📋 Código'
    
    def cantidad_juegos(self, obj):
        """Muestra la cantidad de juegos asociados a esta categoría"""
        count = obj.juego_set.count()
        if count == 0:
            return format_html(
                '<span style="color: #6c757d; font-style: italic;">Sin juegos</span>'
            )
        elif count == 1:
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">1 juego</span>'
            )
        else:
            return format_html(
                '<span style="color: #007bff; font-weight: bold;">{} juegos</span>',
                count
            )
    cantidad_juegos.short_description = '🎮 Juegos'
    
    def acciones_rapidas(self, obj):
        """Botones de acciones rápidas"""
        count = obj.juego_set.count()
        if count > 0:
            try:
                url = reverse('admin:Tareas_juego_changelist') + f'?categorias__id__exact={obj.id}'
                return format_html(
                    '<a href="{}" class="button" style="background: #007cba; color: white; padding: 4px 8px; text-decoration: none; border-radius: 3px; font-size: 11px;">Ver juegos</a>',
                    url
                )
            except:
                return format_html(
                    '<span style="color: #dc3545; font-style: italic; font-size: 11px;">Error en URL</span>'
                )
        return format_html(
            '<span style="color: #6c757d; font-style: italic; font-size: 11px;">Sin acciones</span>'
        )
    acciones_rapidas.short_description = '⚡ Acciones'
    
    def get_queryset(self, request):
        """Optimiza las consultas para evitar N+1 queries"""
        return super().get_queryset(request).prefetch_related('juego_set')
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        nombre = obj.nombre.title()
        if change:
            self.message_user(
                request, 
                f'✅ Categoría "{nombre}" actualizada correctamente.'
            )
        else:
            self.message_user(
                request, 
                f'🎉 Categoría "{nombre}" creada exitosamente.'
            )
    
    def delete_model(self, request, obj):
        nombre = obj.nombre
        super().delete_model(request, obj)
        self.message_user(
            request, 
            f'🗑️ Categoría "{nombre}" eliminada correctamente.'
        )

class JuegoAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Juego.
    Permite seleccionar múltiples categorías fácilmente.
    """
    list_display = ['nombre', 'estudio', 'fecha_publicacion', 'importante', 'categorias_con_iconos']
    list_filter = ['importante', 'categorias', 'estudio', 'fecha_publicacion']
    search_fields = ['nombre', 'estudio', 'descripcion']
    filter_horizontal = ['categorias']
    list_editable = ['importante']
    list_per_page = 20
    
    fieldsets = (
        ('📋 Información Básica', {
            'fields': ('nombre', 'estudio', 'descripcion')
        }),
        ('📅 Fechas y Estado', {
            'fields': ('fecha_publicacion', 'importante'),
            'classes': ('collapse',)
        }),
        ('🎨 Multimedia', {
            'fields': ('imagen',),
            'classes': ('collapse',)
        }),
        ('🏷️ Categorías', {
            'fields': ('categorias',),
            'description': 'Selecciona una o múltiples categorías para clasificar este juego.'
        })
    )
    
    def categorias_con_iconos(self, obj):
        """Muestra las categorías con íconos"""
        iconos = {
            'disparos': '🔫',
            'carrera': '🏎️',
            'puzzles': '🧩',
            'rpg': '⚔️',
            'estrategia': '🧠',
            'deportes': '⚽',
            'aventura': '🗺️',
            'plataformas': '🏃‍♂️',
            'simulacion': '🎮',
            'mundo_abierto': '🌍',
            'terror': '👻',
            'coop': '👥',
            'metroidvania': '🏰',
            'cartas': '🃏',
        }
        
        categorias = obj.categorias.all()
        if not categorias:
            return format_html('<span style="color: #6c757d; font-style: italic;">Sin categorías</span>')
        
        html_parts = []
        for categoria in categorias:
            icono = iconos.get(categoria.nombre.lower(), '🎯')
            nombre_display = categoria.nombre.title()
            html_parts.append(
                f'<span style="background: #e3f2fd; color: #1976d2; padding: 2px 6px; border-radius: 12px; font-size: 11px; margin-right: 4px;">'
                f'{icono} {nombre_display}</span>'
            )
        
        return format_html(''.join(html_parts))
    categorias_con_iconos.short_description = '🏷️ Categorías'

class ResenaAdmin(admin.ModelAdmin):
    list_display = ['juego', 'puntuacion', 'fecha_creacion']
    list_filter = ['puntuacion', 'fecha_creacion']
    search_fields = ['juego__nombre', 'comentario']

class NoticiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'fecha_publicacion']
    list_filter = ['fecha_publicacion']
    search_fields = ['titulo', 'contenido']

class VotoResenaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para gestionar los votos (likes/dislikes) de reseñas.
    """
    list_display = ['resena_info', 'usuario', 'tipo_voto', 'fecha_voto']
    list_filter = ['es_like', 'fecha_voto']
    search_fields = ['usuario__username', 'resena__juego__nombre']
    readonly_fields = ['fecha_voto']
    list_per_page = 50
    ordering = ['-fecha_voto']
    
    def resena_info(self, obj):
        """Muestra información de la reseña votada"""
        return f"{obj.resena.juego.nombre} - {obj.resena.usuario.username}"
    resena_info.short_description = 'Reseña'
    
    def tipo_voto(self, obj):
        """Muestra el tipo de voto con emoji"""
        if obj.es_like:
            return format_html('<span style="color: green;">👍 Like</span>')
        else:
            return format_html('<span style="color: red;">👎 Dislike</span>')
    tipo_voto.short_description = 'Voto'

# Registrar los modelos
admin.site.register(Juego, JuegoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Resena, ResenaAdmin)
admin.site.register(Noticia, NoticiaAdmin)
admin.site.register(VotoResena, VotoResenaAdmin)

