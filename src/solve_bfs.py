from collections import deque

from carving_perfect import DIRECTIONS


def solve_maze_bfs(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
) -> list[tuple[int, int]]:

    queue: deque[tuple[int, int]] = deque([entry])
    visited: set[tuple[int, int]] = {entry}

    parent: dict[
        tuple[int, int],
        tuple[int, int] | None
    ] = {
        entry: None
    }

    while queue:
        current = queue.popleft()

        if current == exit_pos:
            return build_path(parent, exit_pos)

        neighbors = get_neighbors(
            maze,
            current,
            visited,
        )

        for neighbor in neighbors:
            visited.add(neighbor)
            parent[neighbor] = current
            queue.append(neighbor)

    return []


def get_neighbors(
    maze: list[list[int]],
    current: tuple[int, int],
    visited: set[tuple[int, int]],
) -> list[tuple[int, int]]:

    row, col = current
    neighbors: list[tuple[int, int]] = []

    for direction, (dx, dy) in DIRECTIONS.items():
        new_row = row + dy
        new_col = col + dx

        if (
            0 <= new_row < len(maze)
            and 0 <= new_col < len(maze[0])
            and (maze[row][col] & direction) == 0
            and (new_row, new_col) not in visited
        ):
            neighbors.append((new_row, new_col))

    return neighbors


def build_path(
    parent: dict[
        tuple[int, int],
        tuple[int, int] | None
    ],
    exit_pos: tuple[int, int],
) -> list[tuple[int, int]]:

    path: list[tuple[int, int]] = []

    current: tuple[int, int] | None = exit_pos

    while current is not None:
        path.append(current)
        current = parent[current]

    path.reverse()

    return path