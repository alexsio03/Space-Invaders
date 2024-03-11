import pygame, sys
from player import Player
from alien import Alien
from laser import Laser
import obstacle
from random import choice

class Game:
    def __init__(self):
        # Player
        # Create the player sprite from our class
        player_sprite = Player((screen_width/2,screen_height), screen_width, 5)
        # Defineour player as a pygame sprite
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Health and Score
        self.lives = 3
        # Set the lives counter as an image of the player sprite
        self.lives_counter = pygame.image.load('./graphics/player.png').convert_alpha()
        # Set lives counter position
        self.lives_x_pos = screen_width - (self.lives_counter.get_size()[0] * 2 + 20)
        # Set initial score
        self.score = 0
        # Set font for score display
        self.font = pygame.font.SysFont("name", 40)

        # Obstacles
        # Set shape as block shape defined in obstacle class
        self.shape = obstacle.shape
        # Set block size
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        # Set number of blocks
        self.block_num = 4
        # Set list of block positions
        self.block_x_pos = [num * (screen_width/self.block_num) for num in range(self.block_num)]
        # Create multiple blocks
        self.create_mult_blocks(*self.block_x_pos, x_edge= screen_width/15, y_edge= 480)

        # Aliens
        # Create a group of alien sprites
        self.aliens = pygame.sprite.Group()
        # Set initial alien direction
        self.alien_dir = 1
        # Set a group of alien lasers
        self.alien_lasers = pygame.sprite.Group()
        # Create the display of aliens
        self.set_aliens(6, 8, 60, 48, 70, 40)

    def create_block(self, x_start, y_start, off_x):
        # Enumerate the shape array
        for row_i, row in enumerate(self.shape):
            for col_i, col in enumerate(row):
                # For each 'x' in the shape array
                if col == 'x':
                    # Set position of each sprite in the block item
                    x = x_start + col_i * self.block_size + off_x
                    y = y_start + row_i * self.block_size
                    # Set color and positions
                    block = obstacle.Block(self.block_size, (241,79,80), x, y)
                    # Add each square into the overall block
                    self.blocks.add(block)

    def create_mult_blocks(self, *offsets, x_edge, y_edge):
        # Create a block at each offset in the list
        for off in offsets:
            self.create_block(x_edge, y_edge, off)

    def set_aliens(self, rows, cols, x_dist, y_dist, x_off, y_off):
        # Enumerate each row and column of aliens
        for row_i, row in enumerate(range(rows)):
            for col_i, col in enumerate(range(cols)):
                # Define each alien's position
                x = col_i * x_dist + x_off
                y = row_i * y_dist + y_off
                # Determine color based on row
                if row_i == 0: alien_sprite = Alien('yellow', x, y)
                elif 2>=row_i >= 1: alien_sprite = Alien('green', x, y)
                else: alien_sprite = Alien('red', x, y)
                # Add alien to list of overall alien sprites
                self.aliens.add(alien_sprite)

    def alien_sideways(self):
        # Handle changing positions of aliens
        for alien in self.aliens.sprites():
            # If any alien hits right edge, change direction and move down
            if alien.rect.right >= screen_width:
                self.alien_dir = -1
                self.alien_down(2)
            # If any alien hits left edge, change direction and move down
            elif alien.rect.left <= 0:
                self.alien_dir = 1
                self.alien_down(2)

    def alien_down(self, dist):
        # Move all aliens down a certain dist
        if self.aliens.sprites():
            for alien in self.aliens.sprites():
                alien.rect.y += dist

    def alien_shoot(self):
        # Have a random alien from the list shoot a laser
        if self.aliens.sprites():
            rand_alien = choice(self.aliens.sprites())
            laser = Laser(rand_alien.rect.center, 6, screen_height)
            # Add the laser to the alien lasers list
            self.alien_lasers.add(laser)


    def coll_check(self):
        # Player lasers collisions
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # Block collision, remove block piece on collision
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # Alien collision, remove alien on collision
                hit_aliens = pygame.sprite.spritecollide(laser, self.aliens, True)
                if hit_aliens:
                    # For every alien hit, remove the alien and laser, add its value to score
                    for alien in hit_aliens:
                        self.score += alien.value
                        laser.kill()

        # Alien lasers collisions
        if self.alien_lasers:
             for laser in self.alien_lasers:
                 # Block collision, remove block piece on collision
                 if pygame.sprite.spritecollide(laser, self.blocks, True):
                     # Remove laser on collision
                     laser.kill()
                 # Player collision
                 if pygame.sprite.spritecollide(laser, self.player, False):
                     self.lives -= 1
                     # Remove laser on collision
                     laser.kill()
                     # If lives are 0 end the game
                     if self.lives <= 0:
                         pygame.quit()
                         sys.exit()

        # Aliens collision
        if self.aliens:
            for alien in self.aliens:
                # Remove entire obstacle on collision
                pygame.sprite.spritecollide(alien, self.blocks, True)
                # End game on collision
                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def lives_display(self):
        # Display the amount of lives left
        for life in range(self.lives - 1):
            x = self.lives_x_pos + (life * (self.lives_counter.get_size()[0] + 10))
            screen.blit(self.lives_counter, (x,8))

    def score_display(self):
        # Display the score in the top left
        score_disp = self.font.render(f'Score: {self.score}', False, 'white')
        score_rect = score_disp.get_rect(topleft = (10,10))
        screen.blit(score_disp, score_rect)

    def run(self):
        # Update player function
        self.player.update()
        # Update alien function
        self.aliens.update(self.alien_dir)
        # Move aliens sideways
        self.alien_sideways()
        # Update alien lasers
        self.alien_lasers.update()
        # Check for collision
        self.coll_check()

        # Draw player's lasers
        self.player.sprite.lasers.draw(screen)
        # Draw player
        self.player.draw(screen)

        # Draw blocks
        self.blocks.draw(screen)

        # Draw aliens
        self.aliens.draw(screen)
        # Draw alien lasers
        self.alien_lasers.draw(screen)

        # Draw the lives
        self.lives_display()
        # Draw the score
        self.score_display()

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    # Screen display
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    game = Game()

    # Add alien laser to events
    alien_laser = pygame.USEREVENT + 1
    # Set the timer on the alien laser for 8 seconds
    pygame.time.set_timer(alien_laser, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # If alien laser called, shoot a laser
            if event.type == alien_laser:
                game.alien_shoot()

        screen.fill((30,30,30))
        # Run constantly
        game.run()

        pygame.display.flip()
        # 60 FPS
        clock.tick(60)
