import { GAME_CONFIG } from '../utils/Constants.js';

export class ParticleSystem {
    constructor(game) {
        this.game = game;
        this.maxParticles = 500;
        this.pool = [];
        this.active = [];
        this.emitters = [];

        // Pre-allocate particle pool
        for (let i = 0; i < this.maxParticles; i++) {
            this.pool.push(this._createParticle());
        }
    }

    _createParticle() {
        return {
            x: 0, y: 0, vx: 0, vy: 0,
            size: 0, color: '#fff', alpha: 1,
            life: 0, maxLife: 0,
            gravity: 0.35,
            active: false,
            shape: 'circle' // 'circle' | 'rect' (for rain)
        };
    }

    spawn(x, y, config) {
        if (this.active.length >= this.maxParticles) return null;
        if (this.pool.length === 0) return null;

        const p = this.pool.pop();
        p.x = x;
        p.y = y;
        p.vx = config.vx !== undefined ? config.vx : (Math.random() - 0.5) * 14;
        p.vy = config.vy !== undefined ? config.vy : (Math.random() - 0.5) * 14 - 5;
        p.size = config.size || Math.random() * 10 + 4;
        p.color = config.color || '#fff';
        p.alpha = config.alpha !== undefined ? config.alpha : 1;
        p.life = config.life || 35 + Math.random() * 20;
        p.maxLife = p.life;
        p.gravity = config.gravity !== undefined ? config.gravity : 0.35;
        p.active = true;
        p.shape = config.shape || 'circle';

        this.active.push(p);
        return p;
    }

    burst(x, y, color, count) {
        for (let i = 0; i < count; i++) {
            this.spawn(x, y, { color });
        }
    }

    addEmitter(emitterConfig) {
        this.emitters.push({
            type: emitterConfig.type,
            density: emitterConfig.density,
            color: emitterConfig.color,
            sizeRange: emitterConfig.sizeRange || [2, 5],
            alpha: emitterConfig.alpha,
            timer: 0,
            active: true
        });
    }

    clearEmitters() {
        this.emitters = [];
    }

    update(deltaTime) {
        const windX = this.game.environment ? this.game.environment.windX : 0;

        // Emit from active emitters
        for (let e = 0; e < this.emitters.length; e++) {
            const emitter = this.emitters[e];
            if (!emitter.active) continue;

            emitter.timer += deltaTime;
            const interval = this._getEmitterInterval(emitter.density);

            while (emitter.timer >= interval) {
                emitter.timer -= interval;
                this._emitParticle(emitter, windX);
            }
        }

        // Update active particles
        for (let i = this.active.length - 1; i >= 0; i--) {
            const p = this.active[i];
            p.x += p.vx;
            p.y += p.vy;
            p.vy += p.gravity;
            p.life--;
            p.alpha = Math.max(0, p.life / p.maxLife);

            if (p.life <= 0 || p.y > GAME_CONFIG.HEIGHT + 20 || p.x < -50 || p.x > GAME_CONFIG.WIDTH + 50) {
                p.active = false;
                this.active.splice(i, 1);
                this.pool.push(p);
            }
        }
    }

    draw(ctx) {
        if (this.active.length === 0) return;

        ctx.save();
        for (let i = 0; i < this.active.length; i++) {
            const p = this.active[i];
            ctx.globalAlpha = p.alpha;
            ctx.fillStyle = p.color;

            if (p.shape === 'rect') {
                // Rain drops: thin vertical rectangles
                ctx.fillRect(p.x, p.y, p.size * 0.4, p.size * 5);
            } else {
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }
        ctx.globalAlpha = 1;
        ctx.restore();
    }

    _getEmitterInterval(density) {
        switch (density) {
            case 'low': return 200;
            case 'medium': return 80;
            case 'high': return 40;
            case 'very_high': return 16;
            case 'extreme': return 8;
            default: return 80;
        }
    }

    _emitParticle(emitter, windX) {
        const W = GAME_CONFIG.WIDTH;
        const H = GAME_CONFIG.HEIGHT;
        const [minSize, maxSize] = emitter.sizeRange;
        const size = minSize + Math.random() * (maxSize - minSize);

        let cfg;
        switch (emitter.type) {
            case 'dust':
                cfg = {
                    x: Math.random() * W,
                    y: Math.random() * H,
                    vx: (Math.random() - 0.5) * 0.5 + windX * 0.05,
                    vy: (Math.random() - 0.5) * 0.3,
                    gravity: 0,
                    life: 200 + Math.random() * 100
                };
                break;
            case 'spore':
                cfg = {
                    x: Math.random() * W,
                    y: -10,
                    vx: (Math.random() - 0.5) * 1 + windX * 0.1,
                    vy: 0.3 + Math.random() * 0.5,
                    gravity: 0.01,
                    life: 300 + Math.random() * 100
                };
                break;
            case 'rain':
                cfg = {
                    x: Math.random() * (W + 100) - 50,
                    y: -10,
                    vx: windX * 0.3 + 0.5,
                    vy: 8 + Math.random() * 4,
                    gravity: 0,
                    life: 80,
                    shape: 'rect'
                };
                break;
            case 'ash':
                cfg = {
                    x: Math.random() * W,
                    y: -10,
                    vx: (Math.random() - 0.5) * 2 + windX * 0.2,
                    vy: 0.5 + Math.random() * 1,
                    gravity: 0,
                    life: 400 + Math.random() * 200
                };
                break;
            case 'void':
                cfg = {
                    x: Math.random() * W,
                    y: H + 10,
                    vx: (Math.random() - 0.5) * 0.5,
                    vy: -(1 + Math.random() * 2),
                    gravity: -0.01,
                    life: 300 + Math.random() * 100
                };
                break;
            default:
                cfg = {
                    x: Math.random() * W,
                    y: Math.random() * H,
                    vx: (Math.random() - 0.5) * 0.5,
                    vy: (Math.random() - 0.5) * 0.3,
                    gravity: 0,
                    life: 200
                };
        }

        this.spawn(cfg.x, cfg.y, {
            vx: cfg.vx,
            vy: cfg.vy,
            color: emitter.color,
            size,
            gravity: cfg.gravity,
            life: cfg.life,
            alpha: emitter.alpha,
            shape: cfg.shape || 'circle'
        });
    }
}
