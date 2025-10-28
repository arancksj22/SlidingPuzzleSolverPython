import time
from puzzle import Puzzle, SlideDirection

def solve_puzzle_bfs(puzzle, goal_puzzle):
    """Breadth First Search - explores all states level by level"""
    start_time = time.time()
    
    open_list = []
    closed_set = {}
    goal_mapping = Puzzle.get_matrix_mapping(goal_puzzle.matrix)
    cur_puzzle = puzzle
    
    while not goal_puzzle.is_equal_to_puzzle(cur_puzzle):
        closed_set[cur_puzzle.to_string()] = 1
        
        neighboring_states = cur_puzzle.generate_neighbors(goal_mapping)
        for neighbor in neighboring_states:
            # Only explore new states
            if neighbor.to_string() not in closed_set:
                neighbor.came_from = cur_puzzle
                open_list.append(neighbor)
        
        # Check if we have any states to explore
        if not open_list:
            # No solution found
            end_time = time.time()
            return {
                'solution_puzzle': None,
                'runtime_ms': (end_time - start_time) * 1000,
                'max_puzzles_in_memory': len(closed_set)
            }
        
        cur_puzzle = open_list.pop(0)
    
    end_time = time.time()
    return {
        'solution_puzzle': cur_puzzle,
        'runtime_ms': (end_time - start_time) * 1000,
        'max_puzzles_in_memory': len(closed_set) + len(open_list)
    }

def priority_enqueue(open_list, puzzle, cost):
    """Make open list a priority queue by inserting elements in order"""
    for i in range(len(open_list)):
        if open_list[i]['cost'] > cost:
            open_list.insert(i, {'puzzle': puzzle, 'cost': cost})
            return
    # Puzzle cost is greater than all others, add to end
    open_list.append({'puzzle': puzzle, 'cost': cost})

def solve_puzzle_astar(puzzle, goal_puzzle):
    """A* algorithm - uses both cost from start (g) and heuristic (h)"""
    start_time = time.time()
    
    open_list = []
    closed_set = {}
    goal_mapping = Puzzle.get_matrix_mapping(goal_puzzle.matrix)
    puzzle.update_manhattan_sum(goal_mapping)
    priority_enqueue(open_list, puzzle, puzzle.manhattan_sum)
    
    cur_puzzle = puzzle
    while not goal_puzzle.is_equal_to_puzzle(cur_puzzle):
        closed_set[cur_puzzle.to_string()] = 1
        
        neighboring_states = cur_puzzle.generate_neighbors(goal_mapping)
        cost_to_neighbor = cur_puzzle.cost_from_start + 1
        
        for neighbor in neighboring_states:
            # If on closed list, don't explore that path again
            if neighbor.to_string() in closed_set:
                continue
            
            # If on the open list, check if we found a better way
            open_neighbor_index = -1
            for idx, item in enumerate(open_list):
                if item['puzzle'].is_equal_to_puzzle(neighbor):
                    open_neighbor_index = idx
                    break
            
            if open_neighbor_index != -1:
                puzzle_to_maybe_update = open_list[open_neighbor_index]['puzzle']
                if puzzle_to_maybe_update.cost_from_start > cost_to_neighbor:
                    # Remove from queue to re-enqueue with new cost
                    open_list.pop(open_neighbor_index)
                    
                    neighbor.came_from = cur_puzzle
                    neighbor.update_manhattan_sum(goal_mapping)
                    neighbor.cost_from_start = cost_to_neighbor
                    priority_enqueue(open_list, neighbor, neighbor.manhattan_sum + neighbor.cost_from_start)
            else:
                # Add to open list for further exploration
                neighbor.came_from = cur_puzzle
                neighbor.update_manhattan_sum(goal_mapping)
                neighbor.cost_from_start = cost_to_neighbor
                priority_enqueue(open_list, neighbor, neighbor.manhattan_sum + neighbor.cost_from_start)
        
        # Check if we have any states to explore
        if not open_list:
            # No solution found
            end_time = time.time()
            return {
                'solution_puzzle': None,
                'runtime_ms': (end_time - start_time) * 1000,
                'max_puzzles_in_memory': len(closed_set)
            }
        
        # Get front of queue/lowest cost un-explored puzzle state
        cur_puzzle = open_list.pop(0)['puzzle']
    
    end_time = time.time()
    return {
        'solution_puzzle': cur_puzzle,
        'runtime_ms': (end_time - start_time) * 1000,
        'max_puzzles_in_memory': len(closed_set) + len(open_list)
    }


def solve_puzzle_gbfs(puzzle, goal_puzzle):
    """Greedy Best-First Search - uses only heuristic (h), ignores cost"""
    start_time = time.time()
    
    open_list = []
    closed_set = {}
    goal_mapping = Puzzle.get_matrix_mapping(goal_puzzle.matrix)
    puzzle.update_manhattan_sum(goal_mapping)
    priority_enqueue(open_list, puzzle, puzzle.manhattan_sum)
    
    cur_puzzle = puzzle
    while not goal_puzzle.is_equal_to_puzzle(cur_puzzle):
        closed_set[cur_puzzle.to_string()] = 1
        
        neighboring_states = cur_puzzle.generate_neighbors(goal_mapping)
        
        for neighbor in neighboring_states:
            # If on closed list, don't explore that path again
            if neighbor.to_string() in closed_set:
                continue
            
            # Check if already in open list
            already_in_open = False
            for item in open_list:
                if item['puzzle'].is_equal_to_puzzle(neighbor):
                    already_in_open = True
                    break
            
            if not already_in_open:
                neighbor.came_from = cur_puzzle
                neighbor.update_manhattan_sum(goal_mapping)
                # GBFS uses only heuristic, not cost from start
                priority_enqueue(open_list, neighbor, neighbor.manhattan_sum)
        
        # Check if we have any states to explore
        if not open_list:
            # No solution found
            end_time = time.time()
            return {
                'solution_puzzle': None,
                'runtime_ms': (end_time - start_time) * 1000,
                'max_puzzles_in_memory': len(closed_set)
            }
        
        # Get front of queue/lowest heuristic value
        cur_puzzle = open_list.pop(0)['puzzle']
    
    end_time = time.time()
    return {
        'solution_puzzle': cur_puzzle,
        'runtime_ms': (end_time - start_time) * 1000,
        'max_puzzles_in_memory': len(closed_set) + len(open_list)
    }

# Direction mapping for building solution moves
DIRECTION_NAMES = {
    SlideDirection.INITIAL: "INITIAL",
    SlideDirection.UP: "UP",
    SlideDirection.DOWN: "DOWN",
    SlideDirection.LEFT: "LEFT",
    SlideDirection.RIGHT: "RIGHT"
}

def get_solution_moves(solution_puzzle):
    """Build move list from puzzle state working backwards"""
    if solution_puzzle is None:
        return []
    
    solution_moves = []
    current = solution_puzzle
    
    while current and current.last_slide_direction != SlideDirection.INITIAL:
        solution_moves.append(DIRECTION_NAMES[current.last_slide_direction])
        current = current.came_from
    
    # Started from end to finish, so reverse moves
    solution_moves.reverse()
    return solution_moves

