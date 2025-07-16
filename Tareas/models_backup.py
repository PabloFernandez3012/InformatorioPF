from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Categoria(models.Model):
    """
    Modelo para las categorías de juegos.
    Cada categoría tiene un nombre único.
    """
    CATEGORIAS_CHOICES = [
        ('disparos', 'Disparos'),
        ('carrera', 'Carrera'),
        ('puzzles', 'Puzzles'),
        ('rpg', 'RPG'),
        ('estrategia', 'Estrategia'),
        ('deportes', 'Deportes'),
        ('aventura', 'Aventura'),
        ('plataformas', 'Plataformas'),
        ('simulacion', 'Simulación'),
        ('mundo_abierto', 'Mundo Abierto'),
        ('terror', 'Terror'),
        ('coop', 'Cooperativo'),
        ('metroidvania', 'Metroidvania'),
        ('cartas', 'Cartas'),
    ]
    
    nombre = models.CharField(
        max_length=20,
        choices=CATEGORIAS_CHOICES,
        unique=True,
        help_text='Selecciona una categoría para los juegos'
    )
    
    def get_nombre_display(self):
        """Retorna el nombre legible de la categoría"""
        return dict(self.CATEGORIAS_CHOICES).get(self.nombre, self.nombre)
    
    def __str__(self):
        return self.get_nombre_display()
    
    class Meta:
        verbose_name_plural = "Categorías"

class Juego(models.Model):
    nombre = models.CharField(max_length=200)
    fecha_publicacion = models.DateField(default=date.today)
    estudio = models.CharField(max_length=150, default='Desconocido')
    descripcion = models.TextField(default='Sin descripción disponible')
    creado = models.DateTimeField(auto_now_add=True)
    importante = models.BooleanField(default=False)
    
    # Relación many-to-many con categorías (un juego puede tener varias categorías)
    categorias = models.ManyToManyField(Categoria, blank=True, help_text='Selecciona las categorías que corresponden a este juego')
    
    def categorias_texto(self):
        """Retorna las categorías como texto separado por comas para el admin"""
        return ", ".join([categoria.get_nombre_display() for categoria in self.categorias.all()])
    categorias_texto.short_description = 'Categorías'
    
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
    
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    puntuacion = models.IntegerField(choices=PUNTUACIONES)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('juego', 'usuario')  # Un usuario solo puede hacer una reseña por juego
    
    def __str__(self):
        return f"Reseña de {self.usuario.username} para {self.juego.nombre}"

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
