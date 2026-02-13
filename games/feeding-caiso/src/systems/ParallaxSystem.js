import { GAME_CONFIG } from '../utils/Constants.js';

export class ParallaxSystem {
    constructor(game) {
        this.game = game;
        this.layers = [];
    }

    loadStageConfig(parallaxConfig) {
        if (!parallaxConfig || !parallaxConfig.layers) {
            this.layers = [];
            return;
        }

        this.layers = parallaxConfig.layers.map(layerDef => ({
            key: layerDef.key,
            speed: layerDef.speed,
            y: layerDef.y,
            height: layerDef.height,
            offset: 0,
            autoScroll: layerDef.autoScroll || 0
        }));
    }

    update(playerVelocityX, deltaTime) {
        for (let i = 0; i < this.layers.length; i++) {
            const layer = this.layers[i];

            // Player movement-based scrolling
            layer.offset -= playerVelocityX * layer.speed * deltaTime * 0.02;

            // Auto-scroll (for atmospheric backgrounds like Radiance)
            if (layer.autoScroll) {
                layer.offset -= layer.autoScroll * deltaTime * 0.001;
            }

            // Wrapping
            const assets = this.game.assets;
            const img = assets ? assets.get(layer.key) : null;
            const width = img ? img.width : GAME_CONFIG.WIDTH * 2;
            if (Math.abs(layer.offset) > width) {
                layer.offset %= width;
            }
        }
    }

    draw(ctx) {
        const assets = this.game.assets;

        for (let i = 0; i < this.layers.length; i++) {
            const layer = this.layers[i];
            const img = assets ? assets.get(layer.key) : null;

            if (img) {
                const w = img.width;
                ctx.drawImage(img, layer.offset, layer.y, w, layer.height);
                ctx.drawImage(img, layer.offset + w, layer.y, w, layer.height);
                ctx.drawImage(img, layer.offset - w, layer.y, w, layer.height);
            } else {
                this._drawFallback(ctx, layer);
            }
        }
    }

    _drawFallback(ctx, layer) {
        // Atmospheric gradient fallback based on layer depth
        const alpha = Math.max(0.02, 0.15 - layer.speed * 0.2);
        ctx.fillStyle = `rgba(15, 15, 30, ${alpha})`;
        ctx.fillRect(0, layer.y, GAME_CONFIG.WIDTH, layer.height);
    }
}
