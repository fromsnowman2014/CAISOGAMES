import { GAME_CONFIG } from '../utils/Constants.js';

export class Hazard {
    constructor(type, x, y, assets) {
        this.type = type;
        this.x = x;
        this.y = y;
        this.assets = assets;
        this.active = true;
        this.sway = 0;
        this.timer = 0;

        this.vx = (Math.random() - 0.5) * 2;
        this.vy = 1 + Math.random() * 2;
        this.rotation = Math.random() * Math.PI * 2;
        this.rotSpeed = (Math.random() - 0.5) * 0.1;
        this.scale = 0.5 + Math.random() * 0.5;

        // Type-specific initialization
        this._initType();
    }

    _initType() {
        switch (this.type) {
            case 'acid_drop':
                this.vy = 1.5 + Math.random() * 1.5;
                this.vx = (Math.random() - 0.5) * 0.5;
                this.color = '#2ecc71';
                this.glowColor = 'rgba(46, 204, 113, 0.4)';
                break;
            case 'exploding_spore':
                this.vy = 0.8 + Math.random();
                this.sway = Math.random() * Math.PI * 2;
                this.color = '#a29bfe';
                this.scale = 0.6 + Math.random() * 0.3;
                break;
            case 'rain_gust':
                this.vy = 3 + Math.random() * 2;
                this.vx = 1 + Math.random();
                this.color = 'rgba(150, 180, 220, 0.6)';
                this.scale = 0.3;
                break;
            case 'crystal_beam':
                this.vy = 6 + Math.random() * 3;
                this.vx = 0;
                this.color = '#e6a0ff';
                this.scale = 0.4;
                break;
            case 'mimic':
                this.vy = 1 + Math.random() * 1.5;
                this.color = '#74b9ff';
                this.shimmer = 0;
                break;
            case 'ash_gust':
                this.vy = 0.5 + Math.random();
                this.color = '#dfe6e9';
                this.scale = 0.3 + Math.random() * 0.3;
                break;
            case 'void_tendril':
                this.x = Math.random() * GAME_CONFIG.WIDTH;
                this.y = GAME_CONFIG.HEIGHT + 20;
                this.vy = -(2 + Math.random() * 2);
                this.vx = 0;
                this.color = '#0f0f1b';
                this.scale = 0.8;
                break;
            case 'buzzsaw':
                this.y = 200 + Math.random() * 400;
                this.x = -40;
                this.vx = 3 + Math.random() * 2;
                this.vy = 0;
                this.rotSpeed = 0.3;
                this.color = '#b2bec3';
                this.scale = 0.8;
                break;
            case 'infection_rain':
                this.vy = 4 + Math.random() * 3;
                this.vx = (Math.random() - 0.5) * 2;
                this.color = '#ff9500';
                this.scale = 0.4 + Math.random() * 0.3;
                break;
            case 'light_beam':
                this.vy = 8;
                this.vx = 0;
                this.color = '#ffd700';
                this.scale = 0.5;
                break;
            default:
                this.vy = 1 + Math.random() * 2;
                this.color = '#636e72';
        }
    }

    update(deltaTime, environment) {
        if (!this.active) return;
        this.timer += deltaTime;

        if (environment) {
            this.vx += environment.windX * 0.05;
            this.vy += (environment.gravityY - 1) * 0.1;
        }

        this.x += this.vx * (deltaTime / 16);
        this.y += this.vy * (deltaTime / 16);
        this.rotation += this.rotSpeed * (deltaTime / 16);

        // Type-specific updates
        if (this.type === 'exploding_spore') {
            this.sway += 0.05;
            this.x += Math.sin(this.sway) * 0.8;
        } else if (this.type === 'mimic') {
            this.shimmer = Math.sin(this.timer * 0.01) * 2;
        }

        // Bounds check
        if (this.type === 'void_tendril') {
            if (this.y < -100) this.active = false;
        } else if (this.type === 'buzzsaw') {
            if (this.x > GAME_CONFIG.WIDTH + 60) this.active = false;
        } else {
            if (this.y > GAME_CONFIG.HEIGHT + 50 || this.x < -100 || this.x > GAME_CONFIG.WIDTH + 100) {
                this.active = false;
            }
        }
    }

