# Importing Pygame
import pygame

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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swamp of Souls")

# Defining fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 40)

# Background and images
bg_image = pygame.image.load('./assets/backgrounds/bg_menu.png').convert_alpha()
tree_r_image = pygame.transform.scale(pygame.image.load('./assets/backgrounds/tree.png').convert_alpha(), (450, 680))
tree_l_image = pygame.transform.flip(tree_r_image, True, False)
shadow_player = pygame.transform.scale(pygame.image.load('./assets/objects/shadow.png').convert_alpha(), (39, 69))

# Defining fonts
title_font = pygame.font.Font("./level04/IMFellEnglish-Regular.ttf", 75)
small_font = pygame.font.Font("./level04/IMFellEnglish-Regular.ttf", 26)

# players sounds
background_sound = pygame.mixer.Sound('./assets/sounds-effects/Alone at Twilight 5.wav')
click_sound = pygame.mixer.Sound('./level04/click-keyboard.mp3')
background_sound.set_volume(0.5)  # Define o volume para 50%
background_sound.play()

# Animation variables
tree_l_x = 0
tree_r_x = WIDTH - 450
shadow_alpha = 255  # Full opacity
text_alpha = 255
animation_duration = 120  # 2 seconds at 60 FPS

# Helper function to set alpha for surfaces
def set_alpha(surface, alpha):
    temp_surface = surface.copy()
    temp_surface.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
    return temp_surface

# Function to render text and then adjust alpha
def render_text_with_alpha(text, font, color, alpha):
    text_surface = font.render(text, True, color)
    text_surface = set_alpha(text_surface, alpha)  # Apply the fade effect to the text surface
    return text_surface

def animate_closing():
    global tree_l_x, tree_r_x, shadow_alpha, text_alpha

    for frame in range(animation_duration):
        screen.fill(WHITE)

        # Draw background
        screen.blit(bg_image, (0, 0))
        screen.blit(tree_r_image, (tree_r_x, 0))
        screen.blit(tree_l_image, (tree_l_x, 0))

        # Draw gray rectangle as ground
        pygame.draw.rect(screen, GRAY, (0, HEIGHT - 11, WIDTH, 11))  # Adjust height as needed

        # Animate trees moving off screen
        tree_l_x -= 450 / animation_duration  # Move left tree left
        tree_r_x += 450 / animation_duration  # Move right tree right

        # Animate shadow fading out (ghost effect)
        shadow_alpha -= 255 / animation_duration
        if shadow_alpha < 0:
            shadow_alpha = 0
        faded_shadow = set_alpha(shadow_player, int(shadow_alpha))
        screen.blit(faded_shadow, (675, HEIGHT - 78))

        # Fade-out text (reduce alpha gradually)
        text_alpha -= 255 / animation_duration
        if text_alpha < 0:
            text_alpha = 0

        # Render and blit the title text with fade-out effect
        title_text1 = render_text_with_alpha('Swamp   of', title_font, WHITE, int(text_alpha))
        screen.blit(title_text1, (490, 129))
        title_text2 = render_text_with_alpha('Souls', title_font, WHITE, int(text_alpha))
        screen.blit(title_text2, (590, 230))

        # Render and blit the start text with fade-out effect
        start_text = render_text_with_alpha('press any key to play', small_font, WHITE, int(text_alpha))
        screen.blit(start_text, (560, HEIGHT - 180))

        pygame.display.update()
        clock.tick(FPS)

# Game loop
def game_loop():
    running = True

    while running:
        screen.fill(WHITE)

        # Draw background
        screen.blit(bg_image, (0, 0))
        screen.blit(tree_r_image, (WIDTH - 450, 0))
        screen.blit(tree_l_image, (0, 0))
        screen.blit(shadow_player, (675, HEIGHT - 78))

        # Draw gray rectangle as ground
        pygame.draw.rect(screen, GRAY, (0, HEIGHT - 11, WIDTH, 11))  # Adjust height as needed

        # Draw title
        title_text1 = render_text_with_alpha('Swamp   of', title_font, WHITE, 255)
        screen.blit(title_text1, (490, 129))
        title_text2 = render_text_with_alpha('Souls', title_font, WHITE, 255)
        screen.blit(title_text2, (590, 230))

        # Draw start text
        start_text = render_text_with_alpha('press any key to play', small_font, WHITE, 255)
        screen.blit(start_text, (560, HEIGHT - 180))

        clock.tick(FPS)

        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                animate_closing()
                running = False

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    game_loop()
