# file: leaderboard.py
# author: Christopher Smith
# date: 8 June 2020

from django.db import connection


# raw SQL queries to determine user, puzzle ID, and completion time of puzzles
def calculate_leaders(difficulty):
    users = ""
    puzzle_ids = ""
    completion_times = ""
    with connection.cursor() as cursor:
        if difficulty == 1:
            rows = cursor.execute("SELECT sudoku_played.user FROM sudoku_played JOIN sudoku_puzzles ON "
                                  "sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 1 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                users = tuple(users) + row
            rows = cursor.execute("SELECT sudoku_played.puzzle_id_id FROM sudoku_played JOIN sudoku_puzzles ON "
                                  "sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 1 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                puzzle_ids = tuple(puzzle_ids) + row
            rows = cursor.execute("SELECT sudoku_played.end_time - sudoku_played.start_time FROM sudoku_played JOIN "
                                  "sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 1 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                completion_times = tuple(completion_times) + row

        elif difficulty == 2:
            rows = cursor.execute("SELECT sudoku_played.user FROM sudoku_played JOIN sudoku_puzzles ON "
                                  "sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 2 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                users = tuple(users) + row

            rows = cursor.execute("SELECT sudoku_played.puzzle_id_id FROM sudoku_played JOIN sudoku_puzzles ON "
                                  "sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 2 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                puzzle_ids = tuple(puzzle_ids) + row

            rows = cursor.execute("SELECT sudoku_played.end_time - sudoku_played.start_time FROM sudoku_played JOIN "
                                  "sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 2 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                completion_times = tuple(completion_times) + row

        elif difficulty == 3:
            rows = cursor.execute("SELECT sudoku_played.user FROM sudoku_played JOIN sudoku_puzzles ON "
                                  "sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 3 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                users = tuple(users) + row

            rows = cursor.execute("SELECT sudoku_played.puzzle_id_id FROM sudoku_played JOIN sudoku_puzzles ON "
                                  "sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 3 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                puzzle_ids = tuple(puzzle_ids) + row

            rows = cursor.execute("SELECT sudoku_played.end_time - sudoku_played.start_time FROM sudoku_played JOIN "
                                  "sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 3 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                completion_times = tuple(completion_times) + row

        elif difficulty == 4:
            rows = cursor.execute("SELECT sudoku_played.user FROM sudoku_played JOIN sudoku_puzzles ON "
                                  "sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 4 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                users = tuple(users) + row

            rows = cursor.execute("SELECT sudoku_played.puzzle_id_id FROM sudoku_played JOIN sudoku_puzzles ON "
                                  "sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 4 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                puzzle_ids = tuple(puzzle_ids) + row

            rows = cursor.execute("SELECT sudoku_played.end_time - sudoku_played.start_time FROM sudoku_played JOIN "
                                  "sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 4 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                completion_times = tuple(completion_times) + row

        elif difficulty == 5:
            rows = cursor.execute("SELECT sudoku_played.user FROM sudoku_played JOIN sudoku_puzzles ON "
                                  "sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 5 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                users = tuple(users) + row

            rows = cursor.execute("SELECT sudoku_played.puzzle_id_id FROM sudoku_played JOIN sudoku_puzzles ON "
                                  "sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 5 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                puzzle_ids = tuple(puzzle_ids) + row

            rows = cursor.execute("SELECT sudoku_played.end_time - sudoku_played.start_time FROM sudoku_played JOIN "
                                  "sudoku_puzzles ON sudoku_played.puzzle_id_id = sudoku_puzzles.puzzle_id WHERE "
                                  "sudoku_puzzles.difficulty = 5 AND sudoku_played.end_time - sudoku_played.start_time "
                                  "IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time LIMIT 5")
            for row in rows:
                completion_times = tuple(completion_times) + row

    return users, puzzle_ids, completion_times
