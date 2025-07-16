from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from Tareas.models import Categoria

class Command(BaseCommand):
    help = '🎯 Gestiona las categorías de juegos desde la línea de comandos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--crear',
            type=str,
            help='Crear una nueva categoría (ej: --crear disparos)'
        )
        parser.add_argument(
            '--listar',
            action='store_true',
            help='Lista todas las categorías disponibles'
        )
        parser.add_argument(
            '--disponibles',
            action='store_true',
            help='Muestra las categorías disponibles para crear'
        )
        parser.add_argument(
            '--stats',
            action='store_true',
            help='Muestra estadísticas de categorías'
        )
        parser.add_argument(
            '--eliminar',
            type=str,
            help='Eliminar una categoría existente (ej: --eliminar disparos)'
        )

    def handle(self, *args, **options):
        if options['listar']:
            self.listar_categorias()
        elif options['disponibles']:
            self.mostrar_disponibles()
        elif options['stats']:
            self.mostrar_estadisticas()
        elif options['crear']:
            self.crear_categoria(options['crear'])
        elif options['eliminar']:
            self.eliminar_categoria(options['eliminar'])
        else:
            self.mostrar_ayuda()

    def listar_categorias(self):
        """Lista todas las categorías existentes"""
        categorias = Categoria.objects.all().order_by('nombre')
        
        if not categorias:
            self.stdout.write(
                self.style.WARNING('📭 No hay categorías creadas todavía.')
            )
            return

        self.stdout.write(
            self.style.SUCCESS('\n🏷️  CATEGORÍAS EXISTENTES')
        )
        self.stdout.write('=' * 50)
        
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
        
        for categoria in categorias:
            icono = iconos.get(categoria.nombre, '🎯')
            count = categoria.juego_set.count()
            juegos_text = f"({count} juego{'s' if count != 1 else ''})"
            
            self.stdout.write(
                f"{icono} {categoria.get_nombre_display():<20} "
                f"{self.style.HTTP_INFO(juegos_text)}"
            )

    def mostrar_disponibles(self):
        """Muestra las categorías disponibles para crear"""
        categorias_existentes = set(
            Categoria.objects.values_list('nombre', flat=True)
        )
        
        todas_las_categorias = dict(Categoria.CATEGORIAS_CHOICES)
        disponibles = {
            k: v for k, v in todas_las_categorias.items() 
            if k not in categorias_existentes
        }
        
        if not disponibles:
            self.stdout.write(
                self.style.SUCCESS('🎉 ¡Todas las categorías ya están creadas!')
            )
            return

        self.stdout.write(
            self.style.SUCCESS('\n🆕 CATEGORÍAS DISPONIBLES PARA CREAR')
        )
        self.stdout.write('=' * 50)
        
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
        
        for codigo, nombre in disponibles.items():
            icono = iconos.get(codigo, '🎯')
            self.stdout.write(
                f"{icono} {nombre:<20} "
                f"{self.style.HTTP_INFO(f'(código: {codigo})')}"
            )
        
        self.stdout.write('\n💡 Para crear una categoría usa:')
        self.stdout.write(
            f"   {self.style.SUCCESS('python manage.py categorias --crear <codigo>')}"
        )

    def mostrar_estadisticas(self):
        """Muestra estadísticas de las categorías"""
        total_categorias = Categoria.objects.count()
        total_posibles = len(Categoria.CATEGORIAS_CHOICES)
        
        self.stdout.write(
            self.style.SUCCESS('\n📊 ESTADÍSTICAS DE CATEGORÍAS')
        )
        self.stdout.write('=' * 50)
        
        self.stdout.write(f"📋 Total de categorías creadas: {total_categorias}")
        self.stdout.write(f"📝 Total de categorías posibles: {total_posibles}")
        self.stdout.write(f"📈 Completitud: {(total_categorias/total_posibles)*100:.1f}%")
        
        if total_categorias > 0:
            # Categorías con más juegos
            categoria_mas_popular = Categoria.objects.annotate(
                num_juegos=models.Count('juego')
            ).order_by('-num_juegos').first()
            
            if categoria_mas_popular and categoria_mas_popular.juego_set.count() > 0:
                self.stdout.write(
                    f"🏆 Categoría más popular: {categoria_mas_popular.get_nombre_display()} "
                    f"({categoria_mas_popular.juego_set.count()} juegos)"
                )

    def crear_categoria(self, codigo):
        """Crea una nueva categoría"""
        # Verificar que el código es válido
        codigos_validos = dict(Categoria.CATEGORIAS_CHOICES)
        if codigo not in codigos_validos:
            self.stdout.write(
                self.style.ERROR(f'❌ Código "{codigo}" no es válido.')
            )
            self.stdout.write('💡 Códigos válidos:')
            for cod, nombre in codigos_validos.items():
                self.stdout.write(f"   • {cod} → {nombre}")
            return

        try:
            categoria = Categoria.objects.create(nombre=codigo)
            iconos = {
                'disparos': '🔫', 'carrera': '🏎️', 'puzzles': '🧩', 'rpg': '⚔️',
                'estrategia': '🧠', 'deportes': '⚽', 'aventura': '🗺️',
                'plataformas': '🏃‍♂️', 'simulacion': '🎮', 'mundo_abierto': '🌍',
                'terror': '👻', 'coop': '👥', 'metroidvania': '🏰', 'cartas': '🃏',
            }
            icono = iconos.get(codigo, '🎯')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Categoría creada exitosamente: '
                    f'{icono} {categoria.get_nombre_display()}'
                )
            )
            
        except IntegrityError:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ La categoría "{codigos_validos[codigo]}" ya existe.'
                )
            )

    def eliminar_categoria(self, codigo):
        """Elimina una categoría existente"""
        try:
            categoria = Categoria.objects.get(nombre=codigo)
            nombre_display = categoria.get_nombre_display()
            num_juegos = categoria.juego_set.count()
            
            if num_juegos > 0:
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠️  La categoría "{nombre_display}" tiene {num_juegos} juego(s) asociado(s).'
                    )
                )
                confirmacion = input('¿Estás seguro de que quieres eliminarla? (s/N): ')
                if confirmacion.lower() != 's':
                    self.stdout.write(self.style.SUCCESS('✅ Operación cancelada.'))
                    return
            
            categoria.delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f'🗑️  Categoría "{nombre_display}" eliminada exitosamente.'
                )
            )
            
        except Categoria.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ No existe una categoría con código "{codigo}".')
            )

    def mostrar_ayuda(self):
        """Muestra la ayuda del comando"""
        self.stdout.write(
            self.style.SUCCESS('\n🎯 GESTIÓN DE CATEGORÍAS - COMANDOS DISPONIBLES')
        )
        self.stdout.write('=' * 60)
        self.stdout.write('')
        self.stdout.write('📋 Listar categorías existentes:')
        self.stdout.write('   python manage.py categorias --listar')
        self.stdout.write('')
        self.stdout.write('🆕 Ver categorías disponibles para crear:')
        self.stdout.write('   python manage.py categorias --disponibles')
        self.stdout.write('')
        self.stdout.write('➕ Crear una nueva categoría:')
        self.stdout.write('   python manage.py categorias --crear <codigo>')
        self.stdout.write('   Ejemplo: python manage.py categorias --crear disparos')
        self.stdout.write('')
        self.stdout.write('📊 Ver estadísticas:')
        self.stdout.write('   python manage.py categorias --stats')
        self.stdout.write('')
        self.stdout.write('🗑️  Eliminar una categoría:')
        self.stdout.write('   python manage.py categorias --eliminar <codigo>')
        self.stdout.write('')
        self.stdout.write('💡 Usa --help para ver todas las opciones disponibles.')

# Importar models para las anotaciones
from django.db import models
