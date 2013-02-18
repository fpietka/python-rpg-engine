# -*- coding: utf-8 -*-
import pygame
import math

"""
Description of the map to use
"""
tileset_config = {
    'name': 'GRS2ROC.bmp', 'height': 40, 'width': 40, 'map': (
        (80, 40),
        (80, 120),
        (80, 200),
        (80, 280),  # full grass
        (160, 40),
        (160, 120),  # full stone
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
    """
    Class to build the world

    The purpose of this class is to create a picture from a tiles set and a map
    description.
    """

    def __init__(self):
        """
        Construct of the class.

        This method:
            - loads a .map file containing the map description (which tile to
        use at each coordinate of the map)
            - loads the availables tiles for the map as surfaces in a list
        """
        self.level_map = filter(
            None,
            open("map/level1.map", "rb").read().split("\n")
        )
        (self.width, self.height) = (
            len(self.level_map[0]) * tileset_config['width'],
            len(self.level_map) * tileset_config['height']
        )
        self.build_tileset()

    def build_tileset(self):
        """
        Build tiles set

        This method loads the availables tiles for the map as surfaces in a list
        """
        # load the image with the tiles
        resource = pygame.image.load(tileset_config['name']).convert()
        # get width/height from config
        width = tileset_config['width']
        height = tileset_config['height']
        self.tileset = list()
        # cut out tiles from tileset
        for index, mapcells in enumerate(tileset_config['map']):
            top, left = mapcells
            rect = pygame.Rect(left, top, width, height)
            subSurface = resource.subsurface(rect)
            # add subsurface to the collection
            self.tileset.append(subSurface)

    def update(self, (x, y), (width, height)):
        """
        B.update((x, y), (width, height)) -> pygame.Surface

        Build visible map

        This method take in arguments an area described with a tuple for it's
        top-left position and a tuple for it's width-height.
        The visible section of the map is got from this area and a surface is created
        with the visible tiles.

        param
        """

        fond = pygame.Surface((width, height))

        # @TODO lamba or function for that
        #~ Position in the current cell (px)
        # get position in the world (x, y) and figure out
        # where to start blitting the cell itself
        xPosInCell = x % tileset_config['width']
        yPosInCell = y % tileset_config['height']
        #~ number of cells of the area to display
        # according to their size and the display size
        nbCellsWidth = int(
            math.ceil(
                float(xPosInCell + width) / float(tileset_config['width'])
            )
        )
        nbCellsHeight = int(
            math.ceil(
                float(yPosInCell + height) / float(tileset_config['height'])
            )
        )
        #~ index of the first cell to display
        startCellIndexX = x / tileset_config['width']
        startCellIndexY = y / tileset_config['height']

        lines = enumerate(
            range(startCellIndexY, startCellIndexY + nbCellsHeight), 0
        )
        for index_y, line in lines:
            columns = enumerate(
                range(startCellIndexX, startCellIndexX + nbCellsWidth), 0
            )
            for index_x, column in columns:
                square = self.level_map[line][column]
                if square == '#':
                    tile = self.tileset[3]
                elif square == '.':
                    tile = self.tileset[5]

                fond.blit(
                    tile,
                    (
                        index_x * tileset_config['width'] - xPosInCell,
                        index_y * tileset_config['height'] - yPosInCell
                    )
                )

        return fond
