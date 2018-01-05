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


def wordIsInGrid_rec(grid, word):
    """
    search a string in the grid. The string can be constructed from letters of sequentially
    adjencent cell, where "adjancent" cells are those horizontally or vertically neighbouring.

    recursive version.

    :param grid: 2D grid with `__getitem__` method on each dimension
    :param word: the (sub)string to search for
    :return: `True` if the string can be found in the grid
    """

    # availability of each cell
    mask = [[True for c in range(len(grid[r]))] for r in range(len(grid))]

    # try to begin the word at each cell
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if searchWord(grid, mask, word, r, c):
                return True

    return False



def wordIsInGrid_iter(grid, word):
    """
    search a string in the grid. The string can be constructed from letters of sequentially
    adjencent cell, where "adjancent" cells are those horizontally or vertically neighbouring.

    iterative version.

    :param grid: 2D grid with `__getitem__` method on each dimension
    :param word: the (sub)string to search for
    :return: `True` if the string can be found in the grid
    """

    # try to begin the word at each cell
    for r in range(len(grid)):
        for c in range(len(grid[r])):

            # Initialization

            # availability of each cell
            mask = [[True for c in range(len(grid[r]))] for r in range(len(grid))]

            # stack of directions we have traveled
            # used to simulate backtracking
            # 0: up, 1: right, 2: down, 3: left
            # also remember our last position
            # list(tuple(int, tuple(int, int)))
            #            dir        x    y
            dirs = []

            # partition the word to two halves: matched and unmatched
            matched = []
            unmatched = list(word[::-1])
            nextChar = ''



            # begin to search for where possibly the string can begin at

            row = r
            column = c
            nextChar = unmatched.pop()

            # print("\tBegin over")
            # print("\t\tSearching for: " + nextChar + " @(" + str(row) + ", " + str(column) + ")")

            if grid[row][column] == nextChar:
                mask[row][column] = False
                matched.append(nextChar)
                nextChar = unmatched.pop()
                dirs.append([0, (row, column)])

                # once we found possible position of first charactor
                # keep matching the rest
                while True:

                    dir = dirs[-1][0]

                    # if tried all directions and no match
                    # backtrack
                    if dir == 4:
                        dirs.pop()
                        unmatched.append(matched.pop())
                        # if we tried all possible directions
                        # but no match
                        if len(dirs) == 0:
                            # print("\t\t\tNot Found")
                            break
                        else:
                            dirs[-1][0] += 1
                            continue

                    # decide which cell to match next
                    # based on last position and direction to go from that pos
                    row, column = dirs[-1][1]
                    if dir == 0:
                        row -= 1
                    elif dir == 1:
                        column += 1
                    elif dir == 2:
                        row += 1
                    elif dir == 3:
                        column -= 1

                    # print("\t\tSearching for: " + nextChar + " @(" + str(row) + ", " + str(column) + ") in dir " + str(
                    #     dirs[-1][0]))

                    # if we are outside of the grid
                    # backtrack
                    if not (0 <= row < len(grid) and 0 <= column < len(grid[0])):
                        # print("\t\t\tOutside")
                        dirs[-1][0] += 1
                        continue

                    # if next character matches cell
                    if mask[row][column]:
                        # and if the cell is available
                        if grid[row][column] == nextChar:
                            # use the cell
                            mask[row][column] = False
                        # the cell is unavailable
                        else:
                            dirs[-1][0] += 1
                            # print("\t\t\tNot match")
                            continue
                    # if does not match
                    # backtrack
                    else:
                        dirs[-1][0] += 1
                        # print("\t\t\tUsed")
                        continue

                    # at this point, we matched one more character

                    matched.append(nextChar)

                    # if no more left, done
                    if len(unmatched) == 0:
                        # print("\t\t\tFound")
                        return True
                    else:
                        # otherwise continue with next
                        dirs.append([0, (row, column)])
                        nextChar = unmatched.pop()
                        continue

    # if we are still not able to find a match
    # there is no match
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
        print("Is " + "\"" + case + "\"" + " in the grid?")
        for methodName, method in (('Recursion', wordIsInGrid_rec), ('Iteration', wordIsInGrid_iter)):
            print("\t" + methodName + ": " + str(method(grid, case)))
