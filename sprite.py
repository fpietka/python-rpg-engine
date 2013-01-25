#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame


class StaticSprite(pygame.sprite.Sprite):
    IS_STATIC = True


class DynamicSprite(pygame.sprite.Sprite):
    IS_STATIC = False
