import time
from puzzle import Puzzle, SlideDirection

def solve_puzzle_strategically(puzzle, goal_puzzle):
    """
    Strategic algorithm for solving sliding puzzles
    Solves rows and columns systematically until reaching a 2x2
    """
    start_time = time.time()
    
    # Check if already solved
    if goal_puzzle.is_equal_to_puzzle(puzzle):
        return {
            'solution_puzzle': puzzle,
            'runtime_ms': 0,
            'solution_moves': [],
            'max_puzzles_in_memory': 1
        }
    
    solution_moves = []
    goal_matrix = goal_puzzle.matrix
    goal_mapping = Puzzle.get_matrix_mapping(goal_matrix)
    
    # Set state for effective bounds of unsolved puzzle
    puzzle.top_row_progress = 0
    puzzle.left_col_progress = 0
    puzzle.bot_row_progress = puzzle.rows - 1
    puzzle.right_col_progress = puzzle.cols - 1
    
    # Start by solving rows top->bottom and columns left->right
    puzzle.row_in_progress = 0
    puzzle.col_in_progress = 0
    puzzle.solving_row_top_down = True
    puzzle.solving_col_left_right = True
    
    while not goal_puzzle.is_equal_to_puzzle(puzzle):
        # Solve rows while more than 2 unsolved rows
        while more_than_two_unsolved_rows(puzzle) and more_unsolved_rows_than_cols(puzzle):
            puzzle.solving_row = True
            
            if row_finished_and_not_in_goal_row(goal_puzzle, puzzle):
                # Move to next row
                if puzzle.solving_row_top_down:
                    puzzle.top_row_progress += 1
                    puzzle.row_in_progress = puzzle.top_row_progress
                else:
                    puzzle.bot_row_progress -= 1
                    puzzle.row_in_progress = puzzle.bot_row_progress
            else:
                # Solve current row
                if puzzle.solving_row_top_down:
                    puzzle.row_progress_col = puzzle.left_col_progress
                else:
                    puzzle.row_progress_col = puzzle.right_col_progress
                
                while not Puzzle.is_row_equal(goal_puzzle, puzzle, puzzle.row_in_progress):
                    goal_value = goal_matrix[puzzle.row_in_progress][puzzle.row_progress_col]
                    move_tile(puzzle, goal_value, puzzle.row_in_progress, puzzle.row_progress_col, solution_moves)
                    
                    if puzzle.solving_row_top_down:
                        puzzle.row_progress_col += 1
                    else:
                        puzzle.row_progress_col -= 1
        
        # Solve columns while more unsolved columns than rows
        while more_than_two_unsolved_cols(puzzle) and more_unsolved_cols_than_rows(puzzle):
            puzzle.solving_row = False
            
            if col_finished_and_not_in_goal_col(goal_puzzle, puzzle):
                # Move to next column
                if puzzle.solving_col_left_right:
                    puzzle.left_col_progress += 1
                    puzzle.col_in_progress = puzzle.left_col_progress
                else:
                    puzzle.right_col_progress -= 1
                    puzzle.col_in_progress = puzzle.right_col_progress
            else:
                # Solve current column
                if puzzle.solving_col_left_right:
                    puzzle.col_progress_row = puzzle.top_row_progress
                else:
                    puzzle.col_progress_row = puzzle.bot_row_progress
                
                while not Puzzle.is_col_equal(goal_puzzle, puzzle, puzzle.col_in_progress):
                    goal_value = goal_matrix[puzzle.col_progress_row][puzzle.col_in_progress]
                    move_tile(puzzle, goal_value, puzzle.col_progress_row, puzzle.col_in_progress, solution_moves)
                    
                    if puzzle.solving_col_left_right:
                        puzzle.col_progress_row += 1
                    else:
                        puzzle.col_progress_row -= 1
        
        # When down to 2x2, rotate blank until goal state
        if unsolved_puzzle_is_two_by_two(puzzle):
            slide_vertically = True
            while not goal_puzzle.is_equal_to_puzzle(puzzle):
                if slide_vertically:
                    if puzzle.can_slide_up():
                        puzzle.slide_up()
                        solution_moves.append("UP")
                    elif puzzle.can_slide_down():
                        puzzle.slide_down()
                        solution_moves.append("DOWN")
                    slide_vertically = False
                else:
                    if puzzle.can_slide_left():
                        puzzle.slide_left()
                        solution_moves.append("LEFT")
                    elif puzzle.can_slide_right():
                        puzzle.slide_right()
                        solution_moves.append("RIGHT")
                    slide_vertically = True
    
    end_time = time.time()
    return {
        'solution_puzzle': puzzle,
        'runtime_ms': (end_time - start_time) * 1000,
        'solution_moves': solution_moves,
        'max_puzzles_in_memory': 1
    }

