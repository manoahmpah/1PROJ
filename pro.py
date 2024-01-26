class Pawn:
    def __init__(self, player):
        self.__player = player


class Logic:
    def __init__(self):
        self.__n = 11
        self.__Board = self.board()

    def getBoard(self):
        return self.__Board

    def board(self):
        board_2d = []
        for (a, b, c) in [(6, 4, 1), (4, 7, 0), (3, 8, 0), (2, 9, 0), (1, 10, 0), (1, 9, 1), (0, 10, 1), (0, 9, 2),
                          (0, 8, 3), (0, 7, 4), (1, 4, 6)]:
            # nine is a null box & one is an empty box
            boardAnex = [9 for _ in range(a)] + [1 for _ in range(b)] + [9 for _ in range(c)]
            board_2d.append(boardAnex)
        return board_2d

    def Display(self):
        for row in range(self.__n):
            for col in range(self.__n):
                if self.__Board[row][col] == 9:
                    print(".", end=" ")
                elif self.__Board[row][col] == 1:
                    print("0", end=" ")
            print("")


logic_obj = Logic()
logic_obj.Display()
