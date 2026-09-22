from carving_perfect import DIRECTIONS

def solve_maze_dfs(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit_pos: tuple[int, int]
) -> list[tuple[int, int]]:
    stack: list[tuple[int, int]] = [entry]
    visited: set[tuple[int, int]] = set()

    while stack:
        current = stack[-1]

        if current == exit_pos:
            return stack

        visited.add(current)

        neighbors = get_neighbors(
            maze,
            current,
            visited
        )

        if neighbors:
            stack.append(neighbors[0])
        else:
            stack.pop()

    return []

def get_neighbors(
    maze: list[list[int]],
    current: tuple[int, int],
    visited: set[tuple[int, int]]
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