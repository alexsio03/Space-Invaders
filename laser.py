import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height):
        super().__init__()
        # Create a laser by setting the surface
        self.image = pygame.Surface((4, 20))
        # Make the laser white
        self.image.fill('white')
        # Set the rect to the image created
        self.rect = self.image.get_rect(center = pos)
        # Set laser speed
        self.speed = speed
        # Set max y coord
        self.height_y_constraint = screen_height

    def destroy(self):
        # If laser off screen, remove it
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint:
            self.kill()

    def update(self):
        # Move laser up at a certain speed. This will be constantly called during game.run()
        self.rect.y += self.speed
