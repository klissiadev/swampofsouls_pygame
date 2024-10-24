import pygame

PLAYER_WIDTH = 32
PLAYER_HEIGHT = 64

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.sprites = []

        for i in range(1, 9):
            sprite = pygame.image.load(f'level02/sprites/walking/ALMA_WALKING{i}.png').convert_alpha()
            self.sprites.append(sprite)

        self.current_sprite = 0

        self.image = self.sprites[int(self.current_sprite)]

        self.isAnimating = False

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]


    def animate(self):
        self.isAnimating = True

    def stopAnimating(self):
        self.image = pygame.image.load(f'level02/sprites/idle/ALMA.png').convert_alpha()

    def update(self, speed):
        if self.isAnimating == True:
            self.current_sprite += speed

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.isAnimating = False

        self.image = self.sprites[int(self.current_sprite)]




