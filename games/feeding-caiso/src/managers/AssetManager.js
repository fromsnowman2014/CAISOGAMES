export class AssetManager {
    constructor() {
        this.assets = {};
        this.loadedCount = 0;
        this.totalAssets = 0;
    }

    async loadAll() {
        const assetList = [
            // Caiso (Neon Kawaii)
            { key: 'caiso_idle', src: 'assets/sprites/caiso/caiso_idle.png' },
            { key: 'caiso_hungry', src: 'assets/sprites/caiso/caiso_hungry.png' },
            { key: 'caiso_happy', src: 'assets/sprites/caiso/caiso_happy.png' },

            // Mapping legacy keys to new assets for compatibility
            { key: 'caiso_baby', src: 'assets/sprites/caiso/caiso_idle.png' },
            { key: 'caiso_teen', src: 'assets/sprites/caiso/caiso_idle.png' },
            { key: 'caiso_adult', src: 'assets/sprites/caiso/caiso_idle.png' },
            { key: 'caiso_king', src: 'assets/sprites/caiso/caiso_idle.png' },
            { key: 'caiso_adult_happy', src: 'assets/sprites/caiso/caiso_happy.png' },

            // Player
            { key: 'player_idle', src: 'assets/sprites/player/player_throwing.png' }, // Using throwing sprite as idle for now

            // Villagers
            { key: 'villager_normal', src: 'assets/sprites/villagers/villager_normal.png' },
            { key: 'villager_scared', src: 'assets/sprites/villagers/villager_scared.png' },

            // Foods
            { key: 'food_apple', src: 'assets/items/food_apple.png' },
            { key: 'food_burger', src: 'assets/items/food_burger.png' },
            { key: 'food_pizza', src: 'assets/items/food_pizza.png' },
            { key: 'food_dorito', src: 'assets/items/food_dorito.png' },
            { key: 'food_dynamite', src: 'assets/items/food_dynamite.png' },

            // Backgrounds
            { key: 'title_background', src: 'assets/backgrounds/bg_city.png' },
            { key: 'bg_sky', src: 'assets/backgrounds/bg_sky.png' },
            { key: 'bg_city', src: 'assets/backgrounds/bg_city.png' },
            { key: 'ui_button_feed', src: 'assets/ui/ui_button_feed.png' }
        ];

        this.totalAssets = assetList.length;

        const promises = assetList.map(asset => {
            return new Promise((resolve) => {
                const img = new Image();
                img.onload = () => {
                    this.assets[asset.key] = img;
                    this.loadedCount++;
                    // Optional: Call progress callback
                    resolve();
                };
                img.onerror = () => {
                    console.warn(`Failed to load asset: ${asset.key}`);
                    // Resolve anyway to not block game
                    resolve();
                };
                img.src = asset.src;
            });
        });

        await Promise.all(promises);
        console.log("All assets loaded");
    }

    get(key) {
        return this.assets[key];
    }
}
