from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Categoria(models.Model):
    """
    Modelo para las categorías de juegos.
    Cada categoría tiene un nombre único.
    """
    # Categorías comunes como referencia (ya no se usan como choices)
    CATEGORIAS_POPULARES = [
        'Disparos', 'Carrera', 'Puzzles', 'RPG', 'Estrategia', 
        'Deportes', 'Aventura', 'Plataformas', 'Simulación', 
        'Mundo Abierto', 'Terror', 'Cooperativo', 'Metroidvania', 'Cartas'
    ]
    
    nombre = models.CharField(
        max_length=50,  # Aumentamos el límite para permitir nombres más largos
        unique=True,
        help_text='Escribe el nombre de la categoría (ej: Disparos, RPG, Aventura, etc.)'
    )
    
    def get_nombre_display(self):
        """Retorna el nombre de la categoría con formato título"""
        return self.nombre.title()
    
    def __str__(self):
        return self.get_nombre_display()
    
    def save(self, *args, **kwargs):
        """Guarda la categoría normalizando el nombre"""
        # Normalizar el nombre: primera letra mayúscula, resto minúsculas
        self.nombre = self.nombre.strip().title()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Categorías"

class Juego(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_publicacion = models.DateField(default=date.today)
    estudio = models.CharField(max_length=150, default='Desconocido')
    descripcion = models.TextField(default='Sin descripción disponible')
    imagen = models.ImageField(
        upload_to='juegos/', 
        blank=True, 
        null=True,
        help_text='Imagen del juego (opcional)'
    )
    creado = models.DateTimeField(auto_now_add=True)
    importante = models.BooleanField(default=False)
    
    # Relación many-to-many con categorías (un juego puede tener varias categorías)
    categorias = models.ManyToManyField(Categoria, blank=True, help_text='Selecciona las categorías que corresponden a este juego')
    
    def categorias_texto(self):
        """Retorna las categorías como texto separado por comas para el admin"""
        return ", ".join([categoria.get_nombre_display() for categoria in self.categorias.all()])
    categorias_texto.short_description = 'Categorías'
    
    def promedio_puntuacion(self):
        """Calcula el promedio de puntuaciones de todas las reseñas"""
        resenas = self.resenas.all()
        if resenas:
            return sum(resena.puntuacion for resena in resenas) / len(resenas)
        return 0
    
    def total_resenas(self):
        """Retorna el número total de reseñas"""
        return self.resenas.count()
    
    def __str__(self):
        return f"{self.nombre} ({self.estudio})"
    
    class Meta:
        ordering = ['nombre']  # Ordenar por nombre por defecto

class Resena(models.Model):
    """
    Modelo para las reseñas de juegos realizadas por usuarios.
    Cada usuario puede hacer solo una reseña por juego.
    """
    PUNTUACIONES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]
    
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='resenas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    puntuacion = models.IntegerField(choices=PUNTUACIONES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('juego', 'usuario')  # Un usuario solo puede hacer una reseña por juego
    
    def total_likes(self):
        """Retorna el número total de likes de la reseña"""
        return self.votos.filter(es_like=True).count()
    
    def total_dislikes(self):
        """Retorna el número total de dislikes de la reseña"""
        return self.votos.filter(es_like=False).count()
    
    def ratio_likes(self):
        """Calcula el ratio de likes vs total de votos (0-100)"""
        total_votos = self.votos.count()
        if total_votos == 0:
            return 0
        return (self.total_likes() / total_votos) * 100
    
    def __str__(self):
        return f"Reseña de {self.usuario.username} para {self.juego.nombre}"

class VotoResena(models.Model):
    """
    Modelo para gestionar los likes/dislikes de las reseñas.
    Similar al sistema de YouTube, un usuario puede dar like o dislike a una reseña.
    """
    resena = models.ForeignKey(Resena, on_delete=models.CASCADE, related_name='votos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    es_like = models.BooleanField(help_text="True para like, False para dislike")
    fecha_voto = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('resena', 'usuario')  # Un usuario solo puede votar una vez por reseña
        verbose_name = "Voto de Reseña"
        verbose_name_plural = "Votos de Reseñas"
    
    def __str__(self):
        tipo_voto = "👍 Like" if self.es_like else "👎 Dislike"
        return f"{tipo_voto} de {self.usuario.username} en reseña de {self.resena.juego.nombre}"

class Noticia(models.Model):
    """
    Modelo para gestionar noticias de videojuegos desde el panel de administración.
    Permite crear, editar y publicar noticias personalizadas.
    """
    titulo = models.CharField(max_length=200, help_text="Título de la noticia")
    descripcion = models.TextField(help_text="Descripción o resumen de la noticia")
    url = models.URLField(help_text="URL completa hacia la noticia original")
    imagen_url = models.URLField(blank=True, null=True, help_text="URL de la imagen (opcional)")
    fuente = models.CharField(max_length=100, default="Admin", help_text="Fuente de la noticia")
    destacada = models.BooleanField(default=True, help_text="Mostrar en página principal")
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activa = models.BooleanField(default=True, help_text="Noticia visible para usuarios")
    
    class Meta:
        ordering = ['-fecha_publicacion']
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
    
    def __str__(self):
        return f"{self.titulo} - {self.fuente}"
