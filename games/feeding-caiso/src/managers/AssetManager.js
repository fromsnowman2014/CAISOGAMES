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

            // Player (Little Ghost)
            { key: 'player_idle', src: 'assets/sprites/player/player_throwing.png' },

            // Villagers (Husks)
            { key: 'villager_normal', src: 'assets/sprites/villagers/villager_normal.png' },
            { key: 'villager_scared', src: 'assets/sprites/villagers/villager_scared.png' },

            // Items (keys match FOODS for compatibility)
            { key: 'food_apple', src: 'assets/items/food_apple.png' },
            { key: 'food_burger', src: 'assets/items/food_burger.png' },
            { key: 'food_pizza', src: 'assets/items/food_pizza.png' },
            { key: 'food_dorito', src: 'assets/items/food_dorito.png' },
            { key: 'food_watermelon', src: 'assets/items/food_watermelon.png' },
            { key: 'food_dynamite', src: 'assets/items/food_dynamite.png' },

            // UI
            { key: 'title_background', src: 'assets/ui/title_background.png' },
            { key: 'ui_button_feed', src: 'assets/ui/ui_button_feed.png' },

            // Stage 1: Crossroads backgrounds (initial load)
            { key: 'bg_crossroads_far', src: 'assets/backgrounds/bg_crossroads_far.png' },
            { key: 'bg_crossroads_mid', src: 'assets/backgrounds/bg_crossroads_mid.png' },
            { key: 'bg_crossroads_near', src: 'assets/backgrounds/bg_crossroads_near.png' }
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
    }

    get(key) {
        return this.assets[key];
    }

    async preloadStageAssets(parallaxConfig) {
        if (!parallaxConfig || !parallaxConfig.layers) return;

        const promises = parallaxConfig.layers.map(layer => {
            if (this.assets[layer.key]) return Promise.resolve();
            return new Promise((resolve) => {
                const img = new Image();
                img.onload = () => {
                    this.assets[layer.key] = img;
                    resolve();
                };
                img.onerror = () => {
                    resolve();
                };
                img.src = `assets/backgrounds/${layer.key}.png`;
            });
        });

        await Promise.all(promises);
    }
}
