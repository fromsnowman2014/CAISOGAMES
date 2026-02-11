export class AssetManager {
    constructor() {
        this.assets = {};
        this.loadedCount = 0;
        this.totalAssets = 0;
    }

    async loadAll() {
        const assetList = [
            // Caiso expressions
            { key: 'caiso_idle', src: 'assets/sprites/caiso/caiso_idle.png' },
            { key: 'caiso_hungry', src: 'assets/sprites/caiso/caiso_hungry.png' },
            { key: 'caiso_happy', src: 'assets/sprites/caiso/caiso_happy.png' },
            { key: 'caiso_sad', src: 'assets/sprites/caiso/caiso_sad.png' },

            // Player
            { key: 'player_idle', src: 'assets/sprites/player/player_throwing.png' },

            // Villagers
            { key: 'villager_normal', src: 'assets/sprites/villagers/villager_normal.png' },
            { key: 'villager_scared', src: 'assets/sprites/villagers/villager_scared.png' },

            // Foods (aligned with Constants.js FOODS)
            { key: 'food_apple', src: 'assets/items/food_apple.png' },
            { key: 'food_burger', src: 'assets/items/food_burger.png' },
            { key: 'food_pizza', src: 'assets/items/food_pizza.png' },
            { key: 'food_dorito', src: 'assets/items/food_dorito.png' },
            { key: 'food_watermelon', src: 'assets/items/food_watermelon.png' },
            { key: 'food_dynamite', src: 'assets/items/food_dynamite.png' },

            // Backgrounds
            { key: 'title_background', src: 'assets/ui/title_background.png' },
            { key: 'bg_sky', src: 'assets/backgrounds/bg_sky.png' },
            { key: 'bg_clouds', src: 'assets/backgrounds/bg_clouds.png' },
            { key: 'bg_city', src: 'assets/backgrounds/bg_city.png' },
            { key: 'bg_ground', src: 'assets/backgrounds/bg_ground.png' },

            // UI
            { key: 'ui_button_feed', src: 'assets/ui/ui_button_feed.png' }
        ];

        this.totalAssets = assetList.length;

        const promises = assetList.map(asset => {
            return new Promise((resolve) => {
                const img = new Image();
                img.onload = () => {
                    this.assets[asset.key] = img;
                    this.loadedCount++;
                    resolve();
                };
                img.onerror = () => {
                    console.warn(`Failed to load asset: ${asset.key}`);
                    resolve();
                };
                img.src = asset.src;
            });
        });

        await Promise.all(promises);
        console.log(`Assets loaded: ${this.loadedCount}/${this.totalAssets}`);
    }

    get(key) {
        return this.assets[key];
    }
}
