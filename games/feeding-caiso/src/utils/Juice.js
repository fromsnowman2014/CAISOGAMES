export class ScreenShake {
    constructor() {
        this.intensity = 0;
        this.duration = 0;
        this.x = 0;
        this.y = 0;
    }

    trigger(intensity, duration) {
        this.intensity = intensity;
        this.duration = duration;
    }

    update(deltaTime) {
        if (this.duration > 0) {
            this.duration -= deltaTime;
            const currentIntensity = this.intensity * (this.duration / 100); // Decay
            this.x = (Math.random() - 0.5) * 2 * currentIntensity;
            this.y = (Math.random() - 0.5) * 2 * currentIntensity;
        } else {
            this.x = 0;
            this.y = 0;
        }
    }

    apply(ctx) {
        if (this.duration > 0) {
            ctx.translate(this.x, this.y);
        }
    }
}

export class ImpactFrame {
    constructor() {
        this.active = false;
        this.duration = 0;
    }

    trigger(duration) {
        this.active = true;
        this.duration = duration;
    }

    update(deltaTime) {
        if (this.active) {
            this.duration -= deltaTime;
            if (this.duration <= 0) {
                this.active = false;
            }
            return true; // Should freeze frame
        }
        return false;
    }
}
