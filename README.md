# 2048_agent_solver

This project provides an agent which intelligently play 2048-puzzle Game.

## Game Rules
The game rules can be found here: http://mypuzzle.org/sliding

An instance of the 2048-puzzle game is played on a 4×4 grid, with numbered tiles that slide in all four directions when a player moves them. Every turn, a new tile will randomly appear in an empty spot on the board, with a value of either 2 or 4. Per the input direction given by the player, all tiles on the grid slide as far as possible in that direction, until they either (1) collide with another tile, or (2) collide with the edge of the grid. If two tiles of the same number collide while moving, they will merge into a single tile, valued at the sum of the two original tiles that collided. The resulting tile cannot merge with another tile again in the same move.


<img src="https://studio.edx.org/asset-v1:ColumbiaX+CSMM.101x+1T2017+type@asset+block@p2_1.png" width="200">

Here the computer is responsible for placing random tiles of 2 or 4 on the board, while the player is responsible for moving the pieces. However, adversarial search can be applied to this game just the same.


## Prerequisites

- Python 3.X
- No external library needed
- Linux (Should work on Windows too but need to be confirmed)

Note: The use of numpy could simplify and accelerate the steps of the algorithm. But we wanted to create a simple algorithm here without any extra library.

## Running the tests

Run the test by launching the following code :

> $ python3 GameManager

## Algorithms used 

In the 2048-puzzle game, the setup is inherently asymmetric; that is, the computer and player take drastically different actions in their turns. 
Specifically, the computer is responsible for placing random tiles of 2 or 4 on the board, while the player is responsible for moving the pieces. 
However, adversarial search can be applied to this game.

We use the minimax algorithm (https://en.wikipedia.org/wiki/Minimax) with alpha-beta-pruning (https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning).

In this game it is highly impracticable to search the entire depth of the theoretical game tree. So we will use heuristic functions to assign approximate values to nodes in the tree at at given state.

In our case, I used the 5 following heuristics (In file PlayerAI.py):
- Number of empty spaces available: it incites the algorithm to keep as many empty spaces as possible, and thus incites it to fuse tiles when possible.
- Monotonicity : it incites two adjacent tiles to have following values in the space of values possibilites (2,4,8 ..., 2048,..). 
- Identicity : it calculates the number of identical adjacents tiles. It incites to have a number as high as possible to be able to fuse the tiles later.
- Corner : it incites the highest tile to be in a corner
- Penalty : it adds an increasing penalty the farther the values of two adjacents tiles are in the space of values possibilites (2,4,8 ..., 2048,..). Example : 2 and 4 are adjacent and so will have no penalty, while 2 and 2048 are considered to be far and then will have an important penalty

I used heuristic weights to link the different heuristic. Therefore, these weights are not optimized. One way to improve the algorithm would be to do a grid search with various weights and testing the algorithm on an important numbers of times.



## Author
Christian Tchou


