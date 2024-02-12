class Pawn:
    def __init__(self, player, name):
        self.__player = player
        self.__name = name


class Logic:
    def __init__(self, name1, name2):
        self.__n = 11
        self.__Board = []
        self.__PlayerToPlay = 1
        self.__name1, self.__name2 = name1, name2

    def get_current_player(self):
        return self.__PlayerToPlay

    def get_Board(self):
        return self.__Board

    def CreateBoard(self):

        for (a, b, c) in [(6, 4, 1), (4, 7, 0), (3, 8, 0), (2, 9, 0), (1, 10, 0), (1, 9, 1), (0, 10, 1), (0, 9, 2),
                          (0, 8, 3), (0, 7, 4), (1, 4, 6)]:
            # nine is a null box & one is an empty box
            boardAnex = [9 for _ in range(a)] + [1 for _ in range(b)] + [9 for _ in range(c)]
            self.__Board.append(boardAnex)

    def Display(self):
        self.CreateBoard()
        for row in range(self.__n):
            print(" " * row, end=" ")
            for col in range(self.__n):
                if self.__Board[row][col] == 9:
                    print(" ", end=" ")
                elif self.__Board[row][col] == 1:
                    print("0", end=" ")
                elif isinstance(self.__Board[row][col], Pawn) and self.__PlayerToPlay == 1:
                    print("*", end=" ")
                elif isinstance(self.__Board[row][col], Pawn) and self.__PlayerToPlay == 2:
                    print("_", end=" ")
            print("")

    def PossibleToPut(self, i, j):
        return True if 0 <= i < self.__n and 0 <= j < self.__n and self.__Board[i][j] == 1 else False

    def Put(self, i, j):
        if self.PossibleToPut(i, j):
            if self.__PlayerToPlay == 1:
                self.__Board[i][j] = Pawn(self.__PlayerToPlay, self.__name1)
            else:
                self.__Board[i][j] = Pawn(self.__PlayerToPlay, self.__name2)

        else:
            print("Cette position est impossible !")

    def OneDirection(self, PositionY, PositionX, i, j):
        return 1 + self.OneDirection(PositionY + i, PositionX + j, i, j) \
            if (0 <= PositionX + j < self.__n
                and 0 <= PositionY + i < self.__n
                and self.__Board[PositionY + i][PositionX + j] == (-self.__PlayerToPlay)) \
            else 0

    def AllDirection(self, PositionY, PositionX):
        column, line, Slash, = 0, 0, 0
        for index, (i, j) in enumerate([(0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, -1)]):

            if index < 2:
                column += self.OneDirection(PositionY, PositionX, i, j)
            elif 2 <= index < 4:
                line += self.OneDirection(PositionY, PositionX, i, j)
            else:
                Slash += self.OneDirection(PositionY, PositionX, i, j)

        return True if column + 1 >= 5 or line + 1 >= 5 or Slash + 1 >= 5 else False


logic_obj = Logic('Luc', 'Jean-Marc')
logic_obj.CreateBoard()
logic_obj.Put(0, 7)
logic_obj.Display()
