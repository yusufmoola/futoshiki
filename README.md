# Futoshiki Puzzle Solver

A Python implementation of a Futoshiki puzzle solver with two different solving algorithms: basic backtracking and advanced constraint propagation.

## What is Futoshiki?

Futoshiki is a logic puzzle where you fill a 9×9 grid with numbers 1-9, similar to Sudoku, but with additional inequality constraints between adjacent cells. The rules are:

1. Fill each row and column with numbers 1-9 (no duplicates)
2. Respect inequality signs between cells:
   - `>` means left cell > right cell
   - `<` means left cell < right cell  
   - `v` means top cell > bottom cell
   - `^` means top cell < bottom cell

## Features

- **Dual Solving Approaches**:
  - Basic backtracking solver for simple puzzles
  - Advanced constraint propagation solver for better performance on complex puzzles
- **Visual Display**: Clear grid representation with inequality symbols
- **Flexible Input**: Parse puzzles from string format
- **Solution Validation**: Ensures all Futoshiki rules are satisfied

## Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd futoshiki-solver

# Install dependencies
pip install opencv-python numpy
```

## Usage

Run the solver with the included sample puzzle:

```bash
python main.py
```

### Input Format

The solver expects three string inputs:

1. **Numbers**: 9×9 grid with `0` for empty cells
2. **Horizontal inequalities**: `>`, `<`, or `0` for no constraint
3. **Vertical inequalities**: `^`, `v`, or `0` for no constraint

### Example

```python
numbers = """
0 0 0 0 0 8 1 0 0
7 0 8 0 0 6 3 0 2
9 1 2 0 0 0 0 6 0
...
"""

horizontals = """
> 0 0 < 0 0 < >
0 0 > > 0 > < >
...
"""

verticals = """
0 0 ^ ^ v 0 ^ v v
^ v 0 0 ^ 0 0 ^ ^
...
"""

puzzle = FutoshikiPuzzle()
puzzle.parse_puzzle(numbers, horizontals, verticals)
solver = FutoshikiSolver(puzzle.grid, puzzle.inequalities)
solver.solve()
```

## Architecture

### Core Classes

- **`FutoshikiPuzzle`**: Handles puzzle parsing and display
- **`FutoshikiSolver`**: Basic backtracking algorithm
- **`FutoshikiConstraintSolver`**: Advanced constraint propagation with backtracking

### Solving Algorithms

1. **Basic Backtracking**: Simple recursive approach that tries each number 1-9 in empty cells
2. **Constraint Propagation**: Reduces candidate sets using logical deduction before backtracking

## Example Output

```
=== Current Puzzle State ===
Numbers and inequalities:
□ □ □ □ □ 8 < 1 □ □
7 □ 8 > > 6 > 3 < 2
9 > 1 < 2 < □ > □ > 6 □
...

=== Solved Puzzle ===
Solution with inequalities:
3 2 5 7 4 8 < 1 9 6
7 4 8 > > 6 > 3 < 2 5
9 > 1 < 2 < 5 > 7 > 6 8
...
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following the existing code style
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).