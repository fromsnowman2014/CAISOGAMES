import { GAME_CONFIG, EVOLUTION_TIERS } from '../utils/Constants.js';
import { SquashStretch } from '../utils/SquashStretch.js';

export class Caiso {
    constructor() {
        this.x = GAME_CONFIG.WIDTH / 2;
        this.y = GAME_CONFIG.CAISO_Y;
        this.evolutionTier = 0;
        this.expression = 'hungry';
        this.bounceOffset = 0;
        this.eatTimer = 0;
        this.guiltyTimer = 0;
        this.squash = new SquashStretch();
    }

    reset() {
        this.evolutionTier = 0;
        this.expression = 'hungry';
        this.eatTimer = 0;
        this.guiltyTimer = 0;
    }

    getEvolutionTier(level) {
        for (let i = EVOLUTION_TIERS.length - 1; i >= 0; i--) {
            if (level >= EVOLUTION_TIERS[i].level) {
                return i;
            }
        }
        return 0;
    }

    updateEvolution(level) {
        const newTier = this.getEvolutionTier(level);
        if (newTier > this.evolutionTier) {
            this.evolutionTier = newTier;
            this.squash.scaleX = 0.6;
            this.squash.scaleY = 1.5;
            return true;
        }
        return false;
    }

    eat() {
        this.expression = 'happy';
        this.eatTimer = 400;
        this.squash.triggerEat();
    }

    showGuilty() {
        this.expression = 'sad';
        this.guiltyTimer = 600;
    }

    update(deltaTime) {
        this.bounceOffset = Math.sin(Date.now() * 0.003) * 6;

        if (this.eatTimer > 0) {
            this.eatTimer -= deltaTime;
            if (this.eatTimer <= 0 && this.expression === 'happy') {
                this.expression = 'hungry';
            }
        }

        if (this.guiltyTimer > 0) {
            this.guiltyTimer -= deltaTime;
            if (this.guiltyTimer <= 0 && this.expression === 'sad') {
                this.expression = 'hungry';
            }
        }

        this.squash.update();
    }

    draw(ctx, assets) {
        const tier = EVOLUTION_TIERS[this.evolutionTier];

        // Phase 4: Use expression-based sprites primarily
        let spriteKey = 'caiso_idle';

        if (this.expression === 'hungry') {
            spriteKey = 'caiso_hungry';
        } else if (this.expression === 'happy') {
            spriteKey = 'caiso_happy';
        } else if (this.expression === 'sad') {
            spriteKey = 'caiso_hungry'; // Reuse hungry/open mouth for sad/shocked for now
        }

        const img = assets.get(spriteKey);
        const transform = this.squash.getTransform();

        ctx.save();
        ctx.translate(this.x, this.y + this.bounceOffset);
        ctx.scale(transform.scaleX * tier.scale, transform.scaleY * tier.scale);

        const baseSize = 160;

        if (img) {
            // Glow effect
            ctx.shadowColor = '#9b59b6';
            ctx.shadowBlur = 25;
            ctx.drawImage(img, -baseSize / 2, -baseSize / 2, baseSize, baseSize);
            ctx.shadowBlur = 0;
        } else {
            // Fallback
            ctx.fillStyle = '#9b59b6';
            ctx.beginPath();
            ctx.arc(0, 0, baseSize / 2.5, 0, Math.PI * 2);
            ctx.fill();

            // Eyes
            ctx.fillStyle = '#fff';
            ctx.beginPath();
            ctx.arc(-25, -20, 18, 0, Math.PI * 2);
            ctx.arc(25, -20, 18, 0, Math.PI * 2);
            ctx.fill();

            // Mouth
            ctx.fillStyle = '#2c2c2c';
            ctx.beginPath();
            ctx.arc(0, 25, 35, 0, Math.PI);
            ctx.fill();
        }

        ctx.restore();
    }

    getMouthPosition() {
        return { x: this.x, y: this.y + 30 + this.bounceOffset };
    }
}
