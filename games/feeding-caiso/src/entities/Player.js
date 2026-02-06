import { GAME_CONFIG } from '../utils/Constants.js';
import { SquashStretch } from '../utils/SquashStretch.js';

export class Player {
    constructor() {
        this.x = GAME_CONFIG.WIDTH / 2;
        this.y = GAME_CONFIG.PLAYER_Y;
        this.vx = 0;
        this.vy = 0;
        this.throwing = false;
        this.throwTimer = 0;
        this.squash = new SquashStretch();
        this.maxSpeed = 6;
        this.acceleration = 0.4;
        this.friction = 0.88;
    }

    update(deltaTime, joystick) {
        // Apply joystick input
        if (joystick.active) {
            this.vx += joystick.direction.x * this.acceleration * (deltaTime / 16);
            this.vy += joystick.direction.y * this.acceleration * (deltaTime / 16);
        }

        // Friction
        this.vx *= this.friction;
        this.vy *= this.friction;

        // Clamp speed
        const speed = Math.sqrt(this.vx * this.vx + this.vy * this.vy);
        if (speed > this.maxSpeed) {
            this.vx = (this.vx / speed) * this.maxSpeed;
            this.vy = (this.vy / speed) * this.maxSpeed;
        }

        // Move
        this.x += this.vx * (deltaTime / 16);
        this.y += this.vy * (deltaTime / 16);

        // Bounds - keep in control area
        const margin = 50;
        const minY = GAME_CONFIG.HEIGHT - GAME_CONFIG.CONTROL_HEIGHT - 60;
        const maxY = GAME_CONFIG.HEIGHT - 40;

        if (this.x < margin) { this.x = margin; this.vx = Math.abs(this.vx) * 0.5; this.squash.triggerBounce(); }
        if (this.x > GAME_CONFIG.WIDTH - margin) { this.x = GAME_CONFIG.WIDTH - margin; this.vx = -Math.abs(this.vx) * 0.5; this.squash.triggerBounce(); }
        if (this.y < minY) { this.y = minY; this.vy = Math.abs(this.vy) * 0.5; }
        if (this.y > maxY) { this.y = maxY; this.vy = -Math.abs(this.vy) * 0.5; }

        // Throw animation
        if (this.throwTimer > 0) {
            this.throwTimer -= deltaTime;
            if (this.throwTimer <= 0) {
                this.throwing = false;
            }
        }

        this.squash.applyMovement(this.vx, this.vy);
        this.squash.update();
    }

    throw() {
        this.throwing = true;
        this.throwTimer = 250;
        this.squash.triggerEat();
    }

    draw(ctx, assets) {
        const img = assets.get('player_idle');
        const transform = this.squash.getTransform();

        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.scale(transform.scaleX, transform.scaleY);

        const width = 80;
        const height = 100;

        if (img) {
            ctx.drawImage(img, -width / 2, -height / 2, width, height);
        } else {
            // Fallback
            ctx.fillStyle = '#e74c3c';
            ctx.beginPath();
            ctx.arc(0, -10, 25, 0, Math.PI * 2);
            ctx.fill();
            ctx.fillStyle = '#ffeaa7';
            ctx.beginPath();
            ctx.arc(0, -35, 18, 0, Math.PI * 2);
            ctx.fill();
        }

        ctx.restore();
    }
}
