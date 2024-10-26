
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
YELLOW = (255, 255, 0)
GREY = (168, 168, 168)

# Defining fonts
small_font = pygame.font.Font("./level04/IMFellEnglish-Regular.ttf", 24)
x_small_font = pygame.font.Font("./level04/IMFellEnglish-Regular.ttf", 16)

# Screen dimensions
WIDTH, HEIGHT = 1320, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interval - 02")
background_sound = pygame.mixer.Sound('level03/Alone at Twilight 5.wav')
background_sound.set_volume(0.5)
background_sound.play()

scroll = 0

bg_images = []
for i in range(2, 6):
    bg_image = pygame.image.load(f'./level02/background/BG_{i}.png').convert_alpha()
    bg_images.append(bg_image)

bg_width = bg_images[0].get_width()

# Player
moving_sprites = pygame.sprite.Group()
player = player_mod.Player(40, 370, "Right")
moving_sprites.add(player)
player_position = [40,370]

# animal foot
animal_foot = pygame.transform.scale(pygame.image.load('assets/objects/Animal Footstep.png').convert_alpha(), (60, 60))
foot_positions = [WIDTH - 10 , HEIGHT - 100]


def drawBackground():
    static_bg_image = pygame.image.load(f'./level02/background/BG_1.png').convert_alpha()
    screen.blit(static_bg_image, (0, 0))

    for x in range(6):
        speed = 1
        for l in bg_images:
            screen.blit(l, ((x * bg_width) - scroll * speed, 0))
            speed += 0.6

# Game loop
def game_loop():
    global scroll, bg_width

    running = True

    while running:
        screen.fill(WHITE)

        clock.tick(FPS)

        drawBackground()
        screen.blit(player.image, (player_position[0], player_position[1]))

        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.unicode.upper() == 'E':
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            player.orientation = 'Right'
            if player_position[0] < WIDTH - 300:
                player_position[0] += 4
            else:
                scroll += 2
                foot_positions[0] -= 4
            player.animate()
        elif keys[pygame.K_LEFT]:
            player.orientation = "Left"

            if player_position[0] > 40:
                player_position[0] -= 4
                if scroll > 0:
                    scroll -= 2
                    foot_positions[0] += 4
            player.animate()
        else:
            player.stopAnimating()

        if abs(scroll) > bg_width:
            scroll = 0
        elif abs(scroll) < 0:
            scroll = bg_width

        moving_sprites.update(0.25)

        #Draw footsteps
        screen.blit(animal_foot, (foot_positions[0], foot_positions[1]))

        if abs((player_position[0] + 36) - foot_positions[0]) < 70:
            press_e_text = x_small_font.render(f'Press E', True, WHITE)
            screen.blit(press_e_text, (foot_positions[0] + 10 , HEIGHT - 35))
            tip_text = small_font.render(f'Oh...? footsteps of animals...', True, WHITE)
            screen.blit(tip_text, (400, HEIGHT - 200))
            pygame.display.update()


        # Draw the tip
        tip_text = small_font.render(f'Where am i supposed to go...?', True, WHITE)
        screen.blit(tip_text, (50, HEIGHT - 60))
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    game_loop()