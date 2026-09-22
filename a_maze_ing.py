import sys
from pathlib import Path


SRC_PATH = Path(__file__).resolve().parent / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from carving_perfect import carve_perfect_maze, create_table, get_blocked_cells
from carving_pacman import braid_maze
from config_parse import config_parse, config_read
from display import display_maze
from export_maze import export_maze
from solve_bfs import solve_maze_bfs


def main() -> None:
# Check command line arguments.
    if len(sys.argv) != 2:
        print("Usage: python3 src/main.py config.txt")
        return

    config_path = sys.argv[1]

    try:
        config = config_read(config_path)

        if config == "ERROR":
            print("Error: invalid configuration file")
            return

        validated_config = config_parse(*config)

        if validated_config == "ERROR":
            print("Error: invalid configuration values")
            return

        (
            width,
            height,
            entry,
            exit_pos,
            output_file,
            perfect,
            seed,
        ) = validated_config

# Create maze
        maze = create_table(height, width)

        blocked_cells = get_blocked_cells(maze)

        entry_x, entry_y = entry
        exit_x, exit_y = exit_pos

        if blocked_cells[entry_y][entry_x]:
            print("Error: ENTRY cannot be inside the 42 pattern")
            return

        if blocked_cells[exit_y][exit_x]:
            print("Error: EXIT cannot be inside the 42 pattern")
            return

# First generate a perfect maze.
        carve_perfect_maze(
            maze,
            blocked_cells,
            entry,
            seed,
        )

# Convert perfect maze to a pacman-style maze by removing walls from dead ends.
        if not perfect:
            braid_maze(
                maze,
                blocked_cells,
                seed,
            )

        # Config coordinates are (x, y).
        # Solver/display coordinates are (row, col).
        entry_rc = (entry_y, entry_x)
        exit_rc = (exit_y, exit_x)

        # Find the solution.
        path = solve_maze_bfs(
            maze,
            entry_rc,
            exit_rc,
        )

        if not path:
            print("Error: no path found between ENTRY and EXIT")
            return

        # Write maze to output file.
        export_maze(
            maze,
            entry,
            exit_pos,
            path,
            output_file,
        )

        print("\nMaze generated successfully")
        print(f"Size: {width}x{height}")
        print(f"Seed: {seed}")
        print(f"Entry: {entry}")
        print(f"Exit: {exit_pos}")
        print(f"Perfect: {perfect}")
        print(f"Output file: {output_file}")
        print(f"Path length: {len(path)}")

        # Display with MiniLibX.
        display_maze(
            maze,
            entry_rc,
            exit_rc,
            path,
            perfect,
            seed,
            output_file,
        )

    except (OSError, ValueError, IndexError, UnboundLocalError) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()