    draw(ctx) {
        if (!this.active) return;

        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        ctx.scale(this.scale, this.scale);

        switch (this.type) {
            case 'acid_drop':
                this._drawAcidDrop(ctx);
                break;
            case 'exploding_spore':
                this._drawSpore(ctx);
                break;
            case 'rain_gust':
                this._drawRainGust(ctx);
                break;
            case 'crystal_beam':
                this._drawCrystalBeam(ctx);
                break;
            case 'mimic':
                this._drawMimic(ctx);
                break;
            case 'ash_gust':
                this._drawAsh(ctx);
                break;
            case 'void_tendril':
                this._drawVoidTendril(ctx);
                break;
            case 'buzzsaw':
                this._drawBuzzsaw(ctx);
                break;
            case 'infection_rain':
                this._drawInfectionRain(ctx);
                break;
            case 'light_beam':
                this._drawLightBeam(ctx);
                break;
            default:
                this._drawDefault(ctx);
        }

        ctx.restore();
    }

    _drawAcidDrop(ctx) {
        // Glowing green droplet
        ctx.fillStyle = this.glowColor;
        ctx.beginPath();
        ctx.arc(0, 0, 16, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(0, 0, 10, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
        ctx.beginPath();
        ctx.arc(-3, -3, 4, 0, Math.PI * 2);
        ctx.fill();
    }

    _drawSpore(ctx) {
        // Pulsing purple mushroom spore
        const pulse = 1 + Math.sin(this.timer * 0.005) * 0.15;
        ctx.fillStyle = 'rgba(162, 155, 254, 0.3)';
        ctx.beginPath();
        ctx.arc(0, 0, 18 * pulse, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(0, 0, 12, 0, Math.PI * 2);
        ctx.fill();
    }

    _drawRainGust(ctx) {
        ctx.fillStyle = this.color;
        ctx.fillRect(-1, -12, 2, 24);
    }

    _drawCrystalBeam(ctx) {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.moveTo(0, -15);
        ctx.lineTo(8, 0);
        ctx.lineTo(3, 15);
        ctx.lineTo(-3, 15);
        ctx.lineTo(-8, 0);
        ctx.closePath();
        ctx.fill();
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
        ctx.beginPath();
        ctx.arc(0, 0, 5, 0, Math.PI * 2);
        ctx.fill();
    }

    _drawMimic(ctx) {
        // Looks like a food item but shimmers
        const shimX = this.shimmer || 0;
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(shimX, 0, 12, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = 'rgba(255, 118, 117, 0.4)';
        ctx.beginPath();
        ctx.arc(shimX, 0, 6, 0, Math.PI * 2);
        ctx.fill();
    }

    _drawAsh(ctx) {
        ctx.fillStyle = this.color;
        ctx.globalAlpha = 0.6;
        ctx.beginPath();
        ctx.arc(0, 0, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1;
    }

    _drawVoidTendril(ctx) {
        // Dark tendril rising from below
        ctx.fillStyle = '#0f0f1b';
        ctx.beginPath();
        ctx.moveTo(-8, 20);
        ctx.quadraticCurveTo(-3, 0, -5, -20);
        ctx.quadraticCurveTo(0, -30, 5, -20);
        ctx.quadraticCurveTo(3, 0, 8, 20);
        ctx.closePath();
        ctx.fill();
        ctx.fillStyle = 'rgba(162, 155, 254, 0.3)';
        ctx.beginPath();
        ctx.arc(0, -15, 4, 0, Math.PI * 2);
        ctx.fill();
    }

    _drawBuzzsaw(ctx) {
        // Spinning saw blade
        ctx.strokeStyle = this.color;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(0, 0, 20, 0, Math.PI * 2);
        ctx.stroke();
        // Teeth
        for (let i = 0; i < 8; i++) {
            const angle = (Math.PI * 2 / 8) * i;
            ctx.beginPath();
            ctx.moveTo(Math.cos(angle) * 16, Math.sin(angle) * 16);
            ctx.lineTo(Math.cos(angle) * 24, Math.sin(angle) * 24);
            ctx.stroke();
        }
        ctx.fillStyle = '#636e72';
        ctx.beginPath();
        ctx.arc(0, 0, 6, 0, Math.PI * 2);
        ctx.fill();
    }

    _drawInfectionRain(ctx) {
        // Orange infection orb
        ctx.fillStyle = 'rgba(255, 149, 0, 0.3)';
        ctx.beginPath();
        ctx.arc(0, 0, 14, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(0, 0, 8, 0, Math.PI * 2);
        ctx.fill();
    }

    _drawLightBeam(ctx) {
        ctx.fillStyle = 'rgba(255, 215, 0, 0.4)';
        ctx.fillRect(-4, -20, 8, 40);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.fillRect(-2, -20, 4, 40);
    }

    _drawDefault(ctx) {
        ctx.fillStyle = this.color;
        ctx.beginPath();
        ctx.arc(0, 0, 10, 0, Math.PI * 2);
        ctx.fill();
    }
}
