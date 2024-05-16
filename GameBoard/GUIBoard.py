import pygame
from LogicGame import Logic, Pawn
from BoardRenderer import BoardRenderer
from GameLogicHandler import GameLogicHandler
from EventHandler import EventHandler

class GUIBoard:
    def __init__(self):
        pygame.init()
        self.width = 1080
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.SRCALPHA)
        pygame.display.set_caption('yinsh')
        self.running = True

        self.logic_obj = Logic('Maëlys', 'Léa')
        self.board_renderer = BoardRenderer(self.screen, self.logic_obj)
        self.game_logic_handler = GameLogicHandler(self.logic_obj, self.board_renderer)
        self.event_handler = EventHandler(self.game_logic_handler, self.board_renderer)

    def run(self):
        while self.running:
            self.board_renderer.refresh()
            event = pygame.event.poll()
            self.event_handler.handle_event(event)
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

if __name__ == "__main__":
    plateau = GUIBoard()
    plateau.run()
