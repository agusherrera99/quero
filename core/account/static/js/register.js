// Asignar el valor del email al campo username
document.getElementById('id_email').addEventListener('input', function() {
    var email = this.value;
    var username = email.split('@')[0]; // Obtener la parte antes del '@'
    document.getElementById('username').value = username; // Asignar al campo username
});