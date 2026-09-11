import os
import tempfile
import webbrowser
from pathlib import Path

# HTML, CSS, and JavaScript for the Fireworks Night application
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Fireworks Night 🎆</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      background-color: #050814;
      color: #e2e8f0;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      min-height: 100vh;
      padding: 20px;
      overflow: hidden;
    }
    header {
      text-align: center;
      margin-bottom: 10px;
    }
    h1 {
      font-size: 2.2rem;
      color: #ffffff;
      margin-bottom: 6px;
      letter-spacing: 1px;
    }
    p.subtitle {
      font-size: 1rem;
      color: #94a3b8;
    }
    .canvas-container {
      flex: 1;
      width: 100%;
      max-width: 900px;
      min-height: 450px;
      position: relative;
      margin: 15px 0;
      border-radius: 12px;
      overflow: hidden;
      background-color: #050814;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
      border: 1px solid #1e293b;
    }
    canvas {
      width: 100%;
      height: 100%;
      display: block;
      cursor: crosshair;
    }
    .controls {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 15px;
      flex-wrap: wrap;
    }
    button {
      padding: 12px 24px;
      font-size: 0.95rem;
      font-weight: 600;
      border-radius: 30px;
      border: none;
      cursor: pointer;
      transition: background-color 0.2s, transform 0.1s;
    }
    button:active {
      transform: scale(0.98);
    }
    .btn-launch {
      background-color: #3b82f6;
      color: #ffffff;
      box-shadow: 0 0 15px rgba(59, 130, 246, 0.4);
    }
    .btn-launch:hover {
      background-color: #2563eb;
    }
    .btn-clear {
      background-color: #334155;
      color: #cbd5e1;
    }
    .btn-clear:hover {
      background-color: #475569;
    }
    .counter {
      font-size: 1rem;
      color: #cbd5e1;
      margin-left: 10px;
      font-weight: 500;
    }
  </style>
</head>
<body>

  <header>
    <h1>🎆 FIREWORKS NIGHT</h1>
    <p class="subtitle">Click anywhere in the sky or use the button to launch a firework.</p>
  </header>

  <div class="canvas-container">
    <canvas id="fireworksCanvas"></canvas>
  </div>

  <div class="controls">
    <button class="btn-launch" id="launchBtn">LAUNCH FIREWORK</button>
    <button class="btn-clear" id="clearBtn">CLEAR SKY</button>
    <span class="counter">Fireworks launched: <span id="counterVal">0</span></span>
  </div>

  <script>
    const canvas = document.getElementById('fireworksCanvas');
    const ctx = canvas.getContext('2d');
    const launchBtn = document.getElementById('launchBtn');
    const clearBtn = document.getElementById('clearBtn');
    const counterVal = document.getElementById('counterVal');

    let count = 0;
    let fireworks = [];
    let particles = [];
    let stars = [];

    function resizeCanvas() {
      const container = canvas.parentElement;
      const w = container.clientWidth || 800;
      const h = container.clientHeight || 450;
      canvas.width = w;
      canvas.height = h;
      createStars();
    }

    function createStars() {
      stars = [];
      const totalStars = 90;
      for (let i = 0; i < totalStars; i++) {
        stars.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          radius: Math.random() * 1.3 + 0.5,
          alpha: Math.random() * 0.7 + 0.2
        });
      }
    }

    function launchFirework(targetX, targetY) {
      const startX = targetX || Math.random() * (canvas.width - 100) + 50;
      const startY = canvas.height;
      const endY = (targetY !== undefined) ? targetY : (Math.random() * (canvas.height * 0.65) + 40);
      const hue = Math.floor(Math.random() * 360);

      fireworks.push({
        x: startX,
        y: startY,
        startX: startX,
        startY: startY,
        targetX: targetX || startX,
        targetY: endY,
        speed: 8,
        angle: Math.atan2(endY - startY, (targetX || startX) - startX),
        hue: hue
      });

      count++;
      counterVal.textContent = count;
    }

    function createExplosion(x, y, hue) {
      const particleCount = 40;
      for (let i = 0; i < particleCount; i++) {
        const angle = (Math.PI * 2 / particleCount) * i + Math.random() * 0.5;
        const speed = Math.random() * 5 + 1;
        particles.push({
          x: x,
          y: y,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed,
          alpha: 1,
          decay: Math.random() * 0.02 + 0.015,
          hue: hue + Math.random() * 20 - 10,
          radius: Math.random() * 2 + 1
        });
      }
    }

    function animate() {
      const container = canvas.parentElement;
      if (canvas.width !== container.clientWidth || canvas.height !== container.clientHeight) {
        resizeCanvas();
      }

      ctx.fillStyle = 'rgba(5, 8, 20, 0.25)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw subtle stars across the entire canvas height (0 to canvas.height)
      stars.forEach(star => {
        ctx.fillStyle = `rgba(255, 255, 255, ${star.alpha})`;
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fill();
      });

      // Update and draw fireworks rockets
      for (let i = fireworks.length - 1; i >= 0; i--) {
        const f = fireworks[i];
        f.x += Math.cos(f.angle) * f.speed;
        f.y += Math.sin(f.angle) * f.speed;

        ctx.fillStyle = `hsl(${f.hue}, 100%, 70%)`;
        ctx.beginPath();
        ctx.arc(f.x, f.y, 2.5, 0, Math.PI * 2);
        ctx.fill();

        // Check if rocket reached target
        if (f.y <= f.targetY) {
          createExplosion(f.targetX, f.targetY, f.hue);
          fireworks.splice(i, 1);
        }
      }

      // Update and draw particles
      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];
        p.vx *= 0.96;
        p.vy *= 0.96;
        p.vy += 0.06; // Gravity
        p.x += p.vx;
        p.y += p.vy;
        p.alpha -= p.decay;

        if (p.alpha <= 0) {
          particles.splice(i, 1);
          continue;
        }

        ctx.fillStyle = `hsla(${p.hue}, 100%, 65%, ${p.alpha})`;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx.fill();
      }

      requestAnimationFrame(animate);
    }

    // Event Listeners
    canvas.addEventListener('click', (e) => {
      const rect = canvas.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      launchFirework(x, y);
    });

    launchBtn.addEventListener('click', () => {
      const x = Math.random() * (canvas.width - 100) + 50;
      const y = Math.random() * (canvas.height * 0.65) + 40;
      launchFirework(x, y);
    });

    clearBtn.addEventListener('click', () => {
      fireworks = [];
      particles = [];
      count = 0;
      counterVal.textContent = '0';
      ctx.fillStyle = '#050814';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    });

    window.addEventListener('resize', resizeCanvas);

    // Initial setup
    resizeCanvas();
    animate();
  </script>
</body>
</html>
"""

# Create a temporary HTML file
temp_dir = tempfile.gettempdir()
html_path = os.path.join(temp_dir, "fireworks_night.html")

with open(html_path, "w", encoding="utf-8") as file:
    file.write(HTML_CONTENT)

# Open the fireworks in the default browser
webbrowser.open(Path(html_path).as_uri())
