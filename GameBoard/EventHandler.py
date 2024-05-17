import pygame
from GameLogicHandler import GameLogicHandler


class EventHandler(GameLogicHandler):
    def __init__(self, game_logic_handler, board_renderer):
        super().__init__(game_logic_handler, board_renderer)
        self.game_logic_handler = game_logic_handler
        self.board_renderer = board_renderer

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.game_logic_handler.get_pawn_number_on_board() < 10:
                self._put_on_click()
                self._reinitialise_click()
            else:
                self.game_logic_handler.move_pawns()

            self.board_renderer.set_refresh(True)
        elif event.type == pygame.QUIT:
            pygame.quit()
