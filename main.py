import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from puzzle import Puzzle
from search_algorithms import (
    solve_puzzle_bfs,
    solve_puzzle_astar, 
    solve_puzzle_gbfs,
    get_solution_moves
)

class SlidingPuzzleSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sliding Puzzle Solver")
        self.root.geometry("850x650")
        
        # State variables
        self.rows = 3
        self.cols = 3
        self.current_puzzle = None
        self.goal_puzzle = None
        self.tiles = {}
        self.play_mode = False
        self.animating = False
        self.selected_tile = None
        self.edit_mode = None
        self.highlight_tiles = set()
        
        # Colors
        self.bg_color = "#FFFFFF"
        self.blank_color = "#F8F9FA"
        self.selected_color = "#F1C40F"
        self.moving_color = "#FF6B6B"
        self.border_color = "#333333"
        self.text_color = "#FFFFFF"
        
        # Simplified color palette for tiles (8 colors is enough for most puzzles)
        self.tile_colors = [
            "#3498DB", "#E74C3C", "#2ECC71", "#F39C12", 
            "#9B59B6", "#1ABC9C", "#E67E22", "#34495E"
        ]
        
        self.setup_ui()
        self.reset_puzzle()
    
    def setup_ui(self):
        """Create the main UI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Left panel - Controls
        left_panel = ttk.Frame(main_frame, padding="5")
        left_panel.grid(row=0, column=0, rowspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        ttk.Label(left_panel, text="Puzzle Solver", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Dimensions control
        dim_frame = ttk.LabelFrame(left_panel, text="Dimensions", padding="5")
        dim_frame.pack(fill=tk.X, pady=3)
        
        # Rows slider
        rows_container = ttk.Frame(dim_frame)
        rows_container.pack(fill=tk.X, pady=2)
        ttk.Label(rows_container, text="Rows:", width=6).pack(side=tk.LEFT, padx=3)
        self.row_var = tk.IntVar(value=3)
        row_slider = ttk.Scale(rows_container, from_=2, to=8, orient=tk.HORIZONTAL, 
                              variable=self.row_var, command=lambda v: self.update_dimension_labels())
        row_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)
        self.row_label = ttk.Label(rows_container, text="3", width=3)
        self.row_label.pack(side=tk.LEFT, padx=3)
        
        # Cols slider
        cols_container = ttk.Frame(dim_frame)
        cols_container.pack(fill=tk.X, pady=2)
        ttk.Label(cols_container, text="Cols:", width=6).pack(side=tk.LEFT, padx=3)
        self.col_var = tk.IntVar(value=3)
        col_slider = ttk.Scale(cols_container, from_=2, to=8, orient=tk.HORIZONTAL, 
                              variable=self.col_var, command=lambda v: self.update_dimension_labels())
        col_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)
        self.col_label = ttk.Label(cols_container, text="3", width=3)
        self.col_label.pack(side=tk.LEFT, padx=3)
        
        ttk.Button(dim_frame, text="Apply", command=self.apply_dimensions).pack(fill=tk.X, pady=3)
        
        # Puzzle controls
        control_frame = ttk.LabelFrame(left_panel, text="Controls", padding="5")
        control_frame.pack(fill=tk.X, pady=3)
        
        ttk.Button(control_frame, text="Shuffle", command=self.shuffle_puzzle).pack(fill=tk.X, pady=1)
        ttk.Button(control_frame, text="Reset", command=self.reset_puzzle).pack(fill=tk.X, pady=1)
        
        self.play_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(control_frame, text="Play Mode", variable=self.play_var, 
                       command=self.toggle_play_mode).pack(fill=tk.X, pady=3)
        
        # Edit controls
        edit_frame = ttk.LabelFrame(left_panel, text="Edit", padding="5")
        edit_frame.pack(fill=tk.X, pady=3)
        
        ttk.Button(edit_frame, text="Edit Start", command=self.edit_start).pack(fill=tk.X, pady=1)
        ttk.Button(edit_frame, text="Edit Goal", command=self.edit_goal).pack(fill=tk.X, pady=1)
        ttk.Button(edit_frame, text="Exit Edit", command=self.exit_edit_mode).pack(fill=tk.X, pady=1)
        
        # Algorithm selection
        algo_frame = ttk.LabelFrame(left_panel, text="Algorithm", padding="5")
        algo_frame.pack(fill=tk.X, pady=3)
        
        self.algo_var = tk.StringVar(value="A*")
        algorithms = ["BFS", "A*", "GBFS"]
        algo_combo = ttk.Combobox(algo_frame, textvariable=self.algo_var, values=algorithms, state="readonly")
        algo_combo.pack(fill=tk.X, pady=1)
        
        ttk.Button(algo_frame, text="Solve", command=self.solve_puzzle).pack(fill=tk.X, pady=3)
        
        # Animation speed control
        speed_frame = ttk.LabelFrame(left_panel, text="Speed (ms)", padding="5")
        speed_frame.pack(fill=tk.X, pady=3)
        
        self.speed_var = tk.IntVar(value=300)
        speed_scale = ttk.Scale(speed_frame, from_=50, to=1000, orient=tk.HORIZONTAL, 
                               variable=self.speed_var)
        speed_scale.pack(fill=tk.X, padx=3, pady=1)
        ttk.Label(speed_frame, textvariable=self.speed_var).pack(pady=1)
        
        # Center panel - Puzzle grid
        center_panel = ttk.Frame(main_frame, padding="5")
        center_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.puzzle_label = ttk.Label(center_panel, text="Current Puzzle", font=("Arial", 12, "bold"))
        self.puzzle_label.pack(pady=3)
        
        # Canvas for puzzle
        self.canvas_frame = ttk.Frame(center_panel)
        self.canvas_frame.pack(expand=True, fill=tk.BOTH, pady=5)
        
        self.canvas = tk.Canvas(self.canvas_frame, width=350, height=350, bg=self.bg_color, highlightthickness=1)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        # Bottom panel - Output
        output_frame = ttk.LabelFrame(main_frame, text="Solution Output", padding="5")
        output_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=3)
        
        # Summary text
        summary_frame = ttk.Frame(output_frame)
        summary_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(summary_frame, text="Summary:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.summary_text = tk.Text(summary_frame, height=3, width=45, font=("Courier", 8))
        self.summary_text.pack(fill=tk.BOTH, expand=True, pady=1)
        
        # Move list
        moves_frame = ttk.Frame(output_frame)
        moves_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(moves_frame, text="Moves:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        self.moves_text = scrolledtext.ScrolledText(moves_frame, height=6, width=45, font=("Courier", 8))
        self.moves_text.pack(fill=tk.BOTH, expand=True, pady=1)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=3)
    
    def apply_dimensions(self):
        """Apply new puzzle dimensions"""
        if self.animating:
            return
        
        new_rows = int(self.row_var.get())
        new_cols = int(self.col_var.get())
        
        if new_rows < 2 or new_rows > 8 or new_cols < 2 or new_cols > 8:
            messagebox.showwarning("Invalid Dimensions", "Rows and columns must be between 2 and 8")
            return
        
        # Warn for large puzzles
        total_tiles = new_rows * new_cols
        if total_tiles > 36:  # 6x6 or larger
            result = messagebox.askyesno("Large Puzzle Warning", 
                f"Creating a {new_rows}x{new_cols} puzzle ({total_tiles} tiles).\n\n"
                "⚠️ Performance Guide:\n"
                "• 3x3 to 4x4: Fast with all algorithms\n"
                "• 5x5 (25 tiles): BFS/A* may take 10-60 seconds\n"
                "• 6x6+ (36+ tiles): Use GBFS only, may take minutes\n\n"
                "Continue?")
            if not result:
                return
        
        self.rows = new_rows
        self.cols = new_cols
        self.reset_puzzle()
        self.status_var.set(f"Puzzle dimensions changed to {self.rows}x{self.cols}")
    
    def update_dimension_labels(self):
        """Update the dimension labels when sliders change"""
        self.row_label.config(text=str(int(self.row_var.get())))
        self.col_label.config(text=str(int(self.col_var.get())))
    
    def get_tile_color(self, value):
        """Get color for tile based on its value"""
        if value == 0:
            return self.blank_color
        return self.tile_colors[(value - 1) % len(self.tile_colors)]
    
    def reset_puzzle(self):
        """Reset puzzle to goal state"""
        self.current_puzzle = Puzzle(self.rows, self.cols, gen_random=False)
        self.goal_puzzle = Puzzle(self.rows, self.cols, gen_random=False)
        self.selected_tile = None
        self.edit_mode = None
        self.highlight_tiles.clear()
        self.puzzle_label.config(text="Current Puzzle")
        self.draw_puzzle()
        self.clear_output()
        self.status_var.set("Puzzle reset to goal state")
    
    def shuffle_puzzle(self):
        """Shuffle puzzle to random solvable state"""
        if self.animating:
            return
        
        self.current_puzzle = Puzzle(self.rows, self.cols, gen_random=True, solvable=True)
        self.selected_tile = None
        self.highlight_tiles.clear()
        self.draw_puzzle()
        self.clear_output()
        self.status_var.set("Puzzle shuffled")
    
    def toggle_play_mode(self):
        """Toggle play mode on/off"""
        self.play_mode = self.play_var.get()
        self.selected_tile = None
        self.draw_puzzle()
        if self.play_mode:
            self.status_var.set("Play Mode: Click adjacent tiles to slide them")
        else:
            self.status_var.set("Edit Mode: Click any two tiles to swap them")
    
    def edit_start(self):
        """Enter edit start state mode"""
        self.edit_mode = 'start'
        self.puzzle_label.config(text="Editing Start Puzzle (Click tiles to swap)")
        self.status_var.set("Edit Mode: Modify the starting puzzle state")
    
    def edit_goal(self):
        """Enter edit goal state mode"""
        self.edit_mode = 'goal'
        self.puzzle_label.config(text="Editing Goal Puzzle (Click tiles to swap)")
        # Switch to showing goal puzzle
        self.current_puzzle, self.goal_puzzle = self.goal_puzzle, self.current_puzzle
        self.draw_puzzle()
        self.status_var.set("Edit Mode: Modify the goal puzzle state")
    
    def exit_edit_mode(self):
        """Exit edit mode"""
        if self.edit_mode == 'goal':
            # Switch back to start puzzle
            self.current_puzzle, self.goal_puzzle = self.goal_puzzle, self.current_puzzle
        
        self.edit_mode = None
        self.selected_tile = None
        self.puzzle_label.config(text="Current Puzzle")
        self.draw_puzzle()
        self.status_var.set("Exited edit mode")
    
    def draw_puzzle(self):
        """Draw the puzzle on canvas"""
        self.canvas.delete("all")
        
        # Calculate tile size based on canvas size
        canvas_width = self.canvas.winfo_width() if self.canvas.winfo_width() > 1 else 400
        canvas_height = self.canvas.winfo_height() if self.canvas.winfo_height() > 1 else 400
        
        # Use smaller dimension to keep tiles square
        size = min(canvas_width, canvas_height)
        tile_size = (size - 20) // max(self.rows, self.cols)
        
        # Center the puzzle
        offset_x = (canvas_width - tile_size * self.cols) // 2
        offset_y = (canvas_height - tile_size * self.rows) // 2
        
        self.tiles = {}
        
        for row in range(self.rows):
            for col in range(self.cols):
                value = self.current_puzzle.matrix[row][col]
                x1 = offset_x + col * tile_size
                y1 = offset_y + row * tile_size
                x2 = x1 + tile_size
                y2 = y1 + tile_size
                
                # Choose color
                color = self.get_tile_color(value)
                
                # Highlight moving tiles
                if (row, col) in self.highlight_tiles:
                    color = self.moving_color
                
                # Draw tile
                rect = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=self.border_color,
                    width=max(1, tile_size // 30),
                    tags=f"tile_{row}_{col}"
                )
                
                # Draw number
                if value != 0:
                    font_size = max(8, tile_size // 3) if len(str(value)) <= 2 else max(6, tile_size // 4)
                    
                    self.canvas.create_text(
                        (x1 + x2) // 2, (y1 + y2) // 2,
                        text=str(value),
                        font=("Arial", font_size, "bold"),
                        fill=self.text_color,
                        tags=f"tile_{row}_{col}"
                    )
                
                self.tiles[(row, col)] = {'value': value, 'rect': rect}
                
                # Bind click event
                self.canvas.tag_bind(f"tile_{row}_{col}", "<Button-1>", 
                                    lambda e, r=row, c=col: self.tile_clicked(r, c))
    
    def tile_clicked(self, row, col):
        """Handle tile click"""
        if self.animating:
            return
        
        value = self.current_puzzle.matrix[row][col]
        
        if self.play_mode:
            # In play mode, only allow clicking tiles adjacent to blank
            blank_row = self.current_puzzle.blank_row
            blank_col = self.current_puzzle.blank_col
            
            # Check if clicked tile is adjacent to blank
            is_adjacent = (
                (row == blank_row and abs(col - blank_col) == 1) or
                (col == blank_col and abs(row - blank_row) == 1)
            )
            
            if is_adjacent and value != 0:
                # Swap with blank
                self.current_puzzle.matrix[row][col] = 0
                self.current_puzzle.matrix[blank_row][blank_col] = value
                self.current_puzzle.blank_row = row
                self.current_puzzle.blank_col = col
                self.draw_puzzle()
                
                # Check if solved
                if self.goal_puzzle.is_equal_to_puzzle(self.current_puzzle):
                    messagebox.showinfo("Congratulations!", "Puzzle solved!")
                    self.status_var.set("Puzzle solved!")
        else:
            # Edit mode - swap two tiles
            if self.selected_tile is None:
                # First tile selected
                self.selected_tile = (row, col)
                # Highlight selected tile
                rect = self.tiles[(row, col)]['rect']
                self.canvas.itemconfig(rect, fill=self.selected_color)
                self.status_var.set(f"Selected tile {value}. Click another tile to swap.")
            else:
                # Second tile selected - swap
                row1, col1 = self.selected_tile
                val1 = self.current_puzzle.matrix[row1][col1]
                val2 = self.current_puzzle.matrix[row][col]
                
                self.current_puzzle.matrix[row1][col1] = val2
                self.current_puzzle.matrix[row][col] = val1
                
                # Update blank position if swapping blank
                if val1 == 0:
                    self.current_puzzle.blank_row = row
                    self.current_puzzle.blank_col = col
                elif val2 == 0:
                    self.current_puzzle.blank_row = row1
                    self.current_puzzle.blank_col = col1
                
                self.selected_tile = None
                self.draw_puzzle()
                self.status_var.set(f"Swapped tiles {val1} and {val2}")
    
    def solve_puzzle(self):
        """Solve the puzzle using selected algorithm"""
        if self.animating:
            return
        
        if self.goal_puzzle.is_equal_to_puzzle(self.current_puzzle):
            messagebox.showinfo("Already Solved", "Puzzle is already in goal state!")
            return
        
        # Algorithm-specific warnings
        total_tiles = self.rows * self.cols
        algo_name = self.algo_var.get()
        
        # Strong warning for BFS/A* on large puzzles
        if algo_name in ["BFS", "A*"] and total_tiles > 25:
            result = messagebox.askyesno("⚠️ Algorithm Warning", 
                f"Using {algo_name} on {self.rows}x{self.cols} ({total_tiles} tiles) is NOT recommended!\n\n"
                f"❌ {algo_name} may take 5-30+ minutes and use several GB of RAM\n"
                f"✅ Switch to GBFS for faster (non-optimal) solutions\n\n"
                f"For optimal solutions, use puzzles ≤ 5x5 (25 tiles)\n\n"
                "Continue anyway (may freeze)?")
            if not result:
                return
        
        # General warning for very large puzzles
        elif total_tiles > 49:
            result = messagebox.askyesno("Large Puzzle Warning", 
                f"Solving {self.rows}x{self.cols} ({total_tiles} tiles) may take very long.\n\n"
                f"Algorithm Performance:\n"
                f"• BFS - Slowest, most memory (not recommended > 5x5)\n"
                f"• A* - Fast optimal, solution (not recommended > 5x5)\n"
                f"• GBFS - Fastest but non optimal (usable up to 7x7)\n\n"
                "Continue?")
            if not result:
                return
        
        # Check solvability
        current_solvable = Puzzle.is_puzzle_solvable_2d(self.current_puzzle.matrix)
        goal_solvable = Puzzle.is_puzzle_solvable_2d(self.goal_puzzle.matrix)
        
        if current_solvable != goal_solvable:
            messagebox.showerror("Unsolvable..", 
                "This puzzle configuration is unsolvable!\n"
                "Start and goal states have different solvability.")
            return
        
        self.status_var.set("Solving puzzle...")
        self.animating = True
        self.root.update()
        
        # Get algorithm
        algo_name = self.algo_var.get()
        algorithm = {
            "BFS": solve_puzzle_bfs,
            "A*": solve_puzzle_astar,
            "GBFS": solve_puzzle_gbfs
        }.get(algo_name, solve_puzzle_astar)
        
        # Make a copy to solve
        puzzle_copy = Puzzle.from_puzzle(self.current_puzzle)
        
        try:
            # Solve in a way that we can animate live
            self.solve_with_live_animation(algorithm, puzzle_copy, algo_name)
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error solving puzzle: {str(e)}")
            self.status_var.set("Error solving puzzle")
            self.animating = False
    
    def solve_with_live_animation(self, algorithm, puzzle_copy, algo_name):
        """Solve puzzle and animate in real-time"""
        import threading
        
        # Store original puzzle
        original_puzzle = Puzzle.from_puzzle(self.current_puzzle)
        solution_data = {'solution': None, 'error': None}
        
        def solve_in_background():
            try:
                solution_data['solution'] = algorithm(puzzle_copy, self.goal_puzzle)
            except Exception as e:
                solution_data['error'] = str(e)
        
        # Start solving in background thread
        solve_thread = threading.Thread(target=solve_in_background)
        solve_thread.daemon = True
        solve_thread.start()
        
        # Wait for solution with periodic checks
        def check_solution():
            if solve_thread.is_alive():
                # Still solving, check again soon
                self.root.after(100, check_solution)
            else:
                # Solving finished
                if solution_data['error']:
                    messagebox.showerror("Error", f"Error solving: {solution_data['error']}")
                    self.animating = False
                    return
                
                solution = solution_data['solution']
                
                # Check if solution was found
                if solution['solution_puzzle'] is None:
                    messagebox.showerror("No Solution", "Could not find a solution to this puzzle.")
                    self.status_var.set("No solution found")
                    self.animating = False
                    return
                
                # Get moves
                if 'solution_moves' in solution:
                    moves = solution['solution_moves']
                else:
                    moves = get_solution_moves(solution['solution_puzzle'])
                
                # Display results
                self.display_solution(solution, moves, algo_name)
                
                # Reset to original and animate solution
                self.current_puzzle = original_puzzle
                self.draw_puzzle()
                
                # Animate solution
                if moves:
                    self.animate_solution(moves)
                else:
                    self.status_var.set("Puzzle already solved!")
                    self.animating = False
        
        check_solution()
    
    def display_solution(self, solution, moves, algo_name):
        """Display solution summary and move list"""
        self.summary_text.delete(1.0, tk.END)
        self.moves_text.delete(1.0, tk.END)
        
        # Summary
        optimal = "(optimal)" if algo_name in ["BFS", "A*"] else "(non-optimal)"
        summary = (f"Algorithm: {algo_name}\n"
                  f"Runtime: {solution['runtime_ms']:.3f}ms\n"
                  f"Moves: {len(moves)} {optimal}\n"
                  f"Max states: {solution['max_puzzles_in_memory']}")
        self.summary_text.insert(1.0, summary)
        
        # Move list
        if not moves:
            self.moves_text.insert(1.0, "Puzzle already solved!")
            return
        
        move_text = "Move list:\n" + "\n".join(f"{i}: {m}" for i, m in enumerate(moves[:1000], 1))
        if len(moves) > 1000:
            move_text += f"\n... +{len(moves) - 1000} more"
        self.moves_text.insert(1.0, move_text)
    
    def animate_solution(self, moves):
        """Animate the solution moves"""
        self.animating = True
        self.status_var.set("Animating solution...")
        self.root.update()
        self.animate_next_move(moves, 0)
    
    def animate_next_move(self, moves, index):
        """Animate next move in sequence"""
        # Check if window still exists
        try:
            if not self.root.winfo_exists():
                self.animating = False
                return
        except:
            self.animating = False
            return
        
        if index >= len(moves):
            self.animating = False
            self.highlight_tiles.clear()
            self.draw_puzzle()
            self.status_var.set(f"Solved in {len(moves)} moves!")
            return
        
        move = moves[index]
        blank_row = self.current_puzzle.blank_row
        blank_col = self.current_puzzle.blank_col
        
        # Highlight moving tile
        move_map = {"UP": (-1, 0), "DOWN": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}
        if move in move_map:
            dr, dc = move_map[move]
            self.highlight_tiles = {(blank_row + dr, blank_col + dc)}
            self.draw_puzzle()
            self.root.update()
            self.root.after(100)
        
        # Apply move
        {"UP": self.current_puzzle.slide_up, "DOWN": self.current_puzzle.slide_down,
         "LEFT": self.current_puzzle.slide_left, "RIGHT": self.current_puzzle.slide_right
        }.get(move, lambda: None)()
        
        # Redraw
        self.highlight_tiles.clear()
        self.draw_puzzle()
        self.status_var.set(f"Move {index + 1}/{len(moves)}: {move}")
        
        # Schedule next move
        self.root.after(self.speed_var.get(), lambda: self.animate_next_move(moves, index + 1))
    
    def clear_output(self):
        """Clear output text areas"""
        self.summary_text.delete(1.0, tk.END)
        self.moves_text.delete(1.0, tk.END)

def main():
    root = tk.Tk()
    app = SlidingPuzzleSolver(root)
    root.mainloop()

if __name__ == "__main__":
    main()
