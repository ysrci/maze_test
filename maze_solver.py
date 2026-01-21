from collections import deque
from typing import List, Tuple


def read_config(path: str) -> dict[str, str]:
    config = {}
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()
    return config


def hex_to_walls(hex_char: str) -> list[bool]:
    value = int(hex_char, 16)
    # [N, E, S, W]
    walls = [False, False, False, False]

    if value & 8:
        walls[0] = True  # North
    if value & 4:
        walls[1] = True  # East
    if value & 2:
        walls[2] = True  # South
    if value & 1:
        walls[3] = True  # West

    return walls


def get_neighbors(x: int, y: int, maze: List[List[List[bool]]],
                  width: int, height: int) -> List[Tuple[int, int]]:
    moves = [(0, -1, 0), (1, 0, 1), (0, 1, 2), (-1, 0, 3)]
    neighbors = []
    for dx, dy, wall_idx in moves:
        nx, ny = x+dx, y+dy
        if 0 <= nx < width and 0 <= ny < height:
            if not maze[y][x][wall_idx]:
                opposite = (wall_idx + 2) % 4
                if not maze[ny][nx][opposite]:
                    neighbors.append((nx, ny))
    return neighbors


def bfs(maze: List[List[List[bool]]], start: Tuple[int, int], end: Tuple[int,
        int], width: int, height: int) -> List[Tuple[int, int]]:
    queue = deque([start])
    visited = set([start])
    parent = {}

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent[(x, y)]
            path.append(start)
            path.reverse()
            return path

        for nx, ny in get_neighbors(x, y, maze, width, height):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))
    return []


def read_maze_file(path: str, width: int, height:
                   int) -> List[List[List[bool]]]:
    maze = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                row = [hex_to_walls(c) for c in line]
                maze.append(row)
    if len(maze) != height or any(len(r) != width for r in maze):
        raise ValueError("Maze size does not match WIDTH/HEIGHT")
    return maze


def path_to_directions(path: List[Tuple[int, int]]) -> str:
    dirs = ""
    for i in range(1, len(path)):
        x1, y1 = path[i-1]
        x2, y2 = path[i]
        if x2 == x1 + 1:
            dirs += "E"
        elif x2 == x1 - 1:
            dirs += "W"
        elif y2 == y1 + 1:
            dirs += "S"
        elif y2 == y1 - 1:
            dirs += "N"
    return dirs


def write_output_file(
    output_path: str,
    maze_path: str,
    entry: tuple[int, int],
    exit: tuple[int, int],
    directions: str
):
    with open(output_path, "w") as out:
        # write maze exactly as is
        with open(maze_path, "r") as maze_file:
            for line in maze_file:
                out.write(line.rstrip() + "\n")

        # write entry and exit (back to 1-based)
        out.write(f"{entry[0] + 1},{entry[1] + 1}\n")
        out.write(f"{exit[0] + 1},{exit[1] + 1}\n")

        # write path
        out.write(directions + "\n")


if __name__ == "__main__":
    cfg = read_config("yassir.txt")
    WIDTH = int(cfg["WIDTH"])
    HEIGHT = int(cfg["HEIGHT"])
    ENTRY = tuple(int(x) - 1 for x in cfg["ENTRY"].split(","))
    EXIT = tuple(int(x) - 1 for x in cfg["EXIT"].split(","))

    maze = read_maze_file(cfg["OUTPUT_FILE"], WIDTH, HEIGHT)
    path = bfs(maze, ENTRY, EXIT, WIDTH, HEIGHT)

    if not path:
        print("No path found")
    else:
        directions = path_to_directions(path)

        write_output_file("output_maze.txt",
                          cfg["OUTPUT_FILE"], ENTRY, EXIT, directions)

    print("output_maze.txt generated successfully")

