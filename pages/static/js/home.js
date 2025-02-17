document.addEventListener('DOMContentLoaded', function() {
    // Código existente del menú móvil
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const sidebar = document.querySelector('.sidebar');

    mobileMenuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('show');
    });

    // Nuevo código para el efecto flip
    const featureCards = document.querySelectorAll('.feature-card');

    featureCards.forEach(card => {
        const viewBtn = card.querySelector('#feature-btn');
        const closeBtn = card.querySelector('#feature-btn-close');
        const video = card.querySelector('.feature-video');

        viewBtn.addEventListener('click', () => {
            card.classList.add('flipped');
            // Reproducir el video cuando se voltea la card
            if (video) {
                video.play();
            }
        });

        closeBtn.addEventListener('click', () => {
            card.classList.remove('flipped');
            // Pausar el video cuando se cierra
            if (video) {
                video.pause();
                video.currentTime = 0;
            }
        });
    });
});