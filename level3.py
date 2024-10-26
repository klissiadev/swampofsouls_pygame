import pygame
import random
import time
import player as player_mod
from classes.level_3_class import Block
from classes.level_3_class import Camera

pygame.init()

# screen settings
width = 1320
height = 680
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
FPS = 60

#background
bg1 = pygame.image.load('level03/Group 68.png')
bg1 = pygame.transform.scale(bg1, (width, height))
background_sound = pygame.mixer.Sound('level03/Alone at Twilight 5.wav')
background_sound.set_volume(0.5)
background_sound.play()

#blocks
block_image = pygame.image.load('level03/Group 29 (1).png').convert_alpha()
block_rect = block_image.get_rect(topleft=(250, 600))
block_sound = pygame.mixer.Sound('level03/walk-in-dry-leaves-in-the-forest-22431_JTzeMuNJ.mp3')
block_sound.set_volume(0.2)

#random variables
scroll = 0
normal_font = pygame.font.Font('level04/IMFellEnglish-Regular.ttf', 40)
font = pygame.font.Font(None, 50)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
margin = 200

class LevelThreeOnScreen:
    def __init__(self):
        self.scroll = 0
        self.moving_sprites = pygame.sprite.Group()
        self.player = player_mod.Player(40, 370, "Right")
        self.moving_sprites.add(self.player)
        self.player_position = [40, 370]
        self.bg_images = [pygame.image.load(f'./level02/background/BG_{i}.png').convert_alpha() for i in range(2, 6)]
        self.bg_width = self.bg_images[0].get_width()
        self.camera = Camera(width, height)
        self.blocks = self.create_blocks(200, height // 2)
        self.start_time = time.time()
        self.out_of_the_way = 0
        self.errors = 5
        self.score = 0
        self.cont = 0
        self.max_blocks = 45

    def drawBackground(self, bg_images):
        static_bg_image = pygame.image.load(f'./level02/background/BG_1.png').convert_alpha()
        screen.blit(static_bg_image, (0, 0))

        for x in range(6):
            speed = 1
            for l in self.bg_images:
                screen.blit(l, ((x * self.bg_width) - self.scroll * speed, 0))
                speed += 0.6

    def create_blocks(self, margin, y):
        blocks = []
        block_width = 75
        space = 100
        x = margin
        for i in range(5):  # Cria 5 blocos
            letter = random.choice(['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'r', ' '])
            block = Block(x, y, letter)
            blocks.append(block)
            x += block_width + space
        return blocks

    def reset_game(self):
        self.start_time = time.time()
        self.cont = 0
        self.out_of_the_way = 0
        self.errors = 5
        self.score = 0
        self.scroll = 0
        self.player_position = [40, 370]
        self.blocks = self.create_blocks(200, height // 2)
        for block in self.blocks:
            block.is_seeing = True
        self.player.rect.midbottom = (self.player_position[0], self.player_position[1])
        self.player.stopAnimating()

    def run(self):
        running = True
        time_limit = 8
        self.reset_game()


        while running:
            block_found = False

            clock.tick(FPS)

            self.drawBackground(self.bg_images)

            current_time = time.time()
            elapsed_time = current_time - self.start_time


            for block in self.blocks:
                block.draw(self.camera)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    letter_is_pressed = event.unicode.lower()

                    for block in self.blocks:
                        if block.is_seeing and block.letter == letter_is_pressed:
                            if block.rect.x > self.player_position[0] or abs(block.rect.x - self.player_position[0]) < 10:
                                    block.is_seeing = False
                                    self.player.rect.midbottom = (block.rect.centerx, block.rect.top)
                                    block_found = True
                                    self.cont += 1
                                    self.scroll += 5
                                    self.start_time = time.time()
                                    block_sound.play()

                                    if all(not b.is_seeing for b in self.blocks):
                                        y = height // 2
                                        self.blocks = self.create_blocks(margin, y)
                                        self.player_position[0] = margin - 100
                                        self.player.animate()
                                        self.scroll += 20
                                    else:
                                        self.player.stopAnimating()

                                    if self.cont >= self.max_blocks:
                                        running = False
                                    break

                    if not block_found:
                        self.errors -= 1
                        self.score -= 15
                        for block in self.blocks:
                            if block.is_seeing and block.letter != letter_is_pressed:
                                block.incorrect = True
                                break

            if elapsed_time > time_limit:
                self.out_of_the_way += 5
                self.start_time = current_time


            if abs(self.scroll) > self.bg_width:
                self.scroll = 0
            elif abs(self.scroll) < 0:
                self.scroll = self.bg_width

            screen.blit(self.player.image, (self.player_position[0], self.player_position[1]))

            score_text = normal_font.render(f"Perdido em:  {self.out_of_the_way}%", True, WHITE)
            screen.blit(score_text, (10, 10))

            erros_text = normal_font.render(f"Erros: {self.errors}", True, WHITE)
            screen.blit(erros_text, (10, 50))

            level_text = normal_font.render(f"Level 3", True, WHITE)
            screen.blit(level_text, (600, 10))

            if (self.out_of_the_way >= 100 or self.errors <= 0):
                self.reset_game()


            self.moving_sprites.update(0.25)
            pygame.display.update()



if __name__ == "__main__":
    level_three_screen = LevelThreeOnScreen()
    level_three_screen.run()
    pygame.quit()