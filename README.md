# Sudoku
Sudoku is comprised of two main components and is written in Python 3.8.  There is a create_game component designed to be ran in your local IDE to create the puzzles, and a web component to upload/import those puzzles into the database for play in the webbrowser.

1) Run create_game in the local IDE to create new puzzles using the desired solving technique you designate in the desired_technique declaration.
2) Run the web server and navigate to /sudoku/upload to import the JSON objects you created in #1 above.  You will need Django admin priv for this step.
3) Visit /sudoku to randomly play your imported puzzles of varying difficulty levels.
