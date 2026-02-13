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
    }

    init() {
        this.currentStageIndex = 0;
        this.isTransitioning = false;
        this.transitionAlpha = 0;
        this.transitionTimer = 0;
        this.pendingStageIndex = -1;
        this.hazardTimer = 0;
        this.loadStage(0);
    }

    loadStage(index) {
        if (index < 0 || index >= STAGES.length) return;

        this.currentStageIndex = index;
        const config = STAGES[index];
        this.currentConfig = config;

        console.log(`Loading Stage ${index + 1}: ${config.name}`);

        this.game.environment.setAtmosphere(config);
        this.game.lighting.setAtmosphere(config.atmosphere);

        if (this.game.addFloatingText) {
            this.game.addFloatingText(`Stage ${index + 1}: ${config.name}`, this.game.canvas.width / 2, 100, '#fff');
        }
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
        // Stage transition animation
        if (this.isTransitioning) {
            this.transitionTimer += deltaTime;
            const progress = this.transitionTimer / this.transitionDuration;

            if (progress < 0.5) {
                // Fade to black
                this.transitionAlpha = progress * 2;
            } else if (progress < 0.55) {
                // At midpoint, load the new stage
                if (this.pendingStageIndex >= 0) {
                    this.loadStage(this.pendingStageIndex);
                    this.pendingStageIndex = -1;
                }
                this.transitionAlpha = 1;
            } else {
                // Fade from black
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
        const hazards = this.currentConfig.hazards;
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
        if (this.isTransitioning && this.transitionAlpha > 0) {
            ctx.fillStyle = `rgba(0, 0, 0, ${this.transitionAlpha})`;
            ctx.fillRect(0, 0, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT);
        }
    }
}
