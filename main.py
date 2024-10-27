import pygame
from classes.menu_class import SwampOfSoulsScreen
from classes.interval_1_class import IntervalScreen
from classes.interval_2_class import Interval2Screen
from classes.interval_3_class import Interval3Screen
from level_2_class import LevelTwoScreen
from level_4_class import LevelFourScreen
from level1 import LevelOneScreen

# Inicializar o pygame
pygame.init()

# Definir as dimensões da tela
WIDTH, HEIGHT = 1320, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Cria a tela (game_screen)
pygame.display.set_caption("Swamp of Souls")

# Função principal
def main():
    # Inicializar o menu
    #menu_screen = SwampOfSoulsScreen()  # Passa a tela para o menu
    #menu_screen.run()  # Executa o menu

    # Após o menu, inicializa o jogo
    #game_screen = IntervalScreen()  # Inicializa o jogo
    #game_screen.run()  # Executa o jogo

    #level_screen = LevelOneScreen()
    #level_screen.run()

    #game_screen = Interval2Screen()  # Inicializa o jogo
    #game_screen.run()  # Executa o jogo

    #level_screen = LevelTwoScreen()
    #level_screen.run()

    #game_screen = Interval3Screen()  # Inicializa o jogo
    #game_screen.run()  # Executa o jogo

    level_screen = LevelFourScreen()
    level_screen.run()

    game_screen = Interval2Screen()  # Inicializa o jogo
    game_screen.run()  # Executa o jogo




if __name__ == '__main__':
    main()
