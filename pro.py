def board():
    board_2d = []
    for (a, b, c) in [(6, 4, 1), (4, 7, 0), (3, 8, 0), (2, 9, 0), (1, 10, 0), (1, 9, 1), (0, 10, 1), (0, 9, 2),
                      (0, 8, 3), (0, 7, 4), (1, 4, 6)]:
        boardAnex = [9 for _ in range(a)] + [1 for _ in range(b)] + [9 for _ in range(c)]
        board_2d.append(boardAnex)
    return board_2d


def Display(board_2D, n):
    for row in range(n):
        for col in range(n):
            if board_2D[row][col] == 9:
                print(".", end=" ")
            elif board_2D[row][col] == 1:
                print("0", end=" ")
        print("")


Display(board(), 11)
