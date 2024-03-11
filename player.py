import pygame
from laser import Laser

# The Player class is a subclass of pygame.sprite.Sprite and represents the player character in the game.
class Player(pygame.sprite.Sprite):

    # The __init__ method is called when an instance of the class is created.
    # It initializes the player's properties, such as the image, position, speed, etc.
    def __init__(self, pos, constraint, speed):
        # Call the parent class (pygame.sprite.Sprite) constructor
        super().__init__()

        # Load the player's image and allow for transparency in the image
        self.image = pygame.image.load('./graphics/player.png').convert_alpha()

        # Get the rectangle that encloses the image which is used for positioning and collision detection
        self.rect = self.image.get_rect(midbottom=pos)

        # Set the player's movement speed
        self.speed = speed

        # Set up the constraint that the player cannot move beyond (likely the screen width)
        self.max_x_constraint = constraint

        # A flag to determine if the player is able to shoot a laser
        self.ready = True

        # Time-keeping variables for managing laser shooting cooldown
        self.laser_time = 0
        self.laser_cooldown = 600

        # A group to hold all Laser objects the player shoots
        self.lasers = pygame.sprite.Group()

    # Method to handle player input
    def get_input(self):
        # Get the current state of all keyboard buttons
        keys = pygame.key.get_pressed()

        # Move the player right or left when right or left arrow keys are pressed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # Shoot a laser if the spacebar is pressed and the player is ready
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False  # Set ready to False to start the cooldown
            self.laser_time = pygame.time.get_ticks()  # Record the time the laser was shot

    # Method to manage the cooldown timer for shooting lasers
    def recharge(self):
        # Check if the player is not ready to shoot
        if not self.ready:
            # Get the current time
            current_time = pygame.time.get_ticks()

            # If sufficient time has passed since the last shot, set ready to True
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    # Method to ensure the player remains within screen bounds
    def constraint(self):
        # Prevent the player from moving off the screen to the left
        if self.rect.left <= 0:
            self.rect.left = 0
        # Prevent the player from moving off the screen to the right
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    # Method to handle shooting lasers
    def shoot_laser(self):
        # Create a Laser object and add it to the lasers group
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))

    # The update method is called for each frame of the game
    def update(self):
        # Run the various methods to process player input, constrain movement, recharge the laser, and update lasers
        self.get_input()
        self.constraint()
        self.recharge()

        # Update the state of each laser in the lasers group
        self.lasers.update()
