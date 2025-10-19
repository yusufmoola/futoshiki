import cv2
import numpy as np
from typing import List, Tuple
import copy

class FutoshikiPuzzle:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]  # Fixed initialization
        self.inequalities = []

    def parse_puzzle(self, numbers: str, horizontals: str, verticals: str):
        """
        Parse the puzzle from three strings:
        - numbers: List of numbers (0 or empty for blank), row by row
        - horizontals: List of horizontal inequalities (>, <, or - for none)
        - verticals: List of vertical inequalities (v, ^, or - for none)
        """
        # Parse numbers
        numbers = numbers.replace(" ", "").replace("\n", "")
        for i in range(9):
            for j in range(9):
                idx = i * 9 + j
                if idx < len(numbers) and numbers[idx].isdigit():
                    self.grid[i][j] = int(numbers[idx])

        # Parse horizontal inequalities
        horizontals = horizontals.replace(" ", "").replace("\n", "")
        for i in range(9):
            for j in range(8):
                idx = i * 8 + j
                if idx < len(horizontals):
                    if horizontals[idx] == '>':
                        self.inequalities.append((i, j, 'horizontal', True))
                    elif horizontals[idx] == '<':
                        self.inequalities.append((i, j, 'horizontal', False))

        # Parse vertical inequalities
        verticals = verticals.replace(" ", "").replace("\n", "")
        for i in range(8):
            for j in range(9):
                idx = i * 9 + j
                if idx < len(verticals):
                    if verticals[idx] == 'v':
                        self.inequalities.append((i, j, 'vertical', True))
                    elif verticals[idx] == '^':
                        self.inequalities.append((i, j, 'vertical', False))

    def print_puzzle(self):
        """Print the current state of the puzzle with <>^v symbols"""
        print("\n=== Current Puzzle State ===")
        
        # Create a larger grid to accommodate inequality signs
        visual_grid = [[' ' for _ in range(17)] for _ in range(17)]
        
        # Fill in numbers
        for i in range(9):
            for j in range(9):
                visual_grid[i*2][j*2] = str(self.grid[i][j]) if self.grid[i][j] != 0 else '□'
        
        # Fill in horizontal inequalities
        for i, j, dir_type, is_greater in self.inequalities:
            if dir_type == 'horizontal':
                visual_grid[i*2][j*2 + 1] = '>' if is_greater else '<'
        
        # Fill in vertical inequalities
        for i, j, dir_type, is_greater in self.inequalities:
            if dir_type == 'vertical':
                visual_grid[i*2 + 1][j*2] = 'v' if is_greater else '^'
        
        # Print the visual grid
        print("Numbers and inequalities:")
        for row in visual_grid:
            print(' '.join(cell for cell in row))

        print(f"\nTotal numbers: {sum(1 for row in self.grid for num in row if num != 0)}")
        print(f"Total inequalities: {len(self.inequalities)}")
        print("========================\n")


# 2. Solver Implementation
class FutoshikiSolver:
    def __init__(self, grid: List[List[int]], inequalities: List[Tuple]):
        self.grid = grid
        self.inequalities = inequalities
        self.size = 9
        
    def is_valid(self, num: int, pos: Tuple[int, int]) -> bool:
        row, col = pos
        
        # Check row
        for x in range(self.size):
            if self.grid[row][x] == num and col != x:
                return False
                
        # Check column
        for x in range(self.size):
            if self.grid[x][col] == num and row != x:
                return False
        
        # Check inequalities
        for r, c, direction, greater_than in self.inequalities:
            if r == row and c == col:
                if direction == 'horizontal':
                    if greater_than:
                        if c + 1 < self.size and self.grid[r][c + 1] != 0:
                            if num <= self.grid[r][c + 1]:
                                return False
                    else:
                        if c + 1 < self.size and self.grid[r][c + 1] != 0:
                            if num >= self.grid[r][c + 1]:
                                return False
                
                elif direction == 'vertical':
                    if greater_than:
                        if r + 1 < self.size and self.grid[r + 1][c] != 0:
                            if num <= self.grid[r + 1][c]:
                                return False
                    else:
                        if r + 1 < self.size and self.grid[r + 1][c] != 0:
                            if num >= self.grid[r + 1][c]:
                                return False
        
        return True

    def find_empty(self) -> Tuple[int, int]:
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

    def solve(self) -> bool:
        find = self.find_empty()
        if not find:
            return True
            
        row, col = find
        
        for num in range(1, self.size + 1):
            if self.is_valid(num, (row, col)):
                self.grid[row][col] = num
                
                if self.solve():
                    return True
                    
                self.grid[row][col] = 0
                
        return False

