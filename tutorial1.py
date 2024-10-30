import pygame

class Tutorial1Screen:
    def __init__(self):
        # Initializing Pygame
        pygame.init()

        # Clock
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Screen dimensions
        self.WIDTH, self.HEIGHT = 1320, 680
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Swamp of Souls")

        # Background and images
        self.bg_image = pygame.image.load('./assets/tutorials/TUTORIAL1.png').convert_alpha()

        # Sounds
        self.background_sound = pygame.mixer.Sound('./assets/sounds-effects/Alone at Twilight 5.wav')
        self.click_sound = pygame.mixer.Sound('./level04/click-keyboard.mp3')
        self.background_sound.set_volume(0.2)
        self.background_sound.play()

    def run(self):
        running = True

        while running:

            self.screen.fill((255, 255, 255))  # Fill with white

            # Draw background
            self.screen.blit(self.bg_image, (0, 0))

            self.clock.tick(self.FPS)

            # Check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    self.click_sound.play()
                    running = False

            pygame.display.update()

if __name__ == '__main__':
    tutorial_screen = Tutorial1Screen()
    tutorial_screen.run()
    pygame.quit()