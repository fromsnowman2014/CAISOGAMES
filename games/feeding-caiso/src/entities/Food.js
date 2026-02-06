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
    }

    update(deltaTime) {
        this.elapsed += deltaTime;
        this.progress = Math.min(this.elapsed / this.duration, 1);

        // Ease out
        const t = 1 - Math.pow(1 - this.progress, 3);
        this.x = this.startX + (this.endX - this.startX) * t;

        // Arc trajectory
        const controlY = Math.min(this.startY, this.endY) - 150;
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
