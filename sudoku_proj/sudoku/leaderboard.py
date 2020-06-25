# file: leaderboard.py
# author: Christopher Smith
# date: 8 June 2020

from django.db import connection
from collections import namedtuple


# raw SQL queries to determine user, puzzle ID, and completion time of puzzles
def calculate_leaders(difficulty):
    with connection.cursor() as cursor:
        if difficulty == 1:
            cursor.execute("SELECT sudoku_played.user, sudoku_played.puzzle_id_id, sudoku_played.end_time, "
                           "sudoku_played.start_time FROM sudoku_played JOIN "
                           "sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                           "sudoku_puzzles.difficulty = 1 AND sudoku_played.end_time - sudoku_played.start_time "
                           "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            desc = cursor.description
            nt_result = namedtuple('Record', [col[0] for col in desc])
            return [nt_result(*row) for row in cursor.fetchall()]

        if difficulty == 2:
            cursor.execute("SELECT sudoku_played.user, sudoku_played.puzzle_id_id, sudoku_played.end_time, "
                           "sudoku_played.start_time FROM sudoku_played JOIN "
                           "sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                           "sudoku_puzzles.difficulty = 2 AND sudoku_played.end_time - sudoku_played.start_time "
                           "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            desc = cursor.description
            nt_result = namedtuple('Record', [col[0] for col in desc])
            return [nt_result(*row) for row in cursor.fetchall()]

        if difficulty == 3:
            cursor.execute("SELECT sudoku_played.user, sudoku_played.puzzle_id_id, sudoku_played.end_time, "
                           "sudoku_played.start_time FROM sudoku_played JOIN "
                           "sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                           "sudoku_puzzles.difficulty = 3 AND sudoku_played.end_time - sudoku_played.start_time "
                           "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            desc = cursor.description
            nt_result = namedtuple('Record', [col[0] for col in desc])
            return [nt_result(*row) for row in cursor.fetchall()]

        if difficulty == 4:
            cursor.execute("SELECT sudoku_played.user, sudoku_played.puzzle_id_id, sudoku_played.end_time, "
                           "sudoku_played.start_time FROM sudoku_played JOIN "
                           "sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                           "sudoku_puzzles.difficulty = 4 AND sudoku_played.end_time - sudoku_played.start_time "
                           "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            desc = cursor.description
            nt_result = namedtuple('Record', [col[0] for col in desc])
            return [nt_result(*row) for row in cursor.fetchall()]

        if difficulty == 5:
            cursor.execute("SELECT sudoku_played.user, sudoku_played.puzzle_id_id, sudoku_played.end_time, "
                           "sudoku_played.start_time FROM sudoku_played JOIN "
                           "sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                           "sudoku_puzzles.difficulty = 5 AND sudoku_played.end_time - sudoku_played.start_time "
                           "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            desc = cursor.description
            nt_result = namedtuple('Record', [col[0] for col in desc])
            return [nt_result(*row) for row in cursor.fetchall()]
