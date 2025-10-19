# Project Structure

## File Organization

```
.
├── main.py                    # Main application entry point
├── futoshiki_puzzle.jpg       # Sample puzzle image (reference)
├── .vscode/
│   └── settings.json         # VS Code configuration
└── .kiro/
    └── steering/             # AI assistant guidance files
```

## Code Architecture

### Core Classes

**`FutoshikiPuzzle`**
- Handles puzzle representation and parsing
- Methods: `parse_puzzle()`, `print_puzzle()`
- Stores grid state and inequality constraints

**`FutoshikiSolver`** (Basic)
- Simple backtracking algorithm
- Methods: `solve()`, `is_valid()`, `find_empty()`

**`FutoshikiConstraintSolver`** (Advanced)
- Constraint propagation with backtracking
- Methods: `solve()`, `propagate_constraints()`, `backtrack()`
- More efficient for complex puzzles

### Function Organization

**Utility Functions**
- `display_result()` - Formats and prints solved puzzles
- `main()` - Entry point with sample puzzle data

## Data Structures

- **Grid**: 9x9 2D list of integers (0 for empty cells)
- **Inequalities**: List of tuples `(row, col, direction, is_greater)`
  - `direction`: 'horizontal' or 'vertical'
  - `is_greater`: Boolean indicating > vs < or v vs ^
- **Candidates**: 2D list of sets for constraint solver

## Conventions

- All puzzle coordinates use (row, col) indexing starting from 0
- Empty cells represented as 0
- Inequality symbols: `>`, `<`, `^`, `v` (or 0 for none)