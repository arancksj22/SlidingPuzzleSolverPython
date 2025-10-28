import time
from puzzle import Puzzle, SlideDirection

def solve_puzzle_bfs(puzzle, goal_puzzle):
    """Breadth First Search - explores all states level by level"""
    start_time = time.time()
    
    open_list = [puzzle]
    closed_set = {puzzle.to_string()}
    goal_mapping = Puzzle.get_matrix_mapping(goal_puzzle.matrix)
    
    while open_list:
        cur_puzzle = open_list.pop(0)
        
        if goal_puzzle.is_equal_to_puzzle(cur_puzzle):
            return {
                'solution_puzzle': cur_puzzle,
                'runtime_ms': (time.time() - start_time) * 1000,
                'max_puzzles_in_memory': len(closed_set) + len(open_list)
            }
        
        for neighbor in cur_puzzle.generate_neighbors(goal_mapping):
            neighbor_str = neighbor.to_string()
            if neighbor_str not in closed_set:
                closed_set.add(neighbor_str)
                neighbor.came_from = cur_puzzle
                open_list.append(neighbor)
    
    return {
        'solution_puzzle': None,
        'runtime_ms': (time.time() - start_time) * 1000,
        'max_puzzles_in_memory': len(closed_set)
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
    
    goal_mapping = Puzzle.get_matrix_mapping(goal_puzzle.matrix)
    puzzle.update_manhattan_sum(goal_mapping)
    
    open_list = []
    priority_enqueue(open_list, puzzle, puzzle.manhattan_sum)
    closed_set = set()
    
    while open_list:
        cur_puzzle = open_list.pop(0)['puzzle']
        
        if goal_puzzle.is_equal_to_puzzle(cur_puzzle):
            return {
                'solution_puzzle': cur_puzzle,
                'runtime_ms': (time.time() - start_time) * 1000,
                'max_puzzles_in_memory': len(closed_set) + len(open_list)
            }
        
        cur_str = cur_puzzle.to_string()
        if cur_str in closed_set:
            continue
        closed_set.add(cur_str)
        
        cost_to_neighbor = cur_puzzle.cost_from_start + 1
        
        for neighbor in cur_puzzle.generate_neighbors(goal_mapping):
            neighbor_str = neighbor.to_string()
            if neighbor_str in closed_set:
                continue
            
            # Check if already in open list with higher cost
            for idx, item in enumerate(open_list):
                if item['puzzle'].is_equal_to_puzzle(neighbor):
                    if item['puzzle'].cost_from_start > cost_to_neighbor:
                        open_list.pop(idx)
                    else:
                        break
            else:
                neighbor.came_from = cur_puzzle
                neighbor.cost_from_start = cost_to_neighbor
                priority_enqueue(open_list, neighbor, neighbor.manhattan_sum + neighbor.cost_from_start)
    
    return {
        'solution_puzzle': None,
        'runtime_ms': (time.time() - start_time) * 1000,
        'max_puzzles_in_memory': len(closed_set)
    }


def solve_puzzle_gbfs(puzzle, goal_puzzle):
    """Greedy Best-First Search - uses only heuristic (h), ignores cost"""
    start_time = time.time()
    
    goal_mapping = Puzzle.get_matrix_mapping(goal_puzzle.matrix)
    puzzle.update_manhattan_sum(goal_mapping)
    
    open_list = []
    priority_enqueue(open_list, puzzle, puzzle.manhattan_sum)
    closed_set = set()
    
    while open_list:
        cur_puzzle = open_list.pop(0)['puzzle']
        
        if goal_puzzle.is_equal_to_puzzle(cur_puzzle):
            return {
                'solution_puzzle': cur_puzzle,
                'runtime_ms': (time.time() - start_time) * 1000,
                'max_puzzles_in_memory': len(closed_set) + len(open_list)
            }
        
        cur_str = cur_puzzle.to_string()
        if cur_str in closed_set:
            continue
        closed_set.add(cur_str)
        
        for neighbor in cur_puzzle.generate_neighbors(goal_mapping):
            if neighbor.to_string() not in closed_set:
                neighbor.came_from = cur_puzzle
                priority_enqueue(open_list, neighbor, neighbor.manhattan_sum)
    
    return {
        'solution_puzzle': None,
        'runtime_ms': (time.time() - start_time) * 1000,
        'max_puzzles_in_memory': len(closed_set)
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
    if not solution_puzzle:
        return []
    
    moves = []
    current = solution_puzzle
    
    while current and current.last_slide_direction != SlideDirection.INITIAL:
        moves.append(DIRECTION_NAMES[current.last_slide_direction])
        current = current.came_from
    
    moves.reverse()
    return moves

