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
    "Forever in my heart ❤️",
    "Sending you hugs across the universe 🤗💖",
    "You make my heart dance 💃🩰",
    "I love you to the moon and back 🌙💖",
    "You are my everything 💞",
    "Endless love 💖💫",
    "You are magic ✨💖"
];

// Particle & Heart Classes (same as before)
class Particle { constructor(x,y,dx,dy,size,color,life){this.x=x;this.y=y;this.dx=dx;this.dy=dy;this.size=size;this.color=color;this.life=life;} update(){this.x+=this.dx;this.y+=this.dy;this.life--; } draw(){ ctx.fillStyle=this.color; ctx.beginPath(); ctx.arc(this.x,this.y,this.size,0,Math.PI*2); ctx.fill(); } }
class Heart { constructor(){this.x=Math.random()*canvas.width; this.y=Math.random()*canvas.height; this.size=Math.random()*10+8; this.speedY=Math.random()*0.7+0.3; this.opacity=Math.random()*0.4+0.4;} update(){this.y-=this.speedY; if(this.y<-this.size){this.y=canvas.height+this.size; this.x=Math.random()*canvas.width;}} draw(){ctx.fillStyle=`rgba(255,182,193,${this.opacity})`; ctx.beginPath(); ctx.moveTo(this.x,this.y); ctx.bezierCurveTo(this.x,this.y-this.size/2,this.x-this.size,this.y-this.size/2,this.x-this.size,this.y); ctx.bezierCurveTo(this.x-this.size,this.y+this.size/2,this.x,this.y+this.size/1.5,this.x,this.y+this.size); ctx.bezierCurveTo(this.x,this.y+this.size/1.5,this.x+this.size,this.y+this.size/2,this.x+this.size,this.y); ctx.bezierCurveTo(this.x+this.size,this.y-this.size/2,this.x,this.y-this.size/2,this.x,this.y); ctx.fill(); } }

// Init hearts
for(let i=0;i<40;i++){hearts.push(new Heart());}

// Mouse & Touch
let mouse={x:canvas.width/2,y:canvas.height/2};
function spawnParticles(x,y){for(let i=0;i<3;i++){particles.push(new Particle(x,y,Math.random()*2-1,Math.random()*2-1,Math.random()*3+2,`rgba(255,182,193,${Math.random()*0.5+0.5})`,50));}}
window.addEventListener('mousemove', e=>{mouse.x=e.clientX; mouse.y=e.clientY; spawnParticles(mouse.x,mouse.y);});
window.addEventListener('touchmove', e=>{mouse.x=e.touches[0].clientX; mouse.y=e.touches[0].clientY; spawnParticles(mouse.x,mouse.y);});

// Random message
function updateMessage(){document.getElementById('message').textContent=messages[Math.floor(Math.random()*messages.length)];}
setInterval(updateMessage,8000);

// Animation
function animate(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    hearts.forEach(h=>{h.update();h.draw();});
    particles.forEach((p,i)=>{p.update();p.draw();if(p.life<=0)particles.splice(i,1);});
    requestAnimationFrame(animate);
}
animate();
window.addEventListener('resize',()=>{canvas.width=window.innerWidth; canvas.height=window.innerHeight;});

// --- Discord Check-In Functionality ---
async function sendCheckin(userType){
    let msg = "";
    if(userType==="anya") msg="💌 Anya says: "+messages[Math.floor(Math.random()*messages.length)];
    else if(userType==="micheal") msg="💖 Micheal says: Sending love!";
    else msg="🌟 Someone checked in to pay respects!";
    
    try{
        await fetch("https://YOUR_BACKEND_ENDPOINT/send",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({user:userType,message:msg})
        });
        alert("Check-In sent! 💖");
    }catch(e){
        alert("Failed to send check-in 😢");
    }
}
