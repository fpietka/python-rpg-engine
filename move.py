#!/usr/bin/python
# -*- coding: utf-8 -*-

import consts

class move:
    @staticmethod
    def getNextPosition(character, movePattern):

        if movePattern['type'] == 'rect':
            move.getNextPositionRect(character, movePattern['attributes'])
        elif movePattern['type'] == 'circle':
            pass
        else:
            raise move.exception('Unknown move')

    @staticmethod
    def getNextPositionRect(character, attributes):
        xInMove = character.xPos - attributes['topLeft'][0]
        yInMove = character.yPos - attributes['topLeft'][1]

        if xInMove <= 0 and yInMove <= 0:
            #~ character.direction.remove('right')
            character.movefullright()
        elif xInMove >= attributes['width'] and yInMove <= 0:
            #~ character.direction.remove('down')
            character.movefulldown()
        elif xInMove >= attributes['width'] and yInMove >= attributes['height']:
            #~ character.direction.remove('left')
            character.movefullleft()
        elif xInMove <= 0 and yInMove >= attributes['height']:
            #~ character.direction.remove('top')
            character.movefullup()

class exception(BaseException):
    pass
