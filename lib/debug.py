from pygame import USEREVENT, event

class Debug():

    DEBUG = USEREVENT

    @staticmethod
    def post(title, message):
        """
        Title is used as a namespace, and also in the message itself.
        It triggers a user even in pygame.
        """
        message = {'message': {title: "%s: %s" % (title, message)}}
        event.post(event.Event(Debug.DEBUG, message))

