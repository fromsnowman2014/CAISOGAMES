import { GAME_CONFIG } from '../utils/Constants.js';

export class LightingSystem {
    constructor(game) {
        this.game = game;
        this.ambientLight = 0.3;
        this.playerLightRadius = 150;
        this.playerLightColor = "rgba(116, 185, 255, 0.4)";
        this.fixedLights = [];
        this.vignette = true;
        this.bloom = false;
        this.playerShadow = false;
        this.topGradient = null;
        this.ambientLightRamp = null;

        // Legacy overlay support
        this.overlayColor = "rgba(0,0,0,0)";

        // Offscreen canvas for compositing
        this.lightCanvas = document.createElement('canvas');
        this.lightCanvas.width = GAME_CONFIG.WIDTH;
        this.lightCanvas.height = GAME_CONFIG.HEIGHT;
        this.lightCtx = this.lightCanvas.getContext('2d');

        // Bloom pulse timer
        this.bloomTimer = 0;
        this.bloomIntensity = 0;

        // Ambient ramp progress (0-1, based on stage elapsed time)
        this.rampProgress = 0;
    }

    setAtmosphere(config) {
        // Support both legacy format (Phase 5) and new format (Phase 6)
        if (config && config.ambientLight !== undefined) {
            // Phase 6 lighting config
            this.ambientLight = config.ambientLight;
            this.playerLightRadius = config.playerLightRadius || 150;
            this.playerLightColor = config.playerLightColor || "rgba(116, 185, 255, 0.4)";
            this.fixedLights = config.fixedLights || [];
            this.vignette = config.vignette !== false;
            this.bloom = config.bloom || false;
            this.playerShadow = config.playerShadow || false;
            this.topGradient = config.topGradient || null;
            this.ambientLightRamp = config.ambientLightRamp || null;
            this.rampProgress = 0;
        } else if (config && config.overlayColor) {
            // Legacy Phase 5 format
            this.overlayColor = config.overlayColor;
        }
    }

    update(deltaTime) {
        // Bloom pulsing
        if (this.bloom) {
            this.bloomTimer += deltaTime * 0.002;
            this.bloomIntensity = Math.sin(this.bloomTimer) * 0.15 + 0.85;
        }

        // Ambient light ramp (for Radiance stage)
        if (this.ambientLightRamp) {
            this.rampProgress = Math.min(1, this.rampProgress + deltaTime * 0.00001);
            const { from, to } = this.ambientLightRamp;
            this.ambientLight = from + (to - from) * this.rampProgress;
        }
    }

    draw(ctx) {
        const W = GAME_CONFIG.WIDTH;
        const H = GAME_CONFIG.HEIGHT;
        const lc = this.lightCanvas;
        const lctx = this.lightCtx;

        // Resize if needed
        if (lc.width !== W || lc.height !== H) {
            lc.width = W;
            lc.height = H;
        }

        // Clear offscreen
        lctx.clearRect(0, 0, W, H);

        // 1. Base darkness layer
        const darkness = Math.max(0, Math.min(1, 1 - this.ambientLight));
        lctx.fillStyle = `rgba(0, 0, 0, ${darkness})`;
        lctx.fillRect(0, 0, W, H);

        // 2. Cut out light sources using destination-out
        lctx.globalCompositeOperation = 'destination-out';

        // Player light (follows player position)
        const player = this.game.player;
        if (player && this.playerLightRadius > 0) {
            this._drawLight(lctx, player.x, player.y - 20, this.playerLightRadius, 1.0);
        }

        // Caiso glow (subtle)
        const caiso = this.game.caiso;
        if (caiso) {
            this._drawLight(lctx, caiso.x, caiso.y, 80, 0.6);
        }

        // Fixed lights from stage config
        this.fixedLights.forEach(light => {
            this._drawLight(lctx, light.x, light.y, light.radius, 0.7);
        });

        lctx.globalCompositeOperation = 'source-over';

        // 3. Composite darkness onto main canvas
        ctx.drawImage(lc, 0, 0);

        // 4. Top gradient (Kingdom's Edge - light from above)
        if (this.topGradient) {
            const tg = this.topGradient;
            const grad = ctx.createLinearGradient(0, 0, 0, tg.height);
            grad.addColorStop(0, tg.color);
            grad.addColorStop(1, 'rgba(0, 0, 0, 0)');
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, W, tg.height);
        }

        // 5. Vignette
        if (this.vignette) {
            this._drawVignette(ctx, W, H);
        }

        // 6. Bloom overlay
        if (this.bloom && this.bloomIntensity > 0) {
            ctx.fillStyle = `rgba(255, 255, 255, ${(1 - this.bloomIntensity) * 0.08})`;
            ctx.fillRect(0, 0, W, H);
        }

        // 7. Player shadow (White Palace)
        if (this.playerShadow && player) {
            this._drawPlayerShadow(ctx, player);
        }
    }

    _drawLight(ctx, x, y, radius, intensity) {
        const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius);
        gradient.addColorStop(0, `rgba(0, 0, 0, ${intensity})`);
        gradient.addColorStop(0.5, `rgba(0, 0, 0, ${intensity * 0.6})`);
        gradient.addColorStop(0.8, `rgba(0, 0, 0, ${intensity * 0.2})`);
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();
    }

    _drawVignette(ctx, w, h) {
        const gradient = ctx.createRadialGradient(w / 2, h / 2, w * 0.3, w / 2, h / 2, w * 0.85);
        gradient.addColorStop(0, 'rgba(0, 0, 0, 0)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0.5)');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, w, h);
    }

    _drawPlayerShadow(ctx, player) {
        ctx.save();
        ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
        ctx.beginPath();
        ctx.ellipse(player.x, player.y + 30, 25, 8, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    }
}
