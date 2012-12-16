#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame, consts

class Background(object):
    def __init__(self, builder, fouraxis=True):
        # Set movement type
        self.fouraxis = fouraxis
        self.movesquare = False # XXX will be used to move full squares

        self.builder = builder

        self.sprites = list()
        self.mainSprite = None
        #coordinates (top left point) of the camera view in the world
        self.xCamera, self.yCamera = 0, 0;

    def update(self):
        for s in self.sprites:
            s.updatePosition((self.builder.width, self.builder.height))
            s.updateFrame(pygame.time.get_ticks())

            if s == self.sprites[self.mainSprite]:
                self.updateFocus()

        self.builder.update((self.xCamera, self.yCamera))

        for s in self.sprites:
            for g in s.groups():
                g.draw(self.builder.fond)


    def updateFocus(self):
        #get mainSprite (new) coordinates in the world
        xMainSprite, yMainSprite = self.sprites[self.mainSprite].xPos, self.sprites[self.mainSprite].yPos

        #move camera if not out of world boundaries
        self.xCamera = max(0, min(self.builder.width - consts.RESOLUTION[0], xMainSprite - consts.RESOLUTION[0] / 2))
        self.yCamera = max(0, min(self.builder.height - consts.RESOLUTION[1], yMainSprite - consts.RESOLUTION[1] / 2))


    def setMainSprite(self, sprite):
        self.setSprite(sprite)
        self.mainSprite = self.sprites.index(sprite)

    def setSprite(self, sprite):
        if sprite not in self.sprites:
            self.sprites.append(sprite)
