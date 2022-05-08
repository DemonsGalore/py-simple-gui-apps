import PySimpleGUI as sg
from time import time
from random import randint

def convert_pos_to_pixel(cell):
    tl = cell[0] * CELL_SIZE, cell[1] * CELL_SIZE
    br = tl[0] + CELL_SIZE, tl[1] + CELL_SIZE
    return tl, br

def get_random_field_position():
    return randint(0, CELL_NUM - 1), randint(0, CELL_NUM)

def get_random_apple_position():
    apple_pos = get_random_field_position()
    while apple_pos in snake_body:
        apple_pos = get_random_field_position()
    return apple_pos

# game constants
FIELD_SIZE = 400
CELL_NUM = 10
CELL_SIZE = FIELD_SIZE / 10
FIELD_COLOR = '#111111'

# snake
snake_body = [(4, 4), (3, 4), (2,4)]
DIRECTIONS = {'up': (0, 1), 'right': (1, 0), 'down': (0, -1), 'left': (-1, 0)}
direction = DIRECTIONS['up']

# apple
apple_pos = get_random_apple_position()
apple_eaten = False

sg.theme('Green')

field = sg.Graph(
    canvas_size = (FIELD_SIZE, FIELD_SIZE),
    graph_bottom_left = (0, 0),
    graph_top_right = (FIELD_SIZE, FIELD_SIZE),
    background_color = FIELD_COLOR
)
layout = [[field]]

window = sg.Window('Snake', layout, return_keyboard_events = True)

start_time = time()

while True:
    event, values = window.read(timeout = 200)

    if event == sg.WIN_CLOSED: break

    if (event == 'Up:38'    or event == 'w' or event == 'W') and not direction == DIRECTIONS['down']:  direction = DIRECTIONS['up']
    if (event == 'Right:39' or event == 'd' or event == 'D') and not direction == DIRECTIONS['left']:  direction = DIRECTIONS['right']
    if (event == 'Down:40'  or event == 's' or event == 'S') and not direction == DIRECTIONS['up']:    direction = DIRECTIONS['down']
    if (event == 'Left:37'  or event == 'a' or event == 'A') and not direction == DIRECTIONS['right']: direction = DIRECTIONS['left']

    time_since_start = time() - start_time
    if time_since_start >= 0.1:
        start_time = time()

        # snake eats apple
        if snake_body[0] == apple_pos:
            apple_pos = get_random_apple_position()
            apple_eaten = True

        # snake update
        new_head = (snake_body[0][0] + direction[0], snake_body[0][1] + direction[1])
        snake_body.insert(0, new_head)
        if not apple_eaten:
            snake_body.pop()
        apple_eaten = False

        # check death
        if not 0 <= snake_body[0][0] < CELL_NUM - 1 or \
           not 0 <= snake_body[0][1] <= CELL_NUM - 1 or \
           snake_body[0] in snake_body[1:]:
            break;

        # reset
        field.draw_rectangle((0, 0), (FIELD_SIZE, FIELD_SIZE), FIELD_COLOR)

        # draw apple
        apple_tl, apple_br = convert_pos_to_pixel(apple_pos)
        field.DrawRectangle(apple_tl, apple_br, 'red')

        # draw snake
        for index, part in enumerate(snake_body):
            tl, br = convert_pos_to_pixel(part)
            color = 'yellow' if index == 0 else 'green'
            field.DrawRectangle(tl, br, color)

window.close()
