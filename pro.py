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

    def OneDirection(self, PositionY, PositionX, i, j):

        # Condition d'arrêt : la case est à l'intérieur du plateau et contient un pion adverse
        return 1 + self.OneDirection(PositionY + i, PositionX + j, i, j) \
            if (0 <= PositionX + j < self.__n
                and 0 <= PositionY + i < self.__n
                and self.__Board[PositionY + i][PositionX + j] == (-self.__PlayerToPlay)) \
            else 0

    # Méthode pour vérifier si un alignement de pions est présent dans toutes les directions depuis la position spécifiée
    def AllDirection(self, PositionY, PositionX):
        # Initialisation des compteurs pour chaque direction
        column, line, Slash, = 0, 0, 0

        # Parcours de toutes les directions
        for index, (i, j) in enumerate([(0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, -1)]):

            # Comptage du nombre de pions adverses dans chaque direction
            if index < 2:
                column += self.OneDirection(PositionY, PositionX, i, j)
            elif 2 <= index < 4:
                line += self.OneDirection(PositionY, PositionX, i, j)
            else:
                Slash += self.OneDirection(PositionY, PositionX, i, j)

        # Vérification s'il y a suffisamment de pions adverses dans au moins une direction
        return True if column + 1 >= 5 or line + 1 >= 5 or Slash + 1 >= 5 else False


    def isMoveValid(self, gameState, destination):
        # Check that the destination coordinate is on the board and within the range
        if not (0 <= destination[0] < self.__n and 0 <= destination[1] < self.__n):
            return False

        # Check that the destination coordinate is free
        if not self.freeCoord(gameState.board, destination):
            return False

        # Check that the ring can be moved to the destination in all directions
        for direction in directions:
            newRow = destination[0] + direction[0]
            newCol = destination[1] + direction[1]

            # Check if the ring can move to the new coordinate
            if self.ringMoves(gameState.board, gameState.activeRing, (newRow, newCol)):

                # Check that the ring is owned by the current player
                if gameState.turnMode != TurnMode.MoveRing:
                    return False

                return True

        return False

    def ringMoves(self, board, ringCoord, destinationCoord):
        # Check that the ring coordinate is on the board
        if not (0 <= ringCoord[0] < self.__n and 0 <= ringCoord[1] < self.__n):
            return []

        # Check that the ring is not already on an edge
        if not (ringCoord[0] == 0 or ringCoord[1] == 0 or ringCoord[0] == self.__n - 1 or ringCoord[1] == self.__n - 1):
            # Get the coordinates of the neighboring rings in each direction
            neighbors = []
            for direction in directions:
                newRow = ringCoord[0] + direction[0]
                newCol = ringCoord[1] + direction[1]

                if newRow < 0 or newRow >= self.__n or newCol < 0 or newCol >= self.__n:
                    continue

                if self.freeCoord(board, (newRow, newCol)):
                    neighbors.append((newRow, newCol))

            # Add the neighbors as possible moves
            moves = neighbors
        else:
            # If the ring is on an edge, it can only move orthogonally
            moves = []
            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                newRow = ringCoord[0] + direction[0]
                newCol = ringCoord[1] + direction[1]

                if newRow < 0 or newRow >= self.__n or newCol < 0 or newCol >= self.__n:
                    continue

                if self.freeCoord(board, (newRow, newCol)):
                    moves.append((newRow, newCol))

        return moves

    def freeCoord(board, coord):
        row, col = coord
        return board[row, col] is None

logic_obj = Logic('Luc')
# logic_obj.Display()
logic_obj.Put(0, 7)
logic_obj.Display()
