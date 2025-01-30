document.addEventListener('DOMContentLoaded', function() {
    var passwordInput = document.querySelector('#password-input'); // Usamos querySelector
    var eyeIcon = document.querySelector('#toggle-password');

    if (passwordInput && eyeIcon) {
        // Función para mostrar u ocultar la contraseña
        function togglePassword() {
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';  // Mostrar contraseña
                eyeIcon.innerHTML = '<i class="fas fa-eye-slash"></i>';  // Cambiar icono a ojo tachado
            } else {
                passwordInput.type = 'password';  // Ocultar contraseña
                eyeIcon.innerHTML = '<i class="fas fa-eye"></i>';  // Cambiar icono a ojo normal
            }
        }

        // Evento de clic para el icono del ojo
        eyeIcon.addEventListener('click', togglePassword);

        // Función para mostrar u ocultar el icono del ojo según si hay texto
        function toggleEyeIcon() {
            eyeIcon.style.visibility = passwordInput.value.length > 0 ? 'visible' : 'hidden';
        }

        // Ocultar el icono si el campo está vacío al cargar la página
        toggleEyeIcon();
        passwordInput.addEventListener('input', toggleEyeIcon);
    }

    // Lógica para ocultar toasts después de 5 segundos
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.classList.add('toast-fade-out');
            setTimeout(() => {
                toast.remove();
            }, 500);
        }, 5000);
    });
});
