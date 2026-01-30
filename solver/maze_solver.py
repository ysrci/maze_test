from collections import deque
from typing import List, Tuple, Any


class MazeSolver:
    def __init__(self, height: int, width: int, maze: List[List[int]],
                 start: Tuple[int, int], end: Tuple[int, int]) -> None:

        self.height = height
        self.width = width
        self.maze_int = maze
        self.start = start
        self.end = end

        self.maze = self._parse_maze()

        self.steps_to_path: List[Tuple[int, int]] = []
        self.all_steps: List[Tuple[int, int]] = []

    def _int_to_walls(self, value: int) -> List[bool]:
        """
        *  value    = 5
        -> North = True
        -> East  = False
        -> South = True
        -> West  = False
        """
        walls = [False, False, False, False]
        if value & 1:
            walls[0] = True
        if value & 2:
            walls[1] = True
        if value & 4:
            walls[2] = True
        if value & 8:
            walls[3] = True
        return walls

    def _parse_maze(self) -> List[List[List[bool]]]:
        """List[List[int]] --> List[List[List[bool]]]"""
        """maze[y][x] --> [North, East, South, West]"""
        maze = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                value = self.maze_int[y][x]
                walls = self._int_to_walls(value)
                row.append(walls)
            maze.append(row)
        return maze

    def wall_check(self, x: int, y: int) -> List[bool]:
        """Boundary Safety"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.maze[y][x]
        return [True, True, True, True]

    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """Verify that there is no wall"""
        """and also that there is no wall on the opposite side"""
        neighbors = []
        walls = self.wall_check(x, y)
        if y > 0 and not walls[0] and not self.maze[y - 1][x][2]:
            neighbors.append((x, y - 1))
        if x < self.width - 1 and not walls[1] and not self.maze[y][x + 1][3]:
            neighbors.append((x + 1, y))
        if y < self.height - 1 and not walls[2] and not self.maze[y + 1][x][0]:
            neighbors.append((x, y + 1))
        if x > 0 and not walls[3] and not self.maze[y][x - 1][1]:
            neighbors.append((x - 1, y))
        return neighbors

    def bfs(self) -> None:
        queue = deque([self.start])
        visited = [[False] * self.width for _ in range(self.height)]
        visited[self.start[1]][self.start[0]] = True
        parent: dict[Any, Any] = {}
        self.all_steps = [self.start]

        while queue:
            x, y = queue.popleft()

            if (x, y) == self.end:
                path = []
                curr = (x, y)
                while curr in parent:
                    path.append(curr)
                    curr = parent[curr]
                path.append(self.start)
                path.reverse()
                self.steps_to_path = path
                return

            for nx, ny in self._get_neighbors(x, y):
                if not visited[ny][nx]:
                    visited[ny][nx] = True
                    parent[(nx, ny)] = (x, y)
                    self.all_steps.append((nx, ny))
                    queue.append((nx, ny))

        self.steps_to_path = []

    def get_path(self) -> str:
        """change steps_to_path to path"""
        if not self.steps_to_path:
            return ""
        dirs = ""
        for i in range(1, len(self.steps_to_path)):
            x1, y1 = self.steps_to_path[i - 1]
            x2, y2 = self.steps_to_path[i]
            if x2 == x1 + 1:
                dirs += "E"
            elif x2 == x1 - 1:
                dirs += "W"
            elif y2 == y1 + 1:
                dirs += "S"
            elif y2 == y1 - 1:
                dirs += "N"
        return dirs

    def get_maze_hex_strings(self) -> List[str]:
        """maze (int) -> maze(hex)"""
        hex_rows = []
        for y in range(self.height):
            row_str = ""
            for x in range(self.width):
                value = self.maze_int[y][x]
                hex_char = format(value, 'X')
                row_str += hex_char
            hex_rows.append(row_str)
        return hex_rows

    def create_output_file(self, filename: str = "output_maze.txt") -> None:
        """create file output_maze.txt"""
        hex_rows = self.get_maze_hex_strings()
        with open(filename, "w") as out:
            for row in hex_rows:
                out.write(row + "\n")
            out.write("\n")
            out.write(f"{self.start[0]},{self.start[1]}\n")
            out.write(f"{self.end[0]},{self.end[1]}\n")
            out.write(self.get_path() + "\n")
