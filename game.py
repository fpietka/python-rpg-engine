# -*- coding: utf-8 -*-
import pygame
import consts
from background import Background
import player

from os import getpid

try:
    import psutil
except ImportError:
    print "Missing needed module: python-psutil"
    import sys
    sys.exit(1)

from lib.debug import Debug

class Game():
    def __init__(self, debug=False):
        pygame.init()

        # XXX clean up
        self.label = dict()
        self.debug = debug

        self.screen = pygame.display.set_mode(consts.RESOLUTION)
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        # Blit background
        self.background = Background((0, 0))
        # TODO avoid acting on sprite and do actions on group?
        self.player = player.Player({
            'tilesGroup': 'umbrella',
            'x': 400,
            'y': 300
        })
        self.background.setMainSprite(self.player)
        self.clock = pygame.time.Clock()
        self.process = psutil.Process(getpid())
        self.cpu = self.process.get_cpu_percent(interval=0.0)
        self.memory = str(self.process.get_memory_info()[0] / 1024 / 1024) + ' Mb'

    def run(self):
        running = True
        if self.debug:
            # Initialize debug
            running_time = 0
            last_time = 0
        # run until an event tells us to stop
        while running:
            if self.debug:
                running_time += self.clock.tick(consts.FPS)
                if running_time - last_time >= 3000:
                    last_time = running_time
                    self.cpu = self.process.get_cpu_percent(interval=0.0)
                    self.memory = str(self.process.get_memory_info()[0] / 1024 / 1024) + ' Mb'
                Debug.post("RAM", self.memory)
                Debug.post("CPU", self.cpu)
                Debug.post("FPS", "%.2f" % self.clock.get_fps())

            running = self.handleEvents()
            self.background.update(self.screen.get_size())

            camera = - self.background.xCamera, - self.background.yCamera

            # Display all post that occured before that line
            if self.debug and self.label:
                for key, value in enumerate(self.label.itervalues(), 1):
                    self.background.fond.blit(value, (10, key * 14))

            self.screen.blit(self.background.fond, (0, 0))
            # update screen
            rect = pygame.Rect(
                0,
                0,
                consts.RESOLUTION[0],
                consts.RESOLUTION[1]
            )
            pygame.display.update(rect)

    def handleEvents(self):
        # poll for pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == Debug.DEBUG:
                myfont = pygame.font.SysFont("monospace", 15)
                message = event.message.popitem()
                self.label[message[0]] = myfont.render(message[1], 1, (255, 255, 0))
            # handle user input
            elif event.type == pygame.KEYDOWN:
                # if the user presses escape or 'q', quit the event loop.
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    return False
                # handle speed
                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    self.player.speed = 6
                # movement control
                if event.key == pygame.K_UP:
                    self.player.moveVertical(-1)
                if event.key == pygame.K_DOWN:
                    self.player.moveVertical(1)
                if event.key == pygame.K_LEFT:
                    self.player.moveHorizontal(-1)
                if event.key == pygame.K_RIGHT:
                    self.player.moveHorizontal(1)
                if event.key == pygame.K_c:
                    #~ create new sprite
                    s = player.Player({
                        'tilesGroup': 'scholar',
                        'x': 300,
                        'y': 300,
                        'movePattern': {
                            'type': 'rect',
                            'attributes': {
                                'width': 200,
                                'height': 200
                            }
                        }
                    })
                    self.background.addSprite(s, Background.LAYER_CHARACTERS)
            elif event.type == pygame.KEYUP:
                # handle speed
                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    self.player.speed = 3
                # stop movement control
                if event.key == pygame.K_UP:
                    self.player.moveVertical(1)
                if event.key == pygame.K_DOWN:
                    self.player.moveVertical(-1)
                if event.key == pygame.K_LEFT:
                    self.player.moveHorizontal(1)
                if event.key == pygame.K_RIGHT:
                    self.player.moveHorizontal(-1)

        # TODO make the sprite move too
        return True
