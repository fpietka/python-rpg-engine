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


class Builder():
    def __init__(self):
        self.level_map = open("map/level1.map", "rb").read().split("\n")
        (self.height, self.width) = (len(self.level_map) * tileset_config['height'], len(self.level_map[0]) *
                tileset_config['width'])

    def load(self, screen, (x, y)):
        self.screen_size = screen.get_size()
        self.build_tileset()
        # display tiles
        self.fond = pygame.Surface(self.screen_size)
        return self.update((x, y))

    def build_tileset(self):
        "Build tile set"

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
        (width, height) = self.screen_size

        import math
        x_pos = x % tileset_config['width']
        y_pos = y % tileset_config['height']

        # @TODO lamba or function for that
        nb_width = int(math.ceil(float(x % tileset_config['width'] + width) / float(tileset_config['width'])))
        nb_height = int(math.ceil(float(y % tileset_config['height'] + height) / float(tileset_config['height'])))

        x_start = x / tileset_config['width']
        y_start = y / tileset_config['height']

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
