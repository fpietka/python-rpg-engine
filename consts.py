# -*- coding: utf-8 -*-

RESOLUTION = 800, 600
FPS = 60

JOYSTICK = {
    "Xbox 360 Wireless Receiver": {
        "up": 13,
        "down": 14,
        "left": 11,
        "right": 12,
        "A": 0,
        "B": 1,
        "X": 2,
        "Y": 3,
        "LB": 4,
        "RB": 5,
        "Back": 6,
        "Start": 7,
        "Xbox": 8,
        "Left stick": 9,
        "Right stick": 10
    }
}

hitbox_types_rect = 1
hitbox_types_circle = 2

tiles = {
    'scholar': {
        'name': 'dpnpcsq.png', 'height': 32, 'width': 32, 'map': (
            (0, 128),
            (0, 160),
            (0, 192),
            (0, 224),
            (32, 128),
            (32, 160),
            (32, 192),
            (32, 224),
            (64, 128),
            (64, 160),
            (64, 192),
            (64, 224)
        ),
        'hitbox': {
            'type': hitbox_types_rect,
            'positionInSprite': (8, 24),
            'size': (16, 8),
        }
    },
    'umbrella': {
        'name': 'dpnpcsq.png', 'height': 32, 'width': 32, 'map': (
            (0, 0),
            (0, 32),
            (0, 64),
            (0, 96),
            (32, 0),
            (32, 32),
            (32, 64),
            (32, 96),
            (64, 0),
            (64, 32),
            (64, 64),
            (64, 96)
        ),
        'hitbox': {
            'type': hitbox_types_rect,
            'positionInSprite': (8, 24),
            'size': (16, 8),
        }
    }
}


movementsPatterns = {
    'rect': {
        'attributes': ('width', 'height')
    }
}
