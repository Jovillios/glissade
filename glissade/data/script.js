const slides = document.querySelectorAll('.slide');
const navLinks = document.querySelectorAll('.nav-link');
let currentSlide = 0;

// Fonction pour afficher une slide
function showSlide(index) {
    slides.forEach(slide => slide.classList.remove('active'));
    navLinks.forEach(link => link.classList.remove('active'));
    slides[index].classList.add('active');
    navLinks[index].classList.add('active');
    currentSlide = index;
}

// Navigation via les liens
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const slideIndex = parseInt(link.getAttribute('data-slide'));
        showSlide(slideIndex);
    });
});

// Navigation clavier
document.addEventListener('keydown', (e) => {
    if ((e.key === 'ArrowRight' || e.key.toLowerCase() === 'l' ) && currentSlide < slides.length - 1) {
        showSlide(currentSlide + 1);
    } else if ((e.key === 'ArrowLeft' || e.key.toLowerCase() === 'h' ) && currentSlide > 0) {
        showSlide(currentSlide - 1);
    }
});
