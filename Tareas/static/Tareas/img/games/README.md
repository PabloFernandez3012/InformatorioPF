# Imágenes de Juegos

Esta carpeta contiene las imágenes que se pueden asignar a los juegos en el sistema.

## Cómo agregar nuevas imágenes

1. **Coloca tu imagen** en esta carpeta: `Tareas/static/Tareas/img/games/`

2. **Formatos soportados:**
   - PNG (.png)
   - JPEG (.jpg, .jpeg)
   - GIF (.gif)
   - WebP (.webp)
   - SVG (.svg)

3. **Recomendaciones:**
   - Tamaño recomendado: 300x400 píxeles
   - Nombres descriptivos: `minecraft.jpg`, `fifa2024.png`, etc.
   - Sin espacios en el nombre del archivo (usa guiones: `grand-theft-auto-v.jpg`)

4. **Uso en el admin:**
   - Ve al panel de administración Django
   - Edita un juego
   - Selecciona la imagen del menú desplegable
   - La imagen aparecerá automáticamente en la lista

## Imágenes disponibles

- `placeholder-game.svg` - Imagen genérica para juegos sin imagen específica
- `minecraft.svg` - Placeholder para Minecraft
- `fifa2024.svg` - Placeholder para FIFA 2024
- `gta5.svg` - Placeholder para Grand Theft Auto V

## Nota

Después de agregar nuevas imágenes, es posible que necesites reiniciar el servidor de desarrollo para que aparezcan en el menú desplegable del admin.
