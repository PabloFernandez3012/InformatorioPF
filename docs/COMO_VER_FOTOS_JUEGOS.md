# 📸 CÓMO VER LAS FOTOS DE LOS JUEGOS

## 🚀 Para acceder a la página de juegos con imágenes:

1. **Inicia el servidor Django:**
   ```bash
   cd "c:\Users\Pablo\OneDrive\Escritorio\ProyectoDjango"
   python manage.py runserver
   ```

2. **Ve a tu navegador y accede a:**
   - **Página principal de juegos:** http://127.0.0.1:8000/tareas/
   - **Vista de un juego específico:** http://127.0.0.1:8000/juego/1/
   
3. **También puedes usar la navegación:**
   - En la barra de navegación superior verás el enlace **"🎮 Juegos"**
   - Haz clic en ese enlace para ver la vista moderna con imágenes

## 📁 Para agregar fotos a los juegos:

1. **Ve al panel de administración:** http://127.0.0.1:8000/admin/
2. **Inicia sesión como superusuario**
3. **Ve a "Juegos" y edita cualquier juego**
4. **Sube una imagen en el campo "Imagen"**
5. **Guarda el juego**

## 🎨 Características de la nueva vista:

- ✅ **Diseño moderno** con Tailwind CSS integrado
- ✅ **Imágenes responsivas** para cada juego
- ✅ **Gradientes y animaciones** elegantes
- ✅ **Fallback placeholder** si no hay imagen
- ✅ **Grid layout** adaptable
- ✅ **Hover effects** interactivos
- ✅ **Búsqueda y filtros** mejorados
- ✅ **Paginación moderna**

## 📸 Dónde se guardan las imágenes:

Las imágenes se guardan en: `media/juegos/`

## 🔧 URLs disponibles:

- **Juegos:** `/tareas/` 
- **Detalle:** `/juego/<id>/`
- **Admin:** `/admin/`

¡Disfruta de tu nueva galería de juegos con imágenes modernas! 🎮✨
