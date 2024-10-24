import pygame
import time
import math
import player as player_mod

# Initializing Pygame
pygame.init()

#Clock

clock = pygame.time.Clock()
FPS = 60

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen dimensions
WIDTH, HEIGHT = 1320, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fase - 02")

scroll = 0

bg_images = []
for i in range(2, 6):
    print(i)
    bg_image = pygame.image.load(f'./level02/background/BG_{i}.png').convert_alpha()
    bg_images.append(bg_image)

bg_width = bg_images[0].get_width()

moving_sprites = pygame.sprite.Group()
player = player_mod.Player(WIDTH/2 - 65, 370)
moving_sprites.add(player)


def drawBackground():
    static_bg_image = pygame.image.load(f'./level02/background/BG_1.png').convert_alpha()
    screen.blit(static_bg_image, (0, 0))

    for x in range(6):
        speed = 1
        for l in bg_images:
            screen.blit(l, ((x * bg_width) - scroll * speed, 0))
            speed += 0.6


#Defining fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)


# Game loop
def game_loop():
    global scroll, bg_width

    running = True

    while running:
        screen.fill(WHITE)

        clock.tick(FPS)

        drawBackground()

        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if any(keys):
            scroll += 5
            player.animate()
        else:
            player.stopAnimating()

        if abs(scroll) > bg_width:
            scroll = 0
        elif abs(scroll) < 0:
            scroll = bg_width

        moving_sprites.draw(screen)
        moving_sprites.update(0.25)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    game_loop()
