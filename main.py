#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from map.builder import Builder

# Global parameters useful throuhout the game
RESOLUTION = 800, 600
MAPSIZE = 8000, 6000
FPS = 60

MOVING = False

white = 255, 255, 255


# sprite sets, with mapping containing (top, left)
sprite_size = (96, 128)
sprites = list()
for x in range(0, 10):
    for y in range(0, 6):
        sprites.append((sprite_size[0] * x, sprite_size[1] * y))
# choice of the sprite here
sprite = sprites[0]

characterSizeX, characterSizeY = 32, 32

spriteset1 = {
    'name': 'dpnpcsq.png', 'height': characterSizeY, 'width': characterSizeX, 'map': (
        (sprite[0], sprite[1]),
        (sprite[0], sprite[1] + 32),
        (sprite[0], sprite[1] + 64),
        (sprite[0], sprite[1] + 96),
        (sprite[0] + 32, sprite[1]),
        (sprite[0] + 32, sprite[1] + 32),
        (sprite[0] + 32, sprite[1] + 64),
        (sprite[0] + 32, sprite[1] + 96),
        (sprite[0] + 64, sprite[1]),
        (sprite[0] + 64, sprite[1] + 32),
        (sprite[0] + 64, sprite[1] + 64),
        (sprite[0] + 64, sprite[1] + 96)
    )}


class Background(object):
    def __init__(self, fouraxis=True):
        # Set movement type
        self.fouraxis = fouraxis
        self.movesquare = False # XXX will be used to move full squares

        self.sprites = list()
        self.mainSprite = None
        #coordinates (top left point) of the camera view in the world
        self.xCamera, self.yCamera = 0, 0;

    def update(self):
        for s in self.sprites:
            s.updatePosition()
            s.updateFrame(pygame.time.get_ticks())

        self.updateFocus()

    def updateFocus(self):
        #get mainSprite (new) coordinates in the world
        xMainSprite, yMainSprite = self.sprites[self.mainSprite].xPos, self.sprites[self.mainSprite].yPos

        #move camera if not out of world boundaries
        self.xCamera = max(0, min(MAPSIZE[0] - RESOLUTION[0], xMainSprite - RESOLUTION[0] / 2))
        self.yCamera = max(0, min(MAPSIZE[1] - RESOLUTION[1], yMainSprite - RESOLUTION[1] / 2))


    def setMainSprite(self, sprite):
        self.setSprite(sprite)
        self.mainSprite = self.sprites.index(sprite)

    def setSprite(self, sprite):
        if sprite not in self.sprites:
            self.sprites.append(sprite)


