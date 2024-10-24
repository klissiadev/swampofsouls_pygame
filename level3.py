import pygame
import random

pygame.init()

# screen settings
width = 1320
height = 680
screen = pygame.display.set_mode((width, height))

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# font
font = pygame.font.SysFont(None, 50)

class Block:
    def __init__(self, x, y, letter):
        self.rect = pygame.Rect(x, y, 75, 75)
        self.letter = letter
        self.is_seeing = True

    def draw(self, camera):
        if self.is_seeing:
            pos = camera.apply(self.rect)
            pygame.draw.rect(screen, BLACK, pos)
            text = font.render(self.letter, True, WHITE)
            screen.blit(text, (pos.x + 30, pos.y + 20))

    def resetar(self, x, y, letter):
        self.rect.topleft = (x, y)
        self.letter = letter
        self.is_seeing = True

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, rect):
        return rect.move(-self.camera.x, -self.camera.y)

    def update(self, target):
        x = -target.rect.centerx + int(800 / 2)
        y = -target.rect.centery + int(600 / 2)
        x = min(0, x)
        y = max(0, y)
        x = max(-(self.width - 800), x)
        y = max((self.height - 600), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)

def create_blocks(margin, y):
    blocks = []
    block_width = 75
    space = 10
    x = margin
    for i in range(5):  # Cria 5 blocos
        letter = random.choice(['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'R', ' '])
        block = Block(x, y, letter)
        blocks.append(block)
        x += block_width + space
    return blocks

# Chama a função para criar blocos

# Função principal do jogo
def game_loop():
    margin = 150
    y = 650
    blocks = create_blocks(margin, y)
    player = Block(margin - 100, 650, "")
    camera = Camera(1320, 680)
    running = True
    score = 100
    errors = 5

    while running:
        block_found = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                letter_is_pressed = event.unicode.upper()

                for block in blocks:
                    if block.is_seeing and block.letter == letter_is_pressed:
                        if block.rect.x > player.rect.x:
                                block.is_seeing = False
                                player.rect.topleft = block.rect.topleft
                                block_found = True

                                if all(not b.is_seeing for b in blocks):
                                    y = 650
                                    blocks = create_blocks(margin, y)
                                    player.rect.x = margin - 100
                                break

                if not block_found:
                    errors -= 1
                    score -= 15

        camera.update(player)

        screen.fill(WHITE)

        for block in blocks:
            block.draw(camera)

        pygame.draw.rect(screen, BLUE, camera.apply(player.rect))

        score_text = font.render(f"Sanidade caindo em : %{score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        erros_text = font.render(f"ERROS: {errors}", True, BLACK)
        screen.blit(erros_text, (10, 50))

        if score <= 0 or errors <= 0:
            finish_text = font.render("FIM DE JOGO", True, BLACK)
            screen.blit(finish_text, (10, 100))

        pygame.display.flip()

    pygame.quit()


game_loop()