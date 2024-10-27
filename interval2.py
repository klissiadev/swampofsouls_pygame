import pygame
import player as player_mod
from classes.level_2_class import LevelTwoScreen

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



class Interval2Screen:
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

        self.animal_foot = pygame.transform.scale(pygame.image.load('assets/objects/Animal Footstep.png').convert_alpha(), (60, 60))
        self.foot_positions = [WIDTH - 10, HEIGHT - 100]


    def drawBackground(self):
            static_bg_image = pygame.image.load(f'./level02/background/BG_1.png').convert_alpha()
            screen.blit(static_bg_image, (0, 0))

            for x in range(6):
                speed = 1
                for l in self.bg_images:
                    screen.blit(l, ((x * self.bg_width) - self.scroll * speed, 0))
                    speed += 0.6

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
                            running = False

                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]:
                    self.player.orientation = 'Right'
                    if self.player_position[0] < WIDTH - 300:
                        self.player_position[0] += 4
                    else:
                        self.scroll += 2
                        self.foot_positions[0] -= 4
                    self.player.animate()
                elif keys[pygame.K_LEFT]:
                    self.player.orientation = "Left"

                    if self.player_position[0] > 40:
                        self.player_position[0] -= 4
                        if self.scroll > 0:
                            self.scroll -= 2
                            self.foot_positions[0] += 4
                    self.player.animate()
                else:
                    self.player.stopAnimating()

                if abs(self.scroll) > self.bg_width:
                    self.scroll = 0
                elif abs(self.scroll) < 0:
                    self.scroll = self.bg_width

                self.moving_sprites.update(0.25)

                #Draw footsteps
                screen.blit(self.animal_foot, (self.foot_positions[0], self.foot_positions[1]))

                if abs((self.player_position[0] + 36) - self.foot_positions[0]) < 70:
                    press_e_text = x_small_font.render(f'Press E', True, WHITE)
                    screen.blit(press_e_text, (self.foot_positions[0] + 10 , HEIGHT - 35))
                    tip_text = small_font.render(f'Oh...? footsteps of animals...', True, WHITE)
                    screen.blit(tip_text, (400, HEIGHT - 200))
                    pygame.display.update()


                # Draw the tip
                tip_text = small_font.render(f'Where am i supposed to go...?', True, WHITE)
                screen.blit(tip_text, (50, HEIGHT - 60))
                pygame.display.update()

            pygame.quit()


if __name__ == '__main__':
    level_two_screen = LevelTwoScreen()
    level_two_screen.run()
    pygame.quit()