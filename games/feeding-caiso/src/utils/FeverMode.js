import { GAME_CONFIG, FEVER_CONFIG } from '/src/utils/Constants.js';

export class FeverMode {
    constructor() {
        this.gauge = 0;
        this.maxGauge = FEVER_CONFIG.gaugeMax || 100; // Default if missing
        this.active = false;
        this.duration = FEVER_CONFIG.duration;
        this.timer = 0;
        this.screenFlash = 0;
        this.particles = [];
    }

    charge(amount) {
        if (this.active) return;
        this.gauge = Math.min(this.maxGauge, this.gauge + amount);
        if (this.gauge >= this.maxGauge) {
            this.activate();
        }
    }

    activate() {
        this.active = true;
        this.timer = this.duration;
        this.screenFlash = 1;

        // Burst particles
        for (let i = 0; i < 40; i++) {
            this.particles.push(this.createParticle());
        }
    }

    createParticle() {
        const colors = ['#ff006e', '#fb5607', '#ffbe0b', '#8338ec', '#00f5d4'];
        return {
            x: Math.random() * GAME_CONFIG.WIDTH,
            y: Math.random() * GAME_CONFIG.HEIGHT * 0.6,
            vx: (Math.random() - 0.5) * 12,
            vy: (Math.random() - 0.5) * 12,
            size: Math.random() * 12 + 6,
            color: colors[Math.floor(Math.random() * colors.length)],
            life: 800 + Math.random() * 400
        };
    }

    update(deltaTime) {
        if (this.active) {
            this.timer -= deltaTime;
            if (this.timer <= 0) {
                this.deactivate();
            }
            // Continuous particle emission
            if (Math.random() < 0.4) {
                this.particles.push(this.createParticle());
            }
        }

        // Update particles
        this.particles = this.particles.filter(p => {
            p.x += p.vx * deltaTime * 0.05;
            p.y += p.vy * deltaTime * 0.05;
            p.vy += 0.1;
            p.life -= deltaTime;
            p.size *= 0.995;
            return p.life > 0;
        });

        // Fade screen flash
        if (this.screenFlash > 0) {
            this.screenFlash -= deltaTime * 0.003;
        }
    }

    deactivate() {
        this.active = false;
        this.gauge = 0;
    }

    draw(ctx) {
        // Screen flash
        if (this.screenFlash > 0) {
            ctx.fillStyle = `rgba(255, 0, 110, ${this.screenFlash * 0.25})`;
            ctx.fillRect(0, 0, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT);
        }

        // Particles
        this.particles.forEach(p => {
            ctx.globalAlpha = Math.min(1, p.life / 400);
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.globalAlpha = 1;
    }

    drawGauge(ctx) {
        const x = GAME_CONFIG.WIDTH - 35;
        const y = 80;
        const height = 180;
        const width = 18;

        // Background
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
        ctx.beginPath();
        // Check for roundRect support or fallback
        if (ctx.roundRect) {
            ctx.roundRect(x - 2, y - 2, width + 4, height + 4, 8);
        } else {
            ctx.rect(x - 2, y - 2, width + 4, height + 4);
        }
        ctx.fill();

        // Fill
        const fillHeight = (this.gauge / this.maxGauge) * height;
        const gradient = ctx.createLinearGradient(x, y + height, x, y);
        gradient.addColorStop(0, '#ff006e');
        gradient.addColorStop(0.5, '#fb5607');
        gradient.addColorStop(1, '#ffbe0b');

        ctx.fillStyle = gradient;
        ctx.beginPath();
        if (ctx.roundRect) {
            ctx.roundRect(x, y + height - fillHeight, width, fillHeight, 6);
        } else {
            ctx.rect(x, y + height - fillHeight, width, fillHeight);
        }
        ctx.fill();

        // Border
        ctx.strokeStyle = this.active ? '#fff' : 'rgba(255, 255, 255, 0.4)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        if (ctx.roundRect) {
            ctx.roundRect(x - 2, y - 2, width + 4, height + 4, 8);
        } else {
            ctx.rect(x - 2, y - 2, width + 4, height + 4);
        }
        ctx.stroke();

        // "FEVER" text when active
        if (this.active) {
            ctx.save();
            ctx.translate(x + width / 2, y + height / 2);
            ctx.rotate(-Math.PI / 2);
            ctx.fillStyle = '#fff';
            ctx.font = 'bold 14px Fredoka One';
            ctx.textAlign = 'center';
            ctx.fillText('FEVER!', 0, 5);
            ctx.restore();
        }
    }

    getMultiplier() {
        return this.active ? FEVER_CONFIG.scoreMultiplier : 1;
    }

    isMagnetActive() {
        return this.active;
    }
}
