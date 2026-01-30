import sys
from typing import Any, Dict, Tuple

from generator.display_maze import DisplayMaze
from generator.maze_generator import MazeGenerator
from solver import MazeSolver


def read_config(path: str) -> Dict[str, Any]:
    """Read configuration file with KEY=VALUE format."""
    config = {}
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config


def check_is_valid(data: dict[str, Any]) -> None:
    keys = [key for key in data.keys()]
    mandatory = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
    for m in mandatory:
        if m not in keys:
            raise KeyError(f'the mandatory key {m} is not found')
    if data['WIDTH'] < 3 or data['HEIGHT'] < 3:
        raise ValueError('the size is to small')
    if len(data['ENTRY']) != 2:
        lentgh = len(data['ENTRY'])
        raise ValueError((f'(ENTRY) cant be a multiple of {lentgh}'))
    if len(data['EXIT']) != 2:
        lentgh = len(data['EXIT'])
        raise ValueError((f'(EXIT) cant be a multiple of {lentgh}'))
    if data['ENTRY'][0] < 0 or data['ENTRY'][1] < 0:
        raise ValueError(('(ENTRY) cant be a nigative value'))
    if data['EXIT'][0] < 0 or data['EXIT'][1] < 0:
        raise ValueError(('(Exit) cant be a nigative value'))
    if data['ENTRY'][0] > data['HEIGHT'] or data['ENTRY'][1] > data['WIDTH']:
        raise ValueError(('ENTRY is too big then the {HEIGHT/WIDTH}'))
    if data['EXIT'][0] > data['HEIGHT'] or data['EXIT'][1] > data['WIDTH']:
        raise ValueError(('Exit is too big then the {HEIGHT/WIDTH}'))
    if (data['ENTRY'][0] == data['EXIT'][0] and
            data['ENTRY'][1] == data['EXIT'][1]):
        raise ValueError(('ENTRY AND EXIT Cannot be the in the sam possition'))
    if isinstance(data['PERFECT'], bool) is False:
        raise ValueError(f"Error: the {data['PERFECT']} is not a boolean")
    if data['Gen-Algo'] != 'dfs':
        if data['Gen-Algo'] != 'Aldous':
            raise ValueError(
                f"Error: the {data['Gen-Algo']} not a valid algorithem")


def check_start_exit(gen: MazeGenerator, width: int, hight: int,
                     exit: Tuple[int, int], start: Tuple[int, int]) -> None:
    h = hight // 2 - 3
    w = width // 2 - 5
    sr, sc = start
    er, ec = exit
    for x, y in gen.pattern:
        r = h + x
        c = w + y
        if (sr == r and sc == c) or (er == r and ec == c):
            raise Exception(
                'Error: Can not put the start'
                ' or the exit in the pattern blocks'
            )


def procces_data(data: dict[str, Any]) -> dict[str, Any]:
    try:
        for key in data.keys():
            if key == 'WIDTH' or key == 'HEIGHT':
                data[key] = int(data[key])
            elif key == 'ENTRY' or key == 'EXIT':
                data[key] = data[key].split(',')
                for i in range(len(data[key])):
                    data[key][i] = int(data[key][i])
                data[key] = tuple(data[key])
            elif key == 'PERFECT':
                if data[key] == 'True':
                    data[key] = True
                elif data[key] == 'False':
                    data[key] = False
            elif key == 'seed':
                data[key] = int(data[key])
    except ValueError:
        raise ValueError('pleas check ur data maybe u wrot abc instaed of 01')
    return data


try:
    data = read_config("config.txt")
    data = procces_data(data)
    check_is_valid(data)
    WIDTH = data['WIDTH']
    HEIGHT = data['HEIGHT']
    ENTRY = data['ENTRY']
    EXIT = data['EXIT']
    OUTPUT_FILE = data['OUTPUT_FILE']
    PERFECT = data['PERFECT']
    seed = data['seed']
    algo = data['Gen-Algo']

    # MazeGenerator & Mazesolver

    gen = MazeGenerator(WIDTH, HEIGHT, ENTRY, seed, PERFECT)
    maze = gen.wall_generate()
    check_start_exit(gen, WIDTH, HEIGHT, EXIT, ENTRY)
    if algo == 'dfs':
        maze = gen.itrative_dfs()
    else:
        maze = gen.aldous()

    solver = MazeSolver(HEIGHT, WIDTH, maze, (1, 0), (15, 11))
    solver.bfs()
    solver.create_output_file()
    # intialize the maze gen and maze display
    display = DisplayMaze(maze, WIDTH, HEIGHT, ENTRY, EXIT, gen, algo, solver)
    display.start_display()


except (ValueError, KeyError, Exception) as e:
    print(e, file=sys.stderr)
