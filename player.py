# -*- coding: utf-8 -*-
import pygame
import consts
import math
import move
import sprite


class Player(sprite.DynamicSprite):
    def __init__(self, options, fouraxis=False):
        super(Player, self).__init__()

        self.fouraxis = fouraxis
        # based on pririty by orientation
        # XXX we can also do a priority by last input
        self.movement_priority = 'vertical'

        # Spriteset parameters
        self.spriteset = consts.tiles[options['tilesGroup']]
        self.characterSizeX, self.characterSizeY =\
            self.spriteset['width'], self.spriteset['height']

        # Animation parameters
        self._start = pygame.time.get_ticks()
        self._delay = 10000 / consts.FPS
        self._last_update = 0
        self.frame = 0
        self.animation = .5
        # Handle sprite set
        self.build_spriteset()
        self.direction = 'down'
        self.updateDirection()
        self.rect = self.image.get_rect()
        self.xPos, self.yPos = options['x'], options['y']
        self.rect.center = [dimension / 2 for dimension in consts.RESOLUTION]
        self.moveX, self.moveY = 0, 0
        self.speed = 3
        self.moving = False
        self._createHitBox()

        if 'movePattern' not in options:
            self.movePattern = None
        else:
            if 'type' not in options['movePattern']:
                raise move.exception('A move pattern type is required')
            if 'attributes' not in options['movePattern']:
                raise move.exception('Move pattern attributes are required')
            self.movePattern = options['movePattern']
            self.movePattern['attributes']['topLeft'] = (self.xPos, self.yPos)

    def updateDirection(self):
        direction = self.spritesetDirections[self.direction][self.frame]
        self.image = direction.convert()

    def _createHitBox(self):
        self.hitBox = pygame.sprite.Sprite()
        self.hitBox.image = pygame.Surface(self.spriteset['hitbox']['size'])
        self.hitBox.image.fill((0, 0, 0))
        #handle other hitbox types
        self.hitBox.rect = self.hitBox.image.get_rect()

    def calculatePosition(self, mapSize):
        if self.moveX == 0 or self.moveY == 0:
            x_velocity = int(self.moveX * self.speed)
            y_velocity = int(self.moveY * self.speed)
        elif self.fouraxis:
            if self.movement_priority == 'horizontal':
                x_velocity = int(self.moveX * self.speed)
                if x_velocity == 0:
                    y_velocity = int(self.moveY * self.speed)
                else:
                    y_velocity = 0
            elif self.movement_priority == 'vertical':
                y_velocity = int(self.moveY * self.speed)
                if y_velocity == 0:
                    x_velocity = int(self.moveX * self.speed)
                else:
                    x_velocity = 0
        else:
            x_velocity = int(self.moveX * self.speed / math.sqrt(2))
            y_velocity = int(self.moveY * self.speed / math.sqrt(2))

        return (
            min(
                mapSize[0] - self.characterSizeX / 2,
                max(
                    self.characterSizeX / 2,
                    self.xPos + x_velocity
                )
            ),
            min(
                mapSize[1] - self.characterSizeY / 2,
                max(
                    self.characterSizeY / 2,
                    self.yPos + y_velocity
                )
            )
        )

    def updatePosition(self, position):
        self.xPos, self.yPos = position
        # Set moving
        self.moving = not (self.moveX, self.moveY) == (0, 0)

    def draw(self, x, y):
        self.rect.center = (self.xPos - x, self.yPos - y)

    def drawHitBox(self):
        self.hitBox.rect.center = map(
            sum,
            zip(
                (self.xPos, self.yPos),
                self.spriteset['hitbox']['positionInSprite']
            )
        )

    def getPosition(self):
        return (self.xPos, self.yPos)

    def updateFrame(self, tick):
        if not self.moving:
            self.frame = 0
        elif tick - self._last_update > self._delay:
            self._last_update = tick
            # frame should go 0, 1, 0, 2, 0, 1, ...
            if not self.animation == int(self.animation):
                self.frame = 0
            elif self.animation / 2 == int(self.animation / 2):
                self.frame = 1
            else:
                self.frame = 2
            self.animation += .5

        if self.moveX < 0:
            self.direction = 'left'
        if self.moveX > 0:
            self.direction = 'right'
        if self.moveY < 0:
            self.direction = 'up'
        if self.moveY > 0:
            self.direction = 'down'

        self.updateDirection()

    def build_spriteset(self):
        "Cut and build sprite set"
        fond = pygame.image.load(self.spriteset['name']).convert()
        fond.set_colorkey(
            fond.get_at(next(iter(self.spriteset['map'])))
        )
        width = self.spriteset['width']
        height = self.spriteset['height']
        # use map to cut parts
        spriteset = list()
        for (left, top) in self.spriteset['map']:
            rect = pygame.Rect(left, top, width, height)
            spriteset.append(fond.subsurface(rect).convert())
        # build direction there
        self.spritesetDirections = {
            'up': (spriteset[0], spriteset[8], spriteset[7]),
            'down': (spriteset[9], spriteset[10], spriteset[11]),
            'left': (spriteset[2], spriteset[1], spriteset[3]),
            'right': (spriteset[4], spriteset[5], spriteset[6])
        }

    def moveVertical(self, coef=1):
        self.moveY += coef

    def moveHorizontal(self, coef=1):
        self.moveX += coef

    def stop(self):
        self.moveX = self.moveY = 0
