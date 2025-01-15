// Cerrar los toasts después de 3 segundos
document.addEventListener('DOMContentLoaded', function() {
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.classList.add('toast-fade-out');
            setTimeout(() => {
                toast.remove();
            }, 500);
        }, 3000);
    });

    const notificationButton = document.getElementById('notificationButton');
    const notificationCount = document.getElementById('notificationCount');
    const notificationDropdown = document.getElementById('notificationDropdown');

    // Inicialización del contador de notificaciones al cargar la página
    const initialCount = parseInt(notificationCount.textContent);
    if (initialCount > 0) {
        notificationCount.style.display = 'inline-flex';  // Mostrar el contador
    } else {
        notificationCount.style.display = 'none';  // Ocultar el contador
    }

    // Manejo de visibilidad del dropdown de notificaciones
    notificationButton.addEventListener('click', function() {
        // Verificar si el dropdown está oculto
        if (notificationDropdown.style.display === 'none' || notificationDropdown.style.display === '') {
            // Mostrar el dropdown
            notificationDropdown.style.display = 'block';

            // Ocultar el contador si tiene notificaciones
            if (parseInt(notificationCount.textContent) > 0) {
                notificationCount.style.display = 'none';
            }
        } else {
            // Ocultar el dropdown
            notificationDropdown.style.display = 'none';
        }
    });

    // Cerrar el dropdown si se hace clic fuera de él
    document.addEventListener('click', function(event) {
        if (!notificationButton.contains(event.target) && !notificationDropdown.contains(event.target)) {
            notificationDropdown.style.display = 'none';  // Ocultar el dropdown
        }
    });
});