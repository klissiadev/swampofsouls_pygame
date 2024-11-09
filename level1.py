import sys

import pygame
import player as player_mod
from interval_1_class import Firefly
# Initializing Pygame
pygame.init()

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (185, 185, 185)
YELLOW = (255, 255, 0)

# Defining fonts
small_font = pygame.font.Font("assets/IMFellEnglish-Regular.ttf", 24)
x_small_font = pygame.font.Font("assets/IMFellEnglish-Regular.ttf", 16)

# Screen dimensions
WIDTH, HEIGHT = 1320, 680
game_screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Changed 'screen' to 'game_screen'
pygame.display.set_caption("Level - 01")

# Background images
bg_images = [pygame.image.load(f'assets/background/BG_{i}.png').convert_alpha() for i in range(2, 6)]
bg_width = bg_images[0].get_width()

# Players sounds
background_sound = pygame.mixer.Sound('assets/Alone at Twilight 5.wav')
click_sound = pygame.mixer.Sound('assets/click-keyboard.mp3')
click_sound.set_volume(0.4)
background_sound.set_volume(0.5)  # Set volume to 50%
background_sound.play()

# Jar
jar = pygame.transform.scale(pygame.image.load('assets/objects/jar.png').convert_alpha(), (60, 60))
jar_positions = [WIDTH - 60, HEIGHT - 150]

class LevelOneScreen:
    def __init__(self):
        self.scroll = 0
        self.moving_sprites = pygame.sprite.Group()
        self.player = player_mod.Player(40, 370, "Right")
        self.moving_sprites.add(self.player)
        self.player_position = [600, 370]
        self.fireflies = pygame.sprite.Group()
        self.opacity = 200

        # Creating fireflies
        for _ in range(10):
            firefly = Firefly()
            self.fireflies.add(firefly)

    def draw_background(self):
        static_bg_image = pygame.image.load(f'assets/background/BG_1.png').convert_alpha()
        game_screen.blit(static_bg_image, (0, 0))

        for x in range(6):
            speed = 1
            for l in bg_images:
                game_screen.blit(l, ((x * bg_width) - self.scroll * speed, 0))
                speed += 0.6

    def darken_screen(self):
        dark_overlay = pygame.Surface((WIDTH, HEIGHT))
        dark_overlay.set_alpha(self.opacity)
        dark_overlay.fill(BLACK)
        game_screen.blit(dark_overlay, (0, 0))

    def run(self):
        running = True

        # Font for displaying letters
        font = x_small_font

        # Key pressed tracker
        key_pressed = None

        while running:
            game_screen.fill(WHITE)
            clock.tick(FPS)

            # Drawing and updating sprites
            self.draw_background()
            game_screen.blit(self.player.image, (self.player_position[0], self.player_position[1]))
            self.player.grab_jar()

            # Event handling
            key_pressed = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        click_sound.play()
                        key_pressed = "F"
                    elif event.key == pygame.K_j:
                        click_sound.play()
                        key_pressed = "J"

            # Update fireflies and check for "catch" interaction
            caught = False
            for firefly in self.fireflies:
                key_text = font.render(firefly.catch_key, True, YELLOW)
                game_screen.blit(key_text, (firefly.rect.x, firefly.rect.y - 20))

                # Check collision and correct key
                if not caught and key_pressed == firefly.catch_key:
                    # Firefly caught
                    print(f"Firefly with key '{firefly.catch_key}' caught at ({firefly.rect.x}, {firefly.rect.y})!")
                    self.fireflies.remove(firefly)
                    self.opacity = max(0, self.opacity - 20)
                    caught = True  # Set flag to True to exit loop after catching one firefly
                    self.player.catch_firefly()
                    break  # Stop after catching one firefly

            if len(self.fireflies) == 0:
                # Fade-out effect
                self.opacity =  min(255, self.opacity + 5)
                if self.opacity == 255:
                    running = False

            if abs(self.scroll) > bg_width:
                self.scroll = 0
            elif abs(self.scroll) < 0:
                self.scroll = bg_width

            self.moving_sprites.update(0.25)
            self.darken_screen()
            # Update fireflies
            self.fireflies.update()

            # Draw fireflies on screen
            self.fireflies.draw(game_screen)

            pygame.display.update()
