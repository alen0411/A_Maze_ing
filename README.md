*This project has been created as part of the 42 curriculum by agaube and palvare2*

---
## Project Description

A customizable maze generator and solver written in Python, developed as part of the 42 curriculum.
The project focuses on object-oriented programming (OOP), strict type hinting, and clean code structure
while implementing fundamental search algorithms. It is distributed as a standalone utility and a
pip-installable `mazegen` package.

---

## Key Features

- **Dual-Algorithm Generation:** Supports both Depth-First Search (**DFS** via Recursive Backtracking) and Breadth-First Search (**BFS**) architectures to carve custom pathways.
- **Perfect & Imperfect Mazes:** Generates perfect mazes (guaranteed single unique path) or imperfect mazes (dynamically creates multiple valid alternative paths).
**MiniLibX (MLX) Graphical Window:** Real-time 2D window rendering, custom color configurations, dynamic scaling, and smooth visual animations during construction and solution solving phases.
- **Hexadecimal Encoding:** Converts and exports structural layouts into strict, evaluation-ready hex string outputs.
- **Task Automation:** Fully integrated with a local `Makefile` workflow for swift environment setup, testing, linting, and execution.


---

## Repository Structure

The repository includes the following primary files and assets required for compilation and evaluation:

*   `a_maze_ing.py`: The entry-point script responsible for bootstrapping execution, processing configs, and initializing generation.
*   `src/`: Core directory housing the primary internal modules and the structural foundation of the application.
*   `mazegen.tar.gz`: The source distribution archive containing the standalone, pip-installable `mazegen` library pack.
*   `config.txt`: The global workspace parameters file controlling bounds, seeds, and path locations.
*   `Makefile`: Operational rulebook automating developer setup, syntax safety checks, and target execution routines.
*   `.gitignore`: File specifying untracked files that Git should completely ignore.
*   `LICENSE.md`: Legal document defining the open-source license, terms, and permissions for reusing the project's codebase.
*   `README.md`: The main documentation file providing an architectural overview, installation guides, and execution rules.
*   `Setup.py`: The build configuration script used by setuptools to package, build, and compile the `mazegen` distribution bundle.


---

## Instructions & Requirements

### Prerequisites
- Python >= 3.10
- MiniLibX (MLX) source libraries and their required systemic dependencies (X11, AppKit, or OpenGL depending on your OS configuration).
- *Optional:* `flake8` and `mypy` (Strictly required for code style verification and type checks).

### Automation & Tasks
You can easily manage your workflow by using the provided `Makefile` commands:

```bash
make install     # Set up development tools, MLX components, and packages
make run         # Boot and run the primary maze execution and MLX visualization flow
make check-mlx   # Validate that MiniLibX bindings are properly installed and discoverable
make lint        # Validate styling with flake8 and enforce static type checks via mypy
make debug       # Initialize application routines wrapped inside a debugger
make clean       # Wipe out build artifacts and temporary development clutter
```

---

## Configuration File (`config.txt`)

The setup behaviors, boundaries, target generation files, and solving scopes are driven directly by a flat-format parameter file.

```text
WIDTH           = 20
HEIGHT          = 15
ENTRY           = 0,0
EXIT            = 19,14
OUTPUT_FILE     = maze.txt
PERFECT         = True
SEED            = 42
```

### Breakdown of Variables:
- `WIDTH` & `HEIGHT`: Integer bounds determining the raw grid dimensions of the maze canvas.
- `ENTRY` & `EXIT`: Absolute coordinate pairings mapping out the start and finish locations.
- `OUTPUT_FILE`: The designated filesystem string route where structural outputs are preserved.
- `PERFECT`: Boolean flag. `True` creates a clean single-solution environment, while `False` generates loop arrays.
- `SEED`: Optional numeric anchor to lock in deterministic, replicable random generation.


---

## Maze Generator Module (ToDo)

### `MazeGenerator` Class Interface

- Instantiate and use your generator, with at least a basic example.
- Pass custom parameters (e.g., size, seed).
- Access the generated structure, and access at least a solution

### Integration Sample
```python
from a_maze_ing import MazeGenerator
```

---

## Team & Project Management

We discussed each part together and decided on individual responsibilities while ensuring constant collaboration.

- **palvare2** MazeGen module, Maze display and MiniLibX graphics rendering, Saving mazes to a file, Type hints, Makefile, Validation and testing, Packaging
- **agaube** Project initialization, MazeGen module, Algorithms implementation (Backtracking, DFS, BFS), Writing docstrings, Packaging, README.md, License


---

## Lessons & Evolution
* **The Shift to Graphics:** We started with a simple terminal-based text model but upgraded the project to use a MiniLibX (MLX) graphical interface with smooth pixel rendering.
* **What Worked Well:** Collaboration, Clean object-oriented design, fast UI updates, clear type hints, and testing strategy.
* **Future Improvements:** Adding keyboard controls for interactive players, window resizing support, and expanding test coverage, automated testing.

---

## License

MIT License (MIT) Copyright © 2026

A short, permissive software license that lets anyone use, modify, and sell the code for any purpose, as long as they include your original copyright notice.


---

## Resources
* Python official documentation
* Algorithm references for DFS & BFS implementation
* AI assistance was used for general code organization, Makefile structuring
