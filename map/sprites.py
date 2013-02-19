#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import json
import player


class SpritesLoader():
    @staticmethod
    def load(mapName):
        spritesRaw = [
            line.split(';') for line in
                open("map/" + mapName + ".sprites", "rb").read().split("\n")
        ]
        sprites = list()
        for key, sprite in enumerate(spritesRaw):
            if len(sprite) == 1:
                continue
            s = None
            if sprite[0] == 'player':
                s = SpritesLoader.createPlayer(sprite)

            if s is not None:
                sprites.append(s)

        return sprites

    @staticmethod
    def createPlayer(sprite):
        s = dict()
        s['tilesGroup'] = sprite[1]

        position = json.loads(sprite[2])
        s['x'] = position[0]
        s['y'] = position[1]

        s['static'] = (sprite[4] == 'True')

        if not s['static'] and sprite[5] is not '':
            s['movePattern'] = json.loads(sprite[5])

        return (player.Player(s), int(sprite[3]))
