#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame, consts

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
        for l in self.sprites:
            for s in self.sprites[l]:
                s.updatePosition((self.builder.width, self.builder.height))
                s.updateFrame(pygame.time.get_ticks())

            if s == self.mainSprite:
                self.updateFocus()

        self.builder.update((self.xCamera, self.yCamera))

        for l in self.sprites:
            for s in self.sprites[l]:
                for g in s.groups():
                    g.draw(self.builder.fond)


    def updateFocus(self):
        #get mainSprite (new) coordinates in the world
        xMainSprite, yMainSprite = self.mainSprite.xPos, self.mainSprite.yPos

        #move camera if not out of world boundaries
        self.xCamera = max(0, min(self.builder.width - consts.RESOLUTION[0], xMainSprite - consts.RESOLUTION[0] / 2))
        self.yCamera = max(0, min(self.builder.height - consts.RESOLUTION[1], yMainSprite - consts.RESOLUTION[1] / 2))


    def setMainSprite(self, sprite):
        self.addSprite(sprite, Background.LAYER_CHARACTERS)
        self.mainSprite = sprite

    def addSprite(self, sprite, layer = LAYER_GROUND):
        if not self.sprites.has_key(layer):
            self.sprites[layer] = pygame.sprite.Group()
        if sprite not in self.sprites[layer]:
            self.sprites[layer].add(sprite)
