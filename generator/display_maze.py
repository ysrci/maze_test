import random
from typing import Any, List

from mlx import Mlx

from solver.maze_solver import MazeSolver

from .maze_generator import MazeGenerator


class PutImage:
    def __init__(self, file: str, m: Mlx, mlx_ptr: Any, win_ptr: Any) -> None:
        self.m = m
        self.mlx_ptr = mlx_ptr
        self.win_ptr = win_ptr
        self.image, self.h, self.w = self.m.mlx_png_file_to_image(
            self.mlx_ptr, file)

    def put_image(self) -> None:
        self.m.mlx_put_image_to_window(self.mlx_ptr, self.win_ptr,
                                       self.image, 0, 0)


class DisplayMaze:
    def __init__(self,
                 maze: List[List[int]],
                 width: int,
                 height: int,
                 start: tuple[int, int],
                 Exit: tuple[int, int],
                 gen: MazeGenerator,
                 algo: str, solver: MazeSolver) -> None:
        """ Initialize maze display."""
        self.maze = maze
        self.start = start
        self.exit = Exit
        self.maze_width = width
        self.maze_height = height
        self.gen = gen
        self.animation = False
        self.show = False
        self.row = 0
        self.colm = 0
        self.algo = algo
        self.i = 0
        self.p = 0
        self.solver = solver
        self.drawn_cells = [[False for _ in range(
            self.maze_width)] for _ in range(self.maze_height)]

        # MLX initialization
        self.m = Mlx()
        self.mlx_ptr = self.m.mlx_init()

        # Calculate display parameters
        self.cell_size = self._calculate_cell_size()
        self.win_width = self.maze_width * self.cell_size
        self.win_height = self.maze_height * self.cell_size

    def show_path(self) -> None:
        if not self.show:
            return
        if self.p > len(self.steps_path) - 1:
            self.show = False
            return
        if self.show:
            row, col = self.steps_path[self.p]
            x = self.cell_size * row
            y = self.cell_size * col

            border_offset = self.border
            overlay_size = self.cell_size - (border_offset * 2)

            color = self.path_color
            self._draw_rect(
                x + border_offset,
                y + border_offset,
                overlay_size,
                overlay_size,
                color)
            self.p += 1

    def _draw_rect(self, x: int, y: int, w: int, h: int, color: int) -> None:
        """Draw a filled rectangle."""
        for dy in range(h):
            for dx in range(w):
                self._put_pixel(x + dx, y + dy, color)

    def _put_pixel(self, x: int, y: int, color: int) -> None:
        """Draw a single pixel."""
        if 0 <= x < self.win_width and 0 <= y < self.win_height:
            self.m.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, color)

    def _draw_cell(
            self,
            row: int,
            col: int) -> None:
        """Draw a single maze cell with walls."""
        if row >= self.maze_height or col >= self.maze_width:
            return

        cell_value = self.maze[row][col]
        x = col * self.cell_size
        y = row * self.cell_size

        # Determine background color
        if (row, col) == self.start:
            bg_color = self.start_color
        elif (row, col) == self.exit:
            bg_color = self.exit_color
        elif cell_value == 0xF:
            bg_color = self.cell_color
        else:
            bg_color = self.back_color

        # Draw cell background
        self._draw_rect(x, y, self.cell_size, self.cell_size, bg_color)

        #  Draw walls
        wall_color = self.wall_clr
        wall_thickness = self.border

        # North wall (bit 0x1)
        if (cell_value & 0x1):
            self._draw_rect(x, y, self.cell_size, wall_thickness, wall_color)

        # East wall (bit 0x2)
        if cell_value & 0x2:
            self._draw_rect(
                x + self.cell_size - wall_thickness,
                y,
                wall_thickness,
                self.cell_size,
                wall_color
            )
        # South wall (bit 0x4)
        if cell_value & 0x4:
            self._draw_rect(
                x,
                y + self.cell_size - wall_thickness,
                self.cell_size,
                wall_thickness,
                wall_color
            )

        # West wall (bit 0x8)
        if cell_value & 0x8:
            self._draw_rect(x, y, wall_thickness, self.cell_size, wall_color)

    def cell_rendring(self) -> None:
        """ rendring the  maze color"""

        # rendring only cells are visted if the flage A presed
        if self.animation:
            (random.randint(1, 0xffffff) << 8) | 0xff
            for row in range(self.maze_height):
                for col in range(self.maze_width):
                    if self.drawn_cells[row][col]:
                        self._draw_cell(row, col)

        elif not self.animation:
            self.display_maze()

    def put_helper_image(self, image: str) -> None:
        self.s = PutImage(image, self.m, self.mlx_ptr, self.win_info)
        self.s.put_image()

    def key_hook(self, keycode: int, params: tuple[Any]) -> Any:
        """Handle key press events."""
        self.keycode = keycode

        if self.keycode == 65307:
            print(f"pressed Esc key id :({keycode} - Exiting...)")
            self.m.mlx_loop_exit(self.mlx_ptr)
        # clear the curent window and change the color
        elif keycode == 32:
            self.start_color = (random.randint(1, 0xffffff)) | 0xff << 24
            self.exit_color = (random.randint(1, 0xffffff)) | 0xff << 24
            self.cell_color = (random.randint(1, 0xffffff)) | 0xff << 24
            self.back_color = (random.randint(1, 0xffffff)) | 0xff << 24
            self.wall_clr = (random.randint(1, 0xffffff)) | 0xff << 24
            self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)

            self.cell_rendring()

        elif keycode == 114:
            # re genrate a new random maze
            if not self.animation:
                self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)
                self.maze = self.gen.wall_generate()
                self.gen.seed = random.randint(1, 50000000000)
                if self.algo == 'dfs':
                    self.maze = self.gen.itrative_dfs()
                else:
                    self.maze = self.gen.aldous()
                self.solver = MazeSolver(self.maze_height, self.maze_width,
                                         self.maze, self.start, self.exit)
                self.solver.bfs()
                self.solver.create_output_file()
                self.display_maze()
        elif keycode == 97:
            # display with animations
            self.m.mlx_clear_window(self.mlx_ptr, self.win_ptr)
            self.steps = self.gen.steps
            self.i = 0
            self.animation = True
        elif keycode == 104:
            self.win_info = self.m.mlx_new_window(
                self.mlx_ptr, 300, 300, 'help-keys')
            self.put_helper_image('images/m')
            self.m.mlx_hook(self.win_info, 33, 0, self.close_info, None)

        elif keycode == 112 and not self.animation:
            self.p = 0
            self.show = True
            self.path_color = 0x16921D8FF
            self.steps_path = self.solver.steps_to_path

    def display_maze(self) -> None:
        """ display maze without animations"""

        for row in range(self.maze_height):
            for col in range(self.maze_width):
                self._draw_cell(row, col)

    def display_with_animations(self, params: tuple) -> None:
        """ start displaying maze genrations with animations"""
        if self.show and not self.animation:
            self.show_path()
        if not self.animation:
            return
        if self.i >= len(self.steps):
            self.animation = False
            self.drawn_cells = [[False for _ in range(
                self.maze_width)] for _ in range(self.maze_height)]
            return
        self.d, self.dx, self.dy, self.row, self.colm = self.steps[self.i]
        if self.animation and (self.row < self.maze_height):
            self.maze[self.row][self.colm] = self.gen.remove_wall(
                self.maze[self.row][self.colm], self.d)
            self._draw_cell(self.row, self.colm)
            self.drawn_cells[self.row][self.colm] = True

            # there i remove the wall from the current cell
            mirror = self.gen.mirror[self.d]
            # there i reomve the wall from the mirror(neighbor)
            # cell
            rd = self.row + self.dx
            cd = self.colm + self.dy

            if 0 <= rd < self.maze_height and 0 <= cd < self.maze_width:
                self.maze[rd][cd] = self.gen.remove_wall(
                    self.maze[rd][cd], mirror)
                self._draw_cell(rd, cd)
                self.drawn_cells[rd][cd] = True
            self.i += 1

    def _calculate_cell_size(self) -> int:
        """Calculate appropriate cell size based on maze dimensions."""
        if self.maze_width <= 20 and self.maze_height <= 20:
            self.border = 4
            return 30
        elif self.maze_width <= 50 and self.maze_height <= 50:
            self.border = 3
            return 15
        elif self.maze_width <= 100 and self.maze_height <= 100:
            self.border = 2
            return 10
        elif self.maze_width <= 200 and self.maze_height <= 200:
            self.border = 1
            return 4
        else:
            self.border = 1
            return 3

    def close(self, params: Any) -> None:
        '''closing the window if the x key in the bottom is pressed'''
        self.m.mlx_loop_exit(self.mlx_ptr)

    def close_info(self, params: Any) -> None:
        self.m.mlx_destroy_window(self.mlx_ptr, self.win_info)

    def start_display(self) -> None:
        """ Start the display."""
        self.win_ptr = self.m.mlx_new_window(
            self.mlx_ptr, self.win_width, self.win_height, "A-Maze-ing")

        if not self.win_ptr:
            raise Exception('Failed to create window')
        # Setup hooks
        self.m.mlx_hook(self.win_ptr, 33, 0, self.close, None)
        self.m.mlx_key_hook(self.win_ptr, self.key_hook,
                            (self.mlx_ptr, self.win_ptr))

        # set default colors
        self.start_color = 0xff0000ff
        self.exit_color = 0xFFFFFF00
        self.cell_color = 0xFFFF00FF
        self.back_color = 0x000000
        self.wall_clr = 0xFFFFFFFF
        self.display_maze()
        # Start event loop
        self.m.mlx_loop_hook(
            self.mlx_ptr,
            self.display_with_animations, None)
        self.loop = self.m.mlx_loop(self.mlx_ptr)
