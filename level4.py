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
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fase - 04")

# Defining fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Defining game variables
total_planks = 45
crossed_planks = 0
errors = 0
max_errors = 5
LETTER_QUEUE = ['m','v','v','m','m','v','c',',',',','c','c',' ','x','x','.','.','x','.',' ',';',';','z','z',' ','b','n','b','b','n','n','m','c','v',' ','.',';','x','z',' ','b','z',' ',',','n','v']  # Fila de letras pré-definida
letter_queue = LETTER_QUEUE
start_time = time.time()
time_limit = 30
bridge_stability = 100  # The percentage of stability of the bridge

# Positions of the planks
plank_positions = [(50 + i * 100, HEIGHT // 2 + 100) for i in range(total_planks)]

# Player's starting position
player_position = [plank_positions[0][0], plank_positions[0][1] - 40]  # Starts on the first plank

# Function to draw the state of the bridge
def draw_bridge(offset_x):
    # Draw all bridge planks based on displacement
    for i in range(total_planks):
        pygame.draw.rect(screen, GREEN, [plank_positions[i][0] + offset_x, plank_positions[i][1], 20, 10])

# Function to draw the player state
def draw_game_state(offset_x):
    global bridge_stability

    # Draw the player
    pygame.draw.circle(screen, BLUE, (player_position[0] + offset_x, player_position[1]), 15)

    # Draw row of letters (next letter in center)
    center_x = WIDTH // 2
    for i, letter in enumerate(letter_queue):
        letter_surface = font.render(letter, True, WHITE)
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
    global letter_queue, crossed_planks, errors, start_time, bridge_stability, player_position
    running = True
    offset_x = 0  # Screen scroll control

    while running:
        screen.fill(BLACK)

        # Draw bridge and game state with offset
        draw_bridge(offset_x)
        draw_game_state(offset_x)

        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Check if the key pressed
                if event.unicode.upper() == letter_queue[0].upper():
                    # Correct letter, advance on the bridge
                    crossed_planks += 1
                    letter_queue.pop(0)  # Remove the first letter
                    start_time = time.time()

                    # Move the player to the next plank
                    if crossed_planks < total_planks:
                        player_position[0] = plank_positions[crossed_planks][0]
                        player_position[1] = plank_positions[crossed_planks][1] - 40

                    # Move the bridge
                    if player_position[0] > WIDTH // 2:
                        offset_x = WIDTH // 2 - player_position[0]

                else:
                    # Incorrect letter, bridge gives a little
                    errors += 1
                    bridge_stability -= 20  # The bridge gives 20% for each error

        # Check the time
        elapsed_time = time.time() - start_time
        if elapsed_time > time_limit:
            bridge_stability -= 10  # Player delay
            start_time = time.time()

        # Check fault conditions
        if bridge_stability <= 0 or errors >= max_errors:
            crossed_planks = 0
            errors = 0
            bridge_stability = 100
            letter_queue = LETTER_QUEUE
            player_position = [plank_positions[0][0], plank_positions[0][1] - 40]
            offset_x = 0
            start_time = time.time()

        # Check if the player crossed all the boards
        if crossed_planks == total_planks:
            running = False

        pygame.display.flip()
        pygame.time.delay(100)

    pygame.quit()

if __name__ == '__main__':
    game_loop()
