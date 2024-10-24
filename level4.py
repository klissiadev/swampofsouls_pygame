import pygame
import time
import math
import player as player_mod

from level2 import clock

# Initializing Pygame
pygame.init()

# Defining colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)

# Screen dimensions
WIDTH, HEIGHT = 1320, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level - 04")

clock = pygame.time.Clock()
FPS = 60

#Screen background
background_image = pygame.image.load('./level04/background-sky.png').convert()
bg_w= background_image.get_width()

# Defining fonts
font = pygame.font.Font(None, 100)
normal_font = pygame.font.Font("./level04/IMFellEnglish-Regular.ttf", 36)
small_font = pygame.font.Font("./level04/IMFellEnglish-Regular.ttf", 30)

# players sounds
background_sound = pygame.mixer.Sound('./level04/witch-forest-atmo-24654.mp3')
bridge_stability_sound = pygame.mixer.Sound('./level04/wood-creaking.mp3')
click_sound = pygame.mixer.Sound('./level04/click-keyboard.mp3')
background_sound.set_volume(0.5)  # Define o volume para 50%
background_sound.play()

# Defining game variables
tiles = math.ceil(WIDTH / bg_w) + 1
scroll_bg = 0
total_planks = 45
crossed_planks = 0
errors = 0
max_errors = 5
start_time = time.time()
time_limit = 8
bridge_stability = 100  # The percentage of stability of the bridge
error_time = None  # Time when an error occurs
error_color_duration = 2  # Duration in seconds to show the red color

# Player animations
moving_sprites = pygame.sprite.Group()
player = player_mod.Player(WIDTH/2 - 65, 370)
moving_sprites.add(player)

def create_letter_row():
    with open('level04\LetterRow.txt', 'r') as file:
        letter_row = [line.rstrip('\n').replace("'", "") for line in file]
    return letter_row

letter_row = create_letter_row()

