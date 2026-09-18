from carving import (
    carve_perfect_maze,
    create_table,
    get_blocked_cells,
)
from display import display_maze
from solve import solve_maze_dfs


def main() -> None:
    """Generate, solve and display a maze."""

    # -------------------------------------------------------
    # Temporary configuration.
    # Later these values will come from config.txt.
    # -------------------------------------------------------

    width = 20
    height = 15

    entry = (0, 0)
    exit_pos = (19, 14)

    seed = 45
    perfect = True

    # -------------------------------------------------------
    # Create maze.
    # -------------------------------------------------------

    maze = create_table(
        height,
        width,
    )

    # -------------------------------------------------------
    # Create the 42 pattern.
    # -------------------------------------------------------

    blocked_cells = get_blocked_cells(maze)

    entry_x, entry_y = entry
    exit_x, exit_y = exit_pos

    if blocked_cells[entry_y][entry_x]:
        raise ValueError(
            "Entry cannot be inside the 42 pattern"
        )

    if blocked_cells[exit_y][exit_x]:
        raise ValueError(
            "Exit cannot be inside the 42 pattern"
        )

    # -------------------------------------------------------
    # Generate maze.
    # -------------------------------------------------------

    if perfect:
        carve_perfect_maze(
            maze,
            blocked_cells,
            entry,
            seed,
        )
    else:
        raise NotImplementedError(
            "PERFECT=False is not implemented yet"
        )

    # -------------------------------------------------------
    # Print hexadecimal representation for debugging.
    # -------------------------------------------------------

    print("\nMaze generated:\n")

    for row in maze:
        print(
            "".join(
                f"{cell:X}"
                for cell in row
            )
        )

    # -------------------------------------------------------
    # Convert config coordinates:
    #
    # config:   (x, y)
    # internal: (row, col)
    # -------------------------------------------------------

    entry_rc = (
        entry_y,
        entry_x,
    )

    exit_rc = (
        exit_y,
        exit_x,
    )

    # -------------------------------------------------------
    # Solve maze.
    # -------------------------------------------------------

    path = solve_maze_dfs(
        maze,
        entry_rc,
        exit_rc,
    )

    if not path:
        raise ValueError(
            "No path found between entry and exit"
        )

    # -------------------------------------------------------
    # Debug information.
    # -------------------------------------------------------

    print("\nMaze information:")
    print(f"Size: {width}x{height}")
    print(f"Seed: {seed}")
    print(f"Entry: {entry}")
    print(f"Exit: {exit_pos}")
    print(f"Path length: {len(path)}")

    print("\nPath:")
    print(path)

    # -------------------------------------------------------
    # Display using MiniLibX.
    # -------------------------------------------------------

    display_maze(
        maze,
        entry_rc,
        exit_rc,
        path,
    )


if __name__ == "__main__":
    main()