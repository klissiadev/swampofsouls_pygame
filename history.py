import pygame
import sys

class HistoryScreen:
    def __init__(self):
        # Initializing Pygame
        pygame.init()

        # Clock
        self.clock = pygame.time.Clock()
        self.FPS = 40

        # Screen dimensions
        self.WIDTH, self.HEIGHT = 1320, 680
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Swamp of Souls")

        # Background and images
        self.bg_image = pygame.image.load('./assets/tutorials/FIRSTSCENE.png').convert_alpha()
        self.bg_image2 = pygame.image.load('./assets/tutorials/SECONDSCENE.png').convert_alpha()
        self.current_bg = self.bg_image

        # Timer and effect durations
        self.wait_time = 3000           # 5 seconds to show the first image before fade
        self.transition_time = 3000      # 3 seconds for fade-out of the first image
        self.flash_duration = 300        # 500 milliseconds for flash
        self.final_scene_duration = 500 # Show the second image for 3 seconds
        self.start_time = pygame.time.get_ticks()
        self.alpha = 255                 # Initial opacity for fade-out

        # Sound effects
        self.background_sound = pygame.mixer.Sound('./assets/sounds-effects/Exploring Nightmare.wav')
        self.click_sound = pygame.mixer.Sound('./level04/click-keyboard.mp3')
        self.background_sound.set_volume(0.6)
        self.background_sound.play()

        # State tracking
        self.is_waiting = True
        self.is_fading_out_first = False
        self.is_flashing = False
        self.is_final_scene = False
        self.is_fading_to_black = False

    def run(self):
        running = True
        flash_start_time = None
        final_scene_start_time = None
        final_fade_start_time = None

        while running:
            self.screen.fill((0, 0, 0))  # Start with black background

            # Get the current time
            current_time = pygame.time.get_ticks()

            # Initial wait before fade-out
            if self.is_waiting:
                self.screen.blit(self.bg_image, (-90, 0))  # Display the first image
                if current_time - self.start_time >= self.wait_time:
                    self.is_waiting = False
                    self.is_fading_out_first = True

            # Fade out effect for the first image
            elif self.is_fading_out_first:
                if self.alpha > 0:
                    self.alpha -= 5  # Adjust fade-out speed
                    faded_bg = self.bg_image.copy()
                    faded_bg.set_alpha(self.alpha)
                    self.screen.blit(faded_bg, (-90, 0))
                else:
                    self.is_fading_out_first = False
                    self.is_flashing = True
                    flash_start_time = current_time  # Start flash timer

            # Flash effect
            elif self.is_flashing:
                if current_time - flash_start_time < self.flash_duration:
                    self.screen.fill((255, 255, 255))  # Flash white
                else:
                    self.is_flashing = False
                    self.is_final_scene = True
                    final_scene_start_time = current_time  # Start final scene timer
                    self.screen.blit(self.bg_image2, (-90, 0))  # Display the second image

            # Show the second image for a set time
            elif self.is_final_scene:
                self.screen.blit(self.bg_image2, (-90, 0))
                if current_time - final_scene_start_time > self.final_scene_duration:
                    self.is_final_scene = False
                    self.is_fading_to_black = True
                    final_fade_start_time = current_time  # Start final fade-to-black

            # Final fade-to-black effect
            elif self.is_fading_to_black:
                if self.alpha < 255:
                    self.alpha += 5  # Adjust speed of fade-to-black
                    faded_bg = pygame.Surface((self.WIDTH, self.HEIGHT))
                    faded_bg.fill((0, 0, 0))
                    faded_bg.set_alpha(self.alpha)
                    self.screen.blit(self.bg_image2, (-90, 0))  # Keep second image in background
                    self.screen.blit(faded_bg, (0, 0))
                else:
                    running = False  # Exit after fade-to-black completes

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.click_sound.play()
                    running = False

            pygame.display.update()
            self.clock.tick(self.FPS)

        # Stop background sound when exiting
        self.background_sound.stop()

if __name__ == '__main__':
    tutorial_screen = HistoryScreen()
    tutorial_screen.run()
    pygame.quit()
