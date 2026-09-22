import sys
import os
import random
from MazeGenerator import MazeGenerator

# ANSI Terminal Coloring Mechanics
WALL_COLORS = ["\033[90m", "\033[34m", "\033[32m", "\033[35m", "\033[31m"] # Gray, Blue, Green, Purple, Red
RESET = "\033[0m"
ENTRY_COLOR = "\033[93mE"  # Gold Entry
EXIT_COLOR = "\033[91mX"   # Red Exit
PATH_COLOR = "\033[92m*"   # Neon Green Path
PATTERN_42_COLOR = "\033[96m" # Cyan 42 Tracker

def parse_config(file_path: str) -> dict:
    config = {}
    if not os.path.exists(file_path):
        print(f"Error: Configuration file '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                print(f"Error: Bad syntax in config line: {line}", file=sys.stderr)
                sys.exit(1)
            key, val = line.split('=', 1)
            config[key.strip()] = val.strip()
    return config

def write_output(generator: MazeGenerator, filepath: str) -> None:
    try:
        with open(filepath, 'w') as f:
            for row in generator.grid:
                line = "".join(f"{cell:X}" for cell in row)
                f.write(line + "\n")
            f.write("\n")
            f.write(f"{generator.entry[0]},{generator.entry[1]}\n")
            f.write(f"{generator.exit[0]},{generator.exit[1]}\n")
            f.write("".join(generator.solution_path) + "\n")
    except IOError as e:
        print(f"Error: Could not write output file to {filepath}. {e}", file=sys.stderr)
        sys.exit(1)

def display_ascii(generator: MazeGenerator, show_path: bool, color_idx: int) -> None:
    """Renders the maze to the terminal using block elements based on the wall layout."""
    color = WALL_COLORS[color_idx]
    solution_set = set()

    if show_path:
        cx, cy = generator.entry
        solution_set.add((cx, cy))
        for step in generator.solution_path:
            if step == 'N': cy -= 1
            elif step == 'E': cx += 1
            elif step == 'S': cy += 1
            elif step == 'W': cx -= 1
            solution_set.add((cx, cy))

    # Top boundary wall
    print(color + " " + "___" * generator.width + RESET)
    for y in range(generator.height):
        # Line 1: Left wall + Cell floor content
        left_wall = "|" if (generator.grid[y][0] & 8) else " "
        sys.stdout.write(color + left_wall + RESET)

        for x in range(generator.width):
            val = generator.grid[y][x]

            # Identify drawing characters
            char = " "
            if (x, y) == generator.entry:
                char = ENTRY_COLOR
            elif (x, y) == generator.exit:
                char = EXIT_COLOR
            elif (x, y) in solution_set:
                char = PATH_COLOR
            elif (x, y) in generator.pattern_42_cells:
                char = PATTERN_42_COLOR + "█" if x % 2 == 0 else PATTERN_42_COLOR + "█"
                char += RESET

            # Right wall encoding check
            right = color + "|" + RESET if (val & 2) else " "
            # Floor check (South wall)
            floor = color + "_" + RESET if (val & 4) else " "

            sys.stdout.write(f"{floor}{RESET}{char}{right}")
        sys.stdout.write("\n")

def interactive_loop(generator: MazeGenerator, config: dict) -> None:
    show_path = True
    color_idx = 0

    while True:
        print("\033[H\033[2J", end="")
        print(f"\n=== A-MAZE-ING INTERACTIVE VIEWER (Size: {generator.width}x{generator.height}) ===")
        display_ascii(generator, show_path, color_idx)
        print("\n[Please select one option]:\n [P] Toggle Path\n [C] Cycle Colors\n [R] Regenerate Seed\n [Q] Quit")

        try:
            choice = input("Select an option: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            break

        if choice == 'q':
            break
        elif choice == 'p':
            show_path = not show_path
        elif choice == 'c':
            color_idx = (color_idx + 1) % len(WALL_COLORS)
        elif choice == 'r':
            # Seed the layout initialaze shift
            generator.seed = random.randint(1, 99999)
            generator.generate()
            # Catch which layout seed was successfull with solving the maze
            print(f"Solvable Seed Discovered: {generator.seed}")
            write_output(generator, config['OUTPUT_FILE'])

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        sys.exit(1)

    config = parse_config(sys.argv[1])

    try:
        width = int(config['WIDTH'])
        height = int(config['HEIGHT'])
        entry = tuple(map(int, config['ENTRY'].split(',')))
        exit_cell = tuple(map(int, config['EXIT'].split(',')))
        perfect = config.get('PERFECT', 'False').lower() == 'true'
        output_file = config['OUTPUT_FILE']
        seed = int(config.get('SEED', random.randint(0, 100000)))
    except (KeyError, ValueError) as e:
        print(f"Error parsing configuration metrics: {e}", file=sys.stderr)
        sys.exit(1)

    if len(entry) != 2 or len(exit_cell) != 2:
        print("Error: ENTRY and EXIT must match valid format x,y", file=sys.stderr)
        sys.exit(1)

    try:
        maze = MazeGenerator(width, height, entry, exit_cell, perfect=perfect, seed=seed)
        maze.generate()
        write_output(maze, output_file)
        interactive_loop(maze, config)
    except Exception as e:
        print(f"Runtime Crash Halted: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
