import pygame

from ComingSoonScreen import ComingSoonScreen
from menu_class import SwampOfSoulsScreen
from interval_1_class import IntervalScreen
from interval_2_class import Interval2Screen
from interval_3_class import Interval3Screen
from interval4 import Interval4Screen
from level_2_class import LevelTwoScreen
from level1 import LevelOneScreen
from level3 import LevelThreeOnScreen
from level_4_class import LevelFourScreen
from history import HistoryScreen

# Inicializar o pygame
pygame.init()

# Definir as dimensões da tela
WIDTH, HEIGHT = 1320, 680
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Cria a tela (game_screen)
pygame.display.set_caption("Swamp of Souls")

# Função principal
def main():
    # Inicializar o menu
    menu_screen = SwampOfSoulsScreen()  # Passa a tela para o menu
    menu_screen.run()  # Executa o menu

    history = HistoryScreen()
    history.run()

    # Após o menu, inicializa o jogo
    game_screen = IntervalScreen()  # Inicializa o jogo
    game_screen.run()  # Executa o jogo


    level_screen = LevelOneScreen()
    level_screen.run()

    game_screen = Interval2Screen()
    game_screen.run()

    level_screen = LevelTwoScreen()
    level_screen.run()

    game_screen = Interval3Screen()
    game_screen.run()

    level_screen = LevelThreeOnScreen()
    level_screen.run()

    game_screen = Interval4Screen()
    game_screen.run()

    level_screen = LevelFourScreen()
    level_screen.run()

    history_screen = ComingSoonScreen()
    history_screen.run()

if __name__ == '__main__':
    main()
