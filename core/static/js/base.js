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
        } else {
            // Ocultar el dropdown
            notificationDropdown.style.display = 'none';
        }
    });

    // Botón para marcar notificación como leída
    const markAsReadButtons = document.querySelectorAll('.mark-read-btn');

    markAsReadButtons.forEach(button => {
        button.addEventListener('click', function() {
            const notificationId = this.getAttribute('data-id');

            // Deshabilitar el botón
            setTimeout(() => {
                button.disabled = true;
            }, 200);

            // Enviar una solicitud AJAX para marcar la notificacion como leída
            fetch(`/account/marcar-leida/${notificationId}`, {
                method: 'GET'
            })
            // Procesar la respuesta
            .then(response => {
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                if (response.ok) {
                    location.reload();
                }
            })
            .catch(error => {
                alert('Hubo un error al procesar la solicitud');
            });
        });
    });

    // Cerrar el dropdown si se hace clic fuera de él
    document.addEventListener('click', function(event) {
        if (!notificationButton.contains(event.target) && !notificationDropdown.contains(event.target)) {
            notificationDropdown.style.display = 'none';  // Ocultar el dropdown
        }
    });
});