def move_tile(puzzle, value, goal_row, goal_col, solution_moves):
    """Move tile into its goal state"""
    matrix_mapping = Puzzle.get_matrix_mapping(puzzle.matrix)
    value_row = matrix_mapping[value]['row']
    value_col = matrix_mapping[value]['col']
    
    # Already in correct position
    if value_row == goal_row and value_col == goal_col:
        return
    
    tile = {
        'value': value,
        'row': value_row,
        'col': value_col,
        'goal_row': goal_row,
        'goal_col': goal_col
    }
    
    if puzzle.solving_row:
        # Position column first, then row
        while tile['col'] > goal_col:
            move_tile_left(puzzle, tile, solution_moves)
            tile['col'] -= 1
        
        while tile['col'] < goal_col:
            move_tile_right(puzzle, tile, solution_moves)
            tile['col'] += 1
        
        while tile['row'] > goal_row:
            move_tile_up(puzzle, tile, solution_moves)
            tile['row'] -= 1
        
        while tile['row'] < goal_row:
            move_tile_down(puzzle, tile, solution_moves)
            tile['row'] += 1
    else:
        # Position row first, then column
        while tile['row'] > goal_row:
            move_tile_up(puzzle, tile, solution_moves)
            tile['row'] -= 1
        
        while tile['row'] < goal_row:
            move_tile_down(puzzle, tile, solution_moves)
            tile['row'] += 1
        
        while tile['col'] > goal_col:
            move_tile_left(puzzle, tile, solution_moves)
            tile['col'] -= 1
        
        while tile['col'] < goal_col:
            move_tile_right(puzzle, tile, solution_moves)
            tile['col'] += 1

def move_tile_left(puzzle, tile, solution_moves):
    """Move tile one position left"""
    # Blank is to the right of value in same row
    if puzzle.blank_col > tile['col'] and tile['row'] == puzzle.blank_row:
        move_blank_left_or_right(puzzle, solution_moves)
    
    # Move blank to left of tile
    move_blank_to_col(puzzle, tile['col'] - 1, solution_moves)
    move_blank_to_row(puzzle, tile['row'], solution_moves)
    puzzle.slide_right()
    solution_moves.append("RIGHT")

def move_tile_right(puzzle, tile, solution_moves):
    """Move tile one position right"""
    # Blank is to the left of value in same row
    if puzzle.blank_col < tile['col'] and tile['row'] == puzzle.blank_row:
        move_blank_left_or_right(puzzle, solution_moves)
    
    # Move blank to right of tile
    move_blank_to_col(puzzle, tile['col'] + 1, solution_moves)
    move_blank_to_row(puzzle, tile['row'], solution_moves)
    puzzle.slide_left()
    solution_moves.append("LEFT")

def move_tile_up(puzzle, tile, solution_moves):
    """Move tile one position up"""
    # Blank is below the value
    if puzzle.blank_row > tile['row'] and puzzle.blank_col == tile['col']:
        move_blank_left_or_right(puzzle, solution_moves)
    
    # Move blank above the value
    move_blank_to_row(puzzle, tile['row'] - 1, solution_moves)
    move_blank_to_col(puzzle, tile['col'], solution_moves)
    puzzle.slide_down()
    solution_moves.append("DOWN")

def move_tile_down(puzzle, tile, solution_moves):
    """Move tile one position down"""
    # Blank is above the value
    if puzzle.blank_row < tile['row'] and puzzle.blank_col == tile['col']:
        move_blank_left_or_right(puzzle, solution_moves)
    
    # Move blank below the value
    move_blank_to_row(puzzle, tile['row'] + 1, solution_moves)
    move_blank_to_col(puzzle, tile['col'], solution_moves)
    puzzle.slide_up()
    solution_moves.append("UP")

def move_blank_left_or_right(puzzle, solution_moves):
    """Helper to move blank left or right"""
    if puzzle.can_slide_left():
        puzzle.slide_left()
        solution_moves.append("LEFT")
    elif puzzle.can_slide_right():
        puzzle.slide_right()
        solution_moves.append("RIGHT")

def move_blank_to_col(puzzle, target_col, solution_moves):
    """Loop until blank is in target column"""
    while puzzle.blank_col != target_col:
        if puzzle.blank_col < target_col:
            puzzle.slide_right()
            solution_moves.append("RIGHT")
        else:
            puzzle.slide_left()
            solution_moves.append("LEFT")

def move_blank_to_row(puzzle, target_row, solution_moves):
    """Loop until blank is in target row"""
    while puzzle.blank_row != target_row:
        if puzzle.blank_row < target_row:
            puzzle.slide_down()
            solution_moves.append("DOWN")
        else:
            puzzle.slide_up()
            solution_moves.append("UP")

# Helper conditions
def more_than_two_unsolved_rows(puzzle):
    return puzzle.bot_row_progress + 1 - puzzle.top_row_progress > 2

def more_than_two_unsolved_cols(puzzle):
    return puzzle.right_col_progress + 1 - puzzle.left_col_progress > 2

def more_unsolved_rows_than_cols(puzzle):
    return puzzle.bot_row_progress - puzzle.top_row_progress + 1 >= puzzle.right_col_progress + 1 - puzzle.left_col_progress

def more_unsolved_cols_than_rows(puzzle):
    return puzzle.right_col_progress + 1 - puzzle.left_col_progress > puzzle.bot_row_progress + 1 - puzzle.top_row_progress

def col_finished_and_not_in_goal_col(goal_puzzle, puzzle):
    return Puzzle.is_col_equal(goal_puzzle, puzzle, puzzle.col_in_progress) and puzzle.col_in_progress != goal_puzzle.blank_col

def row_finished_and_not_in_goal_row(goal_puzzle, puzzle):
    return Puzzle.is_row_equal(goal_puzzle, puzzle, puzzle.row_in_progress) and puzzle.row_in_progress != goal_puzzle.blank_row

def unsolved_puzzle_is_two_by_two(puzzle):
    return (puzzle.bot_row_progress + 1 - puzzle.top_row_progress == 2 and 
            puzzle.right_col_progress + 1 - puzzle.left_col_progress == 2)
