"""
Background-specific prompt templates

These templates help generate game backgrounds suitable for
parallax scrolling and various game environments
"""

BACKGROUND_TEMPLATES = {
    # Nature environments
    'forest': {
        'base': "game background forest scene",
        'modifiers': ['trees', 'foliage', 'natural lighting'],
        'technical': 'parallax-ready, layered depth, wide composition',
        'layers': ['distant trees', 'mid-ground bushes', 'foreground elements'],
    },
    'meadow': {
        'base': "game background meadow landscape",
        'modifiers': ['grass field', 'flowers', 'open sky'],
        'technical': 'horizontal scrolling friendly, peaceful atmosphere',
    },
    'mountain': {
        'base': "game background mountain vista",
        'modifiers': ['peaks', 'distant horizon', 'atmospheric perspective'],
        'technical': 'layered for parallax, majestic scale',
    },

    # Village/town
    'village': {
        'base': "game background village scene",
        'modifiers': ['houses', 'streets', 'cozy atmosphere'],
        'technical': 'detailed enough for exploration, clear paths',
    },
    'market': {
        'base': "game background marketplace",
        'modifiers': ['stalls', 'colorful awnings', 'busy atmosphere'],
        'technical': 'interactive-looking elements, NPCs space',
    },

    # Fantasy
    'castle': {
        'base': "game background castle scene",
        'modifiers': ['stone walls', 'towers', 'medieval fantasy'],
        'technical': 'grand scale, clear architectural elements',
    },
    'dungeon': {
        'base': "game background dungeon interior",
        'modifiers': ['stone corridors', 'torches', 'mysterious'],
        'technical': 'dark atmosphere, light sources for contrast',
    },
    'magic_forest': {
        'base': "game background enchanted forest",
        'modifiers': ['glowing elements', 'magical plants', 'mystical atmosphere'],
        'technical': 'fantasy colors, ethereal lighting',
    },

    # Sky/space
    'sky_day': {
        'base': "game background daytime sky",
        'modifiers': ['clouds', 'blue gradient', 'sunny'],
        'technical': 'simple tiling, cheerful atmosphere',
    },
    'sky_night': {
        'base': "game background night sky",
        'modifiers': ['stars', 'moon', 'dark blue gradient'],
        'technical': 'twinkling stars effect, atmospheric',
    },
    'space': {
        'base': "game background outer space",
        'modifiers': ['stars', 'nebulae', 'planets'],
        'technical': 'scrolling friendly, cosmic scale',
    },

    # Urban
    'city': {
        'base': "game background city skyline",
        'modifiers': ['buildings', 'urban environment', 'modern'],
        'technical': 'layered buildings for depth, clean silhouettes',
    },

    # Abstract/simple
    'gradient': {
        'base': "simple game background color gradient",
        'modifiers': ['smooth transition', 'complementary colors'],
        'technical': 'minimal, performance-friendly, mood-setting',
    },
}

def get_background_template(bg_type: str) -> dict:
    """Get template for specific background type"""
    return BACKGROUND_TEMPLATES.get(bg_type, BACKGROUND_TEMPLATES['meadow'])
