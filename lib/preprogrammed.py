import pygame

class PreProgrammedCommands:
    def __init__(self, argv):
        try:
            self.cmdlist = list(argv[1])
        except IndexError:
            self.cmdlist = []

    def run(self):
        if not self.cmdlist:
            return

        c = ord(self.cmdlist.pop(0))
        if ord('a') <= c <= ord('z'):
            key = pygame.K_a + (c - ord('a'))
        elif ord('0') <= c <= ord('9'):
            key = pygame.K_0 + (c - ord('0'))
        elif c == ord('E'):
            key = pygame.K_RETURN
        else:
            raise Exception("Unknown preprogrammed key[{}]".format(c))

        ev = pygame.event.Event(pygame.KEYDOWN, key=key)
        pygame.event.post(ev)
