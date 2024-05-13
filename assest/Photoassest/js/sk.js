// Огненные звезды
function drawStars(num) {
    for (var i = 0; i < num; i++) {
        var x = Math.random() * window.innerWidth;
        var y = Math.random() * window.innerHeight;
        var star = document.createElement('div');
        star.style.left = x + 'px';
        star.style.top = y + 'px';
        star.style.width = '5px';
        star.style.height = '5px';
        star.style.backgroundColor = 'rgba(255, 255, 0, 0.5)';
        star.style.position = 'absolute';
        star.style.boxShadow = '0 0 20px rgba(255, 255, 0, 0.5)';
        document.body.appendChild(star);
    }
}
// Вызов функций
drawStars(50);
setInterval(drawClock, 1000);