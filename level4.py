import pygame
import time

# Initializing Pygame
pygame.init()

# Defining colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen dimensions
WIDTH, HEIGHT = 1320, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fase - 04")

#Screen background
background_image = pygame.image.load('./level04/background-sky.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Defining fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Defining game variables
total_planks = 45
crossed_planks = 0
errors = 0
max_errors = 5
start_time = time.time()
time_limit = 10
bridge_stability = 100  # The percentage of stability of the bridge
error_time = None  # Time when an error occurs
error_color_duration = 2  # Duration in seconds to show the red color

def create_letter_row():
    with open('level04\LetterRow.txt', 'r') as file:
        letter_row = [line.rstrip('\n').replace("'", "") for line in file]
    return letter_row

letter_row = create_letter_row()

# Positions of the planks
plank_positions = [( i * 69, HEIGHT // 2 + 200) for i in range(total_planks)]

# Player's starting position
player_position = [plank_positions[0][0] - 75, plank_positions[0][1] - 200]  # Starts on the first plank

# Function to draw the state of the bridge
def draw_bridge(offset_x, stability_y):
    # Draw all bridge planks based on displacement
    for i in range(total_planks):
        image = pygame.transform.scale(pygame.image.load('./level04/plank.png').convert_alpha(), (75, 123))
        screen.blit(image, (plank_positions[i][0] + offset_x, plank_positions[i][1] + stability_y))


# Function to draw the player state
def draw_game_state(offset_x, stability_y):
    global bridge_stability, error_time

    # Draw the player
    player = pygame.transform.scale(pygame.image.load('./level04/ALMA_WALKING1.png').convert_alpha(), (112, 200))
    screen.blit(player, (player_position[0] + offset_x + 35, player_position[1] + stability_y + 37))

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
    error_text = small_font.render(f'Errors: {errors}/{max_errors}', True, RED)
    screen.blit(error_text, (50, 100))

    # Design plank stability
    stability_text = small_font.render(f'Stability: {bridge_stability}%', True, WHITE)
    screen.blit(stability_text, (50, 150))

# Game loop
def game_loop():
    global letter_row, crossed_planks, errors, start_time, bridge_stability, player_position, error_time
    running = True
    offset_x = 0  # Screen scroll control
    stability_y = 0

    while running:
        screen.fill(BLACK)
        screen.blit(background_image, (0, 0))

        # Draw bridge and game state with offset
        draw_bridge(offset_x, stability_y)
        draw_game_state(offset_x, stability_y)

        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Check if the key pressed
                if event.unicode.upper() == letter_row[0].upper():
                    # Correct letter, advance on the bridge
                    crossed_planks += 1
                    letter_row.pop(0)  # Remove the first letter
                    start_time = time.time()

                    # Move the player to the next plank
                    if crossed_planks < total_planks:
                        player_position[0] = plank_positions[crossed_planks][0]
                        player_position[1] = plank_positions[crossed_planks][1] - 200

                    # Move the bridge
                    if player_position[0] > WIDTH - 300:
                        offset_x = WIDTH - 300 - player_position[0]

                else:
                    # Incorrect letter, bridge gives a little
                    errors += 1
                    bridge_stability -= 20  # The bridge gives 20% for each error
                    stability_y += 30
                    error_time = time.time()  # Record the time of the error

        # Check the time
        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            bridge_stability -= 10  # Player delay
            stability_y += 10
            start_time = time.time()

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
        if crossed_planks == total_planks:
            running = False

        pygame.display.flip()
        pygame.time.delay(100)

    pygame.quit()

if __name__ == '__main__':
    game_loop()
