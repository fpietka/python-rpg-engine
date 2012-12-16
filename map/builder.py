#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
try:
    import constraint
except ImportError:
    print "You will need python-constraint module ... eventually"

tileset_config = {
    'name': 'GRS2ROC.bmp', 'height': 40, 'width': 40, 'map': (
        (80, 40),
        (80, 120),
        (80, 200),
        (80, 280), # full grass
        (160, 40),
        (160, 120), # full stone
        (160, 200),
        (160, 280),
        (160, 360),
        (240, 40),
        (240, 120),
        (240, 200),
        (240, 280),
        (240, 360)
    )}

# XXX can be probably done in two properties by side
tileset_properties = (
        {'top': 'ggg', 'bottom': 'gss', 'left': 'ggg', 'right': 'gss'},
        {'top': 'ggg', 'bottom': 'sss', 'left': 'gss', 'right': 'gss'},
        {'top': 'ggg', 'bottom': 'ssg', 'left': 'gss', 'right': 'ggg'},
        {'top': 'ggg', 'bottom': 'ggg', 'left': 'ggg', 'right': 'ggg'},
        {'top': 'gss', 'bottom': 'gss', 'left': 'ggg', 'right': 'sss'},
        {'top': 'sss', 'bottom': 'sss', 'left': 'sss', 'right': 'sss'},
        {'top': 'ssg', 'bottom': 'ssg', 'left': 'sss', 'right': 'ggg'},
        {'top': 'gss', 'bottom': 'sss', 'left': 'gss', 'right': 'sss'},
        {'top': 'ssg', 'bottom': 'sss', 'left': 'sss', 'right': 'gss'},
        {'top': 'gss', 'bottom': 'ggg', 'left': 'ggg', 'right': 'ssg'},
        {'top': 'sss', 'bottom': 'ggg', 'left': 'ssg', 'right': 'ssg'},
        {'top': 'ssg', 'bottom': 'ggg', 'left': 'ssg', 'right': 'ggg'},
        {'top': 'sss', 'bottom': 'gss', 'left': 'ssg', 'right': 'sss'},
        {'top': 'sss', 'bottom': 'ssg', 'left': 'sss', 'right': 'ssg'}
    )

class Builder():
    def __init__(self):
        self.level_map = filter(None, open("map/level1.map", "rb").read().split("\n"))
        (self.width, self.height) = (len(self.level_map[0]) * tileset_config['width'], len(self.level_map) *
                tileset_config['height'])
    def load(self, screen, (x, y)):
        self.screen_size = screen.get_size()
        self.build_tileset()
        # display tiles

        return self.update((x, y))

    def build_tileset(self):
        "Build tile set"
        """
        from xml.dom import minidom
        from base64 import b64decode
        from zlib import decompress

        data = minidom.parse('map.tmx').documentElement

        for layer in data.getElementsByTagName('layer'):
            element = layer.getElementsByTagName('data')[0].firstChild.data
            for char in decompress(b64decode(element)):
                if ord(char) not in (0, 40):
                    print ord(char)

        """
        fond = pygame.image.load(tileset_config['name']).convert()
        width = tileset_config['width']
        height = tileset_config['height']
        self.tileset = list()
        for index, map in enumerate(tileset_config['map']):
            top = map[0]
            left = map[1]
            rect = pygame.Rect(left, top, width, height)
            subSurface = fond.subsurface(rect)
            self.tileset.append(subSurface)
        return self

    def update(self, (x, y)):
        "Build visible map"
        self.fond = pygame.Surface((self.width, self.height))
        (width, height) = self.screen_size

        import math
        x_pos = x % tileset_config['width']
        y_pos = y % tileset_config['height']

        # @TODO lamba or function for that
        nb_width = int(math.ceil(float(x % tileset_config['width'] + width) / float(tileset_config['width'])))
        nb_height = int(math.ceil(float(y % tileset_config['height'] + height) / float(tileset_config['height'])))

        x_start = x / tileset_config['width']
        y_start = y / tileset_config['height']
        #~ print tileset_config['width'], x, x_start, x_start + nb_width
        for index_y, line in enumerate(range(y_start, y_start + nb_height), 0):
            for index_x, column in enumerate(range(x_start, x_start + nb_width), 0):
                #print (line, column)
                square = self.level_map[line][column]
                if square == '#':
                    tile = self.tileset[3]
                elif square == '.':
                    tile = self.tileset[5]
                self.fond.blit(tile, ((index_x * 40) - x_pos, (index_y * 40) - y_pos))
        return self.fond

# create a game and run it
if __name__ == '__main__':
    builder = Builder()
    builder.run()
