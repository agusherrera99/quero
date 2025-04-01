document.addEventListener('DOMContentLoaded', function() {
    // menú móvil
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const sidebar = document.querySelector('.sidebar');

    mobileMenuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('show');
    });
});