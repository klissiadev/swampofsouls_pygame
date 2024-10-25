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
OFF_WHITE = (217, 249, 255)
RED = (100, 20, 0)

# Screen dimensions
WIDTH, HEIGHT = 1320, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fase - 02")

#Game variables
letter_color = OFF_WHITE
opacity = 255
opacity_value = 1
scroll = 0
error_time = 0
error_color_duration = 0.4
moving_sprites = pygame.sprite.Group()
player = player_mod.Player(WIDTH/2 - 400, 370, "Right")
moving_sprites.add(player)
#Defining fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
last_letter_position = 0
last_letter = 0

#sounds
background_sound = pygame.mixer.Sound('./level04/witch-forest-atmo-24654.mp3')
click_sound = pygame.mixer.Sound('./level04/click-keyboard.mp3')
background_sound.set_volume(0.5)
background_sound.play()

bg_images = []
for i in range(2, 6):
    bg_image = pygame.image.load(f'./level02/background/BG_{i}.png').convert_alpha()
    bg_images.append(bg_image)

bg_width = bg_images[0].get_width()


def drawBackground():
    static_bg_image = pygame.image.load(f'./level02/background/BG_1.png').convert_alpha()
    screen.blit(static_bg_image, (0, 0))

    for x in range(6):
        speed = 1
        for l in bg_images:
            screen.blit(l, ((x * bg_width) - scroll * speed, 0))
            speed += 0.6

def lower_opacity():
    global opacity

    if opacity >= 0:
        opacity -= int(opacity_value)

def create_letter_row():
    with open('level02/text/LetterRowLevel02.txt', 'r') as file:
        letter_row = [line.rstrip('\n').replace("'", "") for line in file]
    return letter_row

letter_row = create_letter_row()
current_letter_index = 0

def draw_letters():
    global letter_color, error_color_duration, error_time, current_letter_index, opacity, last_letter, last_letter_position
    x, y = (WIDTH/2 - 200), 470
    shadow_offset = 2
    last_paw = 0
    for index, letter in enumerate(letter_row):
        if index == current_letter_index and error_time and time.time() - error_time < error_color_duration:
            letter_color = RED
        else:
            letter_color = WHITE

        shadow_text = font.render(letter, True, (50, 50, 50))  # Cor da sombra (cinza escuro)
        shadow_text.set_alpha(opacity)
        screen.blit(shadow_text, (x + shadow_offset, y + shadow_offset))  # Desenha a sombra

        text = font.render(letter, True, letter_color)
        text.set_alpha(opacity)
        image = pygame.transform.scale(pygame.image.load('./assets/solo_assets/Animal Footstep.png').convert_alpha(), (50, 50))
        image.set_alpha(opacity)
        screen.blit(text, (x, y))

        if last_paw == 0:
            screen.blit(image, (x, y + 140))
            last_paw = 1
        elif last_paw == 1:
            screen.blit(image, (x, y + 120))
            last_paw = 0
        x += text.get_width() + 50

        if index == len(letter_row)-1:
            last_letter = letter_row[len(letter_row) - 1]
            last_letter_position = x

# Game loop
def game_loop():
    global scroll, bg_width, error_time, opacity, last_letter

    running = True

    while running:
        screen.fill(WHITE)

        clock.tick(FPS)

        drawBackground()

        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode.upper() == letter_row[0].upper():
                    click_sound.play()
                    letter_row.pop(0)
                    player.animate()
                    opacity = 255
                else:
                    error_time = time.time()
                    opacity -= 40

        keys = pygame.key.get_pressed()
        if not any(keys) and player.isAnimating == False:
            player.stopAnimating()

        if player.isAnimating:
            scroll += 3

        if abs(scroll) > bg_width:
            scroll = 0
        elif abs(scroll) < 0:
            scroll = bg_width

        moving_sprites.draw(screen)
        moving_sprites.update(0.4)
        lower_opacity()
        draw_letters()

        if opacity <= 0:
            print("VC PERDEUU")
            running = False
        elif len(letter_row) <= 0:
            print("VC GANHOUU")
            running = False

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    game_loop()
