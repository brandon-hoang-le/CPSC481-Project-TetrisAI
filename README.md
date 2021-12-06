# CPSC481 Tetris AI
Implemented Tetris AI approach based on Yiyuan Lee's [Tetris AI](https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/).

**Base Code:** ibrahimAtespare's [Tetris Python Game](https://github.com/ibrahimAtespare/tetris-python)

## How it works:
Rating system using 5 heuristics: AggregateHeight, CompleteLines, Holes, Bumpiness, MaxHeight
- highest score is chosen as best possible move
- score = **a**(AggregateHeight)+**b**(CompleteLines)+**c**(Holes)+**d**(Bumpiness)+**e**(MaxHeight)
  - Optimal parameters given from Genetic Algorithm
  - Added e parameter and MaxHeight to prevent blocks from stacking too high

## How it can be improved:
Ideas:
- Simulate the next block ahead of time
- Improve heuristics

## Project Members
Brandon Le, Darryn Wong and Dimitra Doiphode
