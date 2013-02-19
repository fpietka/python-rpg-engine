# -*- coding: utf-8 -*-
import pygame
import math
import json


class Builder():
    def __init__(self, mapName):
        self.level_map = open("map/" + mapName + ".map", "rb")\
            .read()\
            .split("\n")

        #~ get tiles definitions in file header
        self.tileSize = json.loads(self.level_map.pop(0))

        self.tilesDefinition = list()
        while self.level_map[0] is not '':
            self.tilesDefinition.append(json.loads(self.level_map.pop(0)))
        #~ remove separator line
        self.level_map.pop(0)

        self.level_map = filter(None, self.level_map)
        (self.width, self.height) = (
            len(self.level_map[0]) * self.tileSize['width'],
            len(self.level_map) * self.tileSize['height']
        )
        self.build_tileset()

    def build_tileset(self):
        "Build tile set"
        # load the image with the tiles
        for tilesGroup in self.tilesDefinition:
            fond = pygame.image.load(tilesGroup[0]).convert()
            self.tileset = list()
            for index, map in enumerate(tilesGroup[1]):
                top = map[0]
                left = map[1]
                rect = pygame.Rect(left, top, self.tileSize['width'], self.tileSize['height'])
                subSurface = fond.subsurface(rect)
                self.tileset.append(subSurface)

    def update(self, (x, y), screen_size):
        "Build visible map"
        (width, height) = screen_size
        fond = pygame.Surface((screen_size))

        # @TODO lamba or function for that
        #~ Position in the current cell (px)
        # get position in the world (x, y) and figure out
        # where to start blitting the cell itself
        xPosInCell = x % self.tileSize['width']
        yPosInCell = y % self.tileSize['height']
        #~ number of cells of the area to display
        # according to their size and the display size
        nbCellsWidth = int(
            math.ceil(
                float(xPosInCell + width) / float(self.tileSize['width'])
            )
        )
        nbCellsHeight = int(
            math.ceil(
                float(yPosInCell + height) / float(self.tileSize['height'])
            )
        )
        #~ index of the first cell to display
        startCellIndexX = x / self.tileSize['width']
        startCellIndexY = y / self.tileSize['height']

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
                        index_x * self.tileSize['width'] - xPosInCell,
                        index_y * self.tileSize['height'] - yPosInCell
                    )
                )

        return fond
