import pygame
import sys

pygame.init()

#screen (example)
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Blocos na Frente do Personagem")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# font
font = pygame.font.SysFont(None, 48)

class Player:
    def __init__(self):
        self.x = width // 2
        self.y = height - 60
        self.width = 50
        self.height = 50

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))


blocks = []  # jogador
black_blocks = [(100, 550, "B"), (30, 300, "B"), (600, 300, "B")]  #bloco que deve desaparecer
player = Player()

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.unicode.isalpha():
                black_blocks = [(bx, by, btext) for (bx, by, btext) in black_blocks
                                if not (player.x < bx + 50 and player.x + player.width > bx and
                                        player.y < by + 50 and player.y + player.height > by)]
                blocks.append((player.x, player.y, event.unicode))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= 5
    if keys[pygame.K_RIGHT] and player.x < width - player.width:
        player.x += 5

    screen.fill(WHITE)
    player.draw()

    # draw black bricks
    for block in black_blocks:
        pygame.draw.rect(screen, BLACK, (block[0], block[1], 50, 50))

    # draw blue bricks
    for block in blocks:
        text = font.render(block[2], True, BLACK)
        screen.blit(text, (block[0], block[1]))

    pygame.display.flip()
    pygame.time.Clock().tick(30)
