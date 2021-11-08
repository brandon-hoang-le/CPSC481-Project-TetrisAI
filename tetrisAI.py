import pygame
import copy


class Event():
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key


counter = 0


def run_ai(game_field, game_width, game_height):
    global counter
    counter += 1
    if counter < 3:
        return []
    counter = 0
    rotation_counter = 1
    e = []
    # print(simulate(game_field, game_field.piece, game_width, game_height))
    rotation, position = best_rotation_position(
        game_field, game_width, game_height)
    # print(rotation_counter, rotation, position)
    # if rotation_counter != rotation:
    #     e.append(Event(pygame.KEYDOWN, pygame.K_UP))
    #     e.append(Event(pygame.KEYUP, pygame.K_UP))
    #     rotation_counter += 1
    if rotation_counter != rotation:
        e.append(Event(pygame.KEYDOWN, pygame.K_UP))
        e.append(Event(pygame.KEYUP, pygame.K_UP))
        rotation_counter += 1
    elif game_field.piece.blocks[2].currentPos.col < position:
        e.append(Event(pygame.KEYDOWN, pygame.K_RIGHT))
        e.append(Event(pygame.KEYUP, pygame.K_RIGHT))
    elif game_field.piece.blocks[2].currentPos.col > position:
        e.append(Event(pygame.KEYDOWN, pygame.K_LEFT))
        e.append(Event(pygame.KEYUP, pygame.K_LEFT))
    else:
        e.append(Event(pygame.KEYDOWN, pygame.K_DOWN))
        e.append(Event(pygame.KEYUP, pygame.K_DOWN))
    # for i in range(0, 4):
    #     print('col num', game_field.piece.blockMat[i])
    #     print('status', game_field.piece.status)
    return e


def simulate(game, game_figure_image, game_width=10, game_height=20):
    game_field = copy.deepcopy(game.blockMat)
    # print(game_field)
    new_game_figure_image = copy.deepcopy(game_figure_image)
    # while not new_game_figure_image.movCollisionCheck("down"):
    #     new_game_figure_image.createNextMove("down")

    # while not new_game_figure_image.movCollisionCheck("down"):
    #     new_game_figure_image.rowNum -= 1
    #     print(new_game_figure_image.rowNum)

    while not new_game_figure_image.movCollisionCheck("down"):
        new_game_figure_image.createNextMove("down")
        new_game_figure_image.applyNextMove()
    for i in range(0, 4):
        game_field[new_game_figure_image.blocks[i].currentPos.row][new_game_figure_image.blocks[i].currentPos.col] = \
            new_game_figure_image.type
    height = game_height
    holes = 0
    filled = []
    for i in range(game_height-1, -1, -1):
        for j in range(game_width):
            u = '_'
            if game_field[i][j] != "empty":
                u = "x"
            for ii in range(4):
                for jj in range(4):
                    if ii * 4 + jj in new_game_figure_image.blockMat:
                        if jj + new_game_figure_image.colNum == j and ii + new_game_figure_image.rowNum == i:
                            u = "x"

            if u == "x" and i < height:
                height = i
            if u == "x":
                filled.append((i, j))
                for k in range(i, game_height):
                    if (k, j) not in filled:
                        holes += 1
                        filled.append((k, j))
    return holes, game_height-height


def best_rotation_position(game_field, game_width, game_height):
    best_height = game_height
    best_holes = game_height*game_width
    best_position = None
    best_rotation = None
    rotation = 0
    for i in range(4):
        new_game_figure = copy.deepcopy(game_field.piece)
        new_game_figure.rotate('CW')
        rotation += 1
        # move to left
        atLeft = False
        for j in range(game_width//2):
            new_game_figure1 = copy.deepcopy(new_game_figure)
            new_game_figure1.createNextMove("left")
            new_game_figure1.applyNextMove()
            for i in range(4):
                if new_game_figure1.blocks[i].currentPos.row <= -1 or new_game_figure1.blocks[i].currentPos.col <= -1:
                    atLeft = True
                    break
            if atLeft:
                break
            new_game_figure = new_game_figure1
        # for j in range(game_width):
        #     new_game_figure.createNextMove("left")
        #     new_game_figure.applyNextMove()
        for j in range(game_width):
            atRight = False
            if not new_game_figure.movCollisionCheck("down"):
                holes, height = simulate(
                    game_field,
                    new_game_figure,
                    game_width,
                    game_height
                )
                print(holes, height)
                if best_position is None or best_holes > holes or \
                        best_holes == holes and best_height > height:
                    best_height = height
                    best_holes = holes
                    best_position = j
                    best_rotation = rotation
            # new_game_figure.createNextMove("right")
            # new_game_figure.applyNextMove()

            new_game_figure1 = copy.deepcopy(new_game_figure)
            new_game_figure1.createNextMove("right")
            new_game_figure1.applyNextMove()
            for i in range(4):
                if new_game_figure1.blocks[i].currentPos.row > game_width - 1 or new_game_figure1.blocks[i].currentPos.col > game_width - 1:
                    atRight = True
                    break
            if atRight:
                break
            new_game_figure = new_game_figure1

    return best_rotation, best_position
