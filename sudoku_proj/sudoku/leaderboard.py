# file: leaderboard.py
# author: Christopher Smith
# date: 8 June 2020

from django.db import connection


# raw SQL queries to determine user, puzzle ID, and completion time of puzzles
def calculate_leaders(difficulty):
    record = ""
    with connection.cursor() as cursor:
        if difficulty == 1:
            rows = cursor.execute("SELECT sudoku_played.user, sudoku_played.puzzle_id_id, time(sudoku_played.end_time "
                                  "- sudoku_played.start_time, 'unixepoch') FROM sudoku_played JOIN "
                                  "sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 1 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                record = tuple(record) + row

        if difficulty == 2:
            rows = cursor.execute("SELECT sudoku_played.user, sudoku_played.puzzle_id_id, time(sudoku_played.end_time "
                                  "- sudoku_played.start_time, 'unixepoch') FROM sudoku_played JOIN "
                                  "sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 2 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                record = tuple(record) + row

        if difficulty == 3:
            rows = cursor.execute("SELECT sudoku_played.user, sudoku_played.puzzle_id_id, time(sudoku_played.end_time "
                                  "- sudoku_played.start_time, 'unixepoch') FROM sudoku_played JOIN "
                                  "sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 3 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                record = tuple(record) + row

        if difficulty == 4:
            rows = cursor.execute("SELECT sudoku_played.user, sudoku_played.puzzle_id_id, time(sudoku_played.end_time "
                                  "- sudoku_played.start_time, 'unixepoch') FROM sudoku_played JOIN "
                                  "sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 4 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                record = tuple(record) + row

        if difficulty == 5:
            rows = cursor.execute("SELECT sudoku_played.user, sudoku_played.puzzle_id_id, time(sudoku_played.end_time "
                                  "- sudoku_played.start_time, 'unixepoch') FROM sudoku_played JOIN "
                                  "sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 5 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                record = tuple(record) + row

    return record
