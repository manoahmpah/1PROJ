import pygame
from LogicGame import Pawn

class GameLogicHandler:
    def __init__(self, logic_obj, board_renderer):
        self.logic_obj = logic_obj
        self.board_renderer = board_renderer
        self.position_click_x = -1
        self.position_click_y = -1
        self.move_click = 1
        self.click_x_p1, self.click_y_p1 = None, None
        self.click_x_p2, self.click_y_p2 = None, None

    @staticmethod
    def transform_cord_to_pos(self, x, y) -> tuple:
        return int(y // 51) - 2, int(((x - (30 * ((y // 51) - 2))) // 60) - 1)

    def pixel_to_coordinate_transformation(self, x: int, y: int) -> tuple:
        for point in self.board_renderer.position_points:
            if (point['pos_x'] - 30 < x < point['pos_x'] + 30) and (point['pos_y'] - 25 < y < point['pos_y'] + 25):
                return self.transform_cord_to_pos(point['pos_x'], point['pos_y'])
        return None

    def put_on_click(self) -> tuple:
        pixel_x, pixel_y = pygame.mouse.get_pos()

        if self.position_click_y == -1 and self.position_click_x == -1:
            coords = self.pixel_to_coordinate_transformation(pixel_x, pixel_y)
            self.position_click_x, self.position_click_y = coords if coords else (-1, -1)

            if self.logic_obj.possible_to_put(self.position_click_x, self.position_click_y):
                self.logic_obj.put(self.position_click_x, self.position_click_y)
                self.logic_obj.set_player_to_play((self.logic_obj.get_player_to_play() % 2) + 1)
                self.logic_obj.set_pawn_number_on_board(self.logic_obj.get_pawn_number_on_board() + 1)
                self.board_renderer.error_message = ''
            else:
                if self.board_renderer.error_message == '':
                    self.board_renderer.error_message = 'Impossible to put your pawn here!'

        return self.position_click_x, self.position_click_y

    def reinitialise_click(self):
        self.position_click_x, self.position_click_y = -1, -1

    def handle_first_click_move(self, mouse_coordinate_x, mouse_coordinate_y, board_piece):
        board_piece.set_selected(True)
        self.click_x_p1, self.click_y_p1 = mouse_coordinate_x, mouse_coordinate_y
        self.move_click = 2
        self.board_renderer.error_message = ''

    def handle_second_click_move(self, mouse_coordinate_x, mouse_coordinate_y):
        winning_move = False
        self.logic_obj.set_list_alignment([[], [], []])

        if mouse_coordinate_x == self.click_x_p1 and mouse_coordinate_y == self.click_y_p1:
            self.logic_obj.get_board()[mouse_coordinate_x][mouse_coordinate_y].set_selected(False)
            self.board_renderer.set_refresh(True)
            self.move_click = 1

        elif self.logic_obj.possible_to_move(self.click_x_p1, self.click_y_p1, mouse_coordinate_x, mouse_coordinate_y)[0]:
            self.logic_obj.change_mark_on_move(self.click_x_p1, self.click_y_p1, mouse_coordinate_x, mouse_coordinate_y)
            if self.logic_obj.check_win(self.click_x_p1, self.click_y_p1):
                self.logic_obj.delete_on_alignment()
                winning_move = True
                if self.logic_obj.get_player_to_play() == 1:
                    self.board_renderer.winning_move_player_one += 1
                else:
                    self.board_renderer.color_pawn_win_player_one[self.board_renderer.winning_move_player_one-1] = (0, 0, 0)
                    self.board_renderer.winning_move_player_two += 1

            self.click_x_p2, self.click_y_p2 = mouse_coordinate_x, mouse_coordinate_y
            self.move_click = 1
            self.logic_obj.move(self.click_x_p1, self.click_y_p1, self.click_x_p2, self.click_y_p2, winning_move)
            if not winning_move:
                self.logic_obj.get_board()[mouse_coordinate_x][mouse_coordinate_y].set_selected(False)

            self.board_renderer.set_refresh(True)
            self.board_renderer.error_message = ''
            self.logic_obj.set_player_to_play(self.logic_obj.get_player_to_play() % 2 + 1)
        else:
            self.board_renderer.error_message = self.logic_obj.possible_to_move(self.click_x_p1, self.click_y_p1, mouse_coordinate_x, mouse_coordinate_y)[1]

    def move_pawns(self):
        mouse_coordinate = self.pixel_to_coordinate_transformation(*pygame.mouse.get_pos())

        if mouse_coordinate is None:
            return

        mouse_coordinate_x, mouse_coordinate_y = mouse_coordinate
        board_piece = self.logic_obj.get_board()[mouse_coordinate_x][mouse_coordinate_y]
        current_player = self.logic_obj.get_player_to_play()

        if self.move_click == 1 and isinstance(board_piece, Pawn) and board_piece.get_player() == current_player:
            self.handle_first_click_move(mouse_coordinate_x, mouse_coordinate_y, board_piece)
        elif self.move_click == 2:
            self.handle_second_click_move(mouse_coordinate_x, mouse_coordinate_y)
        else:
            if self.board_renderer.error_message == '':
                self.board_renderer.error_message = 'please press a white pawn!' if current_player == 1 else 'please press a black pawn!'
