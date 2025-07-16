# 📁 Carpeta de Imágenes - Proyecto Django Gaming

Esta carpeta contiene todas las imágenes y recursos multimedia utilizados en el proyecto.

## 📂 Estructura de la Carpeta

```
img/
├── logos/          # Logos del sitio y marcas
├── games/          # Imágenes de portadas de juegos
├── avatars/        # Avatares de usuarios
├── banners/        # Banners promocionales
├── icons/          # Iconos del sitio
└── backgrounds/    # Imágenes de fondo
```

## 🖼️ Tipos de Imágenes Recomendadas

### **Logos**
- Formato: PNG con transparencia
- Tamaño: 200x200px (logos cuadrados)
- Peso: Máximo 50KB

### **Portadas de Juegos**
- Formato: JPG o PNG
- Tamaño: 400x600px (proporción 2:3)
- Peso: Máximo 200KB

### **Banners**
- Formato: JPG
- Tamaño: 1200x300px
- Peso: Máximo 300KB

### **Iconos**
- Formato: PNG con transparencia
- Tamaño: 32x32px, 64x64px
- Peso: Máximo 10KB

## 🔧 Cómo Usar las Imágenes en Templates

### **1. Cargar archivos estáticos**
```html
{% load static %}
```

### **2. Usar imágenes**
```html
<!-- Logo del sitio -->
<img src="{% static 'Tareas/img/logos/logo.png' %}" alt="Logo">

<!-- Portada de juego -->
<img src="{% static 'Tareas/img/games/cyberpunk2077.jpg' %}" alt="Cyberpunk 2077">

<!-- Icono -->
<img src="{% static 'Tareas/img/icons/star.png' %}" alt="Estrella">
```

## 📋 Convenciones de Nombres

- **Minúsculas**: Todos los nombres en minúsculas
- **Sin espacios**: Usar guiones o guiones bajos
- **Descriptivo**: Nombres que describan el contenido

### **Ejemplos Correctos:**
- `logo-principal.png`
- `the-witcher-3.jpg`
- `avatar-default.png`
- `banner-ofertas.jpg`

### **Ejemplos Incorrectos:**
- `Logo Principal.PNG`
- `THE WITCHER 3.JPG`
- `img1.png`
- `banner ofertas.jpg`

## 🚀 Optimización de Imágenes

### **Herramientas Recomendadas:**
- **TinyPNG**: Para comprimir PNG y JPG
- **ImageOptim**: Para optimización general
- **GIMP**: Para edición avanzada
- **Canva**: Para crear banners y gráficos

### **Consejos:**
1. **Comprime las imágenes** antes de subirlas
2. **Usa formatos apropiados**: PNG para transparencias, JPG para fotos
3. **Redimensiona** a los tamaños necesarios
4. **Usa lazy loading** para imágenes grandes

## 📱 Responsive Images

### **Múltiples Tamaños:**
```html
<img src="{% static 'Tareas/img/games/game-large.jpg' %}" 
     srcset="{% static 'Tareas/img/games/game-small.jpg' %} 480w,
             {% static 'Tareas/img/games/game-medium.jpg' %} 768w,
             {% static 'Tareas/img/games/game-large.jpg' %} 1200w"
     sizes="(max-width: 480px) 480px,
            (max-width: 768px) 768px,
            1200px"
     alt="Descripción del juego">
```

## 🔒 Derechos de Autor

- **Solo usar imágenes libres** de derechos o con licencia apropiada
- **Fuentes recomendadas**: Unsplash, Pixabay, Pexels
- **Citar la fuente** cuando sea necesario
- **Respetar las licencias** Creative Commons

---

**📝 Nota**: Recuerda ejecutar `python manage.py collectstatic` en producción para recopilar todos los archivos estáticos.
