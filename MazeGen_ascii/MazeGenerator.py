import random
from typing import List, Tuple, Set, Dict

class MazeGenerator:
    """
    Automated maze carving via Depth-First Search (DFS),
    Pac-Man Loop Rules,
    '42' Solid Block Implementation,
    and Shortest Path Solving (BFS).

    Wall bitmask Layout (LSB - least significant bit):
    Bit 0 (1): North
    Bit 1 (2): East
    Bit 2 (4): South
    Bit 3 (8): West
    """
    def __init__(self, width: int, height: int, entry: Tuple[int, int] = (0, 0),
                 exit_cell: Tuple[int, int] = None, perfect: bool = False ,seed: int = None) -> None:
        # Basic constraints check
        if width <= 0 or height <= 0:
                    raise ValueError("Maze dimensions must be positive integers.")
        self.width = width
        self.height = height
        self.perfect = perfect
        self.entry = entry
        self.exit = exit_cell if exit_cell is not None else (width - 1, height - 1)

        # Isolated random instance to avoid global side effects
        self.seed = seed
        self.rng = random.Random(seed)

        self.grid: List[List[int]] = []
        self.pattern_42_cells: Set[Tuple[int, int]] = set()
        self.solution_path: List[str] = []

        # Define default entry and exit points
        # self.entry = (0, 0)
        # self.exit = (width - 1, height - 1)

    def generate(self) -> List[str]:
        """" Runs the entire structural design cycle. """
        max_attempts = 1000
        attempt = 0

        while attempt < max_attempts:
            attempt += 1
            # 1. Clear canvas and carve a clean spanning tree backbone
            self.grid = [[15 for _ in range(self.width)] for _ in range(self.height)]
            self.pattern_42_cells.clear()
            # 2. Carve the structural tree backbone
            self.carve_dfs(self.entry)
            # 3. Apply Pac-man layout configuration(corners, loops, no dead-ends)
            self._apply_board_rules()
            # 4. Embed explicit closed-cell text patterns into layout centers
            self._inject_42_pattern()
            # 5. Test if the maze can be solved
            self.solution_path = self.solve()
            if self.solution_path:
                return self.solution_path
            # if path is empty, the solution was blocked by '42'
            # shuffle the seed state to whuffle walls for next attempt
            # Sync the random number generator instance if seed changed externally
            self.seed = self.rng.randint(1, 99999)
            self.rng = random.Random(self.seed)

        raise RuntimeError("Failed to generate a solvable layout after "
                          f"{max_attempts} attempts.")


    def carve_dfs(self, start_cell: Tuple[int, int]) -> None:
        """ Randomized DFS maze layout algorithm using an iterative stack. """
        visited: Set[Tuple[int, int]] = {start_cell}
        stack: List[Tuple[int, int]] = [start_cell]

        while stack:
            cx, cy = stack[-1]
            moves = [
                ((cx, cy - 1), 'N'),
                ((cx + 1, cy), 'E'),
                ((cx, cy + 1), 'S'),
                ((cx - 1, cy), 'W')
            ]
            neighbors = []
            for (nx, ny), direction in moves:
                if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in visited:
                    neighbors.append((nx, ny, direction))

            if neighbors:
                nx, ny, direction = self.rng.choice(neighbors)
                self._break_wall(cx, cy, nx, ny, direction)
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()


    def _break_wall(self, x1: int, y1: int, x2: int, y2: int, direction: str) -> None:
        """ Modifies the walls from both cells that share the boundary """
        if direction == 'N':
            self.grid[y1][x1] &= ~1
            self.grid[y2][x2] &= ~4
        elif direction == 'E':
            self.grid[y1][x1] &= ~2
            self.grid[y2][x2] &= ~8
        elif direction == 'S':
            self.grid[y1][x1] &= ~4
            self.grid[y2][x2] &= ~1
        elif direction == 'W':
            self.grid[y1][x1] &= ~8
            self.grid[y2][x2] &= ~2


    def _apply_board_rules(self) -> None:
        """
        Applies Pac-Man rules to the maze (open corners, centers, extra loops)
        """
        # Open up the 4 outer corners and the geometric center cell
        raw_targets = [
            (0, 0), (self.width - 1, 0),  # top-left corner and top-right corner
            (0, self.height - 1), (self.width - 1, self.height - 1), # bottom-left and bottom-right
            (self.width // 2, self.height // 2)  # // round down division operator - for exact center of the maze
        ]

        # Deduplicate safely without corrupting sequence arrays
        targets = []
        for t in raw_targets:
            if t not in targets and 0 <= t[0] < self.width and 0 <= t[1] < self.height:
                targets.append(t)

        # double loop to create open spaces for Pac-Man mode within the 5 target positions (from above)
        for tx, ty in targets:
            if not (0 <= tx < self.width and 0 <= ty < self.height):
                continue
            moves = [
                ((tx, ty - 1), 'N'),
                ((tx + 1, ty), 'E'),
                ((tx, ty + 1), 'S'),
                ((tx - 1, ty), 'W')
            ]
            # above is the temp checklist of 4 immediate neighbors of a target
            # neighbor x , neighbor y and direction
            for (nx, ny), d in moves:
                # only checks the neighbors within the maze
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    # if the neighbor is within a grid it removes the wall between the neighbor and target cell
                    self._break_wall(tx, ty, nx, ny, d)

        # Open up deep dead ends using integer matching instead of string bin() operations
        dead_end_masks = [14, 13, 11, 7, 15] # create a list
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                # if a cell has 3 or more walls closed, it's a dead end.
                if self.grid[y][x] in dead_end_masks:
                    moves = [
                        ((x, y - 1), 'N'),
                        ((x + 1, y), 'E'),
                        ((x, y + 1), 'S'),
                        ((x - 1, y), 'W')
                    ]
                    valid = list([
                        (nx, ny, d) for (nx, ny), d in moves
                        if 0 <= nx	< self.width and 0 <= ny < self.height
                    ])
                    if len(valid) > 0:
                        nx, ny, d = self.rng.choice(valid)
                        # Safety optimization check to avoid making wide, fully hollow spaces
                        if self.grid[ny][nx] != 0:
                            self._break_wall(x, y, nx, ny, d)


    def _inject_42_pattern(self) -> None:
        """ Inject a visible, hard-walled 42 into the center of the maze """
        if self.width < 14 or self.height < 6:
            print("Warning: The maze is too small to be able display a '42' pattern!", flush=True)
            return

        start_x = (self.width // 2) - 4
        start_y = (self.height // 2) - 1

        # Coordinate patterns generating structural block letters for '4' and '2'
        shape_blocks = [
            # The '4' pattern (5x3 block font)
            (start_x, start_y),     (start_x, start_y + 1), (start_x, start_y + 2),
            (start_x + 2, start_y), (start_x + 2, start_y + 1),
            (start_x + 1, start_y + 2),
            (start_x + 2, start_y + 2), (start_x + 2, start_y + 3), (start_x + 2, start_y + 4),
            # The '2' pattern (5x4 block font)
            (start_x + 4, start_y), (start_x + 5, start_y), (start_x + 6, start_y),
            (start_x + 6, start_y + 1),
            (start_x + 4, start_y + 2), (start_x + 5, start_y + 2), (start_x + 6, start_y + 2),
            (start_x + 4, start_y + 3),
            (start_x + 4, start_y + 4), (start_x + 5, start_y + 4), (start_x + 6, start_y + 4)
        ]

        for bx, by in shape_blocks:
            if 0 <= bx < self.width and 0 <= by < self.height:
                if (bx, by) != self.entry and (bx, by) != self.exit:
                    self.grid[by][bx] = 15  # Isolate completely (Close all 4 internal walls)
                    self.pattern_42_cells.add((bx, by))

                    # Update neighboring wall structures to isolate the block
                    if by > 0:
                        self.grid[by - 1][bx] |= 4  # Close neighbor's South wall
                    if bx < self.width - 1:
                        self.grid[by][bx + 1] |= 8  # Close neighbor's West wall
                    if by < self.height - 1:
                        self.grid[by + 1][bx] |= 1  # Close neighbor's North wall
                    if bx > 0:
                        self.grid[by][bx - 1] |= 2  # Close neighbor's East wall


    def solve(self) -> List[str]:
        """ Finds the shortest valid path using BFS."""
        # Queue stores: ((current_x, current_y), [list_of_directions_taken])
        queue: List[Tuple[int, int]] = [self.entry]
        head = 0
        visited: Set[Tuple[int, int]] = {self.entry}
        parent_map: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}

        path_found = False
        while head < len(queue):
            cx, cy = queue[head]
            # Shifts frame window forward in O(1) time complexity
            head += 1

            if (cx, cy) == self.exit:
                path_found = True
                break

            val = self.grid[cy][cx]
            moves = [
                ((cx, cy - 1), 'N', 1),  # Check North bit
                ((cx + 1, cy), 'E', 2),  # Check East bit
                ((cx, cy + 1), 'S', 4),  # Check South bit
                ((cx - 1, cy), 'W', 8)   # Check West bit
            ]

            for (nx, ny), d, bit in moves:
                # Ensure the wall bit is 0 (open path) and target hasn't been visited
                if not (val & bit) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent_map[(nx, ny)] = ((cx, cy), d)
                    queue.append((nx, ny))

        if not path_found:
            return []

        # Reconstruct optimal sequence backwards
        path = []
        curr = self.exit
        while curr != self.entry:
            parent, direction = parent_map[curr]
            path.append(direction)
            curr = parent

        path.reverse()
        return path


    def render_to_console(self, solution_path: List[str] = None) -> None:
        """
        Renders the maze, creates custom structures
        and overlays the solution path if provided.
        """
        render_width = self.width * 2 + 1
        render_height = self.height * 2 + 1
        canvas = [["#" for _ in range(render_width)] for _ in range(render_height)]

        # Build layout base
        for y in range(self.height):
            for x in range(self.width):
                cx = x * 2 + 1
                cy = y * 2 + 1

                # Check if this cell belongs to '42' pattern
                if (x, y) in self.pattern_42_cells:
                    canvas[cy][cx] = "█"  # Solid block indicator
                else:
                    canvas[cy][cx] = "."

                val = self.grid[y][x]
                # Boundary checks: Prevent broken paths from cutting empty holes into font letters
                # North open
                if not (val & 1):
                    canvas[cy - 1][cx] = " " if not (y > 0 and (x, y - 1) in self.pattern_42_cells) else "█"
                # East open
                if not (val & 2):
                   canvas[cy][cx + 1] = " " if not (x + 1 < self.width and (x + 1, y) in self.pattern_42_cells) else "█"
                # South open
                if not (val & 4):
                    canvas[cy + 1][cx] = " " if not (y + 1 < self.height and (x, y + 1) in self.pattern_42_cells) else "█"
                # West open
                if not (val & 8):
                    canvas[cy][cx - 1] = " " if not (x > 0 and (x - 1, y) in self.pattern_42_cells) else "█"

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in  self.pattern_42_cells:
                    cx = x * 2 + 1
                    cy = y * 2 + 1

                    # if a neighbor to the East is also a '42' cell, merge the horizontal gap
                    if x + 1 < self.width and (x + 1, y) in self.pattern_42_cells:
                        canvas[cy][cx + 1] = "█"

                    # if a neighbor to the South is also a '42' cell, merge the vertical gap
                    if y + 1 < self.height and (x, y + 1) in self.pattern_42_cells:
                        canvas[cy + 1][cx] = "█"

        # Overlay the solution path if it exists
        if solution_path:
            px, py = self.entry
            canvas[py * 2 + 1][px * 2 + 1] = "+"  # Mark entry

            for direction in solution_path:
                if direction == 'N':
                    canvas[py * 2][px * 2 + 1] = '+'  # Fills open gap above
                    py -= 1
                elif direction == 'E':
                    canvas[py * 2 + 1][px * 2 + 2] = '+'  # Fills open gap to the right
                    px += 1
                elif direction == 'S':
                    canvas[py * 2 + 2][px * 2 + 1] = '+'  # Fills open gap below
                    py += 1
                elif direction == 'W':
                    canvas[py * 2 + 1][px * 2] = '+'  # Fills open gap to the left
                    px -= 1

                # Mark the path step on the canvas
                canvas[py * 2 + 1][px * 2 + 1] = '+'  # Mark target room center

        for row in canvas:
            print("".join(row))


# --- RUN SIMULATION ---
#if __name__ == "__main__":
#   maze = MazeGenerator(width=20, height=19, seed=42)

#   print("Executing complete maze generation...")
#   path = maze.generate()

#   print("\n--- Final Render ---")
#   print("('█' = Solid Block Text, '+' = Active Shortest Path Solver)\n")
#   maze.render_to_console(solution_path=path)

