#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame

from game import Game

DEBUG = True

# create a game and run it
if __name__ == '__main__':
    game = Game(DEBUG)
    game.run()
