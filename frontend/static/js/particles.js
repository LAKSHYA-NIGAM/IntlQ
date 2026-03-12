/* ═══════════════════════════════════════════════════════════════════════════
   IntlQ — Particle Mesh Background
   Lightweight canvas-based animated particle network
   ═══════════════════════════════════════════════════════════════════════════ */

(function () {
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let w, h, particles, mouse;
    const PARTICLE_COUNT = 60;
    const MAX_DIST = 140;
    const COLORS = [
        'rgba(124, 58, 237, 0.6)',   // purple
        'rgba(59, 130, 246, 0.5)',    // blue
        'rgba(6, 182, 212, 0.5)',     // cyan
        'rgba(16, 185, 129, 0.3)',    // green
    ];

    mouse = { x: -1000, y: -1000 };

    function resize() {
        w = canvas.width = window.innerWidth;
        h = canvas.height = window.innerHeight;
    }

    function createParticles() {
        particles = [];
        for (let i = 0; i < PARTICLE_COUNT; i++) {
            particles.push({
                x: Math.random() * w,
                y: Math.random() * h,
                vx: (Math.random() - 0.5) * 0.4,
                vy: (Math.random() - 0.5) * 0.4,
                r: Math.random() * 2 + 1,
                color: COLORS[Math.floor(Math.random() * COLORS.length)],
            });
        }
    }

    function drawParticle(p) {
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();
    }

    function drawLines() {
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < MAX_DIST) {
                    const opacity = (1 - dist / MAX_DIST) * 0.15;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(124, 130, 237, ${opacity})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }

            // Mouse proximity lines
            const dx = particles[i].x - mouse.x;
            const dy = particles[i].y - mouse.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 200) {
                const opacity = (1 - dist / 200) * 0.25;
                ctx.beginPath();
                ctx.moveTo(particles[i].x, particles[i].y);
                ctx.lineTo(mouse.x, mouse.y);
                ctx.strokeStyle = `rgba(6, 182, 212, ${opacity})`;
                ctx.lineWidth = 0.8;
                ctx.stroke();
            }
        }
    }

    function update() {
        for (const p of particles) {
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0 || p.x > w) p.vx *= -1;
            if (p.y < 0 || p.y > h) p.vy *= -1;
        }
    }

    function animate() {
        ctx.clearRect(0, 0, w, h);
        update();
        drawLines();
        for (const p of particles) drawParticle(p);
        requestAnimationFrame(animate);
    }

    window.addEventListener('resize', () => { resize(); createParticles(); });
    window.addEventListener('mousemove', (e) => { mouse.x = e.clientX; mouse.y = e.clientY; });
    window.addEventListener('mouseout', () => { mouse.x = -1000; mouse.y = -1000; });

    resize();
    createParticles();
    animate();
})();
