/* =============================================================================
   JAVASCRIPT PRINCIPAL PARA EL PROYECTO DE VIDEOJUEGOS
   =============================================================================
   Este archivo contiene todas las funciones JavaScript para mejorar la
   interactividad y experiencia de usuario de la aplicación.
*/

// =============================================================================
// INICIALIZACIÓN AL CARGAR LA PÁGINA
// =============================================================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('🎮 Proyecto Django Gaming - JavaScript cargado correctamente');
    
    // Inicializar funcionalidades
    initializeNewsCards();
    initializeFormValidation();
    initializeSearchToggle();
    initializeLazyLoading();
});

// =============================================================================
// FUNCIONALIDADES PARA CARDS DE NOTICIAS
// =============================================================================
function initializeNewsCards() {
    const noticiasCards = document.querySelectorAll('article[onclick], .noticia-card');
    
    noticiasCards.forEach(card => {
        // Agregar indicadores de teclado para accesibilidad
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', 'Abrir noticia en nueva pestaña');
        
        // Manejar navegación por teclado
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const url = this.getAttribute('onclick')?.match(/'([^']+)'/)?.[1] || 
                           this.getAttribute('data-url');
                if (url) {
                    window.open(url, '_blank');
                }
            }
        });
        
        // Feedback visual mejorado
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.boxShadow = '0 8px 30px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 5px 20px rgba(0,0,0,0.1)';
        });
        
        // Efecto al hacer click
        card.addEventListener('mousedown', function() {
            this.style.transform = 'translateY(-2px) scale(0.98)';
        });
        
        card.addEventListener('mouseup', function() {
            this.style.transform = 'translateY(-5px) scale(1)';
        });
    });
}

// =============================================================================
// TOGGLE PARA FORMULARIO DE BÚSQUEDA
// =============================================================================
function initializeSearchToggle() {
    // Función global para compatibilidad con onclick en HTML
    window.toggleFormularioBusqueda = function() {
        const formulario = document.getElementById('formularioBusqueda');
        const boton = document.getElementById('toggleBusqueda');
        
        if (formulario) {
            const isVisible = formulario.style.display === 'block';
            
            if (isVisible) {
                formulario.style.display = 'none';
                if (boton) boton.textContent = '🔍';
                if (boton) boton.setAttribute('title', 'Mostrar búsqueda');
            } else {
                formulario.style.display = 'block';
                if (boton) boton.textContent = '❌';
                if (boton) boton.setAttribute('title', 'Ocultar búsqueda');
                
                // Animar la aparición
                formulario.style.opacity = '0';
                formulario.style.transform = 'translateY(-20px)';
                
                setTimeout(() => {
                    formulario.style.transition = 'all 0.3s ease';
                    formulario.style.opacity = '1';
                    formulario.style.transform = 'translateY(0)';
                }, 10);
            }
        }
    };
}

// =============================================================================
// VALIDACIÓN DE FORMULARIOS
// =============================================================================
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');
            
            // Limpiar mensajes de error previos
            const errorMessages = form.querySelectorAll('.error-message');
            errorMessages.forEach(msg => msg.remove());
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    showFieldError(field, 'Este campo es obligatorio');
                }
            });
            
            // Validación específica para emails
            const emailFields = form.querySelectorAll('input[type="email"]');
            emailFields.forEach(field => {
                if (field.value && !isValidEmail(field.value)) {
                    isValid = false;
                    showFieldError(field, 'Ingresa un email válido');
                }
            });
            
            // Validación de contraseñas
            const passwordFields = form.querySelectorAll('input[type="password"]');
            if (passwordFields.length === 2) {
                const [pass1, pass2] = passwordFields;
                if (pass1.value !== pass2.value) {
                    isValid = false;
                    showFieldError(pass2, 'Las contraseñas no coinciden');
                }
            }
            
            if (!isValid) {
                e.preventDefault();
                // Scroll al primer error
                const firstError = form.querySelector('.error-message');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    });
}

function showFieldError(field, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message alert alert-error';
    errorDiv.style.marginTop = '5px';
    errorDiv.style.fontSize = '14px';
    errorDiv.textContent = message;
    
    field.style.borderColor = '#dc3545';
    field.parentNode.appendChild(errorDiv);
    
    // Remover error al empezar a escribir
    field.addEventListener('input', function() {
        this.style.borderColor = '#e9ecef';
        const errorMsg = this.parentNode.querySelector('.error-message');
        if (errorMsg) errorMsg.remove();
    }, { once: true });
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// =============================================================================
// LAZY LOADING PARA IMÁGENES
// =============================================================================
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                observer.unobserve(img);
                
                // Agregar clase de animación
                img.classList.add('fade-in');
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// =============================================================================
// UTILIDADES GENERALES
// =============================================================================

// Función para mostrar notificaciones toast
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast alert alert-${type}`;
    toast.style.position = 'fixed';
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.style.minWidth = '300px';
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    // Animar entrada
    setTimeout(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(0)';
    }, 10);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Función para confirmar acciones destructivas
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Función para formatear fechas
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Función para truncar texto
function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// =============================================================================
// FUNCIONES PARA MEJORAR LA EXPERIENCIA DEL USUARIO
// =============================================================================

// Smooth scroll para enlaces ancla
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Indicador de carga para formularios
function addLoadingToForm(form) {
    form.addEventListener('submit', function() {
        const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Cargando...';
            submitBtn.style.opacity = '0.7';
        }
    });
}

// Aplicar a todos los formularios
document.querySelectorAll('form').forEach(addLoadingToForm);

console.log('✅ JavaScript inicializado correctamente');
