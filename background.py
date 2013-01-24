#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame, consts, operator
from move import move

class Background(object):
    LAYER_GROUND = 0
    LAYER_CHARACTERS = 1

    def __init__(self, builder, fouraxis=True):
        # Set movement type
        self.fouraxis = fouraxis
        self.movesquare = False # XXX will be used to move full squares

        self.builder = builder

        self.sprites = dict()
        self.mainSprite = None
        #coordinates (top left point) of the camera view in the world
        self.xCamera, self.yCamera = 0, 0;

    def update(self):
        # use operator since it's faster than lambda
        cmpfun = operator.attrgetter("yPos")
        for l in self.sprites:
            for s in self.sprites[l]:
                if s.IS_STATIC:
                    continue

                #~ If the sprite has a movement pattern, move it according to its
                #~ current position in the pattern
                if s.movePattern != None:
                    move.getNextPosition (s, s.movePattern)

                s.updatePosition(s.calculatePosition((self.builder.width, self.builder.height)))

                s.updateFrame(pygame.time.get_ticks())

                if s == self.mainSprite:
                    self.updateFocus()

            self.sprites[l] = pygame.sprite.RenderUpdates(sorted(self.sprites[l], key=cmpfun))

            for s in self.sprites[l]:
                s.draw()

        self.builder.update((self.xCamera, self.yCamera))

        for group in self.sprites.itervalues():
            group.draw(self.builder.fond)


    def updateFocus(self):
        #get mainSprite (new) coordinates in the world
        xMainSprite, yMainSprite = self.mainSprite.xPos, self.mainSprite.yPos

        #move camera if not out of world boundaries
        self.xCamera = max(0, min(self.builder.width - consts.RESOLUTION[0], xMainSprite - consts.RESOLUTION[0] / 2))
        self.yCamera = max(0, min(self.builder.height - consts.RESOLUTION[1], yMainSprite - consts.RESOLUTION[1] / 2))


    def setMainSprite(self, sprite, layer = LAYER_CHARACTERS):
        self.addSprite(sprite, layer)
        self.mainSprite = sprite

    def addSprite(self, sprite, layer = LAYER_GROUND):
        if not self.sprites.has_key(layer):
            self.sprites[layer] = pygame.sprite.RenderUpdates()
        if sprite not in self.sprites[layer]:
            self.sprites[layer].add(sprite)
