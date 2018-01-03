def searchWord(grid, mask, word, row, column):
    """
    helper function to search for string in the grid

    :param grid: 2D grid with `__getitem__` method on each dimension
    :param mask: 2D mask as large as the grid, where `Trus` means a cell can be used
    :param word: the (sub)string to search for
    :param row: vertical position to begin the string
    :param column: horizontal position to begin the string
    :return: `True` if the string can be found in the grid beginning at position (row, column)
    """

    from copy import deepcopy

    # an empty string is always in the grid
    if word == "":
        return True

    # a string cannot begin outside of the grid
    if not (0 <= row < len(grid) and 0 <= column < len(grid[0])):
        return False

    # if the string does begin at the given position
    # and if the cell is not used
    if mask[row][column] and grid[row][column] == word[0]:
        # use the cell
        mask[row][column] = False

        # search suffix of length `len(word) - 1`
        # using each of the four neighbours as beginning
        word = word[1:]
        if searchWord(grid, deepcopy(mask), word, row + 1, column) or \
           searchWord(grid, deepcopy(mask), word, row - 1, column) or \
           searchWord(grid, deepcopy(mask), word, row, column + 1) or \
           searchWord(grid, deepcopy(mask), word, row, column - 1):
            return True

    # if the string cannot begin at the given position,
    # or if its suffix cannot begin on any of the four neighbours
    # of the given position
    return False


def wordIsInGrid(grid, word):
    """
    search a string in the grid. The string can be constructed from letters of sequentially
    adjencent cell, where "adjancent" cells are those horizontally or vertically neighbouring.

    :param grid: 2D grid with `__getitem__` method on each dimension
    :param word: the (sub)string to search for
    :return: `True` if the string can be found in the grid
    """

    # availability of each cell
    mask = [[True for c in range(len(grid[r]))] for r in range(len(grid))]

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if searchWord(grid, mask, word, r, c):
                return True

    return False


if __name__ == "__main__":
    grid = (('A', 'B', 'C', 'E'),
            ('S', 'F', 'C', 'S'),
            ('A', 'D', 'E', 'E'))

    # given test cases
    testCases = ("ABCCED", "SEE", "ABCB")
    # additional test cases
    testCases += ("ABCCFB",)  # requires a cell to be used more than once)
    testCases += ("ABCESEEDASFC",)  # made of all cells in the grid
    testCases += ("ABCESEEDASFCA",)  # too long to fit in the entire grid

    for case in testCases:
        print("\"" + case + "\"" + " is in the grid." if wordIsInGrid(grid, case)
              else "\"" + case + "\"" + " is not in the grid.")
