export class Environment {
    constructor(game) {
        this.game = game;
        this.windX = 0;
        this.gravityY = 1.0;
        this.backgroundColor = "#E0F7FA";
    }

    setAtmosphere(stageConfig) {
        // Smooth transitions could happen here
        this.windX = stageConfig.atmosphere.windX;
        this.gravityY = stageConfig.atmosphere.gravityY;
        this.backgroundColor = stageConfig.backgroundColor;
    }

    update(deltaTime) {
        // Dynamic wind changes could happen here
    }

    applyPhysics(entity) {
        if (entity.vx !== undefined) {
            entity.vx += this.windX * 0.01; // Tiny push per frame
        }
        // Gravity is usually applied in entity.update(), but we can modify it there
        // by reading environment.gravityY
    }

    drawBackground(ctx) {
        // Draw the base background color
        ctx.fillStyle = this.backgroundColor;
        ctx.fillRect(0, 0, this.game.canvas.width, this.game.canvas.height);
    }
}
