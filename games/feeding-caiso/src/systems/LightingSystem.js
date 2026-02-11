export class LightingSystem {
    constructor(game) {
        this.game = game;
        this.overlayColor = "rgba(0,0,0,0)";
    }

    setAtmosphere(atmosphereConfig) {
        this.overlayColor = atmosphereConfig.overlayColor;
    }

    update(deltaTime) {
        // Future: dynamic transitions between colors
    }

    draw(ctx) {
        if (!this.overlayColor) return;

        ctx.save();
        ctx.fillStyle = this.overlayColor;
        ctx.fillRect(0, 0, this.game.canvas.width, this.game.canvas.height);

        // Add a subtle vignette or gradient if we want more "sophistication"
        // This is a simple placeholder for now.

        ctx.restore();
    }
}
