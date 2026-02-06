export class SquashStretch {
    constructor() {
        this.scaleX = 1;
        this.scaleY = 1;
        this.targetScaleX = 1;
        this.targetScaleY = 1;
        this.elasticity = 0.15;
        this.friction = 0.85;
        this.velX = 0;
        this.velY = 0;
    }

    update() {
        // Spring force towards target
        const forceX = (this.targetScaleX - this.scaleX) * this.elasticity;
        const forceY = (this.targetScaleY - this.scaleY) * this.elasticity;

        this.velX += forceX;
        this.velY += forceY;

        this.velX *= this.friction;
        this.velY *= this.friction;

        this.scaleX += this.velX;
        this.scaleY += this.velY;

        // Reset target slowly
        this.targetScaleX = 1;
        this.targetScaleY = 1;
    }

    triggerBounce() {
        this.targetScaleX = 1.4;
        this.targetScaleY = 0.6;
    }

    triggerEat() {
        this.targetScaleX = 0.7;
        this.targetScaleY = 1.3;
    }

    applyMovement(vx, vy) {
        // Stretch based on velocity
        const speed = Math.sqrt(vx * vx + vy * vy);
        if (speed > 0.1) {
            this.targetScaleY = 1 + speed * 0.05;
            this.targetScaleX = 1 - speed * 0.05;
        }
    }

    getTransform() {
        return { scaleX: this.scaleX, scaleY: this.scaleY };
    }
}
