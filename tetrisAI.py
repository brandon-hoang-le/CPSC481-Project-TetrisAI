from math import e
import pygame
import copy
import time


def geneticAlgorithm(height, complete_lines, holes, bumpiness, max_height):
    return height * -0.510066 + complete_lines * \
        0.760666 + holes * -0.35663 + bumpiness * -0.184483 + max_height * -0.001


def run_ai(game_field, game_width, game_height):
    game_field.piece.createNextMove('down')
    game_field.piece.applyNextMove()
    if game_field.piece.status != 'moving':
        return []

    # simulate all possible outcomes
    best_pos, best_rotation = simulate(game_field, game_width, game_height)
    # apply drop
    for i in range(best_rotation):
        time.sleep(0.2)
        game_field.piece.rotate("CW")
    shift = game_field.piece.blocks[0].currentPos.col - best_pos[0]
    if shift > 0:
        for i in range(shift):
            game_field.piece.createNextMove('left')
            game_field.piece.applyNextMove()
    elif shift < 0:
        for i in range(-shift):
            game_field.piece.createNextMove('right')
            game_field.piece.applyNextMove()
    while not game_field.piece.movCollisionCheck("down"):
        game_field.piece.createNextMove('down')
        game_field.piece.applyNextMove()
    return[]


def simulate(game, game_width, game_height):
    game1 = copy.deepcopy(game)
    piece = game1.piece
    best_position = None
    best_rotation = None
    best_rating = None
    best_blockMat = None
    best_data = []
    cur_rotation = 0
    # simulate all 4 rotations
    for x in range(4):
        rotate_count = 0
        gameX = copy.deepcopy(game1)
        gameXp = gameX.piece
        while not gameXp.movCollisionCheck("left"):
            gameXp.createNextMove('left')
            gameXp.applyNextMove()
        # simulate all columns
        for ii in range(game_width):
            # place simulated blocks
            game2 = copy.deepcopy(gameX)
            piece = game2.piece
            blockMat = game2.blockMat
            while not piece.movCollisionCheck("down"):
                piece.createNextMove('down')
                piece.applyNextMove()
            for i in range(4):
                blockMat[piece.blocks[i].currentPos.row
                         ][piece.blocks[i].currentPos.col] = 'SIM'
            # if there are rows beling cleared, clear and drop free blocks
            cl = game2.getCompleteLines()
            cl.sort(reverse=True)
            line_cleared = 0
            for i in range(4):
                if cl[i] != -1:
                    line_cleared += 1
                else:
                    break
            if line_cleared > 0:
                for i in range(line_cleared):
                    blockMat.pop(cl[i])
                for i in range(line_cleared):
                    blockMat.insert(0, ['empty', 'empty', 'empty', 'empty',
                                        'empty', 'empty', 'empty', 'empty', 'empty', 'empty'])
            # calculate agregate height, buumpiness, highest height,and holes
            a_height, cleared, holes, bumpiness, highest = calc(
                blockMat, game_width, game_height)
            # calculate the rating of this simulation through genetic algorithm
            rating = geneticAlgorithm(
                a_height, line_cleared, holes, bumpiness, highest)
            # record the best simulation
            if best_rating is None or rating > best_rating:
                best_rating = rating
                cur_pos = [0] * 4
                for i in range(4):
                    cur_pos[i] = piece.blocks[i].currentPos.col
                best_position = cur_pos
                best_rotation = cur_rotation
                best_blockMat = blockMat
                best_data = [a_height, cleared, holes,
                             bumpiness, highest, best_rating]

            if not gameXp.movCollisionCheck("right"):
                gameXp.createNextMove('right')
                gameXp.applyNextMove()
            else:
                break
        game1.piece.rotate("CW")
        cur_rotation += 1
    print("aggregate height:", best_data[0], "line cleared:", best_data[1],
          "holes:", best_data[2], "bumpiness:", best_data[3], 'highest height:', best_data[4], 'value:', best_data[5])
    print(best_blockMat)
    return best_position, best_rotation


def calc_all_heights(blockMat, game_width, game_height):
    height = [0]*game_width
    for i in range(game_height-1, -1, -1):
        for j in range(0, game_width):
            if blockMat[i][j] != 'empty':
                height[j] = game_height - i
    return height


def calc(blockMat, game_width, game_height):
    h = calc_all_heights(blockMat, game_width, game_height)
    # calculate aggregate height
    max_height = max(h)
    a_height = 0
    for height in h:
        a_height += height

    # calculate highest height
    highest_height = max(h)

    # calculate bumpiness
    bumpiness = 0
    for i in range(0, len(h) - 1):
        bumpiness += abs(h[i] - h[i+1])
        
    # calculate lines cleared
    cleared = 0
    for i in range(game_height - 1, -1, -1):
        zeros = 0
        for j in range(game_width):
            if blockMat[i][j] == 'empty':
                break
            zeros += 1
        if zeros == game_width:
            cleared += 1
            
    # calculate holes
    holes = 0
    for c in range(game_width):
        block = False
        for r in range(game_height - 1, -1, -1):
            if (blockMat[r][c] == 'empty'):
                block = True
            elif (blockMat[r][c] != 'empty' and block):
                holes += 1
    return a_height, cleared, holes, bumpiness, highest_height
