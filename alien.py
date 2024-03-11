import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        path = './graphics/' + color + '.png'
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))

        if color == "red": self.value = 100
        elif color == "green": self.value = 200
        else: self.value = 300

    def update(self, dir):
        self.rect.x += dir
