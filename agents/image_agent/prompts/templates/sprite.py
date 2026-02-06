"""
Sprite-specific prompt templates

These templates help generate consistent, game-ready sprites
"""

SPRITE_TEMPLATES = {
    # Character sprites
    'character_idle': {
        'base': "game character sprite in idle pose, front view",
        'modifiers': ['standing still', 'relaxed pose', 'facing viewer'],
        'technical': 'single frame, centered, clear silhouette',
    },
    'character_walk': {
        'base': "game character sprite in walking pose, side view",
        'modifiers': ['mid-stride', 'dynamic pose', 'profile view'],
        'technical': 'animation frame, centered, consistent proportions',
    },
    'character_jump': {
        'base': "game character sprite jumping, side view",
        'modifiers': ['arms up', 'legs bent', 'upward motion'],
        'technical': 'action pose, exaggerated motion',
    },
    'character_attack': {
        'base': "game character sprite in attack pose",
        'modifiers': ['action pose', 'weapon swing', 'combat stance'],
        'technical': 'dynamic angle, clear action lines',
    },

    # Food sprites (for games like Feeding Caiso)
    'food_fruit': {
        'base': "cute cartoon fruit sprite",
        'modifiers': ['kawaii style', 'simple face optional', 'appetizing colors'],
        'technical': 'simple shape, bold colors, game-ready',
    },
    'food_snack': {
        'base': "cute cartoon snack food sprite",
        'modifiers': ['colorful', 'appealing', 'simple design'],
        'technical': 'clear silhouette, icon-like simplicity',
    },

    # Monster/creature sprites
    'creature_blob': {
        'base': "cute blob creature sprite",
        'modifiers': ['round shape', 'simple features', 'expressive eyes'],
        'technical': 'simple silhouette, easy to animate',
    },
    'creature_monster': {
        'base': "friendly monster character sprite",
        'modifiers': ['non-threatening', 'colorful', 'unique design'],
        'technical': 'distinctive shape, game-friendly',
    },

    # Item sprites
    'item_collectible': {
        'base': "game collectible item sprite",
        'modifiers': ['shiny', 'valuable appearance', 'eye-catching'],
        'technical': 'recognizable at small size, high contrast',
    },
    'item_powerup': {
        'base': "game power-up item sprite",
        'modifiers': ['glowing effect', 'magical appearance', 'special'],
        'technical': 'stands out from background, animated-friendly',
    },

    # NPC sprites
    'npc_villager': {
        'base': "simple villager character sprite",
        'modifiers': ['friendly appearance', 'simple clothes', 'neutral pose'],
        'technical': 'generic enough for variety, clear silhouette',
    },
}

def get_sprite_template(sprite_type: str) -> dict:
    """Get template for specific sprite type"""
    return SPRITE_TEMPLATES.get(sprite_type, SPRITE_TEMPLATES['character_idle'])
