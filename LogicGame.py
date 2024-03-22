class Pawn:
    def __init__(self, player, name):
        """
        :param player: player number 1 or 2
        :param name: The name of the players
        """
        self.__player = player
        self.__name = name

    def getPlayer(self):
        return self.__player


class Logic:
    def __init__(self, name1, name2):
        """
        :param name1: Name of the players 1
        :param name2: Name of the players 2
        """
        self.__n = 11
        self.__Board = []
        self.__PlayerToPlay = 1
        self.__name1, self.__name2 = name1, name2
        self.__PawnNumberOnBoard = 0

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
                elif isinstance(self.__Board[row][col], Pawn) and self.__Board[row][col].getPlayer == 1:
                    print("*", end=" ")
                elif isinstance(self.__Board[row][col], Pawn) and self.__PlayerToPlay == 2:
                    print("_", end=" ")
                elif self.__Board[row][col] == -1:
                    print("@", end=" ")
                elif self.__Board[row][col] == -2:
                    print("%", end=" ")
            print("")

    def PossibleToPut(self, i, j):
        """
        :param i: Coordinate X of player
        :param j: Coordinate Y of player
        :return: boolean True or False
        """
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
        """
            Calculate the length of a sequence of opponent's pieces in one direction.

            :param PositionY: The Y coordinate of the current position.
            :param PositionX: The X coordinate of the current position.
            :param i: The change in X direction (vector).
            :param j: The change in Y direction (vector).
            :return: The number of marks of the current player on the liners of the player's position.
    """
        return 1 + self.OneDirection(PositionY + i, PositionX + j, i, j) \
            if (0 <= PositionX + j < self.__n
                and 0 <= PositionY + i < self.__n
                and self.__Board[PositionY + i][PositionX + j] == (-self.__PlayerToPlay)) \
            else 0

    def AllDirection(self, PositionY, PositionX):
        """
            Check if there is a winning sequence in any direction.

            :param PositionY: The Y coordinate of the current position.
            :param PositionX: The X coordinate of the current position.
            :return: True if there's a winning sequence in any direction, False otherwise.
        """
        column, line, Slash, = 0, 0, 0
        for index, (i, j) in enumerate([(0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, -1)]):

            if index < 2:
                column += self.OneDirection(PositionY, PositionX, i, j)
            elif 2 <= index < 4:
                line += self.OneDirection(PositionY, PositionX, i, j)
            else:
                Slash += self.OneDirection(PositionY, PositionX, i, j)

        return True if column + 1 >= 5 or line + 1 >= 5 or Slash + 1 >= 5 else False

    def Move(self, DPositionX, DPositionY, EPositionX, EPositionY):
        if 0 <= DPositionX < 11 and 0 <= DPositionY < 11 and 0 <= EPositionX < 11 and 0 <= EPositionY < 11:
            if self.__Board[EPositionX][EPositionY] == 1:
                if isinstance(self.__Board[DPositionX][DPositionY], Pawn):
                    Hub = self.__Board[DPositionX][DPositionY]
                    self.__Board[DPositionX][DPositionY] = -self.__PlayerToPlay
                    self.__Board[EPositionX][EPositionY] = Hub
        else:
            print("impossible to move !")

    def PlayGame(self):
        while self.__PawnNumberOnBoard < 10:
            PositionI = int(input("Choose your position X : "))
            PositionJ = int(input("Choose your position Y : "))
            self.Put(PositionI, PositionJ)
            print(self.get_Board())
            self.__PawnNumberOnBoard += 1
            self.__PlayerToPlay = (self.__PlayerToPlay % 2) + 1


if __name__ == '__main__':
    logic_obj = Logic('Luc', 'Jean-Marc')
    logic_obj.CreateBoard()
    logic_obj.PlayGame()
