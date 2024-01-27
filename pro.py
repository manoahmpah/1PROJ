class Pawn:
    def __init__(self, player, name):
        self.__player = player
        self.__name = name


class Logic:
    def __init__(self, name):
        self.__n = 11
        self.__Board = self.board()
        self.__PlayerToPlay = 1
        self.__PlayerName = name

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
                elif isinstance(self.__Board[row][col], Pawn):
                    print("*", end=" ")
            print("")

    def PossibleToPut(self, i, j):
        return True if 0 <= i < self.__n and 0 <= j < self.__n and self.__Board[i][j] == 1 else False

    def Put(self, i, j):
        if self.PossibleToPut(i, j):
            self.__Board[i][j] = Pawn(self.__PlayerToPlay, self.__PlayerName)
        else:
            print("Cette position est impossible !")


logic_obj = Logic('Luc')
# logic_obj.Display()
logic_obj.Put(0, 7)
logic_obj.Display()
