import pygame, sys
from player import Player
from alien import Alien
from laser import Laser
import obstacle
from random import choice

class Game:
    def __init__(self):
        #Player
        player_sprite = Player((screen_width/2,screen_height), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Health and Score
        self.lives = 3
        self.lives_counter = pygame.image.load('./graphics/player.png').convert_alpha()
        self.lives_x_pos = screen_width - (self.lives_counter.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.SysFont("name", 40)

        # Obstacles
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.block_num = 4
        self.block_x_pos = [num * (screen_width/self.block_num) for num in range(self.block_num)]
        self.create_mult_blocks(*self.block_x_pos, x_edge= screen_width/15, y_edge= 480)

        # Aliens
        self.aliens = pygame.sprite.Group()
        self.alien_dir = 1
        self.alien_lasers = pygame.sprite.Group()
        self.set_aliens(6, 8, 60, 48, 70, 40)

    def create_block(self, x_start, y_start, off_x):
        for row_i, row in enumerate(self.shape):
            for col_i, col in enumerate(row):
                if col == 'x':
                    x = x_start + col_i * self.block_size + off_x
                    y = y_start + row_i * self.block_size
                    block = obstacle.Block(self.block_size, (241,79,80), x, y)
                    self.blocks.add(block)

    def create_mult_blocks(self, *offsets, x_edge, y_edge):
        for off in offsets:
            self.create_block(x_edge, y_edge, off)

    def set_aliens(self, rows, cols, x_dist, y_dist, x_off, y_off):
        for row_i, row in enumerate(range(rows)):
            for col_i, col in enumerate(range(cols)):
                x = col_i * x_dist + x_off
                y = row_i * y_dist + y_off
                if row_i == 0: alien_sprite = Alien('yellow', x, y)
                elif 2>=row_i >= 1: alien_sprite = Alien('green', x, y)
                else: alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_sideways(self):
        for alien in self.aliens.sprites():
            if alien.rect.right >= screen_width:
                self.alien_dir = -1
                self.alien_down(2)
            elif alien.rect.left <= 0:
                self.alien_dir = 1
                self.alien_down(2)

    def alien_down(self, dist):
        if self.aliens.sprites():
            for alien in self.aliens.sprites():
                alien.rect.y += dist

    def alien_shoot(self):
        if self.aliens.sprites():
            rand_alien = choice(self.aliens.sprites())
            laser = Laser(rand_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser)


    def coll_check(self):
        # player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # block collis
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                # alien collis
                hit_aliens = pygame.sprite.spritecollide(laser, self.aliens, True)
                if hit_aliens:
                    for alien in hit_aliens:
                        self.score += alien.value
                        laser.kill()

        # alien lasers
        if self.alien_lasers:
             for laser in self.alien_lasers:
                 # block collis
                 if pygame.sprite.spritecollide(laser, self.blocks, True):
                     laser.kill()
                 if pygame.sprite.spritecollide(laser, self.player, False):
                     self.lives -= 1
                     laser.kill()
                     if self.lives <= 0:
                         pygame.quit()
                         sys.exit()

        # aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)
                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()

    def lives_display(self):
        for life in range(self.lives - 1):
            x = self.lives_x_pos + (life * (self.lives_counter.get_size()[0] + 10))
            screen.blit(self.lives_counter, (x,8))

    def score_display(self):
        score_disp = self.font.render(f'Score: {self.score}', False, 'white')
        score_rect = score_disp.get_rect(topleft = (10,10))
        screen.blit(score_disp, score_rect)

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_dir)
        self.alien_sideways()
        self.alien_lasers.update()
        self.coll_check()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        self.blocks.draw(screen)

        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)

        self.lives_display()
        self.score_display()

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    game = Game()

    alien_laser = pygame.USEREVENT + 1
    pygame.time.set_timer(alien_laser, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == alien_laser:
                game.alien_shoot()

        screen.fill((30,30,30))
        game.run()

        pygame.display.flip()
        clock.tick(60)
