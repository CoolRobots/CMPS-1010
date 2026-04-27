
------------------------------------------------------------
PICROSS README
------------------------------------------------------------
Game adapted/programmed by Jackson Bethune

Overview
This is an interactive Picross (Nonogram) puzzle game built in Python using the Pygame library. 
The game generates a random puzzle each time you play, displays the clues automatically,
and lets you fill in the grid using your mouse. 
The goal is to match the hidden solution grid using the row and column clues.

Features
- Clean user interface
- Dropdown menu for selecting puzzle size (5x5, 10x10, or 15x15)
- Random puzzle generation every game (that no longer generates impossible puzzles)
- Automatic clue generation for rows and columns
- Left click to fill a cell
- Right click to place an X mark
- Win detection when your filled grid matches the solution
- A puzzle creator where you can draw your own puzzle, export it and check its solvability
- A puzzle importer where you can import puzzles in the form of text
- Unlimited fun

Requirements
You must have Python 3 and the Pygame library installed.

if Pygame isn't installed enter "pip install pygame" in the terminal to install Pygame
if Python 3 isn't installed go to https://www.python.org/downloads/ to download it

Once you've met these requirements, simply open the file using Python to play!

The home screen will appear with a title, a dropdown menu to choose puzzle size, and a Start Game button. Click Start Game to begin.

Controls
Left mouse button: Toggle a filled cell (black square)
Right mouse button: Toggle an X mark (red cross)
Goal: Use the clues to determine which cells should be filled. When your grid matches the hidden solution, the game displays a message and returns to the home screen.

Project Structure
picross.py        Main game file
test_picross.py   Automated test suite
README.txt        This file

Troubleshooting
If you see the error "ModuleNotFoundError: No module named 'picross'", check if:
- The file is named eactly picross.py
- The test file is in the same folder
- You are running the test from inside that folder

Note: Make sure there's only 1 solution when exporting puzzles. Puzzles imported that have more than 1 solution won't work