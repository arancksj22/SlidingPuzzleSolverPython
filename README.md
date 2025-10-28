# Sliding Puzzle Solver (Python Desktop Version)

A desktop application for solving sliding puzzles using various algorithms. This is a Python port of the web-based JavaScript version, built with Tkinter for a simple, native GUI.

## Features

### All Original Features Included:
- **Multiple Solving Algorithms:**
  - A* (A-Star) - Optimal solution with Manhattan distance heuristic
  - GBFS (Greedy Best-First Search) - Fast but non-optimal

- **Puzzle Customization:**
  - Adjustable dimensions (2x2 to 6x6)
  - Shuffle to random solvable state
  - Full randomization (dimensions + state)
  - Edit start state
  - Edit goal state

- **Interactive Features:**
  - Play Mode: Solve the puzzle manually
  - Edit Mode: Swap any tiles to create custom puzzles
  - Animated solution playback
  - Real-time solution statistics

- **Solution Output:**
  - Runtime in milliseconds
  - Number of moves (optimal/non-optimal)
  - Memory usage statistics
  - Complete move list

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes with Python)

## Installation

No additional packages required! Tkinter comes bundled with Python.

```bash
# Clone or download the files to a directory
cd "untitled folder"

# Run the application
python main.py
```

## Usage

### Basic Operation

1. **Start the Application:**
   ```bash
   python main.py
   ```

2. **Shuffle the Puzzle:**
   - Click "Shuffle" to create a random solvable puzzle
   - Or click "Randomize All" to change dimensions and shuffle

3. **Solve the Puzzle:**
   - Select an algorithm from the dropdown
   - Click "Solve Puzzle"
   - Watch the animated solution

### Play Mode

1. Enable "Play Mode" checkbox
2. Click tiles adjacent to the blank space to slide them
3. Try to arrange tiles in order (1, 2, 3, ... with blank in bottom-right)

### Edit Modes

**Edit Start State:**
1. Click "Edit Start State"
2. Click any two tiles to swap them
3. Create your custom starting configuration
4. Click "Exit Edit Mode" when done

**Edit Goal State:**
1. Click "Edit Goal State"
2. Swap tiles to create custom goal configuration
3. Click "Exit Edit Mode" to return

### Adjusting Dimensions

1. Set desired Rows (2-6)
2. Set desired Cols (2-6)
3. Click "Apply Dimensions"
4. Puzzle will reset to new size

## File Structure

```
untitled folder/
├── main.py                    # Main application and GUI
├── puzzle.py                  # Puzzle class with sliding logic
├── search_algorithms.py       # BFS, A*, IDA* implementations
├── strategic_algorithm.py     # Strategic solving algorithm
└── README.md                  # This file
```

## Algorithm Descriptions

### A* (A-Star)
- Optimal solution guaranteed
- Uses Manhattan distance heuristic + actual cost
- Best balance of speed and optimality
- Recommended for all puzzle sizes

### GBFS (Greedy Best-First Search)
- Non-optimal but very fast
- Uses only Manhattan distance heuristic (no cost tracking)
- Good for quick solutions
- May find longer paths than A*

## Tips

- **For Optimal Solutions:** Use A*
- **For Quick Solutions:** Use GBFS
- **Small Puzzles (2x2, 3x3):** Both algorithms work instantly
- **Large Puzzles (4x4+):** GBFS is faster but A* finds shorter solutions
- **Animation Speed:** Fixed at 200ms per move (can be adjusted in code)

## Performance Notes

- **2x2 puzzles:** All algorithms solve instantly
- **3x3 puzzles:** All algorithms work well (< 1 second)
- **4x4 puzzles:** Strategic and IDA* recommended
- **5x5+ puzzles:** Strategic algorithm recommended

## Keyboard Shortcuts

While the puzzle is in Play Mode, you can use arrow keys (if implemented) or click adjacent tiles to the blank space.

## Troubleshooting

**"Unsolvable" Error:**
- The current puzzle configuration cannot reach the goal state
- This happens when start and goal states have different solvability
- Solution: Click "Shuffle" or swap two non-blank tiles

**Application Won't Start:**
- Ensure Python 3.6+ is installed
- Tkinter should come with Python
- On Linux, install: `sudo apt-get install python3-tk`

**Animation Too Fast/Slow:**
- Open `main.py`
- Find line: `delay = 200  # milliseconds`
- Adjust value (higher = slower, lower = faster)

## Differences from Web Version

- **No Image Backgrounds:** Simplified to numbered tiles only
- **No Flip/Rotate:** Removed for simplicity
- **Desktop Native:** Runs as standalone application
- **Same Algorithms:** All solving logic is identical

## License

Free to use and modify. Based on the original web-based sliding puzzle solver.

## Credits

Ported from JavaScript/Web version to Python/Desktop by maintaining all core features and algorithms.
