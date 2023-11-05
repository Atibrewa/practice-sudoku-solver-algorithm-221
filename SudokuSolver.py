import SudokuBoard, time

N = 9

def solveSudoku(initBoard, workBoard, row, col):
    if (row == N):
        return workBoard
    else:
        if initBoard.get(row, col) == 0: # not pre-filled
            possValues = workBoard.computePossibles(row, col)
            row2, col2 = nextPosition(row, col, N)
            for pv in possValues:
                workBoard.set(row, col, pv)
                soln = solveSudoku(initBoard, workBoard, row2, col2)
                if soln is not None:
                    return soln
                workBoard.unset(row, col) # remove current assignment
            return None # if it gets here, there's no solution :(
        else:
            row2, col2 = nextPosition(row, col, N)
            return solveSudoku(initBoard, workBoard, row2, col2)

def nextPosition(row, col, N):
    """
    Returns the next position in the grid,
    Returns first position in the next row if it has reached end of the current row
    """
    if col == N - 1:
        return (row + 1, 0)
    else:
        return (row, col + 1)

f = str(input("Enter the filename in th folder SudokuPuzzles! "))
if f.startswith("sudoku") and f.endswith(".txt"):
    filename = "SudokuPuzzles/" + f
    initBoard = SudokuBoard.Board(file = filename)
    print(initBoard)
    start = time.time()
    workBoard = initBoard.copy()
    ans = solveSudoku(initBoard, workBoard, 0, 0)
    end = time.time()
    print("SOLUTION:")
    print(ans)
    print ("Time taken: ", end-start)
else:
    print ("ERROR File not found!")