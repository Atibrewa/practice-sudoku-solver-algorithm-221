"""
File: SudokuBoard.py
Author: Susan Fox

Contains a Board class to represent a Sudoku puzzle. We can read in a puzzle from a file (represented as 9 lines with
9 digits per line) or we can input a list of lists representation of a Sudoku puzzle.
Methods:
    copy() makes a complete copy of the Board
    get(row, col) returns the value at position (row, col) in the board (a number between 0 (blank) and 9)
    set(row, col, val) changes the board at position (row, col) to be val
    unset(row, col) changes the board at position (row, col) to be zero
    getSubgridIndices(row, col) returns the smallest and largest indices of the cells in the same subgrid as (row, col)
    checkBoard() checks if the board is consistent
    computePossibles(row, col) returns a list of values for (row, col) consistent with others on the board

In addition, you can print the board using print (see example in script below), and you can compare two
board objects with == and it will return True if their contents are identical.
"""


import os


class Board(object):
    """A Sudoku board, which may or may not be complete. 0 represents a blank cell in the board, and otherwise
    the cell values are 1 through 9."""

    def __init__(self, brd=None, file=None):
        """ Takes in either a board as a list of lists, or a filename, and it builds the Sudoku board accordingly.
        Also sets up an instance variable to hold the indices for each subgrid: (r1, c1, r2, c2) where (r1, c1) is the
        upperleft cell in the subgrid, and r2 is one past the last row in the subgrid, and c2 is one past the last
        column in the subgrid."""
        self.subgrids = [[0, 0, 3, 3], [0, 3, 3, 6], [0, 6, 3, 9],
                         [3, 0, 6, 3], [3, 3, 6, 6], [3, 6, 6, 9],
                         [6, 0, 9, 3], [6, 3, 9, 6], [6, 6, 9, 9]]
        if brd is not None and file is not None:
            print("Both board and filename given, ignoring filename")
        if brd is not None:
            self.board = brd
        elif file is not None:
            self.board = self._readBoardFile(file)
        else:
            print("No board constructed, neither board nor file given as input")

    def _readBoardFile(self, filename):
        """A helper method to read in a Sudoku puzzle from a file. Assumes the file has 9 lines, each containing
        9 integer digits. DOES NOT DO ADEQUATE ERROR-CHECKING!"""
        fil = open(filename, 'r')
        board = []
        for line in fil:
            parts = [int(x) for x in line.split()]
            board.append(parts)
        return board

    def copy(self):
        """Makes a new board that is an exact copy of this one (internal board list is copied)."""
        newB = []
        for row in self.board:
            newRow = row[:]
            newB.append(newRow)
        return Board(brd=newB)

    def get(self, row, col):
        """Given (row, col), returns the value at that point. Does check if they are valid positions, and returns
        None if they are not."""
        if (0 <= row < 9) and (0 <= col < 9):
            return self.board[row][col]

    def set(self, row, col, val):
        """Given (row, col) and val, sets the value to val at that point. Does check for in-bounds values
         and returns None when bad input given."""
        if (0 <= row < 9) and (0 <= col < 9) and (0 <= val <= 9):
            self.board[row][col] = val

    def unset(self, row, col):
        """Given (row, col), sets the value at that position to zero. Does check if they are valid positions, and
        returns None if they are not."""
        if (0 <= row < 9) and (0 <= col < 9):
            self.board[row][col] = 0

    def getSubgridIndices(self, row, col):
        """Given (row, col) it determines which subgrid that belongs to, and returns the four-tuple of index values:
        (r1, c1) is upper left cell in subgrid, and (r2, c2) is one past the lower right cell's indices."""
        for (r1, c1, r2, c2) in self.subgrids:
            if (r1 <= row < r2) and (c1 <= col < c2):
                return (r1, c1, r2, c2)
        print("ERROR: should never get here")

    def __str__(self):
        """Allows us to use the print function on a Board. Prints a text version of the board, with _ for blanks
        and the numbers otherwise."""
        descrStr = "+---------+---------+---------+\n"
        rInd = 0
        for row in self.board:
            cInd = 0
            rowStr = "|"
            for v in row:
                if v == 0:
                    rowStr += " _ "
                else:
                    rowStr += ' ' + str(v) + ' '
                cInd += 1
                if cInd in [3, 6]:
                    rowStr += "|"
            rowStr += "|\n"
            descrStr += rowStr
            rInd += 1
            if rInd in [3, 6]:
                descrStr += "+---------+---------+---------+\n"
        descrStr += "+---------+---------+---------+"
        return descrStr

    def __eq__(self, otherBoard):
        """Compares this board to the input board, returning True if every cell has the same value."""
        for r in range(9):
            for c in range(9):
                if self.board[r][c] != otherBoard.board[r][c]:
                    return False
        return True

    def checkBoard(self):
        """Check each row of the board, and see if it has any duplicate values. Then do the same for each
        column of the board, and finally for each subgrid of the board."""
        for row in self.board:
            setOfVals = set()
            for v in row:
                if v != 0:
                    if v in setOfVals:
                        print("Found a problem in row", row, ":", v, setOfVals)
                        return False
                    setOfVals.add(v)
        for c in range(9):
            setOfVals = set()
            for r in range(9):
                v = self.board[r][c]
                if v != 0:
                    if v in setOfVals:
                        print("Found a problem in column", c, ":", v, setOfVals)
                        return False
                    setOfVals.add(v)
        for (r1, c1, r2, c2) in self.subgrids:
            setOfVals = set()
            for row in range(r1, r2):
                for col in range(c1, c2):
                    # print("  ", row, col)
                    v = self.board[row][col]
                    if v != 0:
                        if v in setOfVals:
                            print("Found a problem in subgrid", (r1, c1, r2, c2), ":",
                                  (row, col), self.board[row][col], setOfVals)
                            return False
                        setOfVals.add(v)
        return True

    def computePossibles(self, row, col):
        """Given (row, col) this determines which of the 9 digits can be placed in this cell of the grid. Checks the
        contents of this cell's row, column, and subgrid, and keeps only the values not found in any of those.
        Returns a set of the values."""
        possibles = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for c in range(9):
            currVal = self.board[row][c]
            if currVal != 0:
                # print("in row:", currVal)
                possibles.discard(currVal)
        for r in range(9):
            currVal = self.board[r][col]
            if currVal != 0:
                # print("in col:", currVal)
                possibles.discard(currVal)
        (r1, c1, r2, c2) = self.getSubgridIndices(row, col)
        # print("Subgrid:", (row, col), (r1, c1, r2, c2))
        for r in range(r1, r2):
            for c in range(c1, c2):
                currVal = self.board[r][c]
                if currVal != 0:
                    # print("in subgrid:", currVal)
                    possibles.discard(currVal)
        return possibles


if __name__ == "__main__":
    filenames = os.listdir("SudokuPuzzles")
    filenames.sort()
    for f in filenames:
        if f.startswith("sudoku") and f.endswith(".txt"):
            print("Board = ", f)
            b = Board(file="SudokuPuzzles/"+f)
            print(b)
            print(b.checkBoard())

    # This code actually shows how you might write the code to solve the Sudoku puzzle
    # b = Board(file="sudoku9.txt")
    # print(b)
    # ans = solveSudoku(b)
    # print("SOLUTION:")
    # print(ans)
