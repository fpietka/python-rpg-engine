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
        self.level_map = open("map/level1.map", "rb").read().split("\n")
        (self.width, self.height) = (len(self.level_map[0]) * tileset_config['width'], len(self.level_map) *
                tileset_config['height'])
    def load(self):
        pygame.init()

        RESOLUTION = 800, 600
        self.screen = pygame.display.set_mode(RESOLUTION)

        # build tileset
        self.fond = pygame.image.load(tileset_config['name']).convert()
        width = tileset_config['width']
        height = tileset_config['height']
        tileset = list()
        for index, map in enumerate(tileset_config['map']):
            top = map[0]
            left = map[1]
            rect = pygame.Rect(left, top, width, height)
            subSurface = self.fond.subsurface(rect)
            tileset.append(subSurface)

        # display tiles
        # read map
        # TODO read line by line?
        # XXX start with current script root?
        level_map = open("map/level1.map", "rb").read().split("\n")
        for index_y, line in enumerate(level_map, 0):
            if index_y == 0:
                self.fond = pygame.Surface((len(line) * 40, len(level_map) * 40))
                self.fond.fill((255, 0, 255))
            for index_x, square in enumerate(line, 0):
                if square == '#':
                    tile = tileset[3]
                elif square == '.':
                    tile = tileset[5]
                # XXX handle there properties for neighbour tiles XXX
                # XXX gecode?
                self.fond.blit(tile, (index_x * 40, index_y * 40))

        return self.fond

    def make_problem(self, block_size=40):
        pass

# create a game and run it
if __name__ == '__main__':
    builder = Builder()
    builder.run()
