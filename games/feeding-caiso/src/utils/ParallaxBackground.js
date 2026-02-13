import { GAME_CONFIG } from './Constants.js';

export class ParallaxBackground {
    constructor(assets) {
        this.assets = assets;
        this.layers = [
            // Sky moved to Environment.js
            { key: 'bg_clouds', speed: 0.15, y: 100, height: 150, offset: 0 },
            { key: 'bg_city', speed: 0.3, y: 350, height: 250, offset: 0 },
            { key: 'bg_ground', speed: 0.6, y: 550, height: 304, offset: 0 }
        ];
    }

    update(playerVelocityX, deltaTime) {
        this.layers.forEach(layer => {
            layer.offset -= playerVelocityX * layer.speed * deltaTime * 0.02;
            const img = this.assets.get(layer.key);
            if (img) {
                const width = img.width || GAME_CONFIG.WIDTH * 2;
                if (layer.offset > width) layer.offset = 0;
                if (layer.offset < -width) layer.offset = 0;
            }
        });
    }

    draw(ctx) {
        this.layers.forEach(layer => {
            const img = this.assets.get(layer.key);
            if (img) {
                const width = img.width;
                const height = layer.height;

                // Draw twice for seamless scrolling
                ctx.drawImage(img, layer.offset, layer.y, width, height);
                ctx.drawImage(img, layer.offset + width, layer.y, width, height);
                ctx.drawImage(img, layer.offset - width, layer.y, width, height);
            } else {
                // Fallback gradient
                this.drawFallbackLayer(ctx, layer);
            }
        });
    }

    drawFallbackLayer(ctx, layer) {
        if (layer.key === 'bg_ground') {
            ctx.fillStyle = '#0f3460';
            ctx.fillRect(0, layer.y, GAME_CONFIG.WIDTH, layer.height);
        } else if (layer.key === 'bg_clouds') {
            ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
            ctx.fillRect(0, layer.y, GAME_CONFIG.WIDTH, layer.height);
        }
    }
}
