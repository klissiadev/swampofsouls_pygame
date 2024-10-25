import random

import pygame
import time
import math
import player as player_mod

# Initializing Pygame
pygame.init()

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (185, 185, 185)
YELLOW = (255, 255, 0)

# Defining fonts
small_font = pygame.font.Font("./level04/IMFellEnglish-Regular.ttf", 24)
x_small_font = pygame.font.Font("./level04/IMFellEnglish-Regular.ttf", 16)

# Screen dimensions
WIDTH, HEIGHT = 1320, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interval - 02")

scroll = 0

bg_images = []
for i in range(2, 6):
    bg_image = pygame.image.load(f'./level02/background/BG_{i}.png').convert_alpha()
    bg_images.append(bg_image)

bg_width = bg_images[0].get_width()

# players sounds
background_sound = pygame.mixer.Sound('./assets/sounds-effects/Alone at Twilight 5.wav')
click_sound = pygame.mixer.Sound('./level04/click-keyboard.mp3')
background_sound.set_volume(0.5)  # Define o volume para 50%
background_sound.play()

# Player
moving_sprites = pygame.sprite.Group()
player = player_mod.Player(40, 370, "Right")
moving_sprites.add(player)
player_position = [40,370]

# Jar
jar = pygame.transform.scale(pygame.image.load('./assets/objects/jar.png').convert_alpha(), (60, 60))
jar_positions = [WIDTH - 60 , HEIGHT - 150]

# Classe para os blocos brilhantes (vagalumes)
class Firefly(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Tamanho do bloco (vagalume)
        self.image = pygame.Surface((6, 6))
        self.image.fill(YELLOW)  # Cor inicial do vagalume
        self.rect = self.image.get_rect()

        # Posição inicial aleatória
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)

        # Controle de brilho
        self.alpha = random.randint(50, 255)  # Transparência inicial (opacidade)
        self.fade_speed = random.uniform(1, 3)  # Velocidade do brilho

        # Movimento aleatório (simula voo)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

    def update(self):
        # Movimento aleatório
        self.rect.x += self.vx
        self.rect.y += self.vy

        # Mantém o vagalume dentro dos limites da tela
        if self.rect.x < 0 or self.rect.x > WIDTH:
            self.vx = -self.vx
        if self.rect.y < 0 or self.rect.y > HEIGHT:
            self.vy = -self.vy

        # Alterar o valor de alpha para criar o efeito de "brilho" (fade in/out)
        self.alpha += self.fade_speed

        # Faz o brilho "pulsar" ao atingir certos limites
        if self.alpha >= 255:
            self.alpha = 255
            self.fade_speed *= -1  # Inverter para diminuir o brilho
        elif self.alpha <= 50:
            self.alpha = 50
            self.fade_speed *= -1  # Inverter para aumentar o brilho

        # Aplicar o valor de alpha à imagem
        self.image.set_alpha(self.alpha)

# Criar um grupo de sprites para os vagalumes
fireflies = pygame.sprite.Group()

# Criar múltiplos vagalumes
for _ in range(10):  # 20 vagalumes
    firefly = Firefly()
    fireflies.add(firefly)

def drawBackground():
    static_bg_image = pygame.image.load(f'./level02/background/BG_1.png').convert_alpha()
    screen.blit(static_bg_image, (0, 0))

    for x in range(6):
        speed = 1
        for l in bg_images:
            screen.blit(l, ((x * bg_width) - scroll * speed, 0))
            speed += 0.6


def darken_screen(opacity):
    dark_overlay = pygame.Surface((WIDTH, HEIGHT))
    dark_overlay.set_alpha(opacity)
    dark_overlay.fill(BLACK)
    screen.blit(dark_overlay, (0, 0))

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
                jar_positions[0] -= 4
            player.animate()
        elif keys[pygame.K_LEFT]:
            player.orientation = "Left"

            if player_position[0] > 40:
                player_position[0] -= 4
                if scroll > 0:
                    scroll -= 2
                    jar_positions[0] += 4
            player.animate()
        else:
            player.stopAnimating()

        if abs(scroll) > bg_width:
            scroll = 0
        elif abs(scroll) < 0:
            scroll = bg_width

        moving_sprites.update(0.25)
        darken_screen(180)

        # Atualizar vagalumes
        fireflies.update()

        # Desenhar vagalumes na tela
        fireflies.draw(screen)

        #Draw jar
        screen.blit(jar, (jar_positions[0], jar_positions[1]))

        if abs((player_position[0] + 36) - jar_positions[0]) < 70:
            press_e_text = x_small_font.render(f'Press E', True, WHITE)
            screen.blit(press_e_text, (jar_positions[0] + 5 , jar_positions[1] - 60))

        # Draw the tip
        tip_text = small_font.render(f'Look for some lighting...', True, WHITE)
        screen.blit(tip_text, (50, HEIGHT - 60))
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    game_loop()
