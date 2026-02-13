export const GAME_CONFIG = {
    WIDTH: 480,
    HEIGHT: 854,
    GRAVITY: 0.6,
    PLAYER_Y: 700,
    CAISO_Y: 180,
    VILLAGER_SPAWN_Y: 620,
    VILLAGER_CONSUME_INTERVAL: 4000,
    COMBO_TIMEOUT: 2000,
    CONTROL_HEIGHT: 180,
    HUD_HEIGHT: 80,
    HUNGER_PER_LEVEL: 4
};

export const FOODS = {
    apple:      { name: 'Soul Orb',      color: '#74b9ff', hungerReduction: 8,  unlockLevel: 1, asset: 'food_apple',      weight: 1.0 },
    burger:     { name: 'Geo Cluster',   color: '#b2bec3', hungerReduction: 15, unlockLevel: 2, asset: 'food_burger',     weight: 1.2 },
    pizza:      { name: 'Pale Ore',      color: '#dfe6e9', hungerReduction: 22, unlockLevel: 3, asset: 'food_pizza',      weight: 1.4 },
    dorito:     { name: "King's Idol",   color: '#ffeaa7', hungerReduction: 12, unlockLevel: 4, asset: 'food_dorito',     weight: 0.8 },
    watermelon: { name: 'Lifeblood',     color: '#0984e3', hungerReduction: 30, unlockLevel: 5, asset: 'food_watermelon', weight: 1.5 },
    dynamite:   { name: 'Void Egg',      color: '#a29bfe', hungerReduction: 40, unlockLevel: 7, asset: 'food_dynamite',   weight: 2.0 }
};

export const EVOLUTION_TIERS = [
    { level: 1,  name: 'Grub',        scale: 0.8, sprite: 'caiso_idle' },
    { level: 3,  name: 'Husk',        scale: 1.0, sprite: 'caiso_idle' },
    { level: 6,  name: 'Knight',      scale: 1.2, sprite: 'caiso_idle' },
    { level: 10, name: 'Shade Lord',  scale: 1.5, sprite: 'caiso_idle' }
];

export const FEVER_CONFIG = {
    duration: 8000,
    gaugeMax: 100,
    chargeRate: 15,
    decayRate: 0.1,
    comboBonus: 5,
    scoreMultiplier: 2.0
};
