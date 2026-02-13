import { FOODS, GAME_CONFIG } from '../utils/Constants.js';

export class UIManager {
    constructor(game) {
        this.game = game;
        this.uiLayer = document.getElementById('ui-layer');
        this.levelBadge = document.getElementById('level-badge');
        this.hungerBar = document.getElementById('hunger-bar');
        this.hungerText = document.getElementById('hunger-text');
        this.comboDisplay = document.getElementById('combo-display');
        this.villagerCount = document.getElementById('villager-count');
        this.foodSelector = document.getElementById('food-selector');
        this.dangerBar = document.getElementById('danger-bar-fill');

        this.lastHunger = -1;
        this.lastLevel = -1;
        this.lastVillagers = -1;
        this.lastCombo = -1;

        this.setupFoodSelector();
    }

    setupFoodSelector() {
        this.foodSelector.innerHTML = '';
        Object.entries(FOODS).forEach(([key, food]) => {
            const div = document.createElement('div');
            div.className = 'food-item';
            div.dataset.key = key;
            div.onclick = () => {
                if (this.game.level >= food.unlockLevel) {
                    this.game.selectedFoodKey = key;
                    this.updateFoodSelection();
                }
            };

            const img = this.game.assets.get(food.asset);
            if (img) {
                const imgClone = img.cloneNode();
                imgClone.className = 'food-icon';
                div.appendChild(imgClone);
            } else {
                div.innerText = food.name[0];
            }

            this.foodSelector.appendChild(div);
        });
    }

    updateFoodSelection() {
        const items = this.foodSelector.children;
        for (let item of items) {
            const key = item.dataset.key;
            const food = FOODS[key];
            const isUnlocked = this.game.level >= food.unlockLevel;
            const isSelected = this.game.selectedFoodKey === key;

            item.className = 'food-item' + (isSelected ? ' selected' : '') + (!isUnlocked ? ' locked' : '');
        }
    }

    update() {
        if (this.game.state !== 'playing') return;

        // Hunger
        if (Math.abs(this.game.hunger - this.lastHunger) > 0.1) {
            this.hungerBar.style.width = `${this.game.hunger}%`;
            this.hungerText.innerText = `${this.game.hunger.toFixed(1)}%`;

            if (this.game.hunger > 50) this.hungerBar.style.background = 'linear-gradient(90deg, #e74c3c, #c0392b)';
            else if (this.game.hunger > 25) this.hungerBar.style.background = 'linear-gradient(90deg, #f39c12, #e67e22)';
            else this.hungerBar.style.background = 'linear-gradient(90deg, #2ecc71, #27ae60)';

            this.lastHunger = this.game.hunger;
        }

        // Level
        if (this.game.level !== this.lastLevel) {
            this.levelBadge.innerText = this.game.level;
            this.updateFoodSelection();
            this.lastLevel = this.game.level;
        }

        // Villagers
        if (this.game.villagerCount !== this.lastVillagers) {
            this.villagerCount.innerText = this.game.villagerCount;
            if (this.game.villagerCount > 50) this.villagerCount.style.color = '#2ecc71';
            else if (this.game.villagerCount > 25) this.villagerCount.style.color = '#f39c12';
            else this.villagerCount.style.color = '#e74c3c';

            this.lastVillagers = this.game.villagerCount;
        }

        // Combo
        if (this.game.combo !== this.lastCombo) {
            if (this.game.combo >= 3) {
                this.comboDisplay.innerText = `x${this.game.combo}`;
                this.comboDisplay.style.opacity = 1;
            } else {
                this.comboDisplay.style.opacity = 0;
            }
            this.lastCombo = this.game.combo;
        }

        // Danger Timer - use actual computed interval from Game
        const progress = this.game.villagerTimer / this.game.consumeInterval;
        this.dangerBar.style.width = `${Math.min(progress * 100, 100)}%`;
    }

    show() {
        this.uiLayer.style.display = 'block';
        this.updateFoodSelection();
    }

    hide() {
        this.uiLayer.style.display = 'none';
    }
}
