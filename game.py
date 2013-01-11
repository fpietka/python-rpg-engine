#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame, consts
from map.builder import Builder
from background import Background
import player

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(consts.RESOLUTION)
        self.builder = Builder()
        self.fond = self.builder.load(self.screen, (0, 0))
        # Blit background
        self.screen.blit(self.fond, (0, 0))
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        self.background = Background(self.builder)
        # TODO avoid acting on sprite and do actions on group?
        self.player = player.Player({
            'tilesGroup': 'umbrella',
            'x': 400,
            'y': 300
        })
        self.background.setMainSprite(self.player)

    def run(self):
        running = True
        # run until an event tells us to stop
        while running:
            pygame.time.Clock().tick(consts.FPS)
            running = self.handleEvents()
            self.background.update()

            rect = pygame.Rect(self.background.xCamera, self.background.yCamera, consts.RESOLUTION[0], consts.RESOLUTION[1])
            self.fond = self.builder.fond.subsurface(rect)
            self.screen.blit(self.fond, (0, 0))
            # update part of the script
            rect = pygame.Rect(0, 0, 800, 600)
            pygame.display.update(rect)

    def handleEvents(self):
        # poll for pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # handle user input
            elif event.type == pygame.KEYDOWN:
                # if the user presses escape or 'q', quit the event loop.
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    return False
                # handle speed
                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    self.player.accel()
                # movement control
                if event.key == pygame.K_UP:
                    self.player.direction.append('up')
                    self.player.moveup()
                if event.key == pygame.K_DOWN:
                    self.player.direction.append('down')
                    self.player.movedown()
                if event.key == pygame.K_LEFT:
                    self.player.direction.append('left')
                    self.player.moveleft()
                if event.key == pygame.K_RIGHT:
                    self.player.direction.append('right')
                    self.player.moveright()
                if event.key == pygame.K_c:
                    #~ create new sprite
                    s = player.Player({
                        'tilesGroup': 'scholar',
                        'x': 300,
                        'y': 300
                    })
                    self.background.addSprite(s, Background.LAYER_CHARACTERS)
            elif event.type == pygame.KEYUP:
                # handle speed
                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    self.player.decel()
                # stop movement control
                if event.key == pygame.K_UP:
                    self.player.direction.remove('up')
                    self.player.movedown()
                if event.key == pygame.K_DOWN:
                    self.player.direction.remove('down')
                    self.player.moveup()
                if event.key == pygame.K_LEFT:
                    self.player.direction.remove('left')
                    self.player.moveright()
                if event.key == pygame.K_RIGHT:
                    self.player.direction.remove('right')
                    self.player.moveleft()

        # TODO make the sprite move too
        return True
