const heroSection = document.getElementById('hero');
const animateBtn = document.getElementById('animate-btn');

animateBtn.addEventListener('click', () => {
  heroSection.classList.add('animate');
  setTimeout(() => {
    heroSection.classList.remove('animate');
  }, 500);
});