import { GAME_CONFIG } from '/src/utils/Constants.js';

export class Hazard {
    constructor(type, x, y, assets) {
        this.type = type;
        this.x = x;
        this.y = y;
        this.assets = assets;
        this.active = true;
        this.sway = 0;

        this.vx = (Math.random() - 0.5) * 2;
        this.vy = 1 + Math.random() * 2;
        this.rotation = Math.random() * Math.PI * 2;
        this.rotSpeed = (Math.random() - 0.5) * 0.1;
        this.scale = 0.5 + Math.random() * 0.5;

        // Type specifics
        if (type === 'leaf') {
            this.vy = 0.5 + Math.random();
            this.sway = Math.random() * Math.PI * 2;
        } else if (type === 'star') {
            this.vy = 5 + Math.random() * 3;
        }
    }

    update(deltaTime, environment) {
        if (!this.active) return;

        // Apply environment physics
        if (environment) {
            this.vx += environment.windX * 0.05;
            // Gravity affects vy
            this.vy += (environment.gravityY - 1) * 0.1;
        }

        this.x += this.vx * (deltaTime / 16);
        this.y += this.vy * (deltaTime / 16);
        this.rotation += this.rotSpeed * (deltaTime / 16);

        // Leaf sway (if applicable)
        if (this.type === 'leaf') {
            this.sway += 0.05;
            this.x += Math.sin(this.sway) * 0.5;
        }

        // Check bounds
        if (this.y > GAME_CONFIG.HEIGHT + 50 || this.x < -100 || this.x > GAME_CONFIG.WIDTH + 100) {
            this.active = false;
        }
    }

    draw(ctx) {
        if (!this.active) return;

        const img = this.assets.get(`hazard_${this.type}`);

        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        ctx.scale(this.scale, this.scale);

        if (img) {
            ctx.drawImage(img, -20, -20, 40, 40);
        } else {
            // Fallback
            ctx.fillStyle = this.type === 'leaf' ? '#e67e22' :
                this.type === 'star' ? '#f1c40f' : '#e74c3c';
            ctx.beginPath();
            if (this.type === 'leaf') {
                ctx.ellipse(0, 0, 15, 8, 0, 0, Math.PI * 2);
            } else {
                ctx.arc(0, 0, 10, 0, Math.PI * 2);
            }
            ctx.fill();
        }

        ctx.restore();
    }
}