#variation
class FutoshikiConstraintSolver:
    def __init__(self, grid: List[List[int]], inequalities: List[Tuple]):
        self.grid = [row[:] for row in grid]
        self.inequalities = inequalities
        self.size = 9
        # Initialize candidates for each cell: if cell has a number, candidate set has only that number
        # otherwise it has all possible numbers 1-9
        self.candidates = [[{grid[i][j]} if grid[i][j] != 0 else set(range(1, 10)) 
                          for j in range(9)] for i in range(9)]
        
    def solve(self):
        # Initial constraint propagation
        self.propagate_constraints()
        
        # If puzzle not solved, use backtracking with reduced candidate sets
        if not self.is_solved():
            return self.backtrack()
        return True
    
    def propagate_constraints(self):
        changed = True
        while changed:
            changed = False
            # Apply row and column constraints
            for i in range(self.size):
                for j in range(self.size):
                    if len(self.candidates[i][j]) > 1:
                        changed |= self.apply_row_column_constraints(i, j)
            
            # Apply inequality constraints
            for row, col, direction, is_greater in self.inequalities:
                changed |= self.apply_inequality_constraint(row, col, direction, is_greater)
            
            # Look for single candidates in rows/columns
            for i in range(self.size):
                changed |= self.find_unique_candidates_in_row(i)
                changed |= self.find_unique_candidates_in_column(i)
        return True
    
    def apply_row_column_constraints(self, row, col):
        changed = False
        # Remove numbers that appear in the same row
        for j in range(self.size):
            if j != col and len(self.candidates[row][j]) == 1:
                value = next(iter(self.candidates[row][j]))
                if value in self.candidates[row][col]:
                    self.candidates[row][col].remove(value)
                    changed = True
        
        # Remove numbers that appear in the same column
        for i in range(self.size):
            if i != row and len(self.candidates[i][col]) == 1:
                value = next(iter(self.candidates[i][col]))
                if value in self.candidates[row][col]:
                    self.candidates[row][col].remove(value)
                    changed = True
        
        return changed
    
    def apply_inequality_constraint(self, row, col, direction, is_greater):
        changed = False
        if direction == 'horizontal':
            if col + 1 >= self.size:  # Skip if there's no right cell
                return False
                
            left_candidates = self.candidates[row][col]
            right_candidates = self.candidates[row][col + 1]
            
            # Skip if either set is empty
            if not left_candidates or not right_candidates:
                return False
                
            if is_greater:  # >
                # Remove values from left cell that are <= any definite value in right cell
                min_right = min(right_candidates)
                changed |= self.remove_values_from_set(
                    left_candidates,
                    {x for x in range(1, min_right + 1)}
                )
                
                # Remove values from right cell that are >= any definite value in left cell
                max_left = max(left_candidates)
                changed |= self.remove_values_from_set(
                    right_candidates,
                    {x for x in range(max_left, 10)}
                )
            else:  # <
                max_right = max(right_candidates)
                changed |= self.remove_values_from_set(
                    left_candidates,
                    {x for x in range(max_right, 10)}
                )
                min_left = min(left_candidates)
                changed |= self.remove_values_from_set(
                    right_candidates,
                    {x for x in range(1, min_left + 1)}
                )
        
        elif direction == 'vertical':
            if row + 1 >= self.size:  # Skip if there's no bottom cell
                return False
                
            top_candidates = self.candidates[row][col]
            bottom_candidates = self.candidates[row + 1][col]
            
            # Skip if either set is empty
            if not top_candidates or not bottom_candidates:
                return False
                
            if is_greater:  # v
                min_bottom = min(bottom_candidates)
                changed |= self.remove_values_from_set(
                    top_candidates,
                    {x for x in range(1, min_bottom + 1)}
                )
                max_top = max(top_candidates)
                changed |= self.remove_values_from_set(
                    bottom_candidates,
                    {x for x in range(max_top, 10)}
                )
            else:  # ^
                max_bottom = max(bottom_candidates)
                changed |= self.remove_values_from_set(
                    top_candidates,
                    {x for x in range(max_bottom, 10)}
                )
                min_top = min(top_candidates)
                changed |= self.remove_values_from_set(
                    bottom_candidates,
                    {x for x in range(1, min_top + 1)}
                )
        
        return changed
    
    def find_unique_candidates_in_row(self, row):
        changed = False
        # For each number 1-9, check if it appears as a candidate in only one cell
        for num in range(1, 10):
            appearances = []
            for col in range(self.size):
                if num in self.candidates[row][col]:
                    appearances.append(col)
            if len(appearances) == 1:  # If number appears in only one cell
                col = appearances[0]   # Get the first (and only) column number from the list
                if len(self.candidates[row][col]) > 1:
                    self.candidates[row][col] = {num}
                    changed = True
        return changed

    def find_unique_candidates_in_column(self, col):
        changed = False
        for num in range(1, 10):
            appearances = []
            for row in range(self.size):
                if num in self.candidates[row][col]:
                    appearances.append(row)
            if len(appearances) == 1:  # If number appears in only one cell
                row = appearances[0]   # Get the first (and only) row number from the list
                if len(self.candidates[row][col]) > 1:
                    self.candidates[row][col] = {num}
                    changed = True
        return changed
    
    @staticmethod
    def remove_values_from_set(target_set, values_to_remove):
        initial_len = len(target_set)
        target_set -= values_to_remove
        return initial_len != len(target_set)
    
    def is_solved(self):
        return all(len(self.candidates[i][j]) == 1 
                  for i in range(self.size) 
                  for j in range(self.size))
    
    def backtrack(self):
        if self.is_solved():
            # Transfer candidates to grid
            for i in range(self.size):
                for j in range(self.size):
                    self.grid[i][j] = next(iter(self.candidates[i][j]))
            return True
            
        # Find cell with fewest candidates
        min_candidates = 10
        min_pos = None
        for i in range(self.size):
            for j in range(self.size):
                if len(self.candidates[i][j]) > 1 and len(self.candidates[i][j]) < min_candidates:
                    min_candidates = len(self.candidates[i][j])
                    min_pos = (i, j)
        
        row, col = min_pos
        candidates = sorted(self.candidates[row][col])
        
        # Try each candidate
        for num in candidates:
            old_candidates = [row[:] for row in self.candidates]
            self.candidates[row][col] = {num}
            
            if self.propagate_constraints() and self.backtrack():
                return True
                
            self.candidates = old_candidates
        
        return False

