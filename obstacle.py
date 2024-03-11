import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, size, color, x, y):
        super().__init__()
        # Set each block to a certain size
        self.image = pygame.Surface((size, size))
        # Fill it with the color given
        self.image.fill(color)
        # Set the rectangle to the image given
        self.rect = self.image.get_rect(topleft = (x,y))

# Shape array that will be used to set the obstacle shape in main
shape = [
    '  xxxxxxx',
    ' xxxxxxxxx',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxx     xxx',
    'xx       xx']
