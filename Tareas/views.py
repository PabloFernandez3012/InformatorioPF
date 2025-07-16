# =============================================================================
# IMPORTACIONES NECESARIAS
# =============================================================================
from django.shortcuts import render, redirect, get_object_or_404  # Funciones para renderizar templates y redireccionar
from django.contrib.auth.forms import AuthenticationForm  # Formulario predefinido para login
from django.contrib.auth.models import User  # Modelo de usuario de Django
from django.contrib.auth import login, logout, authenticate  # Funciones para manejo de autenticación
from django.contrib.auth.decorators import login_required  # Decorador para requerir login
from django.db import IntegrityError  # Excepción para errores de base de datos
from .models import Juego, Resena  # Nuestros modelos personalizados
from .forms import FormularioRegistroPersonalizado  # Formulario personalizado de registro
from django.contrib import messages  # Para mostrar mensajes de éxito/error
import requests  # Para hacer peticiones HTTP a APIs externas
from datetime import datetime  # Para manejo de fechas
from functools import wraps  # Para crear decoradores personalizados
from django.core.cache import cache  # Para cachear datos y mejorar rendimiento
from django.core.paginator import Paginator  # Para paginación de resultados


# =============================================================================
# DECORADOR PERSONALIZADO PARA USUARIOS NORMALES
# =============================================================================
def usuarios_normales_required(view_func):
    """
    Decorador que permite acceso solo a usuarios normales (no superusuarios).
    Los superusuarios son redirigidos al panel de administración.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Si no está autenticado, redirigir al login
            return redirect('entrar')
        
        if request.user.is_superuser:
            # Si es superusuario, redirigir al admin
            return redirect('/admin/')
        
        # Si es usuario normal, permitir acceso
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


# =============================================================================
# FUNCIÓN PARA OBTENER NOTICIAS DE VIDEOJUEGOS
# =============================================================================
def obtener_noticias_gaming():
    """
    Obtiene noticias de videojuegos de forma priorizada con caché para mejorar rendimiento:
    1. Noticias de la base de datos (administrables desde Django Admin)
    2. Noticias RSS de sitios gaming españoles
    3. Noticias predefinidas como fallback
    """
    # OPTIMIZACIÓN: Intentar obtener noticias desde caché primero
    cache_key = 'noticias_gaming'
    noticias_cached = cache.get(cache_key)
    
    if noticias_cached:
        print("✅ Usando noticias desde caché (más rápido)")
        return noticias_cached
    
    try:
        # PRIORIDAD 1: Noticias desde la base de datos
        noticias_db = obtener_noticias_base_datos()
        if noticias_db and len(noticias_db) > 0:
            print(f"✅ Usando {len(noticias_db)} noticias de la base de datos")
            # Cachear por 5 minutos si hay noticias de BD
            cache.set(cache_key, noticias_db, 300)
            return noticias_db
        
        # PRIORIDAD 2: Intentar obtener noticias reales de RSS feeds
        noticias_rss = obtener_noticias_rss()
        if noticias_rss and len(noticias_rss) > 0:
            print(f"✅ Usando {len(noticias_rss)} noticias de RSS feeds")
            # Cachear por 15 minutos si son RSS (más tiempo porque son externas)
            cache.set(cache_key, noticias_rss, 900)
            return noticias_rss
        
        # FALLBACK: Usar noticias predefinidas
        print("📰 Usando noticias predefinidas como fallback")
        noticias_demo = obtener_noticias_demo()
        # Cachear noticias demo por 30 minutos
        cache.set(cache_key, noticias_demo, 1800)
        return noticias_demo
            
    except Exception as e:
        print(f"Error obteniendo noticias: {e}")
        return obtener_noticias_demo()  # Fallback a datos demo


def obtener_noticias_base_datos():
    """
    Obtiene noticias desde la base de datos de forma optimizada.
    Estas noticias se pueden gestionar desde el panel de administración de Django.
    """
    try:
        from .models import Noticia
        
        # OPTIMIZACIÓN: Solo obtener los campos necesarios y usar select_related si hay FK
        noticias = Noticia.objects.filter(
            activa=True, 
            destacada=True
        ).only(
            'titulo', 'descripcion', 'url', 'imagen_url', 'fuente', 'fecha_publicacion'
        ).order_by('-fecha_publicacion')[:4]
        
        if not noticias.exists():
            return []
        
        # Convertir a formato compatible con el template
        noticias_formateadas = []
        for noticia in noticias:
            noticia_data = {
                'title': noticia.titulo,
                'description': noticia.descripcion,
                'url': noticia.url,
                'urlToImage': noticia.imagen_url or f"https://via.placeholder.com/400x200/667eea/ffffff?text={noticia.fuente.replace(' ', '+')}",
                'source': {'name': noticia.fuente},
                'publishedAt': noticia.fecha_publicacion.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            noticias_formateadas.append(noticia_data)
        
        return noticias_formateadas
        
    except Exception as e:
        print(f"Error obteniendo noticias de BD: {e}")
        return []


def obtener_noticias_rss():
    """
    Obtiene noticias reales de videojuegos desde feeds RSS de sitios gaming españoles.
    Retorna noticias actuales que se pueden abrir y leer.
    """
    try:
        import feedparser
        from datetime import datetime
        import re
        
        # Lista de feeds RSS de sitios gaming españoles confiables
        feeds_gaming = [
            {
                'url': 'https://vandal.elespanol.com/rss/noticias',
                'source': 'Vandal',
                'max_noticias': 2
            },
            {
                'url': 'https://www.3djuegos.com/rss/noticias/',
                'source': '3DJuegos', 
                'max_noticias': 2
            },
            {
                'url': 'https://www.hobbyconsolas.com/rss/videojuegos/noticias',
                'source': 'HobbyConsolas',
                'max_noticias': 1
            },
            {
                'url': 'https://www.vidaextra.com/rss',
                'source': 'VidaExtra',
                'max_noticias': 1
            }
        ]
        
        todas_las_noticias = []
        
        for feed_info in feeds_gaming:
            try:
                print(f"Obteniendo noticias de {feed_info['source']}...")
                
                # Parsear el feed RSS
                feed = feedparser.parse(feed_info['url'])
                
                # Verificar que el feed se haya parseado correctamente
                if not hasattr(feed, 'entries') or len(feed.entries) == 0:
                    print(f"No se pudieron obtener entradas de {feed_info['source']}")
                    continue
                
                # Procesar las entradas del feed
                for i, entry in enumerate(feed.entries[:feed_info['max_noticias']]):
                    try:
                        # Limpiar el título
                        titulo = entry.title if hasattr(entry, 'title') else 'Sin título'
                        titulo = re.sub(r'<[^>]*>', '', titulo)  # Remover HTML
                        
                        # Obtener descripción
                        descripcion = ''
                        if hasattr(entry, 'summary'):
                            descripcion = entry.summary
                        elif hasattr(entry, 'description'):
                            descripcion = entry.description
                        else:
                            descripcion = 'No disponible'
                        
                        # Limpiar descripción de HTML
                        descripcion = re.sub(r'<[^>]*>', '', descripcion)
                        descripcion = descripcion.strip()
                        
                        # Obtener URL de la noticia
                        url_noticia = entry.link if hasattr(entry, 'link') else '#'
                        
                        # Obtener fecha de publicación
                        fecha_pub = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
                        if hasattr(entry, 'published_parsed') and entry.published_parsed:
                            try:
                                fecha_obj = datetime(*entry.published_parsed[:6])
                                fecha_pub = fecha_obj.strftime('%Y-%m-%dT%H:%M:%SZ')
                            except:
                                pass
                        
                        # Obtener imagen si está disponible
                        imagen_url = None
                        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                            imagen_url = entry.media_thumbnail[0]['url']
                        elif hasattr(entry, 'enclosures') and entry.enclosures:
                            for enclosure in entry.enclosures:
                                if 'image' in enclosure.get('type', ''):
                                    imagen_url = enclosure.get('href')
                                    break
                        
                        # URL de imagen por defecto con el nombre del sitio
                        if not imagen_url:
                            color_map = {
                                'Vandal': '667eea',
                                '3DJuegos': '764ba2', 
                                'HobbyConsolas': 'ff6b6b',
                                'VidaExtra': 'ee5a24'
                            }
                            color = color_map.get(feed_info['source'], '667eea')
                            imagen_url = f"https://via.placeholder.com/400x200/{color}/ffffff?text={feed_info['source']}"
                        
                        # Crear objeto noticia compatible con el template
                        noticia = {
                            'title': titulo,
                            'description': descripcion,
                            'url': url_noticia,
                            'urlToImage': imagen_url,
                            'source': {'name': feed_info['source']},
                            'publishedAt': fecha_pub
                        }
                        
                        todas_las_noticias.append(noticia)
                        print(f"✓ Noticia añadida: {titulo[:50]}...")
                        
                    except Exception as entry_error:
                        print(f"Error procesando entrada de {feed_info['source']}: {entry_error}")
                        continue
                        
            except Exception as feed_error:
                print(f"Error obteniendo feed de {feed_info['source']}: {feed_error}")
                continue
        
        # Ordenar por fecha (más recientes primero) y limitar a 4
        if todas_las_noticias:
            todas_las_noticias.sort(key=lambda x: x['publishedAt'], reverse=True)
            resultado = todas_las_noticias[:4]
            print(f"✅ Total de noticias obtenidas: {len(resultado)}")
            return resultado
        else:
            print("❌ No se pudieron obtener noticias de ningún feed RSS")
            return []
            
    except ImportError:
        print("❌ feedparser no está instalado. Usa: pip install feedparser")
        return []
    except Exception as e:
        print(f"❌ Error general obteniendo noticias RSS: {e}")
        return []


def obtener_noticias_demo():
    """
    Noticias reales de videojuegos con URLs funcionales.
    Estas noticias se actualizan manualmente para mantener contenido relevante.
    """
    from datetime import datetime, timedelta
    
    # Generar fechas recientes realistas
    hoy = datetime.now()
    ayer = hoy - timedelta(days=1)
    hace_2_dias = hoy - timedelta(days=2)
    hace_3_dias = hoy - timedelta(days=3)
    
    # Noticias reales con URLs que funcionan y llevan a contenido real
    noticias_reales = [
        {
            'title': '📚 Guías completas de videojuegos - Todo lo que necesitas saber',
            'description': 'Descubre las mejores guías de videojuegos para dominar tus títulos favoritos. Desde walkthroughs completos hasta trucos secretos, mapas interactivos y estrategias avanzadas. Encuentra guías detalladas para los juegos más populares de PlayStation, Xbox, Nintendo Switch y PC.',
            'urlToImage': 'https://via.placeholder.com/400x200/667eea/ffffff?text=Guias+Gaming',
            'url': 'https://vandal.elespanol.com/guias/',
            'source': {'name': 'Vandal Gaming'},
            'publishedAt': hoy.strftime('%Y-%m-%dT%H:%M:%SZ')
        },
        {
            'title': '🔥 Noticias destacadas de Steam - Últimas actualizaciones gaming',
            'description': 'Mantente al día con las últimas noticias de Steam. Descubre nuevos lanzamientos, actualizaciones de juegos, ofertas especiales, eventos de temporada y las novedades más importantes de la plataforma gaming más popular del mundo. Todo lo que necesitas saber sobre el ecosistema Steam.',
            'urlToImage': 'https://via.placeholder.com/400x200/764ba2/ffffff?text=Steam+News',
            'url': 'https://store.steampowered.com/news/collection/featured/',
            'source': {'name': 'Steam News'},
            'publishedAt': ayer.strftime('%Y-%m-%dT%H:%M:%SZ')
        },
        {
            'title': '💰 Rebajas y ofertas especiales de Steam - Los mejores descuentos',
            'description': 'Descubre las mejores ofertas y rebajas de Steam con descuentos increíbles en miles de juegos. Desde títulos AAA hasta indies destacados, encuentra los mejores precios en los juegos más vendidos. No te pierdas estas oportunidades únicas con descuentos de hasta el 90%.',
            'urlToImage': 'https://via.placeholder.com/400x200/ff6b6b/ffffff?text=Steam+Ofertas',
            'url': 'https://store.steampowered.com/specials#tab=TopSellers',
            'source': {'name': 'Steam Store'},
            'publishedAt': hace_2_dias.strftime('%Y-%m-%dT%H:%M:%SZ')
        },
        {
            'title': '💻 Steam: Los juegos más populares de 2025',
            'description': 'Descubre los juegos más populares y mejor valorados de Steam en 2025. Desde indies innovadores hasta blockbusters AAA, conoce qué está jugando la comunidad gaming mundial y cuáles son las próximas grandes promesas.',
            'urlToImage': 'https://via.placeholder.com/400x200/ee5a24/ffffff?text=Steam+Popular+2025',
            'url': 'https://store.steampowered.com/charts/',
            'source': {'name': 'Steam Store'},
            'publishedAt': hace_3_dias.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
    ]
    
    return noticias_reales


# =============================================================================
# VISTA PRINCIPAL - PÁGINA DE INICIO
# =============================================================================
def home(request):
    """
    Vista que renderiza la página principal del sitio.
    Ahora incluye noticias de videojuegos para hacer la página más atractiva.
    """
    # Obtener noticias de gaming
    noticias = obtener_noticias_gaming()
    
    context = {
        'noticias': noticias
    }
    return render(request, 'home.html', context)


# =============================================================================
# VISTA DE REGISTRO DE USUARIOS
# =============================================================================
def signup(request):
    """
    Vista para registrar nuevos usuarios con validaciones personalizadas.
    - GET: Muestra el formulario vacío
    - POST: Procesa el registro y valida los datos
    """
    if request.method == 'GET':
        # Si es GET, mostrar formulario vacío de registro
        return render(request, 'signup.html', {'form': FormularioRegistroPersonalizado()})
    else:
        # Si es POST, procesar los datos del formulario
        form = FormularioRegistroPersonalizado(request.POST)
        if form.is_valid():
            # Si el formulario es válido, intentar crear el usuario
            try:
                user = form.save()  # Guardar el usuario en la base de datos
                
                # Asegurarse de que los usuarios registrados públicamente no sean superusuarios
                user.is_superuser = False
                user.is_staff = False
                user.save()
                
                login(request, user)  # Iniciar sesión automáticamente
                return redirect('tareas')  # Redirigir a la página de juegos
            except IntegrityError:
                # Si hay error de integridad (ej: usuario duplicado)
                return render(request, 'signup.html', {
                    'form': FormularioRegistroPersonalizado(), 
                    "error": "Error al crear el usuario. Intenta de nuevo."
                })
        else:
            # Si el formulario no es válido, mostrar errores
            return render(request, 'signup.html', {'form': form})
    
    # Fallback en caso de error inesperado
    return render(request, 'signup.html', {'form': FormularioRegistroPersonalizado()})


# =============================================================================
# VISTA DE LISTA DE JUEGOS CON BÚSQUEDA Y FILTROS
# =============================================================================
def tareas(request):
    """
    Vista que muestra todos los juegos disponibles con capacidad de búsqueda y filtrado.
    Permite filtrar por:
    - Nombre del juego (búsqueda de texto)
    - Categoría
    - Estudio desarrollador
    - Año de publicación
    """
    # Importar el modelo aquí para evitar problemas de importación circular
    from .models import Categoria
    
    # OPTIMIZACIÓN: Usar prefetch_related para reducir consultas N+1
    juegos = Juego.objects.prefetch_related('categorias').all()
    
    # ===== OBTENER PARÁMETROS DE BÚSQUEDA Y FILTROS =====
    busqueda = request.GET.get('busqueda', '')  # Texto de búsqueda
    categoria_filtro = request.GET.get('categoria', '')  # Filtro por categoría
    estudio_filtro = request.GET.get('estudio', '')  # Filtro por estudio
    ano_filtro = request.GET.get('ano', '')  # Filtro por año
    
    # ===== APLICAR FILTRO DE BÚSQUEDA POR NOMBRE =====
    if busqueda:
        # Filtrar juegos que contengan el texto de búsqueda en el nombre (insensible a mayúsculas)
        juegos = juegos.filter(nombre__icontains=busqueda)
    
    # ===== APLICAR FILTRO POR CATEGORÍA =====
    if categoria_filtro:
        # Filtrar juegos que tengan la categoría seleccionada
        juegos = juegos.filter(categorias__nombre=categoria_filtro)
    
    # ===== APLICAR FILTRO POR ESTUDIO =====
    if estudio_filtro:
        # Filtrar juegos del estudio seleccionado (insensible a mayúsculas)
        juegos = juegos.filter(estudio__icontains=estudio_filtro)
    
    # ===== APLICAR FILTRO POR AÑO =====
    if ano_filtro:
        try:
            # Filtrar juegos publicados en el año especificado
            juegos = juegos.filter(fecha_publicacion__year=int(ano_filtro))
        except ValueError:
            # Si el año no es válido, ignorar el filtro
            pass
    
    # ===== REMOVER DUPLICADOS (en caso de múltiples categorías) =====
    juegos = juegos.distinct()
    
    # ===== OBTENER DATOS PARA LOS FILTROS (OPTIMIZADO) =====
    # OPTIMIZACIÓN: Usar caché para datos que cambian poco
    cache_key_filtros = 'datos_filtros_juegos'
    datos_filtros = cache.get(cache_key_filtros)
    
    if not datos_filtros:
        # Lista de todas las categorías disponibles para el filtro
        todas_categorias = list(Categoria.objects.all())
        
        # Lista de todos los estudios únicos para el filtro
        todos_estudios = list(Juego.objects.values_list('estudio', flat=True).distinct().order_by('estudio'))
        
        # Lista de años únicos para el filtro
        todos_anos = Juego.objects.dates('fecha_publicacion', 'year', order='DESC')
        anos_lista = [fecha.year for fecha in todos_anos]
        
        datos_filtros = {
            'categorias': todas_categorias,
            'estudios': todos_estudios,
            'anos': anos_lista
        }
        
        # Cachear por 1 hora (los datos de filtros no cambian frecuentemente)
        cache.set(cache_key_filtros, datos_filtros, 3600)
        print("✅ Datos de filtros guardados en caché")
    else:
        print("✅ Usando datos de filtros desde caché")
    
    # ===== IMPLEMENTAR PAGINACIÓN PARA MEJORAR RENDIMIENTO =====
    paginator = Paginator(juegos, 12)  # Mostrar 12 juegos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # ===== PREPARAR CONTEXTO PARA EL TEMPLATE =====
    contexto = {
        'juegos': page_obj,  # Usar page_obj en lugar de juegos para paginación
        'page_obj': page_obj,  # Objeto de paginación para controles
        'busqueda_actual': busqueda,
        'categoria_actual': categoria_filtro,
        'estudio_actual': estudio_filtro,
        'ano_actual': ano_filtro,
        'todas_categorias': datos_filtros['categorias'],
        'todos_estudios': datos_filtros['estudios'],
        'todos_anos': datos_filtros['anos'],
        'total_resultados': paginator.count,  # Total de resultados sin paginar
    }
    
    return render(request, 'tareas.html', contexto)


# =============================================================================
# VISTA DE CERRAR SESIÓN
# =============================================================================
def cerrar_sesion(request):
    """
    Vista para cerrar la sesión del usuario actual.
    Cierra la sesión y redirige a la página principal.
    """
    logout(request)  # Cerrar la sesión del usuario
    return redirect('home')  # Redirigir a la página principal


# =============================================================================
# VISTA DE INICIO DE SESIÓN
# =============================================================================
def entrar(request):
    """
    Vista para que los usuarios existentes inicien sesión.
    - GET: Muestra el formulario de login
    - POST: Procesa las credenciales y autentica al usuario
    - Superusuarios son redirigidos automáticamente al panel de administración
    """
    if request.method == 'GET':
        # Si es GET, mostrar formulario de login vacío
        return render(request, 'entrar.html', {'form': AuthenticationForm()})
    else:
        # Si es POST, procesar las credenciales
        user = authenticate(
            request, 
            username=request.POST['username'], 
            password=request.POST['password']
        )
        if user is None:
            # Si las credenciales son incorrectas
            return render(request, 'entrar.html', {
                'form': AuthenticationForm(), 
                'error': 'Usuario o contraseña incorrectos'
            })
        else:
            # Si las credenciales son correctas
            login(request, user)  # Iniciar sesión
            
            # Verificar si es superusuario
            if user.is_superuser:
                # Redirigir superusuarios al panel de administración
                return redirect('/admin/')
            else:
                # Redirigir usuarios normales a la página de juegos
                return redirect('tareas')


# =============================================================================
# VISTA DE DETALLE DE JUEGO
# =============================================================================
def detalle_juego(request, juego_id):
    """
    Vista que muestra los detalles de un juego específico y sus reseñas.
    - Muestra información del juego
    - Lista todas las reseñas del juego
    - Verifica si el usuario ya hizo una reseña (para mostrar/ocultar botón)
    """
    # Obtener el juego o mostrar error 404 si no existe
    juego = get_object_or_404(Juego, id=juego_id)
    
    # Obtener todas las reseñas del juego ordenadas por fecha (más recientes primero)
    resenas = juego.resenas.all().order_by('-fecha_creacion')
    
    # Verificar si el usuario actual ya hizo una reseña de este juego
    usuario_ya_reseno = False
    if request.user.is_authenticated:
        usuario_ya_reseno = Resena.objects.filter(juego=juego, usuario=request.user).exists()
    
    # Pasar toda la información al template
    return render(request, 'detalle_juego.html', {
        'juego': juego,
        'resenas': resenas,
        'usuario_ya_reseno': usuario_ya_reseno
    })


# =============================================================================
# VISTA DE CREAR RESEÑA (REQUIERE LOGIN)
# =============================================================================
@login_required  # Decorador que requiere que el usuario esté autenticado
def crear_resena(request, juego_id):
    """
    Vista para crear una nueva reseña de un juego.
    Solo usuarios autenticados pueden acceder.
    Previene reseñas duplicadas del mismo usuario para el mismo juego.
    """
    # Obtener el juego o mostrar error 404 si no existe
    juego = get_object_or_404(Juego, id=juego_id)
    
    # Verificar si el usuario ya hizo una reseña de este juego
    if Resena.objects.filter(juego=juego, usuario=request.user).exists():
        # Si ya existe una reseña, redirigir al detalle del juego
        return redirect('detalle_juego', juego_id=juego.id)
    
    if request.method == 'POST':
        # Si es POST, procesar los datos de la reseña
        puntuacion = request.POST.get('puntuacion')
        comentario = request.POST.get('comentario')
        
        if puntuacion and comentario:
            # Si se proporcionaron puntuación y comentario, crear la reseña
            Resena.objects.create(
                juego=juego,
                usuario=request.user,
                puntuacion=int(puntuacion),
                comentario=comentario
            )
            # Redirigir al detalle del juego para ver la nueva reseña
            return redirect('detalle_juego', juego_id=juego.id)
    
    # Si es GET o faltan datos, mostrar el formulario de crear reseña
    return render(request, 'crear_resena.html', {'juego': juego})


# =============================================================================
# PERFIL Y CONFIGURACIÓN DE USUARIO
# =============================================================================

@usuarios_normales_required
def perfil_usuario(request):
    """
    Vista que muestra el perfil del usuario autenticado.
    Incluye información personal y todas las reseñas que ha escrito.
    Solo accesible para usuarios normales (no superusuarios).
    """
    # Obtener todas las reseñas del usuario actual, ordenadas por fecha más reciente
    reseñas_usuario = Resena.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    # Calcular estadísticas del usuario
    total_reseñas = reseñas_usuario.count()
    
    # Preparar contexto para el template
    context = {
        'reseñas_usuario': reseñas_usuario,
        'total_reseñas': total_reseñas,
        'usuario': request.user,
    }
    
    return render(request, 'perfil_usuario.html', context)


@usuarios_normales_required
def configuracion_usuario(request):
    """
    Vista que permite al usuario cambiar su contraseña.
    Muestra formulario para cambio de contraseña con validaciones.
    Solo accesible para usuarios normales (no superusuarios).
    """
    if request.method == 'POST':
        # Obtener datos del formulario
        contraseña_actual = request.POST.get('contraseña_actual')
        nueva_contraseña = request.POST.get('nueva_contraseña')
        confirmar_contraseña = request.POST.get('confirmar_contraseña')
        
        # Lista para almacenar errores
        errores = []
        
        # ===== VALIDACIONES =====
        
        # 1. Verificar que la contraseña actual sea correcta
        if not request.user.check_password(contraseña_actual):
            errores.append('La contraseña actual es incorrecta.')
        
        # 2. Verificar que las nuevas contraseñas coincidan
        if nueva_contraseña != confirmar_contraseña:
            errores.append('Las nuevas contraseñas no coinciden.')
        
        # 3. Verificar longitud mínima de la nueva contraseña
        if len(nueva_contraseña) < 8:
            errores.append('La nueva contraseña debe tener al menos 8 caracteres.')
        
        # 4. Verificar que no sea demasiado simple
        if nueva_contraseña.isdigit():
            errores.append('La contraseña no puede ser solo números.')
        
        # 5. Verificar que no sea igual a la actual
        if request.user.check_password(nueva_contraseña):
            errores.append('La nueva contraseña debe ser diferente a la actual.')
        
        # Si no hay errores, cambiar la contraseña
        if not errores:
            request.user.set_password(nueva_contraseña)
            request.user.save()
            
            # Actualizar la sesión para que no se cierre automáticamente
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            
            # Mensaje de éxito
            messages.success(request, '¡Contraseña cambiada exitosamente!')
            return redirect('configuracion')
        else:
            # Si hay errores, mostrarlos
            for error in errores:
                messages.error(request, error)
    
    return render(request, 'configuracion_usuario.html')


# =============================================================================
# VISTA ACERCA DE - INFORMACIÓN DEL DESARROLLADOR
# =============================================================================
def acerca_de(request):
    """
    Vista que renderiza la página con información sobre el desarrollador
    y el proyecto del Informatorio Chaco.
    """
    context = {
        'desarrollador': 'Pablo Javier Fernandez',
        'institucion': 'Informatorio Chaco',
        'proyecto': 'Plataforma de Reseñas de Videojuegos',
        'año': '2025'
    }
    return render(request, 'acerca_de.html', context)


# =============================================================================
# VISTA PARA EDITAR RESEÑA (REQUIERE LOGIN)
# =============================================================================
@login_required  # Decorador que requiere que el usuario esté autenticado
def editar_resena(request, resena_id):
    """
    Vista para editar una reseña existente.
    Solo el autor de la reseña puede editarla.
    Permite modificar tanto la puntuación como el comentario.
    """
    # Obtener la reseña o mostrar error 404 si no existe
    resena = get_object_or_404(Resena, id=resena_id)
    
    # Verificar que el usuario actual sea el autor de la reseña
    if resena.usuario != request.user:
        messages.error(request, 'No tienes permiso para editar esta reseña.')
        return redirect('detalle_juego', juego_id=resena.juego.id)
    
    if request.method == 'POST':
        # Si es POST, procesar los datos actualizados de la reseña
        puntuacion = request.POST.get('puntuacion')
        comentario = request.POST.get('comentario')
        
        if puntuacion and comentario:
            # Validar que la puntuación esté en el rango correcto
            try:
                puntuacion_int = int(puntuacion)
                if 1 <= puntuacion_int <= 5:
                    # Actualizar la reseña
                    resena.puntuacion = puntuacion_int
                    resena.comentario = comentario
                    resena.save()
                    
                    messages.success(request, '¡Reseña actualizada exitosamente!')
                    return redirect('detalle_juego', juego_id=resena.juego.id)
                else:
                    messages.error(request, 'La puntuación debe estar entre 1 y 5.')
            except ValueError:
                messages.error(request, 'La puntuación debe ser un número válido.')
        else:
            messages.error(request, 'Todos los campos son obligatorios.')
    
    # Si es GET o hay errores, mostrar el formulario de edición
    return render(request, 'editar_resena.html', {
        'resena': resena,
        'juego': resena.juego
    })

# =============================================================================
