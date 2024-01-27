def isMoveValid(gameState, destination):
    # Check that the destination coordinate is on the board and within the range
    if not (0 <= destination[0] < numRows and 0 <= destination[1] < numCols):
        return False

    # Check that the destination coordinate is free
    if not freeCoord(gameState.board, destination):
        return False

    # Check that the ring can be moved to the destination in all directions
    for direction in directions:
        newRow = destination[0] + direction[0]
        newCol = destination[1] + direction[1]

        # Check if the ring can move to the new coordinate
        if ringMoves(gameState.board, gameState.activeRing, (newRow, newCol)):

            # Check that the ring is owned by the current player
            if gameState.turnMode != TurnMode.MoveRing:
                return False

            return True

    return False


def ringMoves(board, ringCoord):
    # Check that the ring coordinate is on the board
    # numCols & numRow while be remplace by self.__n
    if not (0 <= ringCoord[0] < numRows and 0 <= ringCoord[1] < numCols):
        return []

    # Check that the ring is not already on an edge
    if not (ringCoord[0] == 0 or ringCoord[1] == 0 or ringCoord[0] == numRows - 1 or ringCoord[1] == numCols - 1):
        # Get the coordinates of the neighboring rings in each direction
        neighbors = []
        for direction in directions:
            newRow = ringCoord[0] + direction[0]
            newCol = ringCoord[1] + direction[1]

            if newRow < 0 or newRow >= numRows or newCol < 0 or newCol >= numCols:
                continue

            if freeCoord(board, (newRow, newCol)):
                neighbors.append((newRow, newCol))

        # Add the neighbors as possible moves
        moves = neighbors
    else:
        # If the ring is on an edge, it can only move orthogonally
        moves = []
        for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            newRow = ringCoord[0] + direction[0]
            newCol = ringCoord[1] + direction[1]

            if newRow < 0 or newRow >= numRows or newCol < 0 or newCol >= numCols:
                continue

            if freeCoord(board, (newRow, newCol)):
                moves.append((newRow, newCol))

    return moves


def freeCoord(board, coord):
    row, col = coord
    return board[row, col] is None
