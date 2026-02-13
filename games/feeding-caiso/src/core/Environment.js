export class Environment {
    constructor(game) {
        this.game = game;
        this.windX = 0;
        this.gravityY = 1.0;
        this.backgroundColor = "#1a1a2e";

        // Wind direction system
        this.windDirection = "static";
        this.baseWindX = 0;
        this.windAlternateInterval = 5000;
        this.windTimer = 0;
        this.windSign = 1;
        this.windRandomRange = null;

        // Slippery floor
        this.slipperyFloor = false;
    }

    setAtmosphere(stageConfig) {
        this.backgroundColor = stageConfig.backgroundColor;

        const atmo = stageConfig.atmosphere;
        this.baseWindX = atmo.windX;
        this.windX = atmo.windX;
        this.gravityY = atmo.gravityY;

        // Extended gameplay config
        const gp = stageConfig.gameplay;
        if (gp) {
            this.windDirection = gp.windDirection || "static";
            this.windAlternateInterval = gp.windAlternateInterval || 5000;
            this.windRandomRange = gp.windRandomRange || null;
            this.slipperyFloor = gp.slipperyFloor || false;
        } else {
            this.windDirection = "static";
            this.slipperyFloor = false;
            this.windRandomRange = null;
        }

        this.windTimer = 0;
        this.windSign = 1;
    }

    update(deltaTime) {
        if (this.windDirection === "alternating") {
            this.windTimer += deltaTime;
            if (this.windTimer >= this.windAlternateInterval) {
                this.windTimer = 0;
                this.windSign *= -1;
            }
            // Smooth transition using lerp
            const targetWind = this.baseWindX * this.windSign;
            this.windX += (targetWind - this.windX) * 0.02;
        } else if (this.windDirection === "random" && this.windRandomRange) {
            this.windTimer += deltaTime;
            if (this.windTimer >= 3000) {
                this.windTimer = 0;
                const [min, max] = this.windRandomRange;
                this.windX = min + Math.random() * (max - min);
            }
        }
    }

    drawBackground(ctx) {
        ctx.fillStyle = this.backgroundColor;
        ctx.fillRect(0, 0, this.game.canvas.width, this.game.canvas.height);
    }
}
