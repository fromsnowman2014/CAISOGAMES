import { GAME_CONFIG } from '../utils/Constants.js';
import { SquashStretch } from '../utils/SquashStretch.js';

export class Villager {
    constructor(id, startY = GAME_CONFIG.VILLAGER_SPAWN_Y) {
        this.id = id;
        this.fromLeft = Math.random() > 0.5;
        this.x = this.fromLeft ? -40 : GAME_CONFIG.WIDTH + 40;
        this.y = startY + Math.random() * 60 - 30;
        this.targetX = GAME_CONFIG.WIDTH / 2;
        this.speed = 0.4 + Math.random() * 0.3;
        this.scared = false;
        this.bobOffset = Math.random() * Math.PI * 2;
        this.scale = 0.8 + Math.random() * 0.3;
        this.active = true;
        this.beingEaten = false;
        this.eatenProgress = 0;
        this.squash = new SquashStretch();
    }

    update(deltaTime) {
        if (!this.active) return;

        // Move toward center (where Caiso is in vertical layout)
        const moveSpeed = this.speed * (this.scared ? 0.6 : 1) * (deltaTime / 16);
        const direction = this.fromLeft ? 1 : -1;
        this.x += moveSpeed * direction;

        // Get scared when close to center
        const distToCenter = Math.abs(this.x - this.targetX);
        if (distToCenter < 180 && !this.scared) {
            this.scared = true;
        }

        // Being eaten animation
        if (this.beingEaten) {
            this.eatenProgress += deltaTime / 400;
            this.y -= 1.5;
            if (this.eatenProgress >= 1) {
                this.active = false;
            }
        }

        // Bob animation
        this.bobOffset += deltaTime * 0.012;
        this.squash.update();
    }

    draw(ctx, assets) {
        if (!this.active) return;

        const bob = Math.sin(this.bobOffset) * 3;
        const spriteKey = this.scared ? 'villager_scared' : 'villager_normal';
        const img = assets.get(spriteKey);

        ctx.save();

        if (this.beingEaten) {
            ctx.globalAlpha = 1 - this.eatenProgress;
        }

        const width = 50 * this.scale;
        const height = 50 * this.scale;
        const transform = this.squash.getTransform();

        ctx.translate(this.x, this.y + bob);
        ctx.scale(transform.scaleX * (this.fromLeft ? 1 : -1), transform.scaleY);

        if (img) {
            ctx.drawImage(img, -width / 2, -height / 2, width, height);
        } else {
            // Fallback
            ctx.fillStyle = this.scared ? '#e74c3c' : '#3498db';
            ctx.beginPath();
            ctx.arc(0, 0, width / 3, 0, Math.PI * 2);
            ctx.fill();
        }

        ctx.restore();
    }
}
