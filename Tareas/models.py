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
        ('simulador_citas', 'Simulador de Citas'),
        ('dark_souls', 'Tipo Dark Souls'),
        ('metroidvania', 'Metroidvania'),
        ('cartas', 'Cartas'),
        ('deportes', 'Deportes'),
        ('terror', 'Terror'),
        ('coop', 'Cooperativo'),
        ('hack_slash', 'Hack and Slash'),
    ]
    
    nombre = models.CharField(max_length=50, choices=CATEGORIAS_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_nombre_display()  # Muestra el nombre legible
    
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
    categorias = models.ManyToManyField(Categoria, blank=True, related_name='juegos')
    
    def __str__(self):
        return self.nombre
    
    def categorias_lista(self):
        """
        Retorna una lista de nombres de categorías para mostrar en templates.
        """
        return [categoria.get_nombre_display() for categoria in self.categorias.all()]
    
    def categorias_texto(self):
        """
        Retorna las categorías como texto separado por comas.
        """
        categorias = self.categorias_lista()
        if categorias:
            return ", ".join(categorias)
        return "Sin categorías"
    
    def puntuacion_promedio(self):
        """
        Calcula la puntuación promedio de todas las reseñas de este juego.
        Retorna None si no hay reseñas, o el promedio redondeado a 1 decimal.
        """
        resenas = self.resenas.all()
        if resenas.exists():
            total_puntuacion = sum([resena.puntuacion for resena in resenas])
            promedio = total_puntuacion / resenas.count()
            return round(promedio, 1)  # Redondear a 1 decimal
        return None
    
    def numero_resenas(self):
        """
        Retorna el número total de reseñas para este juego.
        """
        return self.resenas.count()
    
    def estrellas_promedio_visual(self):
        """
        Retorna una representación visual del promedio en estrellas.
        Ejemplo: 4.3 -> "★★★★☆ (4.3)"
        """
        promedio = self.puntuacion_promedio()
        if promedio is None:
            return "Sin reseñas"
        
        estrellas_llenas = int(promedio)  # Parte entera
        estrellas_vacias = 5 - estrellas_llenas
        
        visual = "★" * estrellas_llenas + "☆" * estrellas_vacias
        return f"{visual} ({promedio})"

class Resena(models.Model):
    PUNTUACIONES = [
        (1, '1 - Muy malo'),
        (2, '2 - Malo'),
        (3, '3 - Regular'),
        (4, '4 - Bueno'),
        (5, '5 - Excelente'),
    ]
    
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='resenas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(choices=PUNTUACIONES)
    comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('juego', 'usuario')  # Un usuario solo puede hacer una reseña por juego
    
    def __str__(self):
        return f"Reseña de {self.usuario.username} para {self.juego.nombre}"
