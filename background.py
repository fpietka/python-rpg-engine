# -*- coding: utf-8 -*-
import pygame
import consts
import operator
from map.builder import Builder
from move import move


class Background(object):
    """
    This class handle the created world, with one side the map loaded with
    map.Builder and on the other side the sprites to display on the map.

    The camera and the collisions between the sprites are handled here.
    """

    """
    Class variables to define the available layers
    """
    LAYER_GROUND = 0
    LAYER_CHARACTERS = 1

    def __init__(self, (x, y), fouraxis=True):
        """
        Construct of the class

        Defines some modes (not yet used)
        Creates the builder
        Initializes the sprites groups dict
        Initializes the main sprite
        Set the initial position of the camera

        @param (x, y) Unused
        @param fouraxis Unused default True
        """
        # Set movement type
        self.fouraxis = fouraxis
        self.movesquare = False  # XXX will be used to move full squares

        self.builder = Builder()
        self.sprites = dict()
        self.mainSprite = None
        #coordinates (top left point) of the camera view in the world
        self.xCamera, self.yCamera = 0, 0

    def update(self, screen_size):
        """
        B.update(screen_size)

        Update the visible part of the world.

        This method updates the position of each sprite, according to their
        move pattern, or from some events (key pressed for example), handles
        the collisions, then update the camera position from the main sprite
        position

        @param screen_size tuple containing the dimensions of the area to
            display
        """

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

                #~ This part could be moved in a sprite class
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
        """
        Update the camera position from the main sprite position.
        """

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
        """
        B.setMainSprite(sprite, layer)

        Define a sprite as main sprite.
        The camera is always centered on the main sprite, bounded on the world
        boundaries

        @param sprite pygame.sprite object to define as main sprite
        @param layer if the sprite does not exist in the collection, it'll be
            added in the group matching the layer layer. default
            LAYER_CHARACTER
        """

        self.addSprite(sprite, layer)
        self.mainSprite = sprite

    def addSprite(self, sprite, layer=LAYER_GROUND):
        """
        B.addSprite(sprite, layer)

        Add a sprite in the collection.

        The sprite will be added in the collection associated with the layer
            layer

        @param sprite pygame.sprite object to define as main sprite
        @param layer if the sprite does not exist in the collection, it'll be
            added in the group matching the layer layer. default LAYER_GROUND
        """

        if layer not in self.sprites:
            self.sprites[layer] = pygame.sprite.OrderedUpdates()
        if sprite not in self.sprites[layer]:
            self.sprites[layer].add(sprite)
