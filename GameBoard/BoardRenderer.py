import pygame
from LogicGame import Pawn

class BoardRenderer:
    def __init__(self, screen, logic_obj):
        self.screen = screen
        self.logic_obj = logic_obj
        self.width = 1080
        self.height = 720
        self.background = (170, 184, 197)
        self.rect_all = pygame.Rect(0, 0, self.width, self.height)
        self.rect_board = pygame.Rect(self.rect_all.centerx - self.width / 2.4, self.rect_all.centery - self.height / 2.4, self.width / 1.2, self.height / 1.2)
        self.position_points = []
        self.half_dim_hit_box = 25
        self.padding_rect = 30
        self.rect_name1 = pygame.Rect(self.rect_all.left + 10, self.rect_all.centery - 120, 100, 50)
        self.rect_name2 = pygame.Rect(self.rect_all.left + 10, self.rect_all.centery - 20, 100, 50)
        self.rect_error = pygame.Rect(self.rect_all.centerx - 100, self.rect_all.bottom - 100, 200, 50)
        self.error_message = ""
        self.refresh_flag = True
        self.winning_move_player_one = 0
        self.winning_move_player_two = 0
        self.react_pawns_win_player_one = pygame.Rect(self.rect_all.left + 200, self.rect_all.top + 20, 130, 70)
        self.color_pawn_win_player_one = [(50, 50, 50) for _ in range(3)]

    def refresh(self):
        if self.refresh_flag:
            self.screen.fill(self.background)
            self.__display_board_gui()
            self.__player_name_display()
            self.rectangle_pawn_win_player_one()
            pygame.display.flip()
            self.refresh_flag = False

    def set_refresh(self, value: bool):
        self.refresh_flag = value

    def rectangle_pawn_win_player_one(self):
        pygame.draw.circle(self.screen, self.color_pawn_win_player_one[0], (self.react_pawns_win_player_one.centerx + 20, self.react_pawns_win_player_one.centery), 25, 7)
        pygame.draw.circle(self.screen, self.background, (self.react_pawns_win_player_one.centerx - 10, self.react_pawns_win_player_one.centery), 25)
        pygame.draw.circle(self.screen, self.color_pawn_win_player_one[1], (self.react_pawns_win_player_one.centerx - 10, self.react_pawns_win_player_one.centery), 25, 7)
        pygame.draw.circle(self.screen, self.background, (self.react_pawns_win_player_one.centerx - 40, self.react_pawns_win_player_one.centery), 25)
        pygame.draw.circle(self.screen, self.color_pawn_win_player_one[2], (self.react_pawns_win_player_one.centerx - 40, self.react_pawns_win_player_one.centery), 25, 7)

    def __display_board_gui(self):
        self.__create_text_error((0, 0, 0), 20)
        for row in range(len(self.logic_obj.get_board())):
            for col in range(len(self.logic_obj.get_board()[row])):
                pos_x, pos_y = self.__collision_area(row, col)
                self.__draw_circles_and_lines(row, col, pos_x, pos_y)

    def __collision_area(self, row: int, col: int) -> tuple:
        dimension = self.padding_rect * 2
        pos_x = self.rect_board.left + col * dimension + row * self.padding_rect
        pos_y = (self.rect_board.top + row * self.padding_rect) * 1.7
        return pos_x, pos_y

    def __draw_circles_and_lines(self, row: int, col: int, pos_x: int, pos_y: int):
        board = self.logic_obj.get_board()
        if board[row][col] != 9:
            self.position_points.append({'pos_x': pos_x, 'pos_y': pos_y})
            self.__draw_line_to_create_board(row, col, pos_x, pos_y)

            if isinstance(board[row][col], Pawn):
                player = board[row][col].get_player()
                color = (255, 255, 255) if player == 1 else (0, 0, 0)
                pygame.draw.circle(self.screen, color, (pos_x, pos_y), 25, 7)
                if board[row][col].get_selected():
                    pygame.draw.circle(self.screen, color, (pos_x, pos_y), 15)

            if board[row][col] == -1:
                pygame.draw.circle(self.screen, (255, 255, 255), (pos_x, pos_y), 15)
            elif board[row][col] == -2:
                pygame.draw.circle(self.screen, (0, 0, 0), (pos_x, pos_y), 15)

    def __draw_line_to_create_board(self, row, col, pos_x, pos_y):
        board = self.logic_obj.get_board()
        if col + 1 < len(board[row]) and board[row][col + 1] != 9:
            col_pos = self.__collision_area(row, col + 1)
            pygame.draw.line(self.screen, (0, 0, 0), (pos_x, pos_y), col_pos, 2)

        if row + 1 < len(board):
            if col - 1 < len(board) and board[row + 1][col - 1] != 9:
                diag_col_pos = self.__collision_area(row + 1, col - 1)
                pygame.draw.line(self.screen, (0, 0, 0), (pos_x, pos_y), diag_col_pos, 2)

            if board[row + 1][col] != 9:
                next_row_pos = self.__collision_area(row + 1, col)
                pygame.draw.line(self.screen, (0, 0, 0), (pos_x, pos_y), next_row_pos, 2)

    def __create_text_name(self, text: str, rect, color: tuple, color_bg: tuple, font_size: int):
        pygame.draw.rect(self.screen, color_bg, rect)
        font = pygame.font.Font(None, font_size)
        name = font.render(text, True, color)
        text_rect = name.get_rect()
        text_rect.center = rect.center
        self.screen.blit(name, text_rect)

    def __create_text_error(self, color: tuple, font_size: int):
        pygame.draw.rect(self.screen, (170, 184, 197), self.rect_error)
        font = pygame.font.Font(None, font_size)
        name = font.render(self.error_message, True, color)
        text_rect = name.get_rect()
        text_rect.center = (self.rect_error.centerx, self.rect_error.centery)
        self.screen.blit(name, text_rect)

    def __player_name_display(self):
        color_bg_name1 = (255, 255, 255) if self.logic_obj.get_player_to_play() == 1 else (170, 184, 197)
        if self.logic_obj.get_player_to_play() == 2:
            color_font_name2 = (255, 255, 255)
            color_bg_name2 = (0, 0, 0)
        else:
            color_font_name2 = (0, 0, 0)
            color_bg_name2 = (170, 184, 197)

        self.__create_text_name(self.logic_obj.get_name1(), self.rect_name1, (0, 0, 0), color_bg_name1, 29)
        self.__create_text_name(self.logic_obj.get_name2(), self.rect_name2, color_font_name2, color_bg_name2, 29)
