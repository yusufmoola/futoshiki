# Product Overview

This is a Futoshiki puzzle solver application. Futoshiki is a logic puzzle where you fill a 9x9 grid with numbers 1-9, ensuring no duplicates in rows or columns, while respecting inequality constraints (>, <, ^, v) between adjacent cells.

## Key Features

- **Puzzle Parsing**: Parses puzzles from string representations of numbers, horizontal inequalities, and vertical inequalities
- **Visual Display**: Shows puzzles with inequality symbols in a readable grid format
- **Dual Solving Approaches**: 
  - Basic backtracking solver
  - Advanced constraint propagation solver for better performance
- **Solution Validation**: Ensures all Futoshiki rules are satisfied

## Input Format

The application expects three string inputs:
- Numbers: 9x9 grid with 0 for empty cells
- Horizontal inequalities: > < or 0 for no constraint
- Vertical inequalities: ^ v or 0 for no constraint