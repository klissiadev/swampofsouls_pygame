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

# Defining fonts
small_font = pygame.font.Font("./level04/IMFellEnglish-Regular.ttf", 24)
x_small_font = pygame.font.Font("./level04/IMFellEnglish-Regular.ttf", 16)

# Screen dimensions
WIDTH, HEIGHT = 1320, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interval - 03")


class Interval3Screen:
    def __init__(self):
        self.scroll = 0
        self.moving_sprites = pygame.sprite.Group()
        self.player = player_mod.Player(40, 370, "Right")
        self.moving_sprites.add(self.player)
        self.player_position = [40, 370]
        self.bg_image = [pygame.image.load(f'./level02/background/BG_{i}.png').convert_alpha() for i in range(2, 6)]
        self.bg_width = self.bg_image[0].get_width()

        self.background_sound = pygame.mixer.Sound('./assets/sounds-effects/Alone at Twilight 5.wav')
        self.click_sound = pygame.mixer.Sound('./level04/click-keyboard.mp3')
        self.background_sound.set_volume(0.5)  # Define o volume para 50%
        self.background_sound.play()

        # thorns
        self.thorns = pygame.transform.scale(pygame.image.load('./level03/Group 29 (1).png').convert_alpha(), (280, 280))
        self.thorns_positions = [WIDTH + 100, HEIGHT - 350]

        # Opacity for fade effect
        self.opacity = 255
        self.fade_speed = 5  # Control the speed of the fade-out effect

    def darken_screen(self):
        if self.opacity > 0:
            dark_overlay = pygame.Surface((WIDTH, HEIGHT))
            dark_overlay.set_alpha(self.opacity)
            dark_overlay.fill(BLACK)
            screen.blit(dark_overlay, (0, 0))
            self.opacity -= self.fade_speed  # Reduce opacity to create fade-out effect

    def drawBackground(self):
        static_bg_image = pygame.image.load(f'./level02/background/BG_1.png').convert_alpha()
        screen.blit(static_bg_image, (0, 0))

        for x in range(6):
            speed = 1
            for l in self.bg_image:
                screen.blit(l, ((x * self.bg_width) - self.scroll * speed, 0))
                speed += 0.6


# Game loop
    def run(self):

        running = True

        while running:
            screen.fill(WHITE)

            clock.tick(FPS)

            self.drawBackground()
            screen.blit(self.player.image, (self.player_position[0], self.player_position[1]))

            # Check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.unicode.upper() == 'E':
                        self.click_sound.play()
                        running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.player.orientation = 'Right'
                if self.player_position[0] < WIDTH - 300 and self.player_position[0] + 32 < self.thorns_positions[0]:
                    self.player_position[0] += 4
                else:
                    if self.thorns_positions[0] > WIDTH - 240:
                        self.scroll += 2
                        self.thorns_positions[0] -= 4
                self.player.animate()
            elif keys[pygame.K_LEFT]:
                self.player.orientation = "Left"

                if self.player_position[0] > 40:
                    self.player_position[0] -= 4
                    if self.scroll > 0:
                        self.scroll -= 2
                        self.thorns_positions[0] += 4
                self.player.animate()
            else:
                self.player.stopAnimating()

            if abs(self.scroll) > self.bg_width:
                self.scroll = 0
            elif abs(self.scroll) < 0:
                self.scroll = self.bg_width

            self.moving_sprites.update(0.25)

            #Draw jar
            screen.blit(self.thorns, (self.thorns_positions[0], self.thorns_positions[1]))

            if abs((self.player_position[0] + 36) - self.thorns_positions[0]) < 70:
                press_e_text = x_small_font.render(f'Press E', True, WHITE)
                screen.blit(press_e_text, (self.thorns_positions[0] + 120, self.thorns_positions[1] - 60))
                tip_text = small_font.render(f'For god''s sake! Something is blocking the passage...', True, WHITE)
                screen.blit(tip_text, (400, HEIGHT - 200))
                pygame.display.update()

            # Draw the tip
            tip_text = small_font.render(f'Where am i supposed to go...?', True, WHITE)
            screen.blit(tip_text, (50, HEIGHT - 60))

            self.darken_screen()
            pygame.display.update()


if __name__ == '__main__':
    interval_screen = Interval3Screen()
    interval_screen.run()
    pygame.quit()
