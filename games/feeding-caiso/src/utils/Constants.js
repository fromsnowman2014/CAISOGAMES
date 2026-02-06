export const GAME_CONFIG = {
    WIDTH: 480,
    HEIGHT: 854,
    GRAVITY: 0.6,
    PLAYER_Y: 700,
    CAISO_Y: 180,
    VILLAGER_SPAWN_Y: 880,
    VILLAGER_CONSUME_INTERVAL: 4000,
    COMBO_TIMEOUT: 2000,
    CONTROL_HEIGHT: 180,
    HUD_HEIGHT: 80
};

export const FOODS = {
    apple: { name: 'Apple', color: '#e74c3c', hungerReduction: 8, unlockLevel: 1, asset: 'food_apple', weight: 1.0 },
    burger: { name: 'Burger', color: '#f39c12', hungerReduction: 15, unlockLevel: 2, asset: 'food_burger', weight: 1.2 },
    pizza: { name: 'Pizza', color: '#f1c40f', hungerReduction: 22, unlockLevel: 3, asset: 'food_pizza', weight: 1.4 },
    donut: { name: 'Donut', color: '#e056fd', hungerReduction: 12, unlockLevel: 4, asset: 'food_donut', weight: 0.8 },
    sushi: { name: 'Sushi', color: '#2ecc71', hungerReduction: 30, unlockLevel: 5, asset: 'food_sushi', weight: 1.5 }
};

export const EVOLUTION_TIERS = [
    { level: 1, name: 'Baby Caiso', scale: 0.8, sprite: 'caiso_baby' },
    { level: 3, name: 'Teen Caiso', scale: 1.0, sprite: 'caiso_teen' },
    { level: 6, name: 'Adult Caiso', scale: 1.2, sprite: 'caiso_adult' },
    { level: 10, name: 'King Caiso', scale: 1.5, sprite: 'caiso_king' }
];

export const FEVER_CONFIG = {
    duration: 8000,
    chargeRate: 15,
    decayRate: 0.1,
    comboBonus: 5
};
