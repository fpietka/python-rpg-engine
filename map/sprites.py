#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame, json

class SpritesLoader():
    @staticmethod
    def load(mapName):
        spritesRaw = [line.split(';') for line in open("map/" + mapName + ".sprites", "rb").read().split("\n")]
        sprites = list()
        for key, sprite in enumerate(spritesRaw):
            if len(sprite) == 1:
                continue
            sprites.append(dict())
            sprites[key]['tilesGroup'] = sprite[0]
            sprites[key]['layer'] = sprite[2]
            sprites[key]['static'] = (sprite[3] == 'True')

            if not sprites[key]['static'] and sprite[4] is not '':
                sprites[key]['movePattern'] = json.loads(sprite[4])

            position = json.loads(sprite[1])
            sprites[key]['x'] = position[0]
            sprites[key]['y'] = position[1]
        return sprites