class PlayerGroup(pygame.sprite.Group):
    "Group for player class"


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # Animation parameters
        self._start = pygame.time.get_ticks()
        self._delay = 10000 / FPS
        self._last_update = 0
        self.frame = 0
        self.animation = .5
        # Handle sprite set
        self.build_spriteset()
        self.direction = list()
        self.default_direction = 'down'
        self.image = self.spriteset['down'][self.frame].convert()
        self.rect = self.image.get_rect()
        self.xPos, self.yPos = 400, 300;
        self.rect.center = (RESOLUTION[0] / 2, RESOLUTION[1] / 2)
        self.x_velocity = 0
        self.y_velocity = 0
        self.speed = 3
        self.movestack = list()

    def updatePosition(self):
        self.xPos = min(MAPSIZE[0] - characterSizeX / 2, max(characterSizeX / 2, self.xPos + self.x_velocity))
        self.yPos = min(MAPSIZE[1] - characterSizeY / 2, max(characterSizeY / 2, self.yPos + self.y_velocity))

        self.rect.center = (self.xPos, self.yPos)

        # Set moving
        global MOVING
        if self.x_velocity == 0 and self.y_velocity == 0:
            MOVING = False
        else:
            MOVING = True

    def updateFrame(self, tick):
        if not MOVING:
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
        self.image = self.spriteset[direction][self.frame].convert()

    def build_spriteset(self):
        "Cut and build sprite set"
        self.fond = pygame.image.load(spriteset1['name']).convert()
        self.fond.set_colorkey(self.fond.get_at(next(iter(spriteset1['map']))))
        width = spriteset1['width']
        height = spriteset1['height']
        # use map to cut parts
        spriteset = list()
        for (left, top) in spriteset1['map']:
            rect = pygame.Rect(left, top, width, height)
            spriteset.append(self.fond.subsurface(rect))
        # build direction there
        test = {
            'up': (spriteset[0], spriteset[8], spriteset[7]),
            'down': (spriteset[9], spriteset[10], spriteset[11]),
            'left': (spriteset[2], spriteset[1], spriteset[3]),
            'right': (spriteset[4], spriteset[5], spriteset[6])
        }
        self.spriteset = test

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

    def moveup(self):
        self.y_velocity += self.speed
        if self.y_velocity != 0:
            self.movestack.append('vertical')
        else:
            self.movestack.remove('vertical')

    def movedown(self):
        self.y_velocity -= self.speed
        if self.y_velocity != 0:
            self.movestack.append('vertical')
        else:
            self.movestack.remove('vertical')

    def moveleft(self):
        self.x_velocity += self.speed
        if self.x_velocity != 0:
            self.movestack.append('horizontal')
        else:
            self.movestack.remove('horizontal')

    def moveright(self):
        self.x_velocity -= self.speed
        if self.x_velocity != 0:
            self.movestack.append('horizontal')
        else:
            self.movestack.remove('horizontal')


class Game():
    def __init__(self):
        global MAPSIZE
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        self.builder = Builder()
        self.fond = self.builder.load(self.screen, (0, 0))
        MAPSIZE = self.builder.width, self.builder.height
        # Blit background
        self.screen.blit(self.fond, (0, 0))
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
        self.background = Background()
        # TODO avoid acting on sprite and do actions on group?
        self.player = Player()
        self.playerGroup = PlayerGroup(self.player)
        self.background.setMainSprite(self.player)

    def run(self):
        running = True
        # run until an event tells us to stop
        while running:
            pygame.time.Clock().tick(FPS)
            running = self.handleEvents()
            self.background.update()
            # Blit background
            # Blit background
            self.builder.update((self.background.xCamera, self.background.yCamera))
            # Blit sprite
            self.playerGroup.draw(self.builder.fond)

            rect = pygame.Rect(self.background.xCamera, self.background.yCamera, RESOLUTION[0], RESOLUTION[1])
            self.fond = self.builder.fond.subsurface(rect)
            self.screen.blit(self.fond, (0, 0))
            # update part of the script
            rect = pygame.Rect(0, 0, 800, 600)
            pygame.display.update(rect)
            # update all the screen
            #pygame.display.flip()

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
                    self.player.movedown()
                if event.key == pygame.K_DOWN:
                    self.player.direction.append('down')
                    self.player.moveup()
                if event.key == pygame.K_LEFT:
                    self.player.direction.append('left')
                    self.player.moveright()
                if event.key == pygame.K_RIGHT:
                    self.player.direction.append('right')
                    self.player.moveleft()
            elif event.type == pygame.KEYUP:
                # handle speed
                if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                    self.player.decel()
                # stop movement control
                if event.key == pygame.K_UP:
                    self.player.direction.remove('up')
                    self.player.moveup()
                if event.key == pygame.K_DOWN:
                    self.player.direction.remove('down')
                    self.player.movedown()
                if event.key == pygame.K_LEFT:
                    self.player.direction.remove('left')
                    self.player.moveleft()
                if event.key == pygame.K_RIGHT:
                    self.player.direction.remove('right')
                    self.player.moveright()

        # TODO make the sprite move too
        return True

# create a game and run it
if __name__ == '__main__':
    game = Game()
    game.run()
