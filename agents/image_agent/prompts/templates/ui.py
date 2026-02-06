"""
UI-specific prompt templates

These templates help generate game UI elements like
buttons, panels, icons, and other interface components
"""

UI_TEMPLATES = {
    # Buttons
    'button_normal': {
        'base': "game UI button",
        'modifiers': ['rounded corners', 'clear edges', 'pressable look'],
        'technical': 'multiple states possible (normal, hover, pressed)',
        'states': ['normal', 'hover', 'pressed', 'disabled'],
    },
    'button_icon': {
        'base': "game UI icon button",
        'modifiers': ['circular', 'centered icon', 'clear action'],
        'technical': 'recognizable at 32x32, touch-friendly size',
    },

    # Panels
    'panel_dialog': {
        'base': "game UI dialog panel",
        'modifiers': ['text-friendly area', 'decorative border', 'semi-transparent'],
        'technical': '9-slice compatible, scalable',
    },
    'panel_inventory': {
        'base': "game UI inventory panel",
        'modifiers': ['grid-friendly', 'item slots', 'organized layout'],
        'technical': 'clear item boundaries, scalable grid',
    },
    'panel_tooltip': {
        'base': "game UI tooltip panel",
        'modifiers': ['small', 'informative', 'unobtrusive'],
        'technical': 'fits text well, arrow pointer optional',
    },

    # Icons
    'icon_action': {
        'base': "game UI action icon",
        'modifiers': ['clear symbol', 'single concept', 'bold'],
        'technical': 'readable at 24x24, high contrast',
    },
    'icon_status': {
        'base': "game UI status icon",
        'modifiers': ['health/mana style', 'progress indicator'],
        'technical': 'fillable design, clear empty vs full state',
    },
    'icon_item': {
        'base': "game UI item icon",
        'modifiers': ['detailed but clear', 'recognizable item'],
        'technical': 'fits in inventory slot, distinctive silhouette',
    },

    # Bars
    'bar_health': {
        'base': "game UI health bar",
        'modifiers': ['red gradient', 'clear fill level', 'medical cross'],
        'technical': 'horizontal fill, empty and full states',
    },
    'bar_energy': {
        'base': "game UI energy bar",
        'modifiers': ['blue or yellow', 'lightning symbol optional'],
        'technical': 'fillable, segmented optional',
    },
    'bar_progress': {
        'base': "game UI progress bar",
        'modifiers': ['generic fill bar', 'percentage indicator'],
        'technical': 'scalable width, clear progress indication',
    },

    # Decorations
    'frame_portrait': {
        'base': "game UI portrait frame",
        'modifiers': ['decorative border', 'character-sized opening'],
        'technical': 'fits character portrait, stylish border',
    },
    'border_decorative': {
        'base': "game UI decorative border",
        'modifiers': ['ornate', 'corner pieces', 'edge pieces'],
        'technical': '9-slice ready, tileable edges',
    },

    # Special
    'cursor': {
        'base': "game UI cursor pointer",
        'modifiers': ['clear tip', 'visible against backgrounds'],
        'technical': 'hot spot at tip, multiple states (normal, hover, click)',
    },
    'notification': {
        'base': "game UI notification badge",
        'modifiers': ['attention-grabbing', 'exclamation or number'],
        'technical': 'small but visible, animated-friendly',
    },
}

def get_ui_template(ui_type: str) -> dict:
    """Get template for specific UI element type"""
    return UI_TEMPLATES.get(ui_type, UI_TEMPLATES['button_normal'])
