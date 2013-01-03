#!/usr/bin/python
# -*- coding: utf-8 -*-

RESOLUTION = 800, 600
FPS = 60

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
            'positionFromCenter': (0, 8),
            'size': (16, 16),
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
            'positionFromCenter': (0, 8),
            'size': (16, 16),
        }
    }
}


movementsPatterns = {
    'rect': {
        'attributes': ('width', 'height')
    }
}
