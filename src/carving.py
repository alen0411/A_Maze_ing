import config
import random

NORTH = 0b0001  # 1
EAST  = 0b0010  # 2
SOUTH = 0b0100  # 4
WEST  = 0b1000  # 8
ALL_WALLS = 0b1111  # 0xF

OPPOSITES = {
    NORTH: SOUTH,
    EAST: WEST,
    SOUTH: NORTH,
    WEST: EAST,
}

DIRECTIONS = {
    NORTH: (0, -1),
    EAST: (1, 0),
    SOUTH: (0, 1),
    WEST: (-1, 0),
}

def create_table(rows: int, cols: int) -> list[list[int]]:
    return [[ALL_WALLS for _ in range(cols)] for _ in range(rows)]

def open_wall(
    maze: list[list[int]],
    row: int,
    col: int,
    direction: int
) -> None:
    dx, dy = DIRECTIONS[direction]

    neighbour_row = row + dy
    neighbour_col = col + dx

    maze[row][col] &= ~direction
    maze[neighbour_row][neighbour_col] &= ~OPPOSITES[direction]

def get_blocked_cells(
        maze: list[list[int]]
)   -> list[list[bool]]:
    
    blocked_cells = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]

    if (len(maze) < 7 or len(maze[0]) < 9):
        print("Warning: Maze is too small to have a proper 42")
        return blocked_cells

    central_row = len(maze) // 2
    central_col = len(maze[0]) // 2
    
    save_42(central_row, central_col, blocked_cells)

    return blocked_cells

def save_42(
    central_row: int,
    central_col: int,
    blocked_cells: list[list[bool]],
) -> None:

    pattern = [
        "1.1.111",
        "1.1...1",
        "111.111",
        "..1.1..",
        "..1.111",
    ]

    pattern_height = len(pattern)
    pattern_width = len(pattern[0])

    start_row = central_row - pattern_height // 2
    start_col = central_col - pattern_width // 2

    for row in range(pattern_height):
        for col in range(pattern_width):
            if pattern[row][col] == "1":
                blocked_cells[start_row + row][start_col + col] = True

def get_unvisited_neighbors(
    row: int,
    col: int,
    visited: list[list[bool]],
    blocked_cells: list[list[bool]],
) -> list[tuple[int, int, int]]:
    neighbors: list[tuple[int, int, int]] = []

    for direction, (dx, dy) in DIRECTIONS.items():
        new_row = row + dy
        new_col = col + dx

        if (
            0 <= new_row < len(visited)
            and 0 <= new_col < len(visited[0])
            and not visited[new_row][new_col]
            and not blocked_cells[new_row][new_col]
        ):
            neighbors.append((new_row, new_col, direction))

    return neighbors

def carve_perfect_maze(
    maze: list[list[int]],
    blocked_cells: list[list[bool]],
    entry: tuple[int, int],
    seed: int,
) -> None:
    height = len(maze)
    width = len(maze[0])

    visited = [
        [False for _ in range(width)]
        for _ in range(height)
    ]

    rng = random.Random(seed)

    start_col, start_row = entry

    visited[start_row][start_col] = True

    stack: list[tuple[int, int]] = [
        (start_row, start_col)
    ]

    while stack:
        row, col = stack[-1]

        neighbors = get_unvisited_neighbors(
            row,
            col,
            visited,
            blocked_cells,
        )

        if neighbors:
            new_row, new_col, direction = rng.choice(neighbors)

            open_wall(
                maze,
                row,
                col,
                direction,
            )

            visited[new_row][new_col] = True
            stack.append((new_row, new_col))

        else:
            stack.pop()