import pygame
import random
import player as player_mod
pygame.init()

# screen settings
width = 1320
height = 680
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
FPS = 60

#background
bg1 = pygame.image.load('level03/Group 68.png')
bg1 = pygame.transform.scale(bg1, (width, height))
background_sound = pygame.mixer.Sound('level03/Alone at Twilight 5.wav')
background_sound.set_volume(0.5)
background_sound.play()


#blocks
block_image = pygame.image.load('level03/Group 29 (1).png').convert_alpha()
block_rect = block_image.get_rect(topleft=(250, 600))
block_sound = pygame.mixer.Sound('level03/walk-in-dry-leaves-in-the-forest-22431.mp3')
block_sound.set_volume(0.2)

scroll = 0

bg_images = []
for i in range(2, 6):
    print(i)
    bg_image = pygame.image.load(f'./level02/background/BG_{i}.png').convert_alpha()
    bg_images.append(bg_image)

bg_width = bg_images[0].get_width()
moving_sprites = pygame.sprite.Group()
player = player_mod.Player(40, 370, "Right")
moving_sprites.add(player)
player_position = [40,370]

def drawBackground():
    static_bg_image = pygame.image.load(f'./level02/background/BG_1.png').convert_alpha()
    screen.blit(static_bg_image, (0, 0))

    for x in range(6):
        speed = 1
        for l in bg_images:
            screen.blit(l, ((x * bg_width) - scroll * speed, 0))
            speed += 0.6

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# font
normal_font = pygame.font.Font('level04/IMFellEnglish-Regular.ttf', 40)

class Block:
    def __init__(self, x, y, letter, ):
        self.rect = pygame.Rect(x, y, 75, 75)
        self.letter = letter
        self.is_seeing = True
        self.image = pygame.image.load('level03/Group 29 (1).png').convert_alpha()
        self.total_blocks = 10
        self.blocks_positions = [(i * 69, height // 2) for i in range(self.total_blocks)]

    def draw(self, camera):
        if self.is_seeing:
            pos = camera.apply(self.rect)
            screen.blit(self.image, pos)
            font = pygame.font.Font(None, 50)
            text1 = font.render(self.letter, True, (255, 255, 255))
            text_rect = text1.get_rect(center=(pos.centerx + 200 , pos.top - 10))
            screen.blit(text1, text_rect)

    def resetar(self, x, y, letter):
        self.rect.topleft = (x, y)
        self.letter = letter
        self.is_seeing = True
        self.image = pygame.image.load('level03/Group 29 (1).png').convert_alpha()


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, rect):
        return rect.move(-self.camera.x, -self.camera.y)

    def update(self, target):
        x = -target.x + int(800 / 2)
        y = -target.y + int(600 / 2)
        x = min(0, x)
        y = max(0, y)
        x = max(-(self.width - 800), x)
        y = max((self.height - 600), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)

def create_blocks(margin, y):
    blocks = []
    block_width = 75
    space = 100
    x = margin
    for i in range(5):  # Cria 5 blocos
        letter = random.choice(['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'R', ' '])
        block = Block(x, y, letter)
        blocks.append(block)
        x += block_width + space
    return blocks

def game_loop():
    global scroll, bg_width
    margin = 200
    y = height // 2
    blocks = create_blocks(margin, y)
    camera = Camera(1320, 680)
    running = True
    score = 100
    errors = 5


    while running:
        block_found = False

        clock.tick(FPS)

        drawBackground()

        for block in blocks:
            block.draw(camera)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                letter_is_pressed = event.unicode.upper()

                for block in blocks:
                    if block.is_seeing and block.letter == letter_is_pressed:
                        if block.rect.x > player_position[0] or abs(block.rect.x - player_position[0]) < 10:
                                block.is_seeing = False
                                player.rect.midbottom = (block.rect.centerx, block.rect.top)
                                block_found = True
                                scroll += 5
                                block_sound.play()

                                if all(not b.is_seeing for b in blocks):
                                    y = height // 2
                                    blocks = create_blocks(margin, y)
                                    player_position[0] = margin - 100
                                    player.animate()
                                    scroll += 20
                                else:
                                    player.stopAnimating()
                                break

                if not block_found:
                    errors -= 1
                    score -= 15


        if abs(scroll) > bg_width:
            scroll = 0
        elif abs(scroll) < 0:
            scroll = bg_width

        screen.blit(player.image, (player_position[0], player_position[1]))

        score_text = normal_font.render(f"Sanidade caindo em : %{score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        erros_text = normal_font.render(f"ERROS: {errors}", True, WHITE)
        screen.blit(erros_text, (10, 50))

        if score <= 0 or errors <= 0:
            screen.fill(BLACK)
            finish_text = normal_font.render("FIM DE JOGO...?", True, WHITE)
            screen.blit(finish_text, (10, 100))

        moving_sprites.update(0.25)
        pygame.display.update()


    pygame.quit()


game_loop()