import { GAME_CONFIG, FOODS, EVOLUTION_TIERS, FEVER_CONFIG } from '../utils/Constants.js';
import { AssetManager } from '../managers/AssetManager.js';
import { AudioManager } from './Audio.js';
import { VirtualJoystick } from './Input.js';
import { ParallaxSystem } from '../systems/ParallaxSystem.js';
import { ParticleSystem } from '../systems/ParticleSystem.js';
import { FeverMode } from '../utils/FeverMode.js';
import { DistanceBarGauge } from '../utils/DistanceBarGauge.js';
import { ScreenShake, ImpactFrame } from '../utils/Juice.js';
import { Caiso } from '../entities/Caiso.js';
import { Player } from '../entities/Player.js';
import { Villager } from '../entities/Villager.js';
import { Food } from '../entities/Food.js';
import { Hazard } from '../entities/Hazard.js';
import { StageManager } from './StageManager.js';
import { Environment } from './Environment.js';
import { LightingSystem } from '../systems/LightingSystem.js';
import { UIManager } from '../managers/UIManager.js';

export class Game {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.canvas.width = GAME_CONFIG.WIDTH;
        this.canvas.height = GAME_CONFIG.HEIGHT;

        this.assets = new AssetManager();
        this.audio = new AudioManager();
        this.ui = null;
        this.state = 'loading';
        this.hunger = 100;
        this.villagerCount = 100;
        this.level = 1;
        this.score = 0;
        this.combo = 0;
        this.maxCombo = 0;
        this.totalHungerReduced = 0;
        this.selectedFoodKey = 'apple';
        this.gameTime = 0;

        this.lastTime = 0;
        this.villagerTimer = 0;
        this.comboTimer = 0;
        this.consumeInterval = GAME_CONFIG.VILLAGER_CONSUME_INTERVAL;

        // PHASE 7.2: Space bar spam prevention
        this.spacePressed = false;

        this.villagers = [];
        this.flyingFoods = [];
        this.hazards = [];
        this.floatingTexts = [];

        this.caiso = new Caiso();
        this.player = new Player();
        this.joystick = new VirtualJoystick(canvas);
        this.fever = new FeverMode();
        this.distanceBar = new DistanceBarGauge();  // PHASE 7.3: Timing gauge
        this.shake = new ScreenShake();
        this.freeze = new ImpactFrame();

        this.environment = new Environment(this);
        this.lighting = new LightingSystem(this);
        this.stageManager = new StageManager(this);
        this.parallax = new ParallaxSystem(this);
        this.particleSystem = new ParticleSystem(this);

