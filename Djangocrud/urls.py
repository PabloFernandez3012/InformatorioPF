# =============================================================================
# CONFIGURACIÓN DE URLs DEL PROYECTO DJANGOCRUD
# =============================================================================
"""
Este archivo define todas las rutas (URLs) de la aplicación web.
Cada URL se conecta con una vista específica que procesa la petición.

Estructura básica: path('ruta/', views.nombre_vista, name='nombre_url')
- 'ruta/': La URL que el usuario escribe en el navegador
- views.nombre_vista: La función en views.py que se ejecuta
- name='nombre_url': Nombre interno para referenciar la URL en templates
"""

# =============================================================================
# IMPORTACIONES NECESARIAS
# =============================================================================
from django.contrib import admin  # Para acceder al panel de administración
from django.urls import path  # Para definir las rutas URL
from Tareas import views  # Importar todas las vistas de nuestra app Tareas
from django.conf import settings
from django.conf.urls.static import static

# =============================================================================
# LISTA DE PATRONES DE URL
# =============================================================================
urlpatterns = [
    # =========================================================================
    # PANEL DE ADMINISTRACIÓN DE DJANGO
    # =========================================================================
    path('admin/', admin.site.urls),  # URL: /admin/ - Panel de admin para gestionar la base de datos
    
    # =========================================================================
    # PÁGINA PRINCIPAL
    # =========================================================================
    path('', views.home, name='home'),  # URL: / - Página de inicio (raíz del sitio)
    
    # =========================================================================
    # AUTENTICACIÓN DE USUARIOS
    # =========================================================================
    path('signup/', views.signup, name='signup'),  # URL: /signup/ - Registro de nuevos usuarios
    path('entrar/', views.entrar, name='entrar'),  # URL: /entrar/ - Inicio de sesión
    path('logout/', views.cerrar_sesion, name='logout'),  # URL: /logout/ - Cerrar sesión
    
    # =========================================================================
    # GESTIÓN DE JUEGOS
    # =========================================================================
    path('tareas/', views.tareas, name='tareas'),  # URL: /tareas/ - Lista de todos los juegos
    
    # =========================================================================
    # INFORMACIÓN DEL PROYECTO
    # =========================================================================
    path('acerca-de/', views.acerca_de, name='acerca_de'),  # URL: /acerca-de/ - Información del desarrollador
    
    # =========================================================================
    # GESTIÓN DE RESEÑAS (REQUIEREN PARÁMETROS)
    # =========================================================================
    # URL: /juego/1/ - Detalles del juego con ID=1
    path('juego/<int:juego_id>/', views.detalle_juego, name='detalle_juego'),
    
    # URL: /juego/1/resena/ - Crear reseña para el juego con ID=1
    path('juego/<int:juego_id>/resena/', views.crear_resena, name='crear_resena'),
    
    # URL: /resena/1/editar/ - Editar reseña con ID=1
    path('resena/<int:resena_id>/editar/', views.editar_resena, name='editar_resena'),
    
    # =========================================================================
    # SISTEMA DE VOTOS (LIKES/DISLIKES) PARA RESEÑAS
    # =========================================================================
    # URL: /resena/1/votar/ - Votar (like/dislike) en reseña con ID=1
    path('resena/<int:resena_id>/votar/', views.votar_resena, name='votar_resena'),
    
    # URL: /resena/1/estado-voto/ - Obtener estado del voto del usuario (AJAX)
    path('resena/<int:resena_id>/estado-voto/', views.obtener_estado_voto, name='estado_voto'),
    
    # =========================================================================
    # PERFIL Y CONFIGURACIÓN DE USUARIO
    # =========================================================================
    # URL: /perfil/ - Ver perfil del usuario autenticado
    path('perfil/', views.perfil_usuario, name='perfil'),
    
    # URL: /configuracion/ - Configuración del usuario (cambiar contraseña)
    path('configuracion/', views.configuracion_usuario, name='configuracion'),
    
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
