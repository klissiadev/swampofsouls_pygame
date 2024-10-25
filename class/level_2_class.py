import sys

import pygame
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

# Screen dimensions
WIDTH, HEIGHT = 1320, 680
game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swamp of Souls - Fase 02")

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Background and images
bg_images = []
for i in range(2, 6):
    bg_image = pygame.image.load(f'./level02/background/BG_{i}.png').convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()

static_bg_image = pygame.image.load(f'./level02/background/BG_1.png').convert_alpha()

# Player sprite
moving_sprites = pygame.sprite.Group()
player = player_mod.Player(WIDTH / 2 - 65, 370, "Right")
moving_sprites.add(player)


class LevelTwoScreen:
    def __init__(self):
        self.scroll = 0
        self.running = True
        self.tree_l_x = 0
        self.tree_r_x = WIDTH - 450
        self.shadow_alpha = 255
        self.text_alpha = 255
        self.animation_duration = 120

    @staticmethod
    def set_alpha(surface, alpha):
        temp_surface = surface.copy()
        temp_surface.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        return temp_surface

    def draw_background(self):
        # Draw the static background first
        game_screen.blit(static_bg_image, (0, 0))

        # Draw the moving layers of the background
        for x in range(6):
            speed = 1
            for layer in bg_images:
                game_screen.blit(layer, ((x * bg_width) - self.scroll * speed, 0))
                speed += 0.6

    def render_text_with_alpha(self, text, font, color, alpha):
        text_surface = font.render(text, True, color)
        text_surface = self.set_alpha(text_surface, alpha)
        return text_surface

    def animate_closing(self):
        for frame in range(self.animation_duration):

            # Draw background
            self.draw_background()

            # Animate trees (you can add the tree images if needed)
            self.tree_l_x -= 450 / self.animation_duration
            self.tree_r_x += 450 / self.animation_duration

            # Animate shadow fade-out (you can add a shadow image if needed)
            self.shadow_alpha -= 255 / self.animation_duration
            if self.shadow_alpha < 0:
                self.shadow_alpha = 0

            # Animate text fade-out
            self.text_alpha -= 255 / self.animation_duration
            if self.text_alpha < 0:
                self.text_alpha = 0

            # Render title with fade effect
            title_text1 = self.render_text_with_alpha('Swamp   of', font, WHITE, int(self.text_alpha))
            game_screen.blit(title_text1, (490, 129))
            title_text2 = self.render_text_with_alpha('Souls', font, WHITE, int(self.text_alpha))
            game_screen.blit(title_text2, (590, 230))

            # Render start text with fade effect
            start_text = self.render_text_with_alpha('press any key to play', small_font, WHITE, int(self.text_alpha))
            game_screen.blit(start_text, (560, HEIGHT - 180))

            pygame.display.update()
            clock.tick(FPS)

    def run(self):
        while self.running:
            game_screen.fill(WHITE)

            # Draw background and player
            self.draw_background()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Handle player movement
            keys = pygame.key.get_pressed()
            if any(keys):
                self.scroll += 5
                player.animate()
            else:
                player.stopAnimating()

            if abs(self.scroll) > bg_width:
                self.scroll = 0
            elif abs(self.scroll) < 0:
                self.scroll = bg_width

            # Draw sprites
            moving_sprites.draw(game_screen)
            moving_sprites.update(0.25)

            # Handle events


            pygame.display.update()
            clock.tick(FPS)




# Example of how to run this screen
if __name__ == '__main__':
    level_two = LevelTwoScreen()
    level_two.run()
    pygame.quit()
