import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        # Set path to whatever color passed in
        path = './graphics/' + color + '.png'
        # Set image to path given
        self.image = pygame.image.load(path).convert_alpha()
        # Set alien rectangle to image set
        self.rect = self.image.get_rect(topleft = (x,y))

        # Set each aliens value
        if color == "red": self.value = 100
        elif color == "green": self.value = 200
        else: self.value = 300

    def update(self, dir):
        # Move alien left and right
        self.rect.x += dir
