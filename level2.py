import sys

import pygame
import time

import player as player_mod

# Initializing Pygame
pygame.init()

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
OFF_WHITE = (217, 249, 255)
RED = (100, 20, 0)

# Defining fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
normal_font = pygame.font.Font('assets/IMFellEnglish-Regular.ttf', 24)
last_letter_position = 0
last_letter = 0

# Screen dimensions
WIDTH, HEIGHT = 1320, 680
game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swamp of Souls")

# Background and images
bg_images = []
for i in range(2, 6):
    bg_image = pygame.image.load(f'assets/background/BG_{i}.png').convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

static_bg_image = pygame.image.load(f'assets/background/BG_1.png').convert_alpha()

# Player sprite
moving_sprites = pygame.sprite.Group()
player = player_mod.Player(WIDTH / 2 - 350, 370, "Right")
moving_sprites.add(player)

# Sounds
background_sound = pygame.mixer.Sound('assets/witch-forest-atmo-24654.mp3')
click_sound = pygame.mixer.Sound('assets/click-keyboard.mp3')
background_sound.set_volume(0.5)
background_sound.play()

game_over_background = pygame.image.load('assets/background/GAMEOVER2.png').convert()

class LevelTwoScreen:
    def __init__(self):
        self.scroll = 0
        self.running = True
        self.tree_l_x = 0
        self.tree_r_x = WIDTH - 450
        self.shadow_alpha = 255
        self.text_alpha = 255
        self.animation_duration = 120
        self.opacity = 255
        self.opacity_value = 1
        self.letter_color = OFF_WHITE
        self.error_time = 0
        self.error_color_duration = 0.4
        self.last_letter = ''
        self.last_letter_position = 0
        self.letter_row = self.create_letter_row()
        self.current_letter_index = 0
        self.time = pygame.time

        # Opacity for fade effect
        self.opacity2 = 255
        self.fade_speed = 5  # Control the speed of the fade-out effect

    def darken_screen(self):
        if self.opacity2 > 0:
            dark_overlay = pygame.Surface((WIDTH, HEIGHT))
            dark_overlay.set_alpha(self.opacity2)
            dark_overlay.fill(BLACK)
            game_screen.blit(dark_overlay, (0, 0))
            self.opacity2 -= self.fade_speed  # Reduce opacity to create fade-out effect

    def draw_background(self):
        # Draw the static background first
        game_screen.blit(static_bg_image, (0, 0))

        # Draw the moving layers of the background
        for x in range(6):
            speed = 1
            for layer in bg_images:
                game_screen.blit(layer, ((x * bg_width) - self.scroll * speed, 0))
                speed += 0.6

    def show_game_over_screen(self):
        # Exibe a tela de Game Over
        game_screen.blit(game_over_background, (0, 0))
        pygame.display.update()
        time.sleep(3)  # Pausa por 3 segundos

    def lower_opacity(self):
        if self.opacity >= 0:
            self.opacity -= int(self.opacity_value)

    def create_letter_row(self):
        with open('assets/LetterRowLevel02.txt', 'r') as file:
            return [line.rstrip('\n').replace("'", "") for line in file]

    def draw_letters(self):
        x, y = (WIDTH / 2 - 200), 470
        shadow_offset = 2
        last_paw = 0
        for index, letter in enumerate(self.letter_row):
            if index == self.current_letter_index and self.error_time and time.time() - self.error_time < self.error_color_duration:
                self.letter_color = RED
            else:
                self.letter_color = WHITE

            shadow_text = font.render(letter, True, (50, 50, 50))
            shadow_text.set_alpha(self.opacity)
            game_screen.blit(shadow_text, (x + shadow_offset, y + shadow_offset))

            text = font.render(letter, True, self.letter_color)
            text.set_alpha(self.opacity)
            image = pygame.transform.scale(pygame.image.load(
                './assets/objects/Animal Footstep.png').convert_alpha(), (50, 50))
            image.set_alpha(self.opacity)
            game_screen.blit(text, (x, y))

            if last_paw == 0:
                game_screen.blit(image, (x, y + 140))
                last_paw = 1
            elif last_paw == 1:
                game_screen.blit(image, (x, y + 120))
                last_paw = 0
            x += text.get_width() + 50

            if index == len(self.letter_row) - 1:
                self.last_letter = self.letter_row[-1]
                self.last_letter_position = x

    def run(self):
        self.running = True
        while self.running:
            game_screen.fill(WHITE)
            clock.tick(FPS)
            self.draw_background()

            level_text = normal_font.render(f"Level 3", True, WHITE)
            game_screen.blit(level_text, (600, 10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.unicode.upper() == self.letter_row[0].upper():
                        click_sound.play()
                        self.letter_row.pop(0)
                        player.animate()
                        self.opacity = 255
                    else:
                        self.error_time = time.time()
                        self.opacity = max(0, self.opacity - 40)

            keys = pygame.key.get_pressed()
            if not any(keys) and not player.isAnimating:
                player.stopAnimating()

            if player.isAnimating:
                self.scroll += 3

            if abs(self.scroll) > bg_width:
                self.scroll = 0
            elif abs(self.scroll) < 0:
                self.scroll = bg_width

            moving_sprites.draw(game_screen)
            moving_sprites.update(0.4)
            self.lower_opacity()
            self.draw_letters()

            if len(self.letter_row) > 0:
                image_letter = pygame.transform.scale(
                    pygame.image.load(
                        f'./assets/keys/key_{self.letter_row[0].upper().replace(' ', '')}.png').convert_alpha(),
                    (100, 100))
                game_screen.blit(image_letter,(30,30))

            if self.opacity <= 0:
                self.show_game_over_screen()
                self.running = False
            elif len(self.letter_row) <= 0:
                self.running = False
            self.darken_screen()
            pygame.display.update()
            clock.tick(FPS)