#Display Result
def display_result(solved_grid: List[List[int]], inequalities: List[Tuple]):
    print("\n=== Solved Puzzle ===")
    
    # Create a larger grid to accommodate inequality signs
    visual_grid = [[' ' for _ in range(17)] for _ in range(17)]
    
    # Fill in solved numbers
    for i in range(9):
        for j in range(9):
            visual_grid[i*2][j*2] = str(solved_grid[i][j])
    
    # Fill in horizontal inequalities
    for i, j, dir_type, is_greater in inequalities:
        if dir_type == 'horizontal':
            visual_grid[i*2][j*2 + 1] = '>' if is_greater else '<'
    
    # Fill in vertical inequalities
    for i, j, dir_type, is_greater in inequalities:
        if dir_type == 'vertical':
            visual_grid[i*2 + 1][j*2] = 'v' if is_greater else '^'
    
    # Print the visual grid
    print("Solution with inequalities:")
    for row in visual_grid:
        print(' '.join(cell for cell in row))
    print("========================\n")


# Update the main function to use the new display_result
def main():
    #Sample 1:
    numbers = """
    0 0 0 0 0 8 1 0 0
    7 0 8 0 0 6 3 0 2
    9 1 2 0 0 0 0 6 0
    1 4 7 0 9 0 5 0 0
    0 0 0 2 0 9 0 0 1
    8 6 0 5 0 0 9 1 7
    0 0 0 0 6 0 2 0 0
    0 0 1 0 5 0 0 0 9
    6 0 4 0 0 0 0 2 0
    """

    horizontals = """
    > 0 0 < 0 0 < >
    0 0 > > 0 > < >
    > < < > < < > >
    0 0 0 < > < > <
    < 0 0 0 0 0 0 >
    > 0 < > 0 0 0 0
    < < 0 0 < > < 0
    0 0 0 0 > 0 0 0
    0 < < 0 > 0 0 0
    """
    
    verticals = """
    0 0 ^ ^ v 0 ^ v v
    ^ v 0 0 ^ 0 0 ^ ^
    v 0 0 0 0 0 v 0 0
    ^ ^ 0 v v 0 0 ^ 0
    0 0 v ^ 0 v ^ v 0
    0 0 ^ v ^ 0 0 ^ 0
    0 0 v ^ v 0 ^ v 0
    0 v 0 ^ 0 0 ^ v 0
    """

    puzzle = FutoshikiPuzzle()
    puzzle.parse_puzzle(numbers, horizontals, verticals)
    puzzle.print_puzzle()
    
    # Now we can use the existing solver with puzzle.grid and puzzle.inequalities
    solver = FutoshikiSolver(puzzle.grid, puzzle.inequalities)
    #solver = FutoshikiConstraintSolver(puzzle.grid, puzzle.inequalities)
    # After solving the puzzle
    if solver.solve():
        display_result(solver.grid, puzzle.inequalities)
    else:
        print("\nNo solution exists")


if __name__ == "__main__":
    main()

