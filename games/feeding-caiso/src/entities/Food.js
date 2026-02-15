export class Food {
    constructor(foodData, startX, startY, endX, endY, assets) {
        this.foodData = foodData;
        this.assets = assets;
        this.startX = startX;
        this.startY = startY;
        this.endX = endX;
        this.endY = endY;
        this.x = startX;
        this.y = startY;
        this.progress = 0;
        this.duration = 380;
        this.elapsed = 0;
        this.rotation = 0;
        this.arrived = false;
        this.blocked = false;
        this.driftX = 0;

        // PHASE 7.3C: Power level from timing gauge (0-1)
        // Applied to distance multiplier: 0.5 (weak) to 1.0 (strong)
        this.powerLevel = 0.5;  // Default to center if not set
    }

    update(deltaTime, environment) {
        this.elapsed += deltaTime;
        this.progress = Math.min(this.elapsed / this.duration, 1);

        // Environmental Physics
        if (environment) {
            this.driftX += environment.windX * (deltaTime / 16);
        }

        // PHASE 7.3C: Apply power level to distance
        // Power range: 0-1 → Distance multiplier: 0.5-1.0
        // - powerLevel 0.0 (left edge) = 0.5x distance (too weak, falls short)
        // - powerLevel 0.5 (center) = 0.75x distance (good)
        // - powerLevel 1.0 (right edge) = 1.0x distance (too strong, overshoots)
        // Perfect zone (0.4-0.6) maps to ~0.7-0.8x for good gameplay
        const distanceMultiplier = 0.5 + this.powerLevel * 0.5;

        // Ease out
        const t = 1 - Math.pow(1 - this.progress, 3);
        this.x = this.startX + ((this.endX - this.startX) * distanceMultiplier) * t + this.driftX;

        // Arc trajectory
        let gravityScale = environment ? environment.gravityY : 1.0;
        // avoid division by zero
        if (gravityScale < 0.1) gravityScale = 0.1;

        const controlY = Math.min(this.startY, this.endY) - (150 / gravityScale);
        this.y = (1 - t) * (1 - t) * this.startY +
            2 * (1 - t) * t * controlY +
            t * t * this.endY;

        this.rotation += 0.18;

        if (this.progress >= 1) {
            this.arrived = true;
        }
    }

    draw(ctx) {
        const img = this.assets.get(this.foodData.asset);

        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);

        const size = 45;

        // Glow
        ctx.shadowColor = this.foodData.color;
        ctx.shadowBlur = 15;

        if (img) {
            ctx.drawImage(img, -size / 2, -size / 2, size, size);
        } else {
            ctx.fillStyle = this.foodData.color;
            ctx.beginPath();
            ctx.arc(0, 0, size / 2.5, 0, Math.PI * 2);
            ctx.fill();
        }

        ctx.restore();
    }
}
