from copy import deepcopy


class SudokuCSP:
    def __init__(self, puzzle):
        self.puzzle = puzzle  # The initial Sudoku puzzle
        self.nodes_generated = 0    # Initialize the node counter

    def is_complete(self, assignment):
        return all(assignment[row][col] != 0 for row in range(9) for col in range(9))

    # static ordering
    def select_unassigned_mode2(self, assignment):
        for row in range(9):
            for col in range(9):
                if assignment[row][col] == 0:
                    return row, col
        return None

    # MRV heuristics
    def select_unassigned_mode3(self, assignment):
        min_remaining_values = 10  # Larger than the largest domain size
        selected_var = None

        for row in range(9):
            for col in range(9):
                if assignment[row][col] == 0:
                    domain = self.order_domain_values((row, col), assignment)
                    if len(domain) < min_remaining_values:
                        min_remaining_values = len(domain)
                        selected_var = (row, col)

        return selected_var

    def order_domain_values(self, var, assignment):
        row, col = var
        valid_values = []

        # Iterate through the values from 1 to 9
        for value in range(1, 10):
            # Check if the current value is consistent with the assignment
            if self.is_consistent(assignment, row, col, value):
                # If it is, add the value to the list of valid values
                valid_values.append(value)

        # Return the list of valid values
        return valid_values

    def is_consistent(self, assignment, row, col, value):
        # Check row and column
        for i in range(9):
            if assignment[row][i] == value or assignment[i][col] == value:
                return False

        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if assignment[i][j] == value:
                    return False
        return True

    def backtrack_mode2(self, assignment):
        if self.is_complete(assignment):
            return assignment

        var = self.select_unassigned_mode2(assignment)
        if var is None:
            # No unassigned cells left, but puzzle is not complete.
            return None

        row, col = var
        for value in range(1, 10):  # Try all possible values from 1 to 9
            self.nodes_generated += 1
            if self.is_consistent(assignment, row, col, value):
                assignment[row][col] = value  # Assign value if consistent
                result = self.backtrack_mode2(assignment)
                if result is not None:
                    return result  # Puzzle solved successfully

                # If no solution was found after assigning 'value', reset cell and try next value
                assignment[row][col] = 0

        return None  # Trigger backtracking as no value led to a solution

    def initialize_domains(self, puzzle):
        domains = {}    # dictionary
        for row in range(9):
            for col in range(9):
                if puzzle[row][col] == 0:
                    # If the cell is unassigned, its domain is all digits from 1 to 9
                    domains[(row, col)] = set(range(1, 10))
                else:
                    # If the cell is assigned, its domain is a set containing its value
                    domains[(row, col)] = {puzzle[row][col]}

        # Now, reduce the domains based on existing assignments in the puzzle
        for row in range(9):
            for col in range(9):
                if puzzle[row][col] != 0:
                    # Exclude the value from the domains of all cells in the same row, column, and box
                    self.exclude_from_domain(
                        domains, row, col, puzzle[row][col])

        return domains

    def exclude_from_domain(self, domains, row, col, value):
        # Exclude 'value' from the domains of cells in the same row
        for c in range(9):
            if c != col:
                domains[(row, c)].discard(value)

        # Exclude 'value' from the domains of cells in the same column
        for r in range(9):
            if r != row:
                domains[(r, col)].discard(value)

        # Exclude 'value' from the domains of cells in the same 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if (r, c) != (row, col):
                    domains[(r, c)].discard(value)

    def forward_check(self, assignment, var, value, domains):
        row, col = var
        affected_cells = set()  # same row, col, and sub-grid

        # Check row and column
        for i in range(9):
            if i != col and assignment[row][i] == 0:
                affected_cells.add((row, i))
            if i != row and assignment[i][col] == 0:
                affected_cells.add((i, col))

        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if (i, j) != (row, col) and assignment[i][j] == 0:
                    affected_cells.add((i, j))

        # Update domains
        for cell in affected_cells:
            r, c = cell
            if value in domains[(r, c)]:    # value is an assigned value
                domains[(r, c)].remove(value)
                if len(domains[(r, c)]) == 0:
                    return False  # Domain wipeout

        return True

    def backtrack_mode3(self, assignment, domains):
        if self.is_complete(assignment):
            return assignment
        # self.nodes_generated += 1
        var = self.select_unassigned_mode3(assignment)
        if var is not None:
            row, col = var
            for value in self.order_domain_values(var, assignment):
                self.nodes_generated += 1
                if self.is_consistent(assignment, row, col, value):
                    assignment[row][col] = value
                    # Make a copy of the current domains
                    domains_copy = deepcopy(domains)
                    if self.forward_check(assignment, var, value, domains_copy):
                        result = self.backtrack_mode3(assignment, domains_copy)
                        if result is not None:
                            return result
                    assignment[row][col] = 0  # Unassign the value

        return None

    def brute_force_search(self, puzzle):
        empty_cells = self.get_empty_cells(puzzle)
        num_empty = len(empty_cells)
        self.nodes_generated += 1

        # Start with the lowest possible combination
        combo = [1] * num_empty

        while combo:
            # Assign current combination to the puzzle
            for idx, (row, col) in enumerate(empty_cells):
                puzzle[row][col] = combo[idx]

            # self.display_puzzle(puzzle) # debug

            if self.is_puzzle_valid(puzzle):
                return puzzle

            # Generate next combination
            combo = self.get_next_combo(combo)

            # Reset empty cells after each trial
            for row, col in empty_cells:
                puzzle[row][col] = 0

        return None

    def get_empty_cells(self, puzzle):
        """Return a list of coordinates of empty cells in the puzzle."""
        return [(row, col) for row in range(9) for col in range(9) if puzzle[row][col] == 0]

    def get_next_combo(self, combo):
        """Generates the next combination of numbers for the empty cells."""
        self.nodes_generated += 1
        idx = len(combo) - 1
        while idx >= 0:
            if combo[idx] < 9:
                combo[idx] += 1
                return combo
            combo[idx] = 1  # Reset this position
            self.nodes_generated += 1
            idx -= 1  # Move to the previous position

        # If all positions were reset, we've exhausted all combinations
        return None

    def is_puzzle_valid(self, puzzle):
        # Check each row, column, and 3x3 box for validity
        for i in range(9):
            if not self.is_row_valid(puzzle, i) or not self.is_col_valid(puzzle, i):
                return False

        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                if not self.is_box_valid(puzzle, row, col):
                    return False

        return True

    def is_row_valid(self, puzzle, row):
        seen = set()
        for num in puzzle[row]:
            if num in seen:
                return False
            if num != 0:
                seen.add(num)
        return True

    def is_col_valid(self, puzzle, col):
        seen = set()
        for row in range(9):
            num = puzzle[row][col]
            if num in seen:
                return False
            if num != 0:
                seen.add(num)
        return True

    def is_box_valid(self, puzzle, start_row, start_col):
        seen = set()
        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                num = puzzle[row][col]
                if num in seen:
                    return False
                if num != 0:
                    seen.add(num)
        return True

    def is_puzzle_correct(self, puzzle):
        # First, check if the puzzle is completed
        if not self.is_complete(puzzle):
            return False

        # Then, check each row, column, and 3x3 box for validity
        for i in range(9):
            if not self.is_row_valid(puzzle, i) or not self.is_col_valid(puzzle, i):
                return False

        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                if not self.is_box_valid(puzzle, row, col):
                    return False

        return True

    def is_complete(self, puzzle):
        # Initialize a variable to hold the final result
        all_nonzero = True

        # Iterate through each row and column in the puzzle
        for row in range(9):
            for col in range(9):
                # Check if the current cell is zero
                if puzzle[row][col] == 0:
                    # If a zero is found, set all_nonzero to False and break out of the loop
                    all_nonzero = False
                    break

            # If a zero was found in any column, break out of the row loop
            if not all_nonzero:
                break

        # Return the result of the check
        return all_nonzero
