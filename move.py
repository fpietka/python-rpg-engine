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
            character.stop()
            #~ move right
            character.moveHorizontal(1)
        elif xInMove >= attributes['width'] and yInMove <= 0:
            character.stop()
            #~ move down
            character.moveVertical(1)
        elif xInMove >= attributes['width']\
            and yInMove >= attributes['height']:
            character.stop()
            #~ move left
            character.moveHorizontal(-1)
        elif xInMove <= 0 and yInMove >= attributes['height']:
            character.stop()
            #~ move up
            character.moveVertical(-1)


class exception(BaseException):
    pass
