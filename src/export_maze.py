import carving_perfect

def take2coordinates(
    path: list[tuple[int, int]]
) -> str:
    directions = ""

    for i in range(len(path) - 1):
        row1, col1 = path[i]
        row2, col2 = path[i + 1]

        if row2 == row1 - 1:
            directions += "N"
        elif row2 == row1 + 1:
            directions += "S"
        elif col2 == col1 + 1:
            directions += "E"
        elif col2 == col1 - 1:
            directions += "W"

    return directions

def export_maze(maze, entry, exit_pos, path, filename):
    with open(filename, "w") as f:
        for row in maze:
            f.write("".join(f"{cell:x}" for cell in row) + "\n")

        f.write("\n")
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_pos[0]},{exit_pos[1]}\n")
        f.write(take2coordinates(path) + "\n")