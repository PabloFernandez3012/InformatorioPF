# 🎮 Sistema de Gestión de Juegos con Reseñas

Un sistema web desarrollado en Django que permite gestionar una colección de videojuegos con sistema de reseñas y puntuaciones.

## 📋 Características

- ✅ **Gestión de Juegos**: Agregar, visualizar y categorizar videojuegos
- ✅ **Sistema de Reseñas**: Los usuarios pueden escribir reseñas y calificar juegos
- ✅ **Autenticación**: Registro e inicio de sesión de usuarios
- ✅ **Búsqueda y Filtros**: Buscar juegos por nombre, categoría, estudio y año
- ✅ **Puntuaciones**: Sistema de estrellas con promedio automático
- ✅ **Interfaz Moderna**: Diseño responsive con navegación intuitiva

## 🛠️ Tecnologías

- **Backend**: Django 5.2.4
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Frontend**: HTML5, CSS3, JavaScript
- **Python**: 3.8+

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd ProyectoDjango
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
# Instalación básica
pip install -r requirements.txt

# Para desarrollo (incluye herramientas adicionales)
pip install -r requirements-dev.txt

# Para producción
pip install -r requirements-prod.txt
```

### 5. Configurar base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

### 7. Ejecutar servidor de desarrollo
```bash
python manage.py runserver
```

## 📁 Estructura del Proyecto

```
ProyectoDjango/
├── Djangocrud/          # Configuración principal del proyecto
├── Tareas/              # Aplicación principal (Juegos)
│   ├── models.py        # Modelos: Juego, Categoria, Resena
│   ├── views.py         # Vistas del sistema
│   ├── forms.py         # Formularios personalizados
│   ├── urls.py          # URLs de la aplicación
│   └── templates/       # Templates HTML
├── static/              # Archivos estáticos (CSS, JS, imágenes)
├── media/               # Archivos subidos por usuarios
├── requirements.txt     # Dependencias básicas
├── requirements-dev.txt # Dependencias de desarrollo
├── requirements-prod.txt# Dependencias de producción
└── manage.py           # Comando principal de Django
```

## 🎯 Uso

### Para Usuarios
1. **Registrarse**: Crear una cuenta nueva
2. **Explorar Juegos**: Ver la lista de juegos disponibles
3. **Buscar**: Usar la función de búsqueda con filtros
4. **Escribir Reseñas**: Calificar y comentar juegos (requiere login)
5. **Ver Detalles**: Información completa de cada juego

### Para Administradores
1. Acceder al panel de administración: `/admin/`
2. Agregar nuevos juegos y categorías
3. Moderar reseñas de usuarios
4. Gestionar usuarios del sistema

## 🔧 Configuración

### Variables de Entorno (Producción)
Crear un archivo `.env` con:
```
SECRET_KEY=tu-clave-secreta-aquí
DEBUG=False
ALLOWED_HOSTS=tu-dominio.com
DATABASE_URL=postgresql://usuario:password@host:puerto/basedatos
```

### Base de Datos
- **Desarrollo**: SQLite (incluido)
- **Producción**: PostgreSQL recomendado

## 📊 Modelos Principales

### Juego
- Nombre, estudio, descripción
- Fecha de publicación
- Categorías (many-to-many)
- Métodos para cálculo de puntuaciones

### Categoría
- Tipos predefinidos (Acción, RPG, Estrategia, etc.)
- Relación many-to-many con juegos

### Reseña
- Usuario, juego, puntuación (1-5)
- Comentario y fecha
- Una reseña por usuario por juego

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit los cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo `LICENSE` para detalles.

## 👨‍💻 Autor

**Pablo** - Proyecto Django de Gestión de Juegos

## 📞 Soporte

Si tienes problemas o preguntas:
1. Revisa la documentación de Django
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de que el entorno virtual esté activado
4. Ejecuta las migraciones si hay cambios en modelos
