#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame, consts



class Player(pygame.sprite.Sprite):
    def __init__(self, tilesGroup):
        super(Player, self).__init__()
        # Spriteset parameters
        # sprite sets, with mapping containing (top, left)
        # choice of the sprite here
        self.spriteset = consts.tiles[tilesGroup]
        self.characterSizeX, self.characterSizeY = self.spriteset['width'], self.spriteset['height']


        # Animation parameters
        self._start = pygame.time.get_ticks()
        self._delay = 10000 / consts.FPS
        self._last_update = 0
        self.frame = 0
        self.animation = .5
        # Handle sprite set
        self.build_spriteset()
        self.direction = list()
        self.default_direction = 'down'
        self.image = self.spritesetDirections['down'][self.frame].convert()
        self.rect = self.image.get_rect()
        self.xPos, self.yPos = 400, 300;
        self.rect.center = (consts.RESOLUTION[0] / 2, consts.RESOLUTION[1] / 2)
        self.x_velocity = 0
        self.y_velocity = 0
        self.speed = 3
        self.movestack = list()
        self.moving = False


    def updatePosition(self, mapSize):
        self.xPos = min(mapSize[0] - self.characterSizeX / 2, max(self.characterSizeX / 2, self.xPos + self.x_velocity))
        self.yPos = min(mapSize[1] - self.characterSizeY / 2, max(self.characterSizeY / 2, self.yPos + self.y_velocity))

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
        try:
            direction = self.default_direction = self.direction[0]
        except IndexError:
            direction = self.default_direction
        self.image = self.spritesetDirections[direction][self.frame].convert()

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

    # TODO refactor, this is ugly
    def accel(self):
        if self.speed == 3:
            self.speed = 6
        if self.x_velocity == 3:
            self.x_velocity = 6
        if self.x_velocity == -3:
            self.x_velocity = -6
        if self.y_velocity == 3:
            self.y_velocity = 6
        if self.y_velocity == -3:
            self.y_velocity = -6

    def decel(self):
        if self.speed == 6:
            self.speed = 3
        if self.x_velocity == 6:
            self.x_velocity = 3
        if self.x_velocity == -6:
            self.x_velocity = -3
        if self.y_velocity == 6:
            self.y_velocity = 3
        if self.y_velocity == -6:
            self.y_velocity = -3

    def movedown(self):
        self.y_velocity += self.speed
        if self.y_velocity != 0:
            self.movestack.append('vertical')
        else:
            self.movestack.remove('vertical')

    def moveup(self):
        self.y_velocity -= self.speed
        if self.y_velocity != 0:
            self.movestack.append('vertical')
        else:
            self.movestack.remove('vertical')

    def moveright(self):
        self.x_velocity += self.speed
        if self.x_velocity != 0:
            self.movestack.append('horizontal')
        else:
            self.movestack.remove('horizontal')

    def moveleft(self):
        self.x_velocity -= self.speed
        if self.x_velocity != 0:
            self.movestack.append('horizontal')
        else:
            self.movestack.remove('horizontal')
