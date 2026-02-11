import { GAME_CONFIG, FOODS, EVOLUTION_TIERS, FEVER_CONFIG } from '/src/utils/Constants.js';
import { AssetManager } from '/src/managers/AssetManager.js';
import { AudioManager } from '/src/core/Audio.js';
import { VirtualJoystick } from '/src/core/Input.js';
import { ParallaxBackground } from '/src/utils/ParallaxBackground.js';
import { FeverMode } from '/src/utils/FeverMode.js';
import { ScreenShake, ImpactFrame } from '/src/utils/Juice.js';
import { Caiso } from '/src/entities/Caiso.js';
import { Player } from '/src/entities/Player.js';
import { Villager } from '/src/entities/Villager.js';
import { Food } from '/src/entities/Food.js';
import { Hazard } from '/src/entities/Hazard.js';
import { StageManager } from '/src/core/StageManager.js';
import { Environment } from '/src/core/Environment.js';
import { LightingSystem } from '/src/systems/LightingSystem.js';
import { UIManager } from '/src/managers/UIManager.js';

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
        this.combo = 0;
        this.maxCombo = 0;
        this.totalHungerReduced = 0;
        this.selectedFoodKey = 'apple';
        this.gameTime = 0;

        this.lastTime = 0;
        this.villagerTimer = 0;
        this.comboTimer = 0;

        this.villagers = [];
        this.flyingFoods = [];
        this.hazards = [];
        this.particles = [];
        this.floatingTexts = [];

        this.caiso = new Caiso();
        this.player = new Player();
        this.joystick = new VirtualJoystick(canvas);
        this.fever = new FeverMode();
        this.shake = new ScreenShake();
        this.freeze = new ImpactFrame();

        this.environment = new Environment(this);
        this.lighting = new LightingSystem(this);
        this.stageManager = new StageManager(this);

        this.background = null;

        this.init();
    }

    async init() {
        console.log("Feeding Caiso v5.0 - Refactored");
        await this.assets.loadAll();
        this.background = new ParallaxBackground(this.assets);
        this.ui = new UIManager(this);
        this.state = 'menu';

        this.stageManager.init();
        this.setupEventListeners();
        this.hideLoading();
    }

    hideLoading() {
        setTimeout(() => {
            const loadingScreen = document.getElementById('loadingScreen');
            if (loadingScreen) loadingScreen.style.display = 'none';
        }, 1000);
    }

    setupEventListeners() {
        document.addEventListener('keydown', (e) => this.handleKeyDown(e));
        const feedBtn = document.getElementById('touchFeedBtn');
        if (feedBtn) feedBtn.addEventListener('click', () => this.feedCaiso());
        this.canvas.addEventListener('click', (e) => this.handleClick(e));
    }

    handleKeyDown(e) {
        if (e.code === 'Space') {
            e.preventDefault();
            if (this.state === 'menu') this.startGame();
            else if (this.state === 'playing') this.feedCaiso();
        } else if (e.code === 'KeyR') {
            if (this.state === 'gameover' || this.state === 'victory') this.startGame();
        } else if (e.key >= '1' && e.key <= '6') {
            this.selectFoodByKey(e.key);
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
        this.combo = 0;
        this.maxCombo = 0;
        this.totalHungerReduced = 0;
        this.selectedFoodKey = 'apple';
        this.gameTime = 0;
        this.villagerTimer = 0;
        this.comboTimer = 0;
        this.flyingFoods = [];
        this.hazards = [];
        this.particles = [];
        this.floatingTexts = [];
        this.caiso.reset();
        this.fever = new FeverMode();

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

        const food = FOODS[this.selectedFoodKey];
        if (food.unlockLevel > this.level) return;

        this.player.throw();
        this.audio.play('throw');

        const mouthPos = this.caiso.getMouthPosition();
        this.flyingFoods.push(new Food(
            food,
            this.player.x,
            this.player.y - 40,
            mouthPos.x,
            mouthPos.y,
            this.assets
        ));

        this.comboTimer = GAME_CONFIG.COMBO_TIMEOUT;
    }

    consumeFood(foodData) {
        const feverMult = this.fever.getMultiplier();
        const comboMult = this.getComboMultiplier();
        const reduction = foodData.hungerReduction * comboMult * feverMult;

        this.hunger = Math.max(0, this.hunger - reduction);
        this.totalHungerReduced += reduction;

        this.combo++;
        if (this.combo > this.maxCombo) this.maxCombo = this.combo;

        this.fever.charge(FEVER_CONFIG.chargeRate + (this.combo > 3 ? FEVER_CONFIG.comboBonus : 0));

        const newLevel = Math.floor(this.totalHungerReduced / GAME_CONFIG.HUNGER_PER_LEVEL) + 1;
        if (newLevel > this.level) {
            this.levelUp(newLevel);
            this.stageManager.update(0);
        }

        if (this.caiso.updateEvolution(this.level)) {
            const tier = EVOLUTION_TIERS[this.caiso.evolutionTier];
            this.addFloatingText(`EVOLVED: ${tier.name}!`, GAME_CONFIG.WIDTH / 2, 200, '#ff006e');
            this.addParticles(GAME_CONFIG.WIDTH / 2, 180, '#ff006e', 35);
            this.audio.play('levelup');
        }

        const mouthPos = this.caiso.getMouthPosition();
        this.addFloatingText(`-${reduction.toFixed(1)}%`, mouthPos.x, mouthPos.y - 60, '#2ed573');

        if (this.combo >= 3) {
            const comboColors = ['#f1c40f', '#f39c12', '#e74c3c', '#ff006e'];
            const colorIdx = Math.min(Math.floor(this.combo / 5), comboColors.length - 1);
            this.addFloatingText(`${this.combo}x COMBO!`, mouthPos.x, mouthPos.y - 90, comboColors[colorIdx]);
        }

        this.addParticles(mouthPos.x, mouthPos.y, foodData.color, 15);
        this.shake.trigger(5, 150);
        this.freeze.trigger(40);
        this.caiso.eat();
        this.audio.play('eat');

        if (this.hunger <= 0) {
            this.endGame('victory');
        }
    }

    levelUp(newLevel) {
        this.level = newLevel;
        this.addFloatingText(`LEVEL ${newLevel}!`, GAME_CONFIG.WIDTH / 2, 120, '#00d2d3');
        this.addParticles(GAME_CONFIG.WIDTH / 2, 100, '#00d2d3', 25);
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
            this.addFloatingText('-1', 60, GAME_CONFIG.HEIGHT - 100, '#e74c3c');
            this.shake.trigger(8, 200);
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
            this.addParticles(GAME_CONFIG.WIDTH / 2, GAME_CONFIG.HEIGHT / 3, '#ffd700', 60);
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
        for (let i = 0; i < count; i++) {
            this.particles.push({
                x, y,
                vx: (Math.random() - 0.5) * 14,
                vy: (Math.random() - 0.5) * 14 - 5,
                color,
                size: Math.random() * 10 + 4,
                life: 35 + Math.random() * 20
            });
        }
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
        this.background.update(this.player.vx * bgSpeedMult, deltaTime);

        // Villager consume timer with difficulty scaling
        let baseInterval = GAME_CONFIG.VILLAGER_CONSUME_INTERVAL;
        baseInterval = Math.max(baseInterval * 0.5, baseInterval - (this.level * 150));
        const consumeInterval = this.fever.active ? baseInterval * 1.5 : baseInterval;

        this.villagerTimer += deltaTime;
        if (this.villagerTimer >= consumeInterval) {
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

        this.villagers.forEach(v => v.update(deltaTime, this.environment));
        this.villagers = this.villagers.filter(v => v.active);

        // Update flying foods (collect arrived/collided, then process)
        const arrivedFoods = [];
        this.flyingFoods.forEach(food => {
            food.update(deltaTime, this.environment);

            // Check hazard collisions
            for (const hazard of this.hazards) {
                const dx = food.x - hazard.x;
                const dy = food.y - hazard.y;
                if (Math.abs(dx) < 30 && Math.abs(dy) < 30) {
                    food.arrived = true;
                    this.addParticles(food.x, food.y, '#fff', 10);
                    break;
                }
            }

            if (food.arrived) {
                arrivedFoods.push(food);
            }
        });

        // Remove arrived foods and consume
        this.flyingFoods = this.flyingFoods.filter(f => !f.arrived);
        arrivedFoods.forEach(food => {
            // Only consume if it reached Caiso (not blocked by hazard)
            const dx = food.x - this.caiso.x;
            const dy = food.y - this.caiso.getMouthPosition().y;
            if (Math.abs(dx) < 60 && Math.abs(dy) < 60) {
                this.consumeFood(food.foodData);
            }
        });

        // Update hazards
        this.hazards.forEach(h => h.update(deltaTime, this.environment));
        this.hazards = this.hazards.filter(h => h.active);

        // Update particles
        this.particles = this.particles.filter(p => {
            p.x += p.vx;
            p.y += p.vy;
            p.vy += 0.35;
            p.life--;
            return p.life > 0;
        });

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

        this.environment.drawBackground(ctx);
        this.background.draw(ctx);
        this.lighting.draw(ctx);

        if (this.fever.active) {
            this.fever.draw(ctx);
        }

        // Danger zone indicator
        const timerProgress = this.villagerTimer / GAME_CONFIG.VILLAGER_CONSUME_INTERVAL;
        ctx.fillStyle = `rgba(231, 76, 60, ${0.05 + timerProgress * 0.15})`;
        ctx.fillRect(0, GAME_CONFIG.CAISO_Y - 80, GAME_CONFIG.WIDTH, 200);

        this.villagers.forEach(v => v.draw(ctx, this.assets));
        this.caiso.draw(ctx, this.assets);
        this.player.draw(ctx, this.assets);
        this.flyingFoods.forEach(food => food.draw(ctx));
        this.hazards.forEach(h => h.draw(ctx));

        // Draw particles
        this.particles.forEach(p => {
            ctx.globalAlpha = p.life / 55;
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.globalAlpha = 1;

        // Draw floating texts
        ctx.font = 'bold 22px Fredoka One';
        ctx.textAlign = 'center';
        this.floatingTexts.forEach(t => {
            ctx.globalAlpha = t.alpha;
            ctx.fillStyle = t.color;
            ctx.fillText(t.text, t.x, t.y);
        });
        ctx.globalAlpha = 1;

        this.joystick.draw(ctx);

        ctx.restore();
    }

    drawMenuScreen() {
        const ctx = this.ctx;

        const titleBg = this.assets.get('title_background');
        if (titleBg) {
            ctx.drawImage(titleBg, 0, 0, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT);
        } else {
            const grad = ctx.createLinearGradient(0, 0, 0, GAME_CONFIG.HEIGHT);
            grad.addColorStop(0, '#1a1a2e');
            grad.addColorStop(0.5, '#16213e');
            grad.addColorStop(1, '#0f3460');
            ctx.fillStyle = grad;
            ctx.fillRect(0, 0, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT);

            ctx.save();
            ctx.translate(0, 100);
            this.caiso.draw(ctx, this.assets);
            ctx.restore();
        }

        ctx.fillStyle = '#fff';
        ctx.font = 'bold 48px Fredoka One';
        ctx.textAlign = 'center';
        ctx.shadowColor = 'rgba(108, 52, 131, 0.8)';
        ctx.shadowBlur = 15;
        ctx.shadowOffsetX = 3;
        ctx.shadowOffsetY = 3;
        ctx.fillText('FEEDING', GAME_CONFIG.WIDTH / 2, 120);
        ctx.fillText('CAISO', GAME_CONFIG.WIDTH / 2, 175);
        ctx.shadowBlur = 0;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 0;

        ctx.font = 'bold 20px Fredoka One';
        ctx.fillStyle = '#ffe066';
        ctx.fillText('Save the Villagers!', GAME_CONFIG.WIDTH / 2, 215);

        const panelY = 530;
        ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
        if (ctx.roundRect) {
            ctx.beginPath();
            ctx.roundRect(30, panelY, GAME_CONFIG.WIDTH - 60, 160, 15);
            ctx.fill();
        } else {
            ctx.fillRect(30, panelY, GAME_CONFIG.WIDTH - 60, 160);
        }

        ctx.fillStyle = '#fff';
        ctx.font = '15px Nunito';
        ctx.fillText('Feed Caiso before it eats all villagers!', GAME_CONFIG.WIDTH / 2, panelY + 35);
        ctx.fillText('Reduce hunger to 0% to WIN!', GAME_CONFIG.WIDTH / 2, panelY + 65);
        ctx.fillText('Drag to move, tap FEED to throw food', GAME_CONFIG.WIDTH / 2, panelY + 95);
        ctx.fillText('Build combos for FEVER MODE!', GAME_CONFIG.WIDTH / 2, panelY + 125);

        ctx.font = 'bold 28px Fredoka One';
        ctx.fillStyle = '#f1c40f';
        const pulse = Math.sin(Date.now() / 300) * 0.3 + 0.7;
        ctx.globalAlpha = pulse;
        ctx.fillText('TAP TO START', GAME_CONFIG.WIDTH / 2, 760);
        ctx.globalAlpha = 1;
    }

    drawGameOverScreen() {
        const ctx = this.ctx;

        ctx.fillStyle = 'rgba(0, 0, 0, 0.85)';
        ctx.fillRect(0, 0, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT);

        this.caiso.expression = 'sad';
        this.caiso.draw(ctx, this.assets);

        ctx.fillStyle = '#e74c3c';
        ctx.font = 'bold 48px Fredoka One';
        ctx.textAlign = 'center';
        ctx.fillText('GAME OVER', GAME_CONFIG.WIDTH / 2, 400);

        ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
        if (ctx.roundRect) {
            ctx.beginPath();
            ctx.roundRect(80, 450, GAME_CONFIG.WIDTH - 160, 140, 15);
            ctx.fill();
        } else {
            ctx.fillRect(80, 450, GAME_CONFIG.WIDTH - 160, 140);
        }

        ctx.fillStyle = '#fff';
        ctx.font = '16px Nunito';
        ctx.fillText(`Final Level: ${this.level}`, GAME_CONFIG.WIDTH / 2, 485);
        ctx.fillText(`Max Combo: ${this.maxCombo}x`, GAME_CONFIG.WIDTH / 2, 515);
        ctx.fillText(`Evolution: ${EVOLUTION_TIERS[this.caiso.evolutionTier].name}`, GAME_CONFIG.WIDTH / 2, 545);
        ctx.fillText(`Time: ${Math.floor(this.gameTime / 1000)}s`, GAME_CONFIG.WIDTH / 2, 575);

        ctx.font = 'bold 20px Fredoka One';
        ctx.fillStyle = '#f1c40f';
        ctx.fillText('TAP TO RETRY', GAME_CONFIG.WIDTH / 2, 650);
    }

    drawVictoryScreen() {
        const ctx = this.ctx;

        ctx.fillStyle = 'rgba(46, 204, 113, 0.25)';
        ctx.fillRect(0, 0, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT);

        this.particles.forEach(p => {
            ctx.globalAlpha = p.life / 55;
            ctx.fillStyle = p.color;
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.globalAlpha = 1;

        this.caiso.expression = 'happy';
        this.caiso.draw(ctx, this.assets);

        ctx.fillStyle = '#2ecc71';
        ctx.font = 'bold 48px Fredoka One';
        ctx.textAlign = 'center';
        ctx.strokeStyle = '#fff';
        ctx.lineWidth = 3;
        ctx.strokeText('YOU WIN!', GAME_CONFIG.WIDTH / 2, 400);
        ctx.fillText('YOU WIN!', GAME_CONFIG.WIDTH / 2, 400);

        ctx.fillStyle = '#f1c40f';
        ctx.font = 'bold 18px Fredoka One';
        ctx.fillText('Caiso is full! Villagers are safe!', GAME_CONFIG.WIDTH / 2, 440);

        ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
        if (ctx.roundRect) {
            ctx.beginPath();
            ctx.roundRect(80, 470, GAME_CONFIG.WIDTH - 160, 160, 15);
            ctx.fill();
        } else {
            ctx.fillRect(80, 470, GAME_CONFIG.WIDTH - 160, 160);
        }

        ctx.fillStyle = '#fff';
        ctx.font = '16px Nunito';
        ctx.fillText(`Final Level: ${this.level}`, GAME_CONFIG.WIDTH / 2, 505);
        ctx.fillText(`Max Combo: ${this.maxCombo}x`, GAME_CONFIG.WIDTH / 2, 535);
        ctx.fillText(`Evolution: ${EVOLUTION_TIERS[this.caiso.evolutionTier].name}`, GAME_CONFIG.WIDTH / 2, 565);
        ctx.fillText(`Villagers Saved: ${this.villagerCount}`, GAME_CONFIG.WIDTH / 2, 595);
        ctx.fillText(`Time: ${Math.floor(this.gameTime / 1000)}s`, GAME_CONFIG.WIDTH / 2, 620);

        ctx.font = 'bold 20px Fredoka One';
        ctx.fillStyle = '#f1c40f';
        ctx.fillText('TAP TO PLAY AGAIN', GAME_CONFIG.WIDTH / 2, 680);

        if (Math.random() < 0.12) {
            this.addParticles(
                Math.random() * GAME_CONFIG.WIDTH,
                Math.random() * GAME_CONFIG.HEIGHT / 2,
                ['#f1c40f', '#2ecc71', '#e74c3c', '#9b59b6', '#3498db'][Math.floor(Math.random() * 5)],
                4
            );
        }
    }

    drawLoadingScreen() {
        const ctx = this.ctx;
        ctx.fillStyle = '#1a1a2e';
        ctx.fillRect(0, 0, GAME_CONFIG.WIDTH, GAME_CONFIG.HEIGHT);
        ctx.fillStyle = '#a29bfe';
        ctx.font = '28px Fredoka One';
        ctx.textAlign = 'center';
        ctx.fillText('Loading...', GAME_CONFIG.WIDTH / 2, GAME_CONFIG.HEIGHT / 2);
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
