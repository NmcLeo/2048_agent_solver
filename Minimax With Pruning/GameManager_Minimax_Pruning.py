from Grid_3 import Grid
from ComputerAI_3 import ComputerAI
from PlayerAI_minimax_pruning import PlayerAI_minimax_pruning
from Displayer_3 import Displayer
from random import randint
import time
import sys

defaultInitialTiles = 2
defaultProbability = 0.9

actionDic = {
    0: "UP",
    1: "DOWN",
    2: "LEFT",
    3: "RIGHT"
}

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

# Time Limit Before Losing
timeLimit = 0.2
allowance = 0.05

arg_list = sys.argv


class GameManager:
    def __init__(self, size=4):
        self.grid = Grid(size)
        self.possibleNewTiles = [2, 4]
        self.probability = defaultProbability
        self.initTiles = defaultInitialTiles
        self.numOfMoves = 0
        self.computerAI = None
        self.playerAI = None
        self.displayer = None
        self.over = False
        self.maxAllowedTile = 0
        if (len(arg_list) > 1):
            self.maxAllowedTile = int(arg_list[1])

    def setComputerAI(self, computerAI):
        self.computerAI = computerAI

    def setPlayerAI(self, playerAI):
        self.playerAI = playerAI

    def setDisplayer(self, displayer):
        self.displayer = displayer

    def start(self):
        for i in range(self.initTiles):
            self.insertRandonTile()

        self.displayer.display(self.grid)

        # Player AI Goes First
        turn = PLAYER_TURN
        maxTile = 0

        while not self.isGameOver() and (
                self.maxAllowedTile == 0 or (self.maxAllowedTile > 0 and maxTile < self.maxAllowedTile)):
            # Copy to Ensure AI Cannot Change the Real Grid to Cheat
            gridCopy = self.grid.clone()

            move = None

            if turn == PLAYER_TURN:
                print("Player's Turn:", end="")
                move = self.playerAI.getMove(gridCopy)
                print(actionDic[move])

                # Validate Move
                if move != None and move >= 0 and move < 4:
                    if self.grid.canMove([move]):
                        self.grid.move(move)

                        # Update maxTile
                        maxTile = self.grid.getMaxTile()
                    else:
                        print("Invalid PlayerAI Move")
                        self.over = True
                else:
                    print("Invalid PlayerAI Move - 1")
                    self.over = True
            else:
                print("Computer's turn:")
                move = self.computerAI.getMove(gridCopy)

                # Validate Move
                if move and self.grid.canInsert(move):
                    self.grid.setCellValue(move, self.getNewTileValue())
                else:
                    print("Invalid Computer AI Move")
                    self.over = True

            if not self.over:
                self.displayer.display(self.grid)
            turn = 1 - turn
            self.numOfMoves += 1
        f = open("Stats/output_minimax_pruning.txt", "a")
        f.write("\n\nMax tile reached:" + str(maxTile) + "\nNumber of moves: " + str(self.numOfMoves))
        f.close()

    def isGameOver(self):
        return not self.grid.canMove()

    def getNewTileValue(self):
        if randint(0, 99) < 100 * self.probability:
            return self.possibleNewTiles[0]
        else:
            return self.possibleNewTiles[1]

    def insertRandonTile(self):
        tileValue = self.getNewTileValue()
        cells = self.grid.getAvailableCells()
        cell = cells[randint(0, len(cells) - 1)]
        self.grid.setCellValue(cell, tileValue)


def PlayGame():
    gameManager = GameManager()
    playerAI = PlayerAI_minimax_pruning()
    computerAI = ComputerAI()
    displayer = Displayer()
    gameManager.setDisplayer(displayer)
    gameManager.setPlayerAI(playerAI)
    gameManager.setComputerAI(computerAI)

    start_time = time.perf_counter()
    gameManager.start()
    end_time = time.perf_counter()

    f = open("Stats/output_minimax_pruning.txt", "a")
    f.write("\nTotal Time = " + str(end_time - start_time))
    f.close()


def main():
    num_time_to_play = 10
    for i in range(num_time_to_play):
        PlayGame()


if __name__ == '__main__':
    main()
