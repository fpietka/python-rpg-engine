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
            (0, 4),
            (0, 5),
            (0, 6),
            (0, 7),
            (1, 4),
            (1, 5),
            (1, 6),
            (1, 7),
            (2, 4),
            (2, 5),
            (2, 6),
            (2, 7)
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
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 3),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3)
        ),
        'hitbox': {
            'type': hitbox_types_rect,
            'positionInSprite': (8, 24),
            'size': (16, 8),
        }
    },
    'new': {
        'name': '43510_1256969973.PNG', 'height': 32, 'width': 24, 'map': (
            (0, 0),
            (1, 3),
            (0, 3),
            (2, 3),
            (0, 1),
            (1, 1),
            (2, 1),
            (2, 0),
            (1, 0),
            (0, 2),
            (1, 2),
            (2, 2)
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
