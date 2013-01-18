#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame, consts



class Player(pygame.sprite.Sprite):
    def __init__(self, options):
        super(Player, self).__init__()
        # Spriteset parameters
        self.spriteset = consts.tiles[options['tilesGroup']]
        self.characterSizeX, self.characterSizeY = self.spriteset['width'], self.spriteset['height']


        # Animation parameters
        self._start = pygame.time.get_ticks()
        self._delay = 10000 / consts.FPS
        self._last_update = 0
        self.frame = 0
        self.animation = .5
        # Handle sprite set
        self.build_spriteset()
        self.direction = 'down'
        self.image = self.spritesetDirections[self.direction][self.frame].convert()
        self.rect = self.image.get_rect()
        self.xPos, self.yPos = options['x'], options['y']
        self.rect.center = (consts.RESOLUTION[0] / 2, consts.RESOLUTION[1] / 2)
        self.x_velocity, self.y_velocity = 0, 0
        self.speed = 3
        self.moving = False

        if not options.has_key('movePattern'):
            self.movePattern = None
        else:
            if not options['movePattern'].has_key('type'):
                raise move.exception('A move pattern type is required')
            if not options['movePattern'].has_key('attributes'):
                raise move.exception('Move pattern attributes are required')
            self.movePattern = options['movePattern']
            self.movePattern['attributes']['topLeft'] = (self.xPos, self.yPos)

    def calculatePosition(self, mapSize):
        return (
            min(mapSize[0] - self.characterSizeX / 2, max(self.characterSizeX / 2, self.xPos + self.x_velocity)),
            min(mapSize[1] - self.characterSizeY / 2, max(self.characterSizeY / 2, self.yPos + self.y_velocity))
        )

    def updatePosition(self, position):
        self.xPos = position[0]
        self.yPos = position[1]

        self.rect.center = (self.xPos, self.yPos)

        # Set moving
        if self.x_velocity == 0 and self.y_velocity == 0:
            self.moving = False
        else:
            self.moving = True

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

        if self.x_velocity < 0:
            self.direction = 'left'
        if self.x_velocity > 0:
            self.direction = 'right'
        if self.y_velocity < 0:
            self.direction = 'up'
        if self.y_velocity > 0:
            self.direction = 'down'

        self.image = self.spritesetDirections[self.direction][self.frame].convert()

    def build_spriteset(self):
        "Cut and build sprite set"
        self.fond = pygame.image.load(self.spriteset['name']).convert()
        self.fond.set_colorkey(self.fond.get_at(next(iter(self.spriteset['map']))))
        width = self.spriteset['width']
        height = self.spriteset['height']
        # use map to cut parts
        spriteset = list()
        for (left, top) in self.spriteset['map']:
            rect = pygame.Rect(left, top, width, height)
            spriteset.append(self.fond.subsurface(rect))
        # build direction there
        self.spritesetDirections = {
            'up': (spriteset[0], spriteset[8], spriteset[7]),
            'down': (spriteset[9], spriteset[10], spriteset[11]),
            'left': (spriteset[2], spriteset[1], spriteset[3]),
            'right': (spriteset[4], spriteset[5], spriteset[6])
        }

    def moveup(self):
        self.y_velocity += self.speed

    def movedown(self):
        self.y_velocity -= self.speed

    def moveleft(self):
        self.x_velocity += self.speed

    def moveright(self):
        self.x_velocity -= self.speed

    def movefulldown(self):
        self.x_velocity = 0
        self.movedown()

    def movefullup(self):
        self.x_velocity = 0
        self.moveup()

    def movefullright(self):
        self.y_velocity = 0
        self.moveright()

    def movefullleft(self):
        self.y_velocity = 0
        self.moveleft()
