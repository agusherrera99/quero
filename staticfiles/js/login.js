var passwordInput = document.getElementById('password-input');
var eyeIcon = document.getElementById('toggle-password');

// Función para mostrar u ocultar la contraseña
function togglePassword() {
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';  // Mostrar la contraseña
        eyeIcon.innerHTML = '<i class="fas fa-eye-slash"></i>';  // Cambiar el icono a ojo tachado
    } else {
        passwordInput.type = 'password';  // Ocultar la contraseña
        eyeIcon.innerHTML = '<i class="fas fa-eye"></i>';  // Cambiar el icono a ojo
    }
}

// Función para mostrar u ocultar el ícono de ojo
function toggleEyeIcon() {
    if (passwordInput.value.length > 0) {
        eyeIcon.style.visibility = 'visible';  // Mostrar el ícono cuando hay texto
    } else {
        eyeIcon.style.visibility = 'hidden';  // Ocultar el ícono cuando no hay texto
    }
}

// Llamado a la función para mostrar u ocultar el ícono al escribir en el campo
passwordInput.addEventListener('input', toggleEyeIcon);

// Oculta el ícono al cargar la página si no hay texto en el campo
toggleEyeIcon();