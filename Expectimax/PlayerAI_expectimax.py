from BaseAI_3 import BaseAI


class PlayerAI_expectimax(BaseAI):
    def __init__(self):
        self.possibleNewTiles = [2, 4]
        self.probability = 0.9

    def getMove(self, grid):
        self.depth_max = 3
        depth = 0
        child = self.maximize(grid, -10 ** 9, 10 ** 9, depth)[0]
        return child

    def maximize(self, grid, alpha, beta, depth):
        available_moves = grid.getAvailableMoves()
        if depth >= self.depth_max or available_moves == []:
            return None, self.heuristic(grid)

        (max_child, max_utility) = (None, -10 ** 9)

        for childIndex in available_moves:
            gridCopy = grid.clone()
            gridCopy.move(childIndex)
            utility = self.minimize(gridCopy, alpha, beta, depth + 1)[1]
            if utility > max_utility:
                (max_child, max_utility) = (childIndex, utility)
            if max_utility >= beta:
                break
            if max_utility > alpha:
                alpha = max_utility

        return (max_child, max_utility)

    def minimize(self, grid, alpha, beta, depth):
        available_moves = grid.getAvailableCells()
        if depth >= self.depth_max or available_moves == []:
            return (None, self.heuristic(grid))

        cells = grid.getAvailableCells()
        (minChild1, minUtility1) = (None, 10 ** 9)
        (minChild2, minUtility2) = (None, 10 ** 9)

        for set_value in self.possibleNewTiles:
            # When computer next move is add tile 2
            if set_value == 2:
                for child_cell in cells:
                    gridCopy1 = grid.clone()
                    gridCopy1.setCellValue(child_cell, 2)
                    (next_move, utility) = self.maximize(gridCopy1, alpha, beta, depth + 1)
                    if utility < minUtility1:
                        (minChild1, minUtility1) = (child_cell, utility)
                    if minUtility1 <= alpha:
                        break
                    if minUtility1 < beta:
                        beta = minUtility1
            # When computer next move is add tile 4
            if set_value == 4:
                for child_cell in cells:
                    gridCopy2 = grid.clone()
                    gridCopy2.setCellValue(child_cell, 4)
                    (next_move, utility) = self.maximize(gridCopy2, alpha, beta, depth + 1)
                    if utility < minUtility2:
                        (minChild2, minUtility2) = (child_cell, utility)
                    if minUtility2 <= alpha:
                        break
                    if minUtility2 < beta:
                        beta = minUtility2

        minUtility = self.probability * minUtility1 + (1 - self.probability) * minUtility2
        return next_move, minUtility

    def heuristic(self, grid):
        (w1, w2, w3, w4, w5, w6, w7) = (18, 20,  18, 0, 18, 23, 18)
        ##heuristic number one : available number of tiles
        ##larger the evalution, better the grid
        free_tiles = self.free_tiles(grid)
        monoton = self.monotonicity(grid)
        ident = self.identicity(grid)
        corner = self.corner(grid)
        penal = self.penalty(grid)
        large_corner = self.large_corner(grid)
        free_tiles_penalty = self.free_tiles_penalty(grid)
        return w1 * free_tiles + w2 * monoton + w3 * ident + w4 * corner + w5 * penal + w6 * large_corner + w7 * free_tiles_penalty

    def free_tiles(self, grid):
        free_tiles_count = len(grid.getAvailableCells())
        value = free_tiles_count * grid.getMaxTile()
        return value

    def monotonicity(self, grid):
        value = 0
        for i in range(grid.size - 1):
            for j in range(grid.size):
                if grid.map[i][j] == grid.map[i + 1][j] / 2:
                    value += grid.map[i + 1][j]

        for i in range(grid.size):
            for j in range(grid.size - 1):
                if grid.map[i][j] == grid.map[i][j + 1] / 2:
                    value += grid.map[i][j + 1]
        return value

    # Adjacent tiles have the same value
    def identicity(self, grid):
        value = 0
        for i in range(grid.size - 1):
            for j in range(grid.size):
                if grid.map[i][j] == grid.map[i + 1][j]:
                    value += grid.map[i][j]

        for i in range(grid.size):
            for j in range(grid.size - 1):
                if grid.map[i][j] == grid.map[i][j + 1]:
                    value += grid.map[i][j]
        return value

    def corner(self, grid):
        value = 0
        for x in range(grid.size):
            for y in range(grid.size):
                if (grid.map[x][y] != 0):
                    value += grid.map[x][y] * (x * x * y * y)
        return value

    def penalty(self, grid):
        value = 0
        for x in range(grid.size - 1):
            for y in range(grid.size):
                if grid.map[x][y] not in (grid.map[x + 1][y] / 2, grid.map[x + 1][y]) and grid.map[x][y] != 0:
                    if grid.map[x][y] < grid.map[x + 1][y]:
                        value -= grid.map[x + 1][y] - grid.map[x][y]
                    else:
                        value -= 2 * (grid.map[x][y] - grid.map[x + 1][y] / 2)

        for x in range(grid.size):
            for y in range(grid.size - 1):
                if grid.map[x][y] not in (grid.map[x][y + 1] / 2, grid.map[x][y + 1]) and grid.map[x][y] != 0:
                    if grid.map[x][y] < grid.map[x][y + 1]:
                        value -= grid.map[x][y + 1] - grid.map[x][y]
                    else:
                        value -= 2 * (grid.map[x][y] - grid.map[x][y + 1] / 2)
        return value

    # Larger the value in the right botton corner, better the heuristic
    def large_corner(self, grid):
        value = 0
        loacation_weight = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7]]
        for i in range(grid.size):
            for j in range(grid.size):
                value += grid.getCellValue((i, j)) * loacation_weight[i][j]
        return value

    def free_tiles_penalty(self, grid):
        value = 0
        for i in range(1, grid.size - 1):
            for j in range(1, grid.size - 1):
                if grid.getCellValue((i, j)) == 0:
                    count = 0
                    if grid.getCellValue((i + 1, j)) != 0:
                        count += 1
                    if grid.getCellValue((i - 1, j)) != 0:
                        count += 1
                    if grid.getCellValue((i, j + 1)) != 0:
                        count += 1
                    if grid.getCellValue((i, j - 1)) != 0:
                        count += 1
                    if (count > 2):
                        value = 0 - grid.getCellValue((i + 1, j)) - grid.getCellValue((i - 1, j)) - grid.getCellValue(
                            (i, j + 1)) - grid.getCellValue((i, j - 1))
        return value