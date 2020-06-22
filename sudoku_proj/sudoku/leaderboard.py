# file: leaderboard.py
# author: Christopher Smith
# date: 8 June 2020

from django.db import connection


# raw SQL queries to determine user, puzzle ID, and completion time of puzzles
def calculate_leaders(difficulty):
    with connection.cursor() as cursor:
        if difficulty == 1:
            cursor.execute("SELECT sudoku_played.user FROM sudoku_played JOIN sudoku_puzzles ON"
                           " sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE sudoku_puzzles.difficulty ="
                           " 1 AND sudoku_played.end_time - sudoku_played.start_time IS NOT NULL ORDER BY"
                           " sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            users = cursor.fetchall()
            cursor.execute("SELECT sudoku_played.puzzle_id_id FROM sudoku_played JOIN sudoku_puzzles ON"
                           " sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE sudoku_puzzles.difficulty ="
                           " 1 AND sudoku_played.end_time - sudoku_played.start_time IS NOT NULL ORDER BY"
                           " sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            puzzle_ids = cursor.fetchall()
            cursor.execute("SELECT sudoku_played.end_time - sudoku_played.start_time FROM sudoku_played JOIN"
                           " sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE"
                           " sudoku_puzzles.difficulty = 1 AND sudoku_played.end_time - sudoku_played.start_time"
                           " IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            completion_times = cursor.fetchall()

        elif difficulty == 2:
            cursor.execute("SELECT sudoku_played.user FROM sudoku_played JOIN sudoku_puzzles ON"
                           " sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE sudoku_puzzles.difficulty ="
                           " 2 AND sudoku_played.end_time - sudoku_played.start_time IS NOT NULL ORDER BY"
                           " sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            users = cursor.fetchall()
            cursor.execute("SELECT sudoku_played.puzzle_id_id FROM sudoku_played JOIN sudoku_puzzles ON"
                           " sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE sudoku_puzzles.difficulty ="
                           " 2 AND sudoku_played.end_time - sudoku_played.start_time IS NOT NULL ORDER BY"
                           " sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            puzzle_ids = cursor.fetchall()
            cursor.execute("SELECT sudoku_played.end_time - sudoku_played.start_time FROM sudoku_played JOIN"
                           " sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE"
                           " sudoku_puzzles.difficulty = 2 AND sudoku_played.end_time - sudoku_played.start_time"
                           " IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            completion_times = cursor.fetchall()

        elif difficulty == 3:
            cursor.execute("SELECT sudoku_played.user FROM sudoku_played JOIN sudoku_puzzles ON"
                           " sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE sudoku_puzzles.difficulty ="
                           " 3 AND sudoku_played.end_time - sudoku_played.start_time IS NOT NULL ORDER BY"
                           " sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            users = cursor.fetchall()
            cursor.execute("SELECT sudoku_played.puzzle_id_id FROM sudoku_played JOIN sudoku_puzzles ON"
                           " sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE sudoku_puzzles.difficulty ="
                           " 3 AND sudoku_played.end_time - sudoku_played.start_time IS NOT NULL ORDER BY"
                           " sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            puzzle_ids = cursor.fetchall()
            cursor.execute("SELECT sudoku_played.end_time - sudoku_played.start_time FROM sudoku_played JOIN"
                           " sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE"
                           " sudoku_puzzles.difficulty = 3 AND sudoku_played.end_time - sudoku_played.start_time"
                           " IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            completion_times = cursor.fetchall()

        elif difficulty == 4:
            cursor.execute("SELECT sudoku_played.user FROM sudoku_played JOIN sudoku_puzzles ON"
                           " sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE sudoku_puzzles.difficulty ="
                           " 4 AND sudoku_played.end_time - sudoku_played.start_time IS NOT NULL ORDER BY"
                           " sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            users = cursor.fetchall()
            cursor.execute("SELECT sudoku_played.puzzle_id_id FROM sudoku_played JOIN sudoku_puzzles ON"
                           " sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE sudoku_puzzles.difficulty ="
                           " 4 AND sudoku_played.end_time - sudoku_played.start_time IS NOT NULL ORDER BY"
                           " sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            puzzle_ids = cursor.fetchall()
            cursor.execute("SELECT sudoku_played.end_time - sudoku_played.start_time FROM sudoku_played JOIN"
                           " sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE"
                           " sudoku_puzzles.difficulty = 4 AND sudoku_played.end_time - sudoku_played.start_time"
                           " IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            completion_times = cursor.fetchall()

        elif difficulty == 5:
            cursor.execute("SELECT sudoku_played.user FROM sudoku_played JOIN sudoku_puzzles ON"
                           " sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE sudoku_puzzles.difficulty ="
                           " 5 AND sudoku_played.end_time - sudoku_played.start_time IS NOT NULL ORDER BY"
                           " sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            users = cursor.fetchall()
            cursor.execute("SELECT sudoku_played.puzzle_id_id FROM sudoku_played JOIN sudoku_puzzles ON"
                           " sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE sudoku_puzzles.difficulty ="
                           " 5 AND sudoku_played.end_time - sudoku_played.start_time IS NOT NULL ORDER BY"
                           " sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            puzzle_ids = cursor.fetchall()
            cursor.execute("SELECT sudoku_played.end_time - sudoku_played.start_time FROM sudoku_played JOIN"
                           " sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE"
                           " sudoku_puzzles.difficulty = 5 AND sudoku_played.end_time - sudoku_played.start_time"
                           " IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            completion_times = cursor.fetchall()

    return users, puzzle_ids, completion_times
