import { STAGES } from '../config/Stages.js';
import { Hazard } from '../entities/Hazard.js';
import { GAME_CONFIG } from '../utils/Constants.js';

export class StageManager {
    constructor(game) {
        this.game = game;
        this.currentStageIndex = 0;
        this.stageTimer = 0;
        this.isTransitioning = false;
        this.transitionAlpha = 0;
        this.transitionDuration = 1200;
        this.transitionTimer = 0;
        this.pendingStageIndex = -1;
        this.hazardTimer = 0;
        this.currentConfig = STAGES[0];

        // Stage name display
        this.stageNameAlpha = 0;
        this.stageNameTimer = 0;
        this.stageNameDuration = 2500;
    }

    init() {
        this.currentStageIndex = 0;
        this.isTransitioning = false;
        this.transitionAlpha = 0;
        this.transitionTimer = 0;
        this.pendingStageIndex = -1;
        this.hazardTimer = 0;
        this.stageNameAlpha = 0;
        this.stageNameTimer = 0;
        this.loadStage(0);
    }

    loadStage(index) {
        if (index < 0 || index >= STAGES.length) return;

        this.currentStageIndex = index;
        const config = STAGES[index];
        this.currentConfig = config;

        // Core systems
        this.game.environment.setAtmosphere(config);
        this.game.lighting.setAtmosphere(config.lighting);

        // Parallax system
        if (this.game.parallax) {
            this.game.parallax.loadStageConfig(config.parallax);
        }

        // Particle system (environmental emitters)
        if (this.game.particleSystem) {
            this.game.particleSystem.clearEmitters();
            if (config.particles && config.particles.emitters) {
                config.particles.emitters.forEach(e => {
                    this.game.particleSystem.addEmitter(e);
                });
            }
        }

        // Audio
        if (this.game.audio && config.audio) {
            this.game.audio.setReverbLevel(config.audio.reverbLevel || 0);
        }

        // Stage name display
        this.stageNameAlpha = 1;
        this.stageNameTimer = 0;
    }

    startTransition(nextIndex) {
        if (nextIndex < 0 || nextIndex >= STAGES.length) return;
        this.isTransitioning = true;
        this.transitionTimer = 0;
        this.transitionAlpha = 0;
        this.pendingStageIndex = nextIndex;
    }

    nextStage() {
        this.startTransition(this.currentStageIndex + 1);
    }

    update(deltaTime) {
        // Stage name fade
        if (this.stageNameAlpha > 0) {
            this.stageNameTimer += deltaTime;
            if (this.stageNameTimer > this.stageNameDuration * 0.6) {
                this.stageNameAlpha = Math.max(0, this.stageNameAlpha - deltaTime * 0.003);
            }
        }

        // Stage transition animation
        if (this.isTransitioning) {
            this.transitionTimer += deltaTime;
            const progress = this.transitionTimer / this.transitionDuration;

            if (progress < 0.5) {
                this.transitionAlpha = progress * 2;
            } else if (progress < 0.55) {
                if (this.pendingStageIndex >= 0) {
                    this.loadStage(this.pendingStageIndex);
                    this.pendingStageIndex = -1;
                }
                this.transitionAlpha = 1;
            } else {
                this.transitionAlpha = 1 - ((progress - 0.5) * 2);
            }

            if (progress >= 1) {
                this.isTransitioning = false;
                this.transitionAlpha = 0;
            }
            return;
        }

        // Check if level requires stage advancement
        if (this.game.level > this.currentStageIndex + 1) {
            this.nextStage();
        }

        // Hazard Spawning
        const gameplay = this.currentConfig.gameplay;
        const hazards = gameplay ? gameplay.hazards : (this.currentConfig.hazards || []);

        if (hazards && hazards.length > 0) {
            this.hazardTimer += deltaTime;
            const spawnInterval = Math.max(500, 2000 - (this.game.level * 100));

            if (this.hazardTimer > spawnInterval) {
                this.hazardTimer = 0;
                if (Math.random() < 0.7) {
                    const type = hazards[Math.floor(Math.random() * hazards.length)];
                    const x = Math.random() * GAME_CONFIG.WIDTH;
                    const y = -50;
                    this.game.hazards.push(new Hazard(type, x, y, this.game.assets));
                }
            }
        }
    }

    draw(ctx) {
        // Stage name overlay
        if (this.stageNameAlpha > 0 && this.currentConfig) {
            ctx.save();
            ctx.globalAlpha = this.stageNameAlpha;
            ctx.fillStyle = '#dfe6e9';
            ctx.font = 'bold 22px Fredoka One';
            ctx.textAlign = 'center';
            ctx.shadowColor = 'rgba(0, 0, 0, 0.8)';
            ctx.shadowBlur = 8;
            ctx.fillText(
                `Stage ${this.currentStageIndex + 1}`,
                GAME_CONFIG.WIDTH / 2,
                GAME_CONFIG.HEIGHT / 2 - 30
            );
            ctx.font = '16px Nunito';
            ctx.fillStyle = '#b2bec3';
            ctx.fillText(
                this.currentConfig.name,
                GAME_CONFIG.WIDTH / 2,
                GAME_CONFIG.HEIGHT / 2
            );
            if (this.currentConfig.nameKo) {
                ctx.font = '13px Nunito';
                ctx.fillStyle = '#636e72';
                ctx.fillText(
                    this.currentConfig.nameKo,
                    GAME_CONFIG.WIDTH / 2,
                    GAME_CONFIG.HEIGHT / 2 + 22
                );
            }
            ctx.shadowBlur = 0;
            ctx.restore();
        }

        // Transition overlay
        if (this.isTransitioning && this.transitionAlpha > 0) {
            ctx.fillStyle = `rgba(0, 0, 0, ${this.transitionAlpha})`;
            ctx.fillRect(0, 0, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT);
        }
    }
}
