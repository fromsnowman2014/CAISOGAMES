import { STAGES } from '../config/Stages.js';
import { Hazard } from '../entities/Hazard.js';
import { GAME_CONFIG } from '../utils/Constants.js';

export class StageManager {
    constructor(game) {
        this.game = game;
        this.currentStageIndex = 0;
        this.stageTimer = 0;
        this.isTransitioning = false;
        this.hazardTimer = 0;
        this.currentConfig = STAGES[0];
    }

    init() {
        this.loadStage(0);
    }

    loadStage(index) {
        if (index < 0 || index >= STAGES.length) return;

        this.currentStageIndex = index;
        const config = STAGES[index];
        this.currentConfig = config;

        console.log(`Loading Stage ${index + 1}: ${config.name}`);

        // Update Game Systems
        this.game.environment.setAtmosphere(config);
        this.game.lighting.setAtmosphere(config.atmosphere);

        // Notify user/UI
        if (this.game.addFloatingText) {
            this.game.addFloatingText(`Stage ${index + 1}: ${config.name}`, this.game.canvas.width / 2, 100, '#fff');
        }
    }

    nextStage() {
        this.loadStage(this.currentStageIndex + 1);
    }

    update(deltaTime) {
        if (this.game.level > this.currentStageIndex + 1) {
            this.nextStage();
        }

        // Hazard Spawning
        const hazards = this.currentConfig.hazards;
        if (hazards && hazards.length > 0) {
            this.hazardTimer += deltaTime;
            // Spawn rate could depend on difficulty/level too
            const spawnInterval = Math.max(500, 2000 - (this.game.level * 100));

            if (this.hazardTimer > spawnInterval) {
                this.hazardTimer = 0;
                if (Math.random() < 0.7) { // 70% chance to spawn when timer hits
                    const type = hazards[Math.floor(Math.random() * hazards.length)];
                    const x = Math.random() * GAME_CONFIG.WIDTH;
                    const y = -50;
                    this.game.hazards.push(new Hazard(type, x, y, this.game.assets));
                }
            }
        }
    }
}
