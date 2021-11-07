import pygame
import copy


class Event():
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key


counter = 0


# def run_ai(game_field, game_figure, game_width, game_height):
#     global counter
#     counter += 1
#     if counter < 3:
#         return []
#     counter = 0
#     e1 = Event(pygame.KEYDOWN, pygame.K_UP)
#     # e2 = Event(pygame.KEYUP, pygame.K_UP)
#     return [e1]

def run_ai(game_field, game_figure, game_width, game_height):
    global counter
    counter += 1
    if counter < 3:
        return []
    counter = 0
    rotation_counter = 0
    rotation, position = best_rotation_position(
        game_field, game_figure, game_width, game_height)
    if rotation_counter != rotation:
        e = Event(pygame.KEYDOWN, pygame.K_UP)
        rotation_counter += 1
    elif game_figure.colNum < position:
        e = Event(pygame.KEYDOWN, pygame.K_RIGHT)
    elif game_figure.colNum > position:
        e = Event(pygame.KEYDOWN, pygame.K_LEFT)
    else:
        e = Event(pygame.KEYDOWN, pygame.K_DOWN)
    return [e]


def simulate(game_field, game_figure_image, game_width=10, game_height=20):
    while not game_figure_image.movCollisionCheck_BLOCK("down", game_figure_image.rowNum):
        game_figure_image.rowNum += 1
    game_figure_image.rowNum -= 1
    height = game_height
    holes = 0
    filled = []
    for i in range(game_height-1, -1, -1):
        for j in range(game_width):
            u = '_'
            if game_field[i][j] != 0:
                u = "x"
            for ii in range(4):
                for jj in range(4):
                    if ii * 4 + jj in game_figure_image:
                        if jj + game_figure_image.colNum == j and ii + game_figure_image.rowNum == i:
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


def best_rotation_position(game_field, game_figure, game_width, game_height):
    best_height = game_height
    best_holes = game_height*game_width
    best_position = None
    best_rotation = None
    rotation = 0
    for i in range(4):
        new_game_figure = copy.deepcopy(game_figure)
        new_game_figure.rotate('cCW')
        rotation += 1
        for j in range(game_width):
            print(new_game_figure.colNum)
            if not new_game_figure.movCollisionCheck_BLOCK("down", new_game_figure.colNum):
                holes, height = simulate(
                    game_field,
                    new_game_figure
                )
                if best_position is None or best_holes > holes or \
                        best_holes == holes and best_height > height:
                    best_height = height
                    best_holes = holes
                    best_position = j
                    best_rotation = rotation
    return best_rotation, best_position
