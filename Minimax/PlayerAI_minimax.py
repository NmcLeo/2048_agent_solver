from random import randint
from BaseAI_3 import BaseAI
import time

# Time Limit Before Losing
timeLimit = 0.15


class PlayerAI_minimax(BaseAI):
    def __init__(self):
        self.possibleNewTiles = [2, 4]
        self.probability = 0.9

    def getMove(self, grid):
        self.depth_max = 4
        moves = grid.getAvailableMoves()
        player_move = self.maximize(grid, 0)[0]
        return player_move if moves else None

    def maximize(self, grid, depth):
        available_moves = grid.getAvailableMoves()
        if depth >= self.depth_max or available_moves == []:
            return (None, self.heuristic(grid))

        # Iniatilizing final move and utility
        (max_move, max_utility) = (None, -10 ** 9)

        for child_move in available_moves:

            gridCopy = grid.clone()
            gridCopy.move(child_move)
            utility = self.minimize(gridCopy, depth+1)[1]

            if utility > max_utility:
                (max_move, max_utility) = (child_move, utility)

        return max_move, max_utility

    def minimize(self, grid, depth):
        available_moves = grid.getAvailableCells()
        if depth >= self.depth_max or available_moves == []:
            return (None, self.heuristic(grid))

        # Iniatilizing final move and utility
        (min_cell, min_utility) = (None, 10 ** 9)

        for child_cell in available_moves:
            gridCopy = grid.clone()
            gridCopy.setCellValue(child_cell, 2)
            utility = self.maximize(gridCopy, depth + 1)[1]
            if utility < min_utility:
                (min_cell, min_utility) = (child_cell, utility)

            gridCopy = grid.clone()
            gridCopy.setCellValue(child_cell, 4)
            utility = self.maximize(gridCopy, depth + 1)[1]
            if utility < min_utility:
                (min_cell, min_utility) = (child_cell, utility)

        return min_cell, min_utility

    def heuristic(self, grid):
        (w1, w2, w3, w4, w5) = (1, 1, 1, 1, 1)
        ##heuristic number one : available number of tiles
        ##larger the evalution, better the grid
        avail = grid.getAvailableCells()
        monoton = self.monotonicity(grid)
        ident = self.identicity(grid)
        corner = self.corner(grid)
        penal = self.penalty(grid)
        return w1 * len(avail) * grid.getMaxTile() + w2 * monoton + w3 * ident + w4 * corner + w5 * penal

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
