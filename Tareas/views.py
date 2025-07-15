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


# =============================================================================
# VISTA PRINCIPAL - PÁGINA DE INICIO
# =============================================================================
def home(request):
    """
    Vista que renderiza la página principal del sitio.
    No requiere autenticación y sirve como punto de entrada.
    """
    return render(request, 'home.html')


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
    
    # Comenzar con todos los juegos
    juegos = Juego.objects.all()
    
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
    
    # ===== OBTENER DATOS PARA LOS FILTROS =====
    # Lista de todas las categorías disponibles para el filtro
    todas_categorias = Categoria.objects.all()
    
    # Lista de todos los estudios únicos para el filtro
    todos_estudios = Juego.objects.values_list('estudio', flat=True).distinct().order_by('estudio')
    
    # Lista de años únicos para el filtro
    todos_anos = Juego.objects.dates('fecha_publicacion', 'year', order='DESC')
    anos_lista = [fecha.year for fecha in todos_anos]
    
    # ===== PREPARAR CONTEXTO PARA EL TEMPLATE =====
    contexto = {
        'tareas': juegos,  # Mantener 'tareas' para compatibilidad con el template
        'busqueda_actual': busqueda,
        'categoria_actual': categoria_filtro,
        'estudio_actual': estudio_filtro,
        'ano_actual': ano_filtro,
        'todas_categorias': todas_categorias,
        'todos_estudios': todos_estudios,
        'todos_anos': anos_lista,
        'total_resultados': juegos.count(),
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
            return redirect('tareas')  # Redirigir a la página de juegos


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

@login_required
def perfil_usuario(request):
    """
    Vista que muestra el perfil del usuario autenticado.
    Incluye información personal y todas las reseñas que ha escrito.
    Requiere que el usuario esté autenticado.
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


@login_required
def configuracion_usuario(request):
    """
    Vista que permite al usuario cambiar su contraseña.
    Muestra formulario para cambio de contraseña con validaciones.
    Requiere que el usuario esté autenticado.
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
