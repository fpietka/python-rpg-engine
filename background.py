# -*- coding: utf-8 -*-
import pygame
import consts
import operator
from map.builder import Builder
from map.sprites import SpritesLoader
from move import move


class Background(object):
    LAYER_GROUND = 0
    LAYER_CHARACTERS = 1

    def __init__(self, (x, y), fouraxis=True):
        # Set movement type
        self.fouraxis = fouraxis
        self.movesquare = False  # XXX will be used to move full squares

        self.sprites = dict()
        self.loadMap('level1')
        self.mainSprite = None
        #coordinates (top left point) of the camera view in the world
        self.xCamera, self.yCamera = 0, 0

    def loadMap(self, mapName):
        #~ Build the level's map
        self.builder = Builder(mapName)

        #~ Load the level's sprites
        sprites = SpritesLoader.load(mapName)

        for sprite in sprites:
            self.addSprite(sprite[0], sprite[1])

    def update(self, screen_size):
        for l in self.sprites:
            for s in self.sprites[l]:
                if s.IS_STATIC:
                    continue

                oldPosition = s.getPosition()

                #~ If the sprite has a movement pattern, move it according to
                #~ its current position in the pattern
                if s.movePattern is not None:
                    move.getNextPosition(s, s.movePattern)

                s.updatePosition(
                    s.calculatePosition(
                        (self.builder.width, self.builder.height)
                    )
                )
                s.drawHitBox()
                colliding = pygame.sprite.spritecollide(
                    s.hitBox,
                    [s2.hitBox for s2 in self.sprites[l]],
                    False
                )
                if len(colliding) > 1:
                    s.updatePosition(oldPosition)
                    s.moving = False
                    s.drawHitBox()
                elif s.movePattern is not None:
                    # Get sprites with move patterns move again
                    s.moving = True

                s.updateFrame(pygame.time.get_ticks())

                if s == self.mainSprite:
                    self.updateFocus()

            for s in self.sprites[l]:
                s.draw(self.xCamera, self.yCamera)

        self.fond = self.builder.update(
            (self.xCamera, self.yCamera), screen_size
        )

        # use operator since it's faster than lambda
        cmpfun = operator.attrgetter("yPos")

        for group in self.sprites.itervalues():
            # to debug, display the hitbox
            #~ for sprite in group:
                #~ sprite.image.blit(
                    #~ sprite.hitBox.image,
                    #~ sprite.spriteset['hitbox']['positionInSprite']
                #~ )
            pygame.sprite.OrderedUpdates(
                sorted(group, key=cmpfun)
            ).draw(self.fond)

    def updateFocus(self):
        #get mainSprite (new) coordinates in the world
        xMainSprite, yMainSprite = self.mainSprite.xPos, self.mainSprite.yPos

        #move camera if not out of world boundaries
        self.xCamera = max(
            0,
            min(
                self.builder.width - consts.RESOLUTION[0],
                xMainSprite - consts.RESOLUTION[0] / 2
            )
        )
        self.yCamera = max(
            0,
            min(
                self.builder.height - consts.RESOLUTION[1],
                yMainSprite - consts.RESOLUTION[1] / 2
            )
        )

    def setMainSprite(self, sprite, layer=LAYER_CHARACTERS):
        self.addSprite(sprite, layer)
        self.mainSprite = sprite

    def addSprite(self, sprite, layer=LAYER_GROUND):
        if layer not in self.sprites:
            self.sprites[layer] = pygame.sprite.OrderedUpdates()
        if sprite not in self.sprites[layer]:
            self.sprites[layer].add(sprite)