# Positions of the planks
plank_positions = [( i * 69, HEIGHT // 2 + 200) for i in range(total_planks)]

# Player's starting position
player_position = [plank_positions[0][0], plank_positions[0][1] - 200]  # Starts on the first plank

# Function to draw the state of the bridge
def draw_bridge(offset_x, stability_y):
    # Draw all bridge planks based on displacement
    for i in range(total_planks):
        image = pygame.transform.scale(pygame.image.load('./level04/plank.png').convert_alpha(), (75, 123))
        screen.blit(image, (plank_positions[i][0] + offset_x, plank_positions[i][1] + stability_y))
    floor = pygame.transform.scale(pygame.image.load('./level04/floor.png').convert_alpha(), (320, 250))
    screen.blit(floor, (plank_positions[total_planks -1][0] + offset_x + 75, plank_positions[total_planks-1][1]))


# Function to jump animation
def player_jump(target_x, target_y, offset_x, stability_y):
    global scroll_bg
    jump_peak = -100  # Altura máxima do pulo (negativo para subir)
    jump_duration = 10  # Duração total do pulo (número de frames)

    start_x, start_y = player_position[0] , player_position[1]

    # Se o jogador está próximo do final da tela, altera o comportamento
    if player_position[0] > WIDTH - 300:
        for i in range(jump_duration):
            # Progresso do pulo de 0 a 1
            t = i / jump_duration
            # Movimento vertical parabólico: o y diminui para o jogador subir
            parabola = 4 * jump_peak * t * (1 - t)
            player_position[1] = start_y + (target_y - start_y) * t + parabola

            # Desenha o estado atual do jogo para cada frame do pulo
            screen.fill(BLACK)
            for i in range(0, tiles):
                screen.blit(background_image, (i * bg_w + scroll_bg, 0))
            # Scroll background
            scroll_bg -= 1
            # Reset scroll
            if abs(scroll_bg) > bg_w:
                scroll_bg = 0
            draw_bridge(offset_x, stability_y)
            draw_game_state(offset_x, stability_y)
            pygame.display.flip()
            pygame.time.delay(20)
    else:
        # Movimento de pulo normal
        for i in range(jump_duration):
            # Progresso do pulo de 0 a 1
            t = i / jump_duration

            # Movimento horizontal linear: interpolação de posição x
            player_position[0] = start_x + (target_x - start_x) * t

            # Movimento vertical parabólico: o y diminui para o jogador subir
            parabola = 4 * jump_peak * t * (1 - t)
            player_position[1] = start_y + (target_y - start_y) * t + parabola

            # Desenha o estado atual do jogo para cada frame do pulo
            screen.fill(BLACK)
            for i in range(0, tiles):
                screen.blit(background_image, (i * bg_w + scroll_bg, 0))
            # Scroll background
            scroll_bg -= 1
            # Reset scroll
            if abs(scroll_bg) > bg_w:
                scroll_bg = 0
            draw_bridge(offset_x, stability_y)
            draw_game_state(offset_x, stability_y)
            pygame.display.flip()
            pygame.time.delay(20)

# Function to draw the player state
def draw_game_state(offset_x, stability_y):
    global bridge_stability, error_time,player,player_position

    # Draw the player
    player_img = pygame.transform.scale(player.image, (112, 200))
    screen.blit(player_img, (player_position[0] + offset_x - 37, player_position[1] + stability_y + 45))

    # Draw level
    level_text = normal_font.render(f'Level 4', True, WHITE)
    screen.blit(level_text, (WIDTH//2 - 50, 20))

    # Draw row of letters (next letter in center)
    center_x = WIDTH // 2
    for i, letter in enumerate(letter_row):
        if i == 0 and error_time and time.time() - error_time < error_color_duration:
            letter_color = RED
        else:
            letter_color = WHITE
        letter_surface = font.render(letter, True, letter_color)
        x_position = center_x + (i * 100)
        screen.blit(letter_surface, (x_position, HEIGHT // 2 - 50))

    # Draw the number of crossed planks
    plank_text = small_font.render(f'Crossed planks: {crossed_planks}', True, WHITE)
    screen.blit(plank_text, (50, 50))

    # Draw errors
    error_text = small_font.render(f'Errors: {errors}/{max_errors}', True, BROWN)
    screen.blit(error_text, (50, 100))

    # Design plank stability
    stability_text = small_font.render(f'Stability: {bridge_stability}%', True, WHITE)
    screen.blit(stability_text, (50, 150))

# Game loop
def game_loop():
    global letter_row, crossed_planks, errors, start_time, bridge_stability, player_position, error_time,scroll_bg,tiles,bg_w, FPS, clock, player
    running = True
    offset_x = 0  # Screen scroll control
    stability_y = 0

    while running:
        clock.tick(FPS)
        screen.fill(BLACK)
        for i in range(0,tiles):
            screen.blit(background_image, (i * bg_w + scroll_bg, 0))

        # Scroll background
        scroll_bg -= 1

        # Reset scroll
        if abs(scroll_bg) > bg_w:
            scroll_bg = 0

        # Draw bridge and game state with offset
        draw_bridge(offset_x, stability_y)
        draw_game_state(offset_x, stability_y)

        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                click_sound.play()
                # Check if the key pressed
                if event.unicode.upper() == letter_row[0].upper():
                    # Correct letter, advance on the bridge
                    crossed_planks += 1
                    letter_row.pop(0)  # Remove the first letter
                    start_time = time.time()
                    # Move the player to the next plank
                    if crossed_planks < total_planks:
                        player_jump(plank_positions[crossed_planks][0] + 12, plank_positions[crossed_planks][1] - 200 + 45, offset_x, stability_y)

                    # Move the bridge
                    if player_position[0] > WIDTH - 300:
                        offset_x = WIDTH - 300 - player_position[0]
                else:
                    # Incorrect letter, bridge gives a little
                    errors += 1
                    bridge_stability -= 20  # The bridge gives 20% for each error
                    stability_y += 30
                    error_time = time.time()  # Record the time of the error
                    bridge_stability_sound.play()

        # Check the time
        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            bridge_stability -= 10  # Player delay
            stability_y += 10
            start_time = time.time()
            bridge_stability_sound.play()

        # Check fault conditions
        if bridge_stability <= 0 or errors >= max_errors:
            crossed_planks = 0
            errors = 0
            bridge_stability = 100
            letter_row = create_letter_row()
            player_position = [plank_positions[0][0] - 60, plank_positions[0][1] - 200]
            offset_x = 0
            stability_y = 0
            start_time = time.time()

        # Check if the player crossed all the boards
        if crossed_planks >= total_planks:
            # Move the player to the floor
            player_position[0] += 5
            player.animate()
        else:
            player.stopAnimating()

        if player_position[0] > WIDTH:  # If the player has already left the screen
            running = False  # End the game

        moving_sprites.update(0.25)
        pygame.display.flip()
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    game_loop()
