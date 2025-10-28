#!/usr/bin/env python3
"""
Sliding Puzzle Solver - Launcher Script
This is the main entry point for the application.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run main application
from main import main

if __name__ == "__main__":
    print("Starting Sliding Puzzle Solver...")
    print("Close the window to exit.")
    main()
