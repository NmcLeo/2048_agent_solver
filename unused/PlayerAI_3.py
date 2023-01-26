from random import randint
from BaseAI_3 import BaseAI
import time

# Time Limit Before Losing
timeLimit = 0.15

class PlayerAI(BaseAI):
	def __init__(self):
		self.possibleNewTiles = [2, 4]
		self.probability = 0.9

	def getMove(self, grid):
		self.prevTime = time.perf_counter()
		self.depth_max=0
		self.over = False
		moves = grid.getAvailableMoves()
		
		while self.over == False:
			self.updateAlarm(time.perf_counter())
			self.depth_max += 1
			player_move = self.maximize(grid, -10**9, 10**9, 1)[0]
			if player_move != None:
				final_move = player_move

		return final_move if moves else None

	def updateAlarm(self, currTime):
		if currTime - self.prevTime > timeLimit:
			self.over = True

	def maximize(self, grid, alpha, beta, depth):
		if grid.getAvailableMoves() == []:
			return (None, self.evaluate(grid))

		# Iniatilizing final move and utility
		(max_move, max_utility) = (None, -10 ** 9)

		for child_move in grid.getAvailableMoves():

			gridCopy = grid.clone()
			gridCopy.move(child_move)
			utility = self.minimize(gridCopy, alpha, beta, depth)[1]
			self.updateAlarm(time.perf_counter())
			if self.over or utility == None:
				return (None, None)
			if utility > max_utility:
				(max_move, max_utility) = (child_move, utility)
			if max_utility >= beta:
				break
			if max_utility > alpha:
				alpha = max_utility

		return (max_move, max_utility)

	def minimize(self, grid, alpha, beta, depth):
		if grid.getAvailableCells()==[] :
			return (None, self.evaluate(grid))

		if depth == self.depth_max:
			return (None, self.evaluate(grid))

		#Iniatilizing final move and utility
		(min_cell,min_utility) = (None, 10**9)	

		for child_cell in grid.getAvailableCells():
			gridCopy = grid.clone()
			gridCopy.setCellValue(child_cell, 2)
			utility = self.maximize(gridCopy, alpha, beta, depth+1)[1]
			self.updateAlarm(time.perf_counter())
			if self.over or utility == None:
				return (None, None)
			if utility < min_utility:
				(min_cell, min_utility) = (child_cell, utility)
			if min_utility <= alpha:
				break
			if min_utility < beta:
				beta = min_utility
		return (min_cell, min_utility)
	


	def evaluate(self, grid):
		(w1, w2, w3, w4, w5) = (1, 1, 1, 1, 2)
		##heuristic number one : available number of tiles
		##larger the evalution, better the grid
		avail = grid.getAvailableCells()
		monoton = self.monotonicity(grid)
		ident = self.identicity(grid)
		corner = self.corner(grid)
		penal = self.penalty(grid)
		return w1*len(avail)*grid.getMaxTile() + w2*monoton + w3*ident + w4*corner + w5*penal


	def monotonicity(self, grid):
		value= 0
		for i in range(grid.size-1):
			for j in range (grid.size):
				if grid.map[i][j]==grid.map[i+1][j]/2:
					value +=grid.map[i+1][j]

		for i in range(grid.size):
			for j in range (grid.size-1):
				if grid.map[i][j]==grid.map[i][j+1]/2:
					value +=grid.map[i][j+1]
		return value

	def identicity(self, grid):
		value= 0
		for i in range(grid.size-1):
			for j in range (grid.size):
				if grid.map[i][j]==grid.map[i+1][j]:
					value +=grid.map[i][j]

		for i in range(grid.size):
			for j in range (grid.size-1):
				if grid.map[i][j]==grid.map[i][j+1]:
					value +=grid.map[i][j]
		return value

	def corner(self, grid):
		value=0
		for x in range(grid.size):
			for y in range(grid.size):
				if (grid.map[x][y] != 0):
					value+=grid.map[x][y]*(x*x*y*y)
		return value

	def penalty(self, grid):
		value=0
		for x in range(grid.size-1):
			for y in range(grid.size):
				if grid.map[x][y] not in (grid.map[x+1][y]/2, grid.map[x+1][y]) and grid.map[x][y] != 0:
					if grid.map[x][y] < grid.map[x+1][y]:
						value -= grid.map[x+1][y]-grid.map[x][y]
					else:
						value -= 2*(grid.map[x][y]-grid.map[x+1][y]/2)

		for x in range(grid.size):
			for y in range(grid.size-1):
				if grid.map[x][y] not in (grid.map[x][y+1]/2, grid.map[x][y+1]) and grid.map[x][y] != 0:
					if grid.map[x][y] < grid.map[x][y+1]:
						value -= grid.map[x][y+1]-grid.map[x][y]
					else:
						value -= 2*(grid.map[x][y]-grid.map[x][y+1]/2)
		return value


