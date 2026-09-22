from carving_perfect import DIRECTIONS, open_wall, WEST, SOUTH, NORTH, EAST
import random

def get_dead_ends(
        maze: list[list[int]],
        blocked_cells: list[list[bool]]
) -> list[tuple[int, int]]:
    dead_ends_values: set[int] = {0b1110, 0b1101, 0b1011, 0b0111}
    dead_ends: list[tuple[int, int]] = []
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if not blocked_cells[row][col] and maze[row][col] in dead_ends_values:
                dead_ends.append((row, col))
    return dead_ends

def get_removable_walls(
        maze: list[list[int]],
        blocked_cells: list[list[bool]],
        cell: tuple[int, int]
) -> list[int]:
    row, col = cell
    removable_walls: list[int] = []
    for direction, (dx, dy) in DIRECTIONS.items():
        new_row = row + dy
        new_col = col + dx
        if (
            0 <= new_row < len(maze)
            and 0 <= new_col < len(maze[0])
            and (direction & maze[row][col]) != 0
            and not blocked_cells[new_row][new_col]
        ):
            removable_walls.append(direction)
    return removable_walls


def has_open_3x3(
    maze: list[list[int]],
) -> bool:
    for row in range(len(maze) - 2):
        for col in range(len(maze[0]) - 2):

            open_area = True

            for r in range(3):
                for c in range(2):
                    if maze[row + r][col + c] & EAST:
                        open_area = False
                        break

                if not open_area:
                    break

            if not open_area:
                continue

            for r in range(2):
                for c in range(3):
                    if maze[row + r][col + c] & SOUTH:
                        open_area = False
                        break

                if not open_area:
                    break

            if open_area:
                return True

    return False

def would_create_3x3(
        maze: list[list[int]],
        cell: tuple[int, int],
        direction: int
) -> bool:
    row, col = cell

    aux_maze = [maze_row.copy() for maze_row in maze]
    open_wall(aux_maze, row, col, direction)
    return has_open_3x3(aux_maze)


def braid_maze(
    maze: list[list[int]],
    blocked_cells: list[list[bool]],
    seed: int,
) -> None:
    rng = random.Random(seed)

    dead_end_values = {
        0b1110,
        0b1101,
        0b1011,
        0b0111,
    }

    dead_ends = get_dead_ends(
        maze,
        blocked_cells,
    )
    rng.shuffle(dead_ends)
    opened_walls = 0

    for cell in dead_ends:
        row, col = cell

        if maze[row][col] not in dead_end_values:
            continue

        removable_walls = list(
            get_removable_walls(
                maze,
                blocked_cells,
                cell,
            )
        )

        rng.shuffle(removable_walls)

        for direction in removable_walls:

            if would_create_3x3(
                maze,
                cell,
                direction,
            ):
                continue

            open_wall(
                maze,
                row,
                col,
                direction,
            )

            opened_walls += 1
            break

    print(f"Walls opened for braiding: {opened_walls}")
    print(
        "Remaining dead ends:",
        len(get_dead_ends(maze, blocked_cells)),
    )