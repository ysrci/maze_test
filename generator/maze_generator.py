import random
from typing import List, Optional


class MazeGenerator:
    """
    A maze generator using Depth-First Search (DFS) with backtracking.
    Each cell can have walls on 4 sides (North, East, South, West).
    Walls are represented using bitwise flags (0xf = all walls closed).
    """
    N = 0
    E = 1
    S = 2
    W = 3
    mirror = [2, 3, 0, 1]
    moves = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __init__(
            self,
            width: int,
            height: int,
            start: tuple[int, int],
            seed: Optional[int] = None,
            perfect: Optional[bool] = None) -> None:
        """
        Initialize the maze grid with all walls closed (0xf = 0b1111).
        Creates:
        - A maze grid where each cell has all 4 walls closed.
        - A visited matrix to track DFS progression.
        Returns:
        The initialized maze grid (also stored in self.maze)."""
        self.seed = seed
        self.start = start
        self.width = width
        self.height = height
        self.perfect = perfect
        if seed is not None:
            random.seed(seed)

    def wall_generate(self) -> List[List[int]]:
        """
    Initialize the maze grid with all walls closed (0xf = 0b1111).
    Creates:
    - A maze grid where each cell has all 4 walls closed.
    - A visited matrix to track DFS progression.

    Returns:
    The initialized maze grid (also stored in self.maze).
        """
        self.maze = [[0xf for _ in range(self.width)]
                     for _ in range(self.height)]
        self.visited = [[False for _ in range(
            self.width)] for _ in range(self.height)]

        self.write_pattern_42()
        return self.maze

    def write_pattern_42(self) -> None:
        """
        Draws a '42' pattern using fully closed cells (0xF).
        These cells are marked visited so DFS never touches them.
        """
        h, w = self.height, self.width
        error = "Warning: Maze too small for '42'"
        if self.height < 8 or self.width < 10:
            raise ValueError(f'{error} pattern (need 8x10, got {h}x{w})')
    # Top-left anchor (centered)
        base_r = h // 2 - 3
        base_c = w // 2 - 3

        self.pattern = [
            # ---- 4 ----
            (0, 0),
            (1, 0),
            (2, 0), (2, 1), (2, 2),
            (3, 2), (4, 2),
            # ---- 2 ----
            (0, 4), (0, 5), (0, 6),
            (1, 6),
            (2, 4), (2, 5), (2, 6),
            (3, 4),
            (4, 4), (4, 5), (4, 6),
        ]
        for dr, dc in self.pattern:
            r = base_r + dr
            c = base_c + dc

            if 0 <= r < h and 0 <= c < w:
                self.maze[r][c] = 0xF        # fully closed
                self.visited[r][c] = True   # block DFS

    def remove_wall(self, wall: int, dirction: int) -> int:
        """
            Remove a wall from a cell in the specified direction.
            Args:
            cell_walls: Current wall configuration (bitwise).
            direction: Direction constant (NORTH, EAST, SOUTH, or WEST).
            Returns:
            Updated wall configuration with the specified wall removed.

            Example:
            cell = 0xf (0b1111 - all walls closed)
            remove_wall(cell, EAST) -> 0xd (0b1101 - east wall open)
        """
        walls = (0x1, 0x2, 0x4, 0x8)
        if not 0 <= dirction < 4:
            return wall
        # walls: North,East,South,West
        return wall & ~walls[dirction]

    def itrative_dfs(self) -> List[list[int]]:
        """gen maze with itratve dfs this algo is
        start with a full closed cells and moves
        in itch cell and open thier walls
        randomlly tell all cell marked as visited"""
        self.steps = []
        stack = [self.start]
        self.dirction = [self.N, self.E, self.S, self.W]

        while stack:
            row, colm = stack[-1]
            # row, colm = stack.pop()

            found_unvisited = False
            # if the curretn cell is allready visited then skiped it
            if not self.visited[row][colm]:
                self.visited[row][colm] = True

            # marked the current cell as viited

            # shufll the dirctions
            self.dirction = [self.N, self.E, self.S, self.W]
            random.shuffle(self.dirction)

            for d in self.dirction:
                dx, dy = self.moves[d]
                rd = row + dx
                cd = colm + dy
                if (0 <= rd < self.height and
                        0 <= cd < self.width and not
                        self.visited[rd][cd]):

                    # marke this wall as not extranll wall
                    is_external_wall = False

                    if d == self.N and row == 0:  # North wall at top edge
                        is_external_wall = True
                    elif (d == self.S and
                          row == self.height - 1):  # South wall at bottom edge
                        is_external_wall = True
                    elif (d == self.E and
                          colm == self.width - 1):  # East wall at right edge
                        is_external_wall = True
                    elif d == self.W and colm == 0:  # West wall at left edge
                        is_external_wall = True

                    if not is_external_wall:
                        self.maze[row][colm] = self.remove_wall(
                            self.maze[row][colm], d)
                        # there i remove the wall from the current cell
                        mirror = self.mirror[d]
                        # there i reomve the wall from the mirror(neighbor)
                        # cell
                        self.maze[rd][cd] = self.remove_wall(
                            self.maze[rd][cd], mirror)
                        stack.append((rd, cd))
                        self.steps.append((d, dx, dy, row, colm))
                        found_unvisited = True
                        break
            if not found_unvisited:
                stack.pop()
        return self.maze

    def aldous(self) -> List[List[int]]:
        """  choos a wall, any wall and thier
        connected neighbor and travel to it ,
        if the neighbor has not yet been visited
        add it to the visited list
         repeat step 2 untile all cells have been visited"""

        row = random.randint(0, self.height - 1)
        colm = random.randint(0, self.width - 1)

        self.visited[row][colm] = True

        self.dirction = [self.N, self.E, self.S, self.W]
        self.steps = []

        total_cells = self.height * self.width
        pattern_cells = sum(1 for r in range(self.height)
                            for c in range(self.width)
                            if self.visited[r][c])

        visited_count = pattern_cells

        itrate = 0
        while visited_count < total_cells:
            itrate += 1
            valid_neighbors = []

            for d in self.dirction:
                dx, dy = self.moves[d]
                cd = colm + dy
                rd = row + dx

                if 0 <= rd < self.height and 0 <= cd < self.width:
                    valid_neighbors.append((d, rd, cd))

            if not valid_neighbors:
                break

            d, rd, cd = random.choice(valid_neighbors)

            is_pattern_cell = (self.visited[rd][cd] and
                               self.maze[rd][cd] == 0xF)

            if not self.visited[rd][cd]:
                is_external_wall = False

                if d == self.N and row == 0:
                    is_external_wall = True
                elif (d == self.S and
                      row == self.height - 1):
                    is_external_wall = True
                elif (d == self.E and
                      colm == self.width - 1):
                    is_external_wall = True

                elif d == self.W and colm == 0:
                    is_external_wall = True

                if not is_external_wall:
                    self.maze[row][colm] = self.remove_wall(
                        self.maze[row][colm], d)

                    mirror = self.mirror[d]
                    self.maze[rd][cd] = self.remove_wall(
                        self.maze[rd][cd], mirror)
                    dx, dy = self.moves[d]
                    self.steps.append((d, dx, dy, row, colm))
                    self.visited[rd][cd] = True
                    visited_count += 1
            if not is_pattern_cell:
                row = rd
                colm = cd
            if itrate > total_cells * 100:
                break
        return self.maze
