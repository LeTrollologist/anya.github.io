const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

let particles = [];
let hearts = [];
let messages = [
    "I love you mostest times infinity times perpetuity 💖",
    "I love you more than chocos 🍫💖",
    "You are my sun, moon, and stars 🌞🌙✨",
    "Forever in my heart, always ❤️",
    "Sending you hugs across the universe 🤗💖",
    "You make my heart dance 💃🩰",
    "I love you to the moon and back 🌙💖",
    "You are my everything 💞",
    "Endless love for you 💖💫",
    "You are magic in my life ✨💖"
];

function random(min, max) { return Math.random() * (max - min) + min; }

// Particle class
class Particle {
    constructor(x, y, dx, dy, size, color, life) {
        this.x = x;
        this.y = y;
        this.dx = dx;
        this.dy = dy;
        this.size = size;
        this.color = color;
        this.life = life;
    }
    update() {
        this.x += this.dx;
        this.y += this.dy;
        this.life -= 1;
    }
    draw() {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

// Heart class
class Heart {
    constructor() {
        this.x = random(0, canvas.width);
        this.y = random(0, canvas.height);
        this.size = random(8, 18);
        this.speedY = random(0.3, 1);
        this.opacity = random(0.4, 0.8);
    }
    update() {
        this.y -= this.speedY;
        if (this.y < -this.size) {
            this.y = canvas.height + this.size;
            this.x = random(0, canvas.width);
        }
    }
    draw() {
        ctx.fillStyle = `rgba(255,182,193,${this.opacity})`;
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.bezierCurveTo(this.x, this.y - this.size / 2, this.x - this.size, this.y - this.size / 2, this.x - this.size, this.y);
        ctx.bezierCurveTo(this.x - this.size, this.y + this.size / 2, this.x, this.y + this.size / 1.5, this.x, this.y + this.size);
        ctx.bezierCurveTo(this.x, this.y + this.size / 1.5, this.x + this.size, this.y + this.size / 2, this.x + this.size, this.y);
        ctx.bezierCurveTo(this.x + this.size, this.y - this.size / 2, this.x, this.y - this.size / 2, this.x, this.y);
        ctx.fill();
    }
}

// Initialize hearts
for (let i = 0; i < 40; i++) {
    hearts.push(new Heart());
}

// Mouse interaction
let mouse = {x: canvas.width/2, y: canvas.height/2};
window.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
    for (let i = 0; i < 3; i++) {
        particles.push(new Particle(mouse.x, mouse.y, random(-1,1), random(-1,1), random(2,5), `rgba(255,182,193,${random(0.5,1)})`, 50));
    }
});

// Touch for mobile
window.addEventListener('touchmove', (e) => {
    mouse.x = e.touches[0].clientX;
    mouse.y = e.touches[0].clientY;
    for (let i = 0; i < 3; i++) {
        particles.push(new Particle(mouse.x, mouse.y, random(-1,1), random(-1,1), random(2,5), `rgba(255,182,193,${random(0.5,1)})`, 50));
    }
});

// Random loving messages
function updateMessage() {
    const msg = messages[Math.floor(Math.random() * messages.length)];
    document.getElementById('message').textContent = msg;
}
setInterval(updateMessage, 8000);

// Animation loop
function animate() {
    ctx.clearRect(0,0,canvas.width,canvas.height);

    // Draw hearts
    hearts.forEach(h => { h.update(); h.draw(); });

    // Draw particles
    particles.forEach((p, index) => {
        p.update();
        p.draw();
        if (p.life <= 0) particles.splice(index,1);
    });

    requestAnimationFrame(animate);
}

animate();

// Responsive
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});