        this.init();
    }

    async init() {
        try {
            await this.assets.loadAll();
            this.ui = new UIManager(this);
            this.state = 'menu';

            this.stageManager.init();
            this.setupEventListeners();
            this.hideLoading();
        } catch (err) {
            console.error("Game init failed:", err);
            this.state = 'menu';
            this.setupEventListeners();
            this.hideLoading();
        }
    }

    hideLoading() {
        setTimeout(() => {
            const loadingScreen = document.getElementById('loadingScreen');
            if (loadingScreen) loadingScreen.style.display = 'none';
        }, 1000);
    }

    setupEventListeners() {
        document.addEventListener('keydown', (e) => this.handleKeyDown(e));
        document.addEventListener('keyup', (e) => this.handleKeyUp(e)); // PHASE 7.2
        const feedBtn = document.getElementById('touchFeedBtn');
        if (feedBtn) feedBtn.addEventListener('click', () => this.feedCaiso());
        this.canvas.addEventListener('click', (e) => this.handleClick(e));
    }

    handleKeyDown(e) {
        if (e.code === 'Space') {
            e.preventDefault();
            // PHASE 7.2: Prevent space bar spam
            if (this.spacePressed) return;
            this.spacePressed = true;

            if (this.state === 'menu') this.startGame();
            else if (this.state === 'playing') this.feedCaiso();
        } else if (e.code === 'KeyR') {
            if (this.state === 'gameover' || this.state === 'victory') this.startGame();
        } else if (e.key >= '1' && e.key <= '6') {
            this.selectFoodByKey(e.key);
        }
    }

    // PHASE 7.2: Reset space bar flag on key release
    handleKeyUp(e) {
        if (e.code === 'Space') {
            this.spacePressed = false;
        }
    }

    handleClick(e) {
        if (this.state === 'menu') this.startGame();
        else if (this.state === 'gameover' || this.state === 'victory') this.startGame();

        if (this.audio && this.audio.ctx.state === 'suspended') {
            this.audio.ctx.resume();
        }
    }

    selectFoodByKey(key) {
        const foodEntries = Object.entries(FOODS);
        const index = parseInt(key) - 1;
        if (index >= 0 && index < foodEntries.length) {
            const [foodKey, food] = foodEntries[index];
            if (food.unlockLevel <= this.level) {
                this.selectedFoodKey = foodKey;
                if (this.ui) this.ui.updateFoodSelection();
            }
        }
    }

    startGame() {
        this.state = 'playing';
        this.hunger = 100;
        this.villagerCount = 100;
        this.level = 1;
        this.score = 0;
        this.combo = 0;
        this.maxCombo = 0;
        this.totalHungerReduced = 0;
        this.selectedFoodKey = 'apple';
        this.gameTime = 0;
        this.villagerTimer = 0;
        this.comboTimer = 0;
        this.consumeInterval = GAME_CONFIG.VILLAGER_CONSUME_INTERVAL;
        this.spacePressed = false; // PHASE 7.2: Reset spam flag
        this.flyingFoods = [];
        this.hazards = [];
        this.floatingTexts = [];
        this.caiso.reset();
        this.fever = new FeverMode();
        this.distanceBar.reset();  // PHASE 7.3: Reset timing gauge
        this.particleSystem.clearEmitters();
        this.particleSystem.active = [];
        this.stageManager.init();

        this.villagers = [];
        for (let i = 0; i < 12; i++) {
            this.spawnVillager(i);
        }

        if (this.audio && this.audio.ctx.state === 'suspended') {
            this.audio.ctx.resume();
        }

        if (this.ui) this.ui.show();

        const feedBtn = document.getElementById('touchFeedBtn');
        if (feedBtn) feedBtn.style.display = 'flex';
    }

    spawnVillager(id) {
        this.villagers.push(new Villager(id, GAME_CONFIG.VILLAGER_SPAWN_Y));
    }

    feedCaiso() {
        if (this.state !== 'playing') return;

        // PHASE 7.2: Prevent touch button spam (same as space bar)
        if (this.spacePressed) return;
        this.spacePressed = true;

        // Reset flag after a short delay (for touch button)
        setTimeout(() => {
            this.spacePressed = false;
        }, 100);

        const food = FOODS[this.selectedFoodKey];
        if (food.unlockLevel > this.level) return;

        // PHASE 7.3: Check timing and get power level
        const timing = this.distanceBar.checkTiming();
        this.distanceBar.triggerFeedback(timing);

        this.player.throw();
        this.audio.play('throw');

        const mouthPos = this.caiso.getMouthPosition();
        const newFood = new Food(
            food,
            this.player.x,
            this.player.y - 40,
            mouthPos.x,
            mouthPos.y,
            this.assets
        );

        // PHASE 7.3: Apply power level from timing
        newFood.powerLevel = timing.power;

        // PHASE 7.3: Handle timing results
        if (timing.result === 'miss') {
            // Miss: Food falls short or overshoots
            newFood.duration = 250;  // Shorter flight time
            this.combo = 0;  // Break combo on miss
            this.addFloatingText('MISS!', this.player.x, this.player.y - 80, timing.color);
            this.audio.play('miss');  // TODO: Add miss sound
        } else if (timing.result === 'perfect') {
            // Perfect: Bonus points and visual feedback
            this.addFloatingText('PERFECT!', this.player.x, this.player.y - 80, timing.color);
            this.score += 50;  // Bonus points for perfect timing
            this.addParticles(this.player.x, this.player.y - 40, timing.color, 8);
        } else {
            // Good: Standard feedback
            this.addFloatingText('GOOD', this.player.x, this.player.y - 80, timing.color);
        }

        this.flyingFoods.push(newFood);
        this.comboTimer = GAME_CONFIG.COMBO_TIMEOUT;
    }

    consumeFood(foodData) {
        const feverMult = this.fever.getMultiplier();
        const comboMult = this.getComboMultiplier();

        // Stage score multiplier
        const stageScoreMult = this.stageManager.currentConfig.gameplay
            ? (this.stageManager.currentConfig.gameplay.scoreMultiplier || 1.0)
            : 1.0;

        const reduction = foodData.hungerReduction * comboMult * feverMult;

        this.hunger = Math.max(0, this.hunger - reduction);
        this.totalHungerReduced += reduction;

        this.combo++;
        if (this.combo > this.maxCombo) this.maxCombo = this.combo;

        const basePoints = Math.round(reduction * 10 * stageScoreMult);
        this.score += basePoints;

        const wasFeverActive = this.fever.active;
        this.fever.charge(FEVER_CONFIG.chargeRate + (this.combo > 3 ? FEVER_CONFIG.comboBonus : 0));
        if (!wasFeverActive && this.fever.active) {
            this.audio.play('fever');
            this.addFloatingText('SOUL SURGE!', GAME_CONFIG.WIDTH / 2, GAME_CONFIG.HEIGHT / 2 - 50, '#74b9ff');
        }

        const newLevel = Math.floor(this.totalHungerReduced / GAME_CONFIG.HUNGER_PER_LEVEL) + 1;
        if (newLevel > this.level) {
            this.levelUp(newLevel);
            this.stageManager.update(0);
        }

        if (this.caiso.updateEvolution(this.level)) {
            const tier = EVOLUTION_TIERS[this.caiso.evolutionTier];
            this.addFloatingText(`EVOLVED: ${tier.name}!`, GAME_CONFIG.WIDTH / 2, 200, '#a29bfe');
            this.addParticles(GAME_CONFIG.WIDTH / 2, 180, '#a29bfe', 15);
            this.audio.play('levelup');
        }

        const mouthPos = this.caiso.getMouthPosition();
        this.addFloatingText(`-${reduction.toFixed(1)}%`, mouthPos.x, mouthPos.y - 60, '#74b9ff');

        if (this.combo >= 3) {
            const comboColors = ['#74b9ff', '#a29bfe', '#dfe6e9', '#ff7675'];
            const colorIdx = Math.min(Math.floor(this.combo / 5), comboColors.length - 1);
            this.addFloatingText(`${this.combo}x COMBO!`, mouthPos.x, mouthPos.y - 90, comboColors[colorIdx]);
            this.audio.play('combo');
        }

        this.addParticles(mouthPos.x, mouthPos.y, foodData.color, 8);
        this.shake.trigger(2, 80);
        this.caiso.eat();
        this.audio.play('eat');

        if (this.hunger <= 0) {
            this.endGame('victory');
        }
    }

    levelUp(newLevel) {
        this.level = newLevel;
        this.addFloatingText(`LEVEL ${newLevel}!`, GAME_CONFIG.WIDTH / 2, 120, '#74b9ff');
        this.addParticles(GAME_CONFIG.WIDTH / 2, 100, '#74b9ff', 12);
        this.audio.play('levelup');

        Object.entries(FOODS).forEach(([key, food]) => {
            if (food.unlockLevel === newLevel) {
                this.addFloatingText(`${food.name} UNLOCKED!`, GAME_CONFIG.WIDTH / 2, 160, food.color);
            }
        });
    }

    getComboMultiplier() {
        if (this.combo >= 15) return 4.0;
        if (this.combo >= 10) return 3.0;
        if (this.combo >= 5) return 2.0;
        if (this.combo >= 3) return 1.5;
        return 1.0;
    }

    consumeVillager() {
        if (this.villagerCount <= 0) return;

        let closestVillager = null;
        let closestDist = Infinity;

        this.villagers.forEach(v => {
            if (v.active && !v.beingEaten) {
                const dist = Math.abs(v.x - this.caiso.x) + Math.abs(v.y - GAME_CONFIG.CAISO_Y);
                if (dist < closestDist) {
                    closestDist = dist;
                    closestVillager = v;
                }
            }
        });

        if (closestVillager) {
            closestVillager.beingEaten = true;
            this.villagerCount--;
            this.addFloatingText('-1', 60, GAME_CONFIG.HEIGHT - 100, '#ff7675');
            this.shake.trigger(3, 100);
            this.caiso.showGuilty();

            if (this.villagerCount > 0) {
                this.spawnVillager(Date.now());
            }

            if (this.villagerCount <= 0) {
                this.endGame('gameover');
            }
        }
    }

    endGame(state) {
        this.state = state;
        this.caiso.expression = state === 'victory' ? 'happy' : 'sad';

        if (state === 'victory') {
            this.addParticles(GAME_CONFIG.WIDTH / 2, GAME_CONFIG.HEIGHT / 3, '#74b9ff', 20);
            this.audio.play('levelup');
        } else {
            this.audio.play('gameover');
        }

        if (this.ui) this.ui.hide();
        const feedBtn = document.getElementById('touchFeedBtn');
        if (feedBtn) feedBtn.style.display = 'none';
    }

    addFloatingText(text, x, y, color) {
        this.floatingTexts.push({ text, x, y, color, alpha: 1, vy: -2.5, life: 50 });
    }

    addParticles(x, y, color, count) {
        this.particleSystem.burst(x, y, color, count);
    }

    update(deltaTime) {
        if (this.state !== 'playing') return;

        this.shake.update(deltaTime);
        if (this.freeze.update(deltaTime)) return;

        this.gameTime += deltaTime;

        this.environment.update(deltaTime);
        this.lighting.update(deltaTime);
        this.stageManager.update(deltaTime);
        if (this.ui) this.ui.update();

        const bgSpeedMult = this.fever.active ? 2.5 : 1.0;
        this.parallax.update(this.player.vx * bgSpeedMult, deltaTime);

        // Particle system (environmental + burst particles)
        this.particleSystem.update(deltaTime);

        // Villager consume timer with difficulty scaling
        let baseInterval = GAME_CONFIG.VILLAGER_CONSUME_INTERVAL;
        baseInterval = Math.max(baseInterval * 0.5, baseInterval - (this.level * 150));
        this.consumeInterval = this.fever.active ? baseInterval * 1.5 : baseInterval;

        this.villagerTimer += deltaTime;
        if (this.villagerTimer >= this.consumeInterval) {
            this.villagerTimer = 0;
            this.consumeVillager();
        }

        // Combo decay
        if (this.comboTimer > 0) {
            this.comboTimer -= deltaTime;
            if (this.comboTimer <= 0) this.combo = 0;
        }

        // Update entities
        this.caiso.update(deltaTime);
        this.player.update(deltaTime, this.joystick);
        this.fever.update(deltaTime);

        // PHASE 7.3: Update distance bar gauge
        this.distanceBar.update(deltaTime);
        this.distanceBar.setDifficulty(this.stageManager.currentStageIndex);

        // Slippery floor effect on player
        if (this.environment.slipperyFloor) {
            this.player.friction = 0.94; // More slippery (default is 0.88)
        } else {
            this.player.friction = 0.88;
        }

        this.villagers.forEach(v => v.update(deltaTime, this.environment));
        this.villagers = this.villagers.filter(v => v.active);

        // Update flying foods with hazard collision and Caiso consumption
        this.flyingFoods.forEach(food => {
            food.update(deltaTime, this.environment);

            // Check hazard collisions
            for (const hazard of this.hazards) {
                const dx = food.x - hazard.x;
                const dy = food.y - hazard.y;
                if (Math.abs(dx) < 30 && Math.abs(dy) < 30) {
                    food.arrived = true;
                    food.blocked = true;
                    this.addParticles(food.x, food.y, '#636e72', 10);
                    break;
                }
            }

            // Check if food reached Caiso's mouth
            if (food.arrived && !food.blocked) {
                const dx = food.x - this.caiso.x;
                const dy = food.y - this.caiso.getMouthPosition().y;
                if (Math.abs(dx) < 60 && Math.abs(dy) < 60) {
                    this.consumeFood(food.foodData);
                }
            }
        });

        this.flyingFoods = this.flyingFoods.filter(f => !f.arrived);

        // Update hazards
        this.hazards.forEach(h => h.update(deltaTime, this.environment));
        this.hazards = this.hazards.filter(h => h.active);

        // Update floating texts
        this.floatingTexts = this.floatingTexts.filter(t => {
            t.y += t.vy;
            t.alpha -= 0.018;
            t.life--;
            return t.life > 0;
        });
    }

    render() {
        const ctx = this.ctx;

        ctx.fillStyle = '#0a0a1a';
        ctx.fillRect(0, 0, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT);

        if (this.state === 'loading') {
            this.drawLoadingScreen();
        } else if (this.state === 'menu') {
            this.drawMenuScreen();
        } else if (this.state === 'playing') {
            this.drawGame();
        } else if (this.state === 'gameover') {
            this.drawGameOverScreen();
        } else if (this.state === 'victory') {
            this.drawVictoryScreen();
        }
    }

    drawGame() {
        const ctx = this.ctx;

        ctx.save();
        this.shake.apply(ctx);

        // 1. Background color
        this.environment.drawBackground(ctx);

        // 2. Parallax layers
        this.parallax.draw(ctx);

        // 3. Environmental particles (behind lighting)
        this.particleSystem.draw(ctx);

        // 4. Dynamic lighting overlay
        this.lighting.draw(ctx);

        // 5. Fever effects
        if (this.fever.active) {
            this.fever.draw(ctx);
        }

        // 6. Danger zone indicator
        const timerProgress = this.villagerTimer / this.consumeInterval;
        ctx.fillStyle = `rgba(255, 118, 117, ${0.03 + timerProgress * 0.1})`;
        ctx.fillRect(0, GAME_CONFIG.CAISO_Y - 80, GAME_CONFIG.WIDTH, 200);

        // 7. Entities
        this.villagers.forEach(v => v.draw(ctx, this.assets));
        this.caiso.draw(ctx, this.assets);
        this.player.draw(ctx, this.assets);
        this.flyingFoods.forEach(food => food.draw(ctx));
        this.hazards.forEach(h => h.draw(ctx));

        // 8. PHASE 7.3: Trajectory preview (shows where food will land)
        this.drawTrajectoryPreview(ctx);

        // 9. PHASE 7.3: Distance bar gauge (timing system)
        this.distanceBar.draw(ctx);

        // 10. Fever gauge
        this.fever.drawGauge(ctx);

        // 11. Score display
        ctx.font = 'bold 14px Fredoka One';
        ctx.textAlign = 'right';
        ctx.fillStyle = 'rgba(223, 230, 233, 0.7)';
        ctx.fillText(`SCORE: ${this.score}`, GAME_CONFIG.WIDTH - 15, GAME_CONFIG.HEIGHT - 155);

        // 12. Stage name (bottom left, subtle)
        if (this.stageManager.currentConfig) {
            ctx.font = '12px Nunito';
            ctx.textAlign = 'left';
            ctx.fillStyle = 'rgba(178, 190, 195, 0.5)';
            ctx.fillText(this.stageManager.currentConfig.name, 15, GAME_CONFIG.HEIGHT - 155);
        }

        // 13. Floating texts
        ctx.font = 'bold 22px Fredoka One';
        ctx.textAlign = 'center';
        this.floatingTexts.forEach(t => {
            ctx.globalAlpha = t.alpha;
            ctx.fillStyle = t.color;
            ctx.fillText(t.text, t.x, t.y);
        });
        ctx.globalAlpha = 1;

        // 12. Joystick
        this.joystick.draw(ctx);

        // 13. Stage transition overlay (topmost)
        this.stageManager.draw(ctx);

        ctx.restore();
    }

    /**
     * PHASE 7.3B: Draw trajectory preview showing where food will land
     * based on current needle position
     *
     * Uses quadratic bezier curve to simulate food flight path
     * Color-coded to match timing result (green/yellow/red)
     */
    drawTrajectoryPreview(ctx) {
        if (this.state !== 'playing') return;

        const timing = this.distanceBar.checkTiming();
        const power = timing.power;

        // Calculate start and end positions
        const startX = this.player.x;
        const startY = this.player.y - 40;
        const mouthPos = this.caiso.getMouthPosition();

        // Apply power multiplier to distance (same as Food.js)
        const distanceMultiplier = 0.5 + power * 0.5;
        const targetX = startX + (mouthPos.x - startX) * distanceMultiplier;
        const targetY = mouthPos.y;

        // Calculate control point for arc (mid-point with height)
        const midX = (startX + targetX) / 2;
        const midY = Math.min(startY, targetY) - 120;  // Arc height

        // Draw dotted trajectory arc
        ctx.save();
        ctx.globalAlpha = 0.5;
        ctx.strokeStyle = timing.color;
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 8]);  // Dotted line pattern

        ctx.beginPath();
        ctx.moveTo(startX, startY);
        ctx.quadraticCurveTo(midX, midY, targetX, targetY);
        ctx.stroke();

        // Draw landing indicator (circle at end point)
        ctx.setLineDash([]);
        ctx.globalAlpha = 0.6;
        ctx.fillStyle = timing.color;
        ctx.beginPath();
        ctx.arc(targetX, targetY, 12, 0, Math.PI * 2);
        ctx.fill();

        // Draw inner circle
        ctx.globalAlpha = 0.3;
        ctx.fillStyle = '#dfe6e9';
        ctx.beginPath();
        ctx.arc(targetX, targetY, 6, 0, Math.PI * 2);
        ctx.fill();

        ctx.restore();
    }

    drawMenuScreen() {
        const ctx = this.ctx;

        // Dark atmospheric gradient
        const grad = ctx.createLinearGradient(0, 0, 0, GAME_CONFIG.HEIGHT);
        grad.addColorStop(0, '#0f0f1b');
        grad.addColorStop(0.4, '#1a1a2e');
        grad.addColorStop(0.7, '#16213e');
        grad.addColorStop(1, '#0f0f1b');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT);

        // Atmospheric dust particles
        const time = Date.now() * 0.001;
        ctx.globalAlpha = 0.3;
        for (let i = 0; i < 15; i++) {
            const px = (Math.sin(time * 0.3 + i * 1.7) * 0.5 + 0.5) * GAME_CONFIG.WIDTH;
            const py = (Math.cos(time * 0.2 + i * 2.1) * 0.5 + 0.5) * GAME_CONFIG.HEIGHT;
            ctx.fillStyle = '#636e72';
            ctx.beginPath();
            ctx.arc(px, py, 2 + Math.sin(time + i) * 1, 0, Math.PI * 2);
            ctx.fill();
        }
        ctx.globalAlpha = 1;

        // Caiso in menu
        ctx.save();
        ctx.translate(0, 100);
        this.caiso.draw(ctx, this.assets);
        ctx.restore();

        // Title
        ctx.fillStyle = '#dfe6e9';
        ctx.font = 'bold 44px Fredoka One';
        ctx.textAlign = 'center';
        ctx.shadowColor = 'rgba(116, 185, 255, 0.5)';
        ctx.shadowBlur = 20;
        ctx.fillText('FEEDING', GAME_CONFIG.WIDTH / 2, 120);
        ctx.fillText('CAISO', GAME_CONFIG.WIDTH / 2, 175);
        ctx.shadowBlur = 0;

        // Subtitle
        ctx.font = 'bold 18px Fredoka One';
        ctx.fillStyle = '#74b9ff';
        ctx.fillText('The Hollow Deep', GAME_CONFIG.WIDTH / 2, 210);

        // Info panel
        const panelY = 530;
        ctx.fillStyle = 'rgba(15, 15, 27, 0.85)';
        if (ctx.roundRect) {
            ctx.beginPath();
            ctx.roundRect(30, panelY, GAME_CONFIG.WIDTH - 60, 160, 12);
            ctx.fill();
        } else {
            ctx.fillRect(30, panelY, GAME_CONFIG.WIDTH - 60, 160);
        }

        // Panel border
        ctx.strokeStyle = 'rgba(116, 185, 255, 0.3)';
        ctx.lineWidth = 1;
        if (ctx.roundRect) {
            ctx.beginPath();
            ctx.roundRect(30, panelY, GAME_CONFIG.WIDTH - 60, 160, 12);
            ctx.stroke();
        }

        ctx.fillStyle = '#b2bec3';
        ctx.font = '14px Nunito';
        ctx.fillText('Feed the Void before it consumes all.', GAME_CONFIG.WIDTH / 2, panelY + 35);
        ctx.fillText('Reduce the Void gauge to 0% to purify.', GAME_CONFIG.WIDTH / 2, panelY + 60);
        ctx.fillText('Drag to move, tap FEED to throw souls.', GAME_CONFIG.WIDTH / 2, panelY + 90);
        ctx.fillText('Build combos for SOUL SURGE!', GAME_CONFIG.WIDTH / 2, panelY + 115);

        // Start prompt
        ctx.font = 'bold 24px Fredoka One';
        ctx.fillStyle = '#74b9ff';
        const pulse = Math.sin(Date.now() / 400) * 0.3 + 0.7;
        ctx.globalAlpha = pulse;
        ctx.fillText('TAP TO ENTER', GAME_CONFIG.WIDTH / 2, 760);
        ctx.globalAlpha = 1;
    }

    drawGameOverScreen() {
        const ctx = this.ctx;

        ctx.fillStyle = 'rgba(10, 5, 15, 0.9)';
        ctx.fillRect(0, 0, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT);

        this.caiso.expression = 'sad';
        this.caiso.draw(ctx, this.assets);

        ctx.fillStyle = '#ff7675';
        ctx.font = 'bold 44px Fredoka One';
        ctx.textAlign = 'center';
        ctx.shadowColor = 'rgba(255, 118, 117, 0.5)';
        ctx.shadowBlur = 15;
        ctx.fillText('SHADE FALLS', GAME_CONFIG.WIDTH / 2, 400);
        ctx.shadowBlur = 0;

        // Stats panel
        ctx.fillStyle = 'rgba(15, 15, 27, 0.8)';
        if (ctx.roundRect) {
            ctx.beginPath();
            ctx.roundRect(80, 440, GAME_CONFIG.WIDTH - 160, 160, 12);
            ctx.fill();
        } else {
            ctx.fillRect(80, 440, GAME_CONFIG.WIDTH - 160, 160);
        }

        ctx.fillStyle = '#dfe6e9';
        ctx.font = '15px Nunito';
        ctx.fillText(`Score: ${this.score}`, GAME_CONFIG.WIDTH / 2, 475);
        ctx.fillText(`Level: ${this.level}`, GAME_CONFIG.WIDTH / 2, 500);
        ctx.fillText(`Max Combo: ${this.maxCombo}x`, GAME_CONFIG.WIDTH / 2, 525);
        ctx.fillText(`Form: ${EVOLUTION_TIERS[this.caiso.evolutionTier].name}`, GAME_CONFIG.WIDTH / 2, 550);
        ctx.fillText(`Time: ${Math.floor(this.gameTime / 1000)}s`, GAME_CONFIG.WIDTH / 2, 575);

        ctx.font = 'bold 20px Fredoka One';
        ctx.fillStyle = '#74b9ff';
        ctx.fillText('TAP TO RETRY', GAME_CONFIG.WIDTH / 2, 650);
    }

    drawVictoryScreen() {
        const ctx = this.ctx;

        // Dark background with soul blue tint
        ctx.fillStyle = 'rgba(10, 15, 30, 0.85)';
        ctx.fillRect(0, 0, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT);

        // Victory particles
        if (Math.random() < 0.12) {
            this.addParticles(
                Math.random() * GAME_CONFIG.WIDTH,
                Math.random() * GAME_CONFIG.HEIGHT / 2,
                ['#74b9ff', '#a29bfe', '#dfe6e9', '#636e72'][Math.floor(Math.random() * 4)],
                4
            );
        }

        // Render burst particles
        this.particleSystem.draw(ctx);

        this.caiso.expression = 'happy';
        this.caiso.draw(ctx, this.assets);

        ctx.fillStyle = '#74b9ff';
        ctx.font = 'bold 44px Fredoka One';
        ctx.textAlign = 'center';
        ctx.shadowColor = 'rgba(116, 185, 255, 0.6)';
        ctx.shadowBlur = 20;
        ctx.strokeStyle = '#dfe6e9';
        ctx.lineWidth = 2;
        ctx.strokeText('PURIFIED', GAME_CONFIG.WIDTH / 2, 400);
        ctx.fillText('PURIFIED', GAME_CONFIG.WIDTH / 2, 400);
        ctx.shadowBlur = 0;

        ctx.fillStyle = '#a29bfe';
        ctx.font = 'bold 16px Fredoka One';
        ctx.fillText('The Void is at peace.', GAME_CONFIG.WIDTH / 2, 435);

        // Stats panel
        ctx.fillStyle = 'rgba(15, 15, 27, 0.8)';
        if (ctx.roundRect) {
            ctx.beginPath();
            ctx.roundRect(80, 460, GAME_CONFIG.WIDTH - 160, 170, 12);
            ctx.fill();
        } else {
            ctx.fillRect(80, 460, GAME_CONFIG.WIDTH - 160, 170);
        }

        ctx.fillStyle = '#dfe6e9';
        ctx.font = '15px Nunito';
        ctx.fillText(`Score: ${this.score}`, GAME_CONFIG.WIDTH / 2, 495);
        ctx.fillText(`Level: ${this.level}`, GAME_CONFIG.WIDTH / 2, 518);
        ctx.fillText(`Max Combo: ${this.maxCombo}x`, GAME_CONFIG.WIDTH / 2, 541);
        ctx.fillText(`Form: ${EVOLUTION_TIERS[this.caiso.evolutionTier].name}`, GAME_CONFIG.WIDTH / 2, 564);
        ctx.fillText(`Masks Saved: ${this.villagerCount}`, GAME_CONFIG.WIDTH / 2, 587);
        ctx.fillText(`Time: ${Math.floor(this.gameTime / 1000)}s`, GAME_CONFIG.WIDTH / 2, 610);

        ctx.font = 'bold 20px Fredoka One';
        ctx.fillStyle = '#74b9ff';
        ctx.fillText('TAP TO PLAY AGAIN', GAME_CONFIG.WIDTH / 2, 680);
    }

    drawLoadingScreen() {
        const ctx = this.ctx;
        ctx.fillStyle = '#0f0f1b';
        ctx.fillRect(0, 0, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT);
        ctx.fillStyle = '#a29bfe';
        ctx.font = '28px Fredoka One';
        ctx.textAlign = 'center';
        ctx.fillText('Entering the Hollow...', GAME_CONFIG.WIDTH / 2, GAME_CONFIG.HEIGHT / 2);
    }

    start() {
        this.lastTime = performance.now();
        requestAnimationFrame((t) => this.gameLoop(t));
    }

    gameLoop(timestamp) {
        const deltaTime = Math.min(timestamp - this.lastTime, 50);
        this.lastTime = timestamp;

        this.update(deltaTime);
        this.render();

        requestAnimationFrame((t) => this.gameLoop(t));
    }
}
