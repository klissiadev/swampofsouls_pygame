import pygame
import player as player_mod

class Interval4Screen:
    def __init__(self):
        # Initializing Pygame
        pygame.init()

        # Clock
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Screen dimensions
        self.WIDTH, self.HEIGHT = 1320, 680
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Interval - 03")

        # Screen background
        self.background_image = pygame.transform.scale(pygame.image.load('./assets/backgrounds/BG-6.png'), (1400, 690))

        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (185, 185, 185)
        self.YELLOW = (255, 255, 0)

        # Defining fonts
        self.small_font = pygame.font.Font("./level04/IMFellEnglish-Regular.ttf", 24)
        self.x_small_font = pygame.font.Font("./level04/IMFellEnglish-Regular.ttf", 16)

        # Sounds
        self.background_sound = pygame.mixer.Sound('./assets/sounds-effects/Alone at Twilight 5.wav')
        self.click_sound = pygame.mixer.Sound('./level04/click-keyboard.mp3')
        self.background_sound.set_volume(0.5)  # Define o volume para 50%
        self.background_sound.play()

        # Player setup
        self.moving_sprites = pygame.sprite.Group()
        self.player = player_mod.Player(40, 370, "Right")
        self.moving_sprites.add(self.player)
        self.player_position = [40, 370]

        # Opacity for fade effect
        self.opacity = 255
        self.fade_speed = 5  # Control the speed of the fade-out effect

    def darken_screen(self):
        if self.opacity > 0:
            dark_overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
            dark_overlay.set_alpha(self.opacity)
            dark_overlay.fill(self.BLACK)
            self.screen.blit(dark_overlay, (0, 0))
            self.opacity -= self.fade_speed  # Reduce opacity to create fade-out effect

    def draw_elements(self):
        # Draw background and player
        self.screen.fill(self.WHITE)
        self.screen.blit(self.background_image, (-80, 0))
        self.screen.blit(self.player.image, (self.player_position[0], self.player_position[1]))

        # Draw the tip
        tip_text = self.small_font.render(f'Look, a bridge!', True, self.WHITE)
        self.screen.blit(tip_text, (50, self.HEIGHT - 60))

        if self.player_position[0] > self.WIDTH - 300:
            press_e_text = self.x_small_font.render(f'Press E', True, self.WHITE)
            self.screen.blit(press_e_text, (self.WIDTH - 100, self.HEIGHT - 300))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.unicode.upper() == 'E' and self.player_position[0] > self.WIDTH - 230:
                    self.click_sound.play()
                    return False
        return True

    def update_player_position(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.player.orientation = 'Right'
            if self.player_position[0] < self.WIDTH - 200:
                self.player_position[0] += 3
            self.player.animate()
        elif keys[pygame.K_LEFT]:
            self.player.orientation = "Left"
            if self.player_position[0] > 40:
                self.player_position[0] -= 3
            self.player.animate()
        else:
            self.player.stopAnimating()

    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)
            running = self.handle_events()
            self.update_player_position()
            self.moving_sprites.update(0.20)
            self.draw_elements()
            self.darken_screen()
            pygame.display.update()

        # Stop the background sound after exiting
        self.background_sound.stop()

if __name__ == '__main__':
    game = Interval4Screen()
    game.run()
    pygame.quit()
