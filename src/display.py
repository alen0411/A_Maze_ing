from mlx import Mlx

from carving import EAST, NORTH, SOUTH, WEST


CELL_SIZE = 30
MARGIN = 20
HEADER_HEIGHT = 45

WALL_COLORS = [
    0xFFFFFFFF,  # White
    0xFF00FFFF,  # Cyan
    0xFFFF66FF,  # Magenta
    0xFFFFAA33,  # Orange
]

PATH_COLOR = 0xFFFFFF00
ENTRY_COLOR = 0xFF00CC66
EXIT_COLOR = 0xFFFF4444
PATTERN_COLOR = 0xFF303850
TEXT_COLOR = 0xFFFFFFFF

KEY_ESC = 65307
KEY_SPACE = 32
KEY_C = 99


class MazeDisplay:
    """Graphical maze representation using MiniLibX."""

    def __init__(
        self,
        maze: list[list[int]],
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        path: list[tuple[int, int]],
    ) -> None:
        """Initialize the maze display."""
        self.maze = maze
        self.entry = entry
        self.exit_pos = exit_pos
        self.path = path

        self.height = len(maze)
        self.width = len(maze[0])

        self.show_path = True
        self.wall_color_index = 0

        self.needs_redraw = True

        self.window_width = (
            self.width * CELL_SIZE
            + (MARGIN * 2)
            + 1
        )

        self.window_height = (
            self.height * CELL_SIZE
            + HEADER_HEIGHT
            + MARGIN
            + 1
        )

        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()

        if self.mlx_ptr is None:
            raise RuntimeError("Could not initialize MiniLibX")

        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr,
            self.window_width,
            self.window_height,
            "A-Maze-ing",
        )

        if self.win_ptr is None:
            raise RuntimeError("Could not create MiniLibX window")

    def cell_origin(
        self,
        row: int,
        col: int,
    ) -> tuple[int, int]:
        """Return the top-left pixel of a maze cell."""
        x = MARGIN + col * CELL_SIZE
        y = HEADER_HEIGHT + row * CELL_SIZE

        return x, y

    def cell_center(
        self,
        row: int,
        col: int,
    ) -> tuple[int, int]:
        """Return the center pixel of a maze cell."""
        x, y = self.cell_origin(row, col)

        return (
            x + CELL_SIZE // 2,
            y + CELL_SIZE // 2,
        )

    def draw_rectangle(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        color: int,
    ) -> None:
        """Draw a filled rectangle."""
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                self.mlx.mlx_pixel_put(
                    self.mlx_ptr,
                    self.win_ptr,
                    x,
                    y,
                    color,
                )

    def draw_circle(
        self,
        center_x: int,
        center_y: int,
        radius: int,
        color: int,
    ) -> None:
        """Draw a filled circle."""
        radius_squared = radius * radius

        for y in range(-radius, radius + 1):
            for x in range(-radius, radius + 1):
                if x * x + y * y <= radius_squared:
                    self.mlx.mlx_pixel_put(
                        self.mlx_ptr,
                        self.win_ptr,
                        center_x + x,
                        center_y + y,
                        color,
                    )

    def draw_horizontal_wall(
        self,
        x: int,
        y: int,
    ) -> None:
        """Draw a horizontal wall."""
        thickness = 2

        self.draw_rectangle(
            x,
            y,
            x + CELL_SIZE,
            y + thickness - 1,
            WALL_COLORS[self.wall_color_index],
        )

    def draw_vertical_wall(
        self,
        x: int,
        y: int,
    ) -> None:
        """Draw a vertical wall."""
        thickness = 2

        self.draw_rectangle(
            x,
            y,
            x + thickness - 1,
            y + CELL_SIZE,
            WALL_COLORS[self.wall_color_index],
        )

    def draw_cell(
        self,
        row: int,
        col: int,
    ) -> None:
        """Draw the walls of one maze cell."""
        cell = self.maze[row][col]

        x, y = self.cell_origin(row, col)

        if cell & NORTH:
            self.draw_horizontal_wall(x, y)

        if cell & EAST:
            self.draw_vertical_wall(
                x + CELL_SIZE,
                y,
            )

        if cell & SOUTH:
            self.draw_horizontal_wall(
                x,
                y + CELL_SIZE,
            )

        if cell & WEST:
            self.draw_vertical_wall(x, y)

    def draw_walls(self) -> None:
        """Draw all maze walls."""
        for row in range(self.height):
            for col in range(self.width):
                self.draw_cell(row, col)

    def draw_42_pattern(self) -> None:
        """Highlight cells that belong to the closed 42 pattern."""
        padding = 5

        for row in range(self.height):
            for col in range(self.width):

                if self.maze[row][col] != 0xF:
                    continue

                x, y = self.cell_origin(row, col)

                self.draw_rectangle(
                    x + padding,
                    y + padding,
                    x + CELL_SIZE - padding,
                    y + CELL_SIZE - padding,
                    PATTERN_COLOR,
                )

    def draw_path_segment(
        self,
        first: tuple[int, int],
        second: tuple[int, int],
    ) -> None:
        """Draw a segment connecting two path cells."""
        row1, col1 = first
        row2, col2 = second

        x1, y1 = self.cell_center(row1, col1)
        x2, y2 = self.cell_center(row2, col2)

        thickness = 5
        half = thickness // 2

        if row1 == row2:
            left = min(x1, x2)
            right = max(x1, x2)

            self.draw_rectangle(
                left,
                y1 - half,
                right,
                y1 + half,
                PATH_COLOR,
            )

        elif col1 == col2:
            top = min(y1, y2)
            bottom = max(y1, y2)

            self.draw_rectangle(
                x1 - half,
                top,
                x1 + half,
                bottom,
                PATH_COLOR,
            )

    def draw_path(self) -> None:
        """Draw the solution path."""
        if len(self.path) < 2:
            return

        for index in range(len(self.path) - 1):
            self.draw_path_segment(
                self.path[index],
                self.path[index + 1],
            )

    def draw_entry_exit(self) -> None:
        """Draw entry and exit markers."""
        entry_row, entry_col = self.entry
        exit_row, exit_col = self.exit_pos

        entry_x, entry_y = self.cell_center(
            entry_row,
            entry_col,
        )

        exit_x, exit_y = self.cell_center(
            exit_row,
            exit_col,
        )

        radius = 8

        self.draw_circle(
            entry_x,
            entry_y,
            radius,
            ENTRY_COLOR,
        )

        self.draw_circle(
            exit_x,
            exit_y,
            radius,
            EXIT_COLOR,
        )

    def draw_header(self) -> None:
        """Draw controls at the top of the window."""
        self.mlx.mlx_string_put(
            self.mlx_ptr,
            self.win_ptr,
            MARGIN,
            20,
            TEXT_COLOR,
            "SPACE: path   C: colour   ESC: quit",
        )

    def render(self) -> None:
        """Draw the complete maze."""
        self.mlx.mlx_clear_window(
            self.mlx_ptr,
            self.win_ptr,
        )

        self.draw_header()

        self.draw_42_pattern()

        if self.show_path:
            self.draw_path()

        self.draw_walls()

        self.draw_entry_exit()

        self.mlx.mlx_do_sync(self.mlx_ptr)

    def toggle_path(self) -> None:
        """Show or hide the solution path."""
        self.show_path = not self.show_path
        self.needs_redraw = True

    def change_wall_color(self) -> None:
        """Change maze wall colour."""
        self.wall_color_index += 1
        self.wall_color_index %= len(WALL_COLORS)

        self.needs_redraw = True

    def close(self) -> None:
        """Stop the MiniLibX loop."""
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def run(self) -> None:
        """Start the graphical interface."""
        self.mlx.mlx_key_hook(
            self.win_ptr,
            on_key,
            self,
        )

        self.mlx.mlx_loop_hook(
            self.mlx_ptr,
            on_loop,
            self,
        )

        self.mlx.mlx_expose_hook(
            self.win_ptr,
            on_expose,
            self,
        )

        self.mlx.mlx_loop(self.mlx_ptr)


def on_key(
    keycode: int,
    display: MazeDisplay,
) -> int:
    """Handle keyboard events."""
    if keycode == KEY_ESC:
        display.close()

    elif keycode == KEY_SPACE:
        display.toggle_path()

    elif keycode == KEY_C:
        display.change_wall_color()

    return 0


def on_loop(display: MazeDisplay) -> int:
    """Render the window whenever a redraw is required."""
    if display.needs_redraw:
        display.render()
        display.needs_redraw = False

    return 0


def on_expose(display: MazeDisplay) -> int:
    """Request a redraw when the window is exposed."""
    display.needs_redraw = True

    return 0


def display_maze(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
    path: list[tuple[int, int]],
) -> None:
    """Display a maze using MiniLibX."""
    display = MazeDisplay(
        maze,
        entry,
        exit_pos,
        path,
    )

    display.run()