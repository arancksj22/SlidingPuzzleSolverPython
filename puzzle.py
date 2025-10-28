import random

class SlideDirection:
    INITIAL = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Puzzle:
    def __init__(self, rows, cols, gen_random=True, solvable=True):
        self.rows = rows
        self.cols = cols
        self.blank_row = 0
        self.blank_col = 0
        self.last_slide_direction = SlideDirection.INITIAL
        self.manhattan_sum = 0
        self.came_from = None
        self.cost_from_start = 0
        
        if gen_random:
            self.matrix = self.generate_random_puzzle(rows, cols, solvable)
            # Find blank tile position
            for row_idx in range(rows):
                for col_idx in range(cols):
                    if self.matrix[row_idx][col_idx] == 0:
                        self.blank_row = row_idx
                        self.blank_col = col_idx
                        break
        else:
            # Fill matrix with default goal state (in order tiles)
            self.matrix = [[col + row * cols + 1 for col in range(cols)] for row in range(rows)]
            # Set last tile as blank (0)
            self.matrix[rows - 1][cols - 1] = 0
            self.blank_row = rows - 1
            self.blank_col = cols - 1
    
    @staticmethod
    def from_puzzle(puzzle):
        """Create deep copy of another puzzle"""
        copy_puzzle = Puzzle(puzzle.rows, puzzle.cols, False)
        copy_puzzle.matrix = [row[:] for row in puzzle.matrix]
        copy_puzzle.blank_row = puzzle.blank_row
        copy_puzzle.blank_col = puzzle.blank_col
        copy_puzzle.manhattan_sum = puzzle.manhattan_sum
        copy_puzzle.cost_from_start = puzzle.cost_from_start
        return copy_puzzle
    
    @staticmethod
    def from_matrix(matrix):
        """Create puzzle from existing matrix"""
        puzzle = Puzzle(len(matrix), len(matrix[0]), False)
        puzzle.matrix = [row[:] for row in matrix]
        # Find blank tile
        for row in range(len(matrix)):
            for col in range(len(matrix[0])):
                if matrix[row][col] == 0:
                    puzzle.blank_row = row
                    puzzle.blank_col = col
                    return puzzle
        return puzzle
    
    @staticmethod
    def generate_random_puzzle(rows, cols, solvable):
        """Returns random puzzle with defined solvability"""
        values = list(range(rows * cols))
        
        while True:
            random.shuffle(values)
            if Puzzle.is_puzzle_solvable_1d(values, rows, cols) == solvable:
                break
        
        # Turn 1D array into puzzle matrix
        return [[values[row * cols + col] for col in range(cols)] for row in range(rows)]
    
    def can_slide_left(self):
        return self.blank_col > 0
    
    def can_slide_right(self):
        return self.blank_col < self.cols - 1
    
    def can_slide_up(self):
        return self.blank_row > 0
    
    def can_slide_down(self):
        return self.blank_row < self.rows - 1
    
    def slide_left(self):
        if not self.can_slide_left():
            return
        self.matrix[self.blank_row][self.blank_col] = self.matrix[self.blank_row][self.blank_col - 1]
        self.matrix[self.blank_row][self.blank_col - 1] = 0
        self.blank_col -= 1
    
    def slide_right(self):
        if not self.can_slide_right():
            return
        self.matrix[self.blank_row][self.blank_col] = self.matrix[self.blank_row][self.blank_col + 1]
        self.matrix[self.blank_row][self.blank_col + 1] = 0
        self.blank_col += 1
    
    def slide_up(self):
        if not self.can_slide_up():
            return
        self.matrix[self.blank_row][self.blank_col] = self.matrix[self.blank_row - 1][self.blank_col]
        self.matrix[self.blank_row - 1][self.blank_col] = 0
        self.blank_row -= 1
    
    def slide_down(self):
        if not self.can_slide_down():
            return
        self.matrix[self.blank_row][self.blank_col] = self.matrix[self.blank_row + 1][self.blank_col]
        self.matrix[self.blank_row + 1][self.blank_col] = 0
        self.blank_row += 1
    
    def update_manhattan_sum(self, goal_mapping):
        """Updates manhattan sum for this puzzle state"""
        self.manhattan_sum = sum(
            abs(row - goal_mapping[self.matrix[row][col]]['row']) + 
            abs(col - goal_mapping[self.matrix[row][col]]['col'])
            for row in range(self.rows)
            for col in range(self.cols)
            if self.matrix[row][col] != 0
        )
    
    @staticmethod
    def get_matrix_mapping(matrix):
        """Map goal state's (row, col) for each tile value"""
        return {
            matrix[row][col]: {'row': row, 'col': col}
            for row in range(len(matrix))
            for col in range(len(matrix[0]))
        }
    
    def generate_neighbors(self, goal_mapping=None):
        """Generate all valid neighboring puzzle states"""
        neighbors = []
        
        if self.can_slide_up() and self.last_slide_direction != SlideDirection.DOWN:
            neighbor = Puzzle.from_puzzle(self)
            neighbor.slide_up()
            neighbor.last_slide_direction = SlideDirection.UP
            neighbor.came_from = self
            neighbor.cost_from_start = self.cost_from_start + 1
            if goal_mapping:
                neighbor.update_manhattan_sum(goal_mapping)
            neighbors.append(neighbor)
        
        if self.can_slide_down() and self.last_slide_direction != SlideDirection.UP:
            neighbor = Puzzle.from_puzzle(self)
            neighbor.slide_down()
            neighbor.last_slide_direction = SlideDirection.DOWN
            neighbor.came_from = self
            neighbor.cost_from_start = self.cost_from_start + 1
            if goal_mapping:
                neighbor.update_manhattan_sum(goal_mapping)
            neighbors.append(neighbor)
        
        if self.can_slide_left() and self.last_slide_direction != SlideDirection.RIGHT:
            neighbor = Puzzle.from_puzzle(self)
            neighbor.slide_left()
            neighbor.last_slide_direction = SlideDirection.LEFT
            neighbor.came_from = self
            neighbor.cost_from_start = self.cost_from_start + 1
            if goal_mapping:
                neighbor.update_manhattan_sum(goal_mapping)
            neighbors.append(neighbor)
        
        if self.can_slide_right() and self.last_slide_direction != SlideDirection.LEFT:
            neighbor = Puzzle.from_puzzle(self)
            neighbor.slide_right()
            neighbor.last_slide_direction = SlideDirection.RIGHT
            neighbor.came_from = self
            neighbor.cost_from_start = self.cost_from_start + 1
            if goal_mapping:
                neighbor.update_manhattan_sum(goal_mapping)
            neighbors.append(neighbor)
        
        return neighbors
    
    def is_equal_to_puzzle(self, puzzle):
        """Check if two puzzles have the same state"""
        return all(
            self.matrix[row][col] == puzzle.matrix[row][col]
            for row in range(self.rows)
            for col in range(self.cols)
        )
    
    @staticmethod
    def is_puzzle_solvable_1d(arr, rows, cols):
        """Check if puzzle is solvable based on inversion count"""
        inversions = 0
        for i in range(len(arr)):
            if arr[i] == 0:
                blank_row = i // cols
                continue
            for j in range(i + 1, len(arr)):
                if arr[j] != 0 and arr[i] > arr[j]:
                    inversions += 1
        
        # Odd columns: Number of inversions must be even
        if cols % 2:
            return inversions % 2 == 0
        else:
            # Even columns: inversions + blank row must be odd
            return (inversions + blank_row) % 2 == 1
    
    @staticmethod
    def is_puzzle_solvable_2d(matrix):
        """Check if 2D puzzle matrix is solvable"""
        arr = [val for row in matrix for val in row]
        return Puzzle.is_puzzle_solvable_1d(arr, len(matrix), len(matrix[0]))
    
    def to_string(self):
        """Convert matrix to string for hashing"""
        return str(self.matrix)
