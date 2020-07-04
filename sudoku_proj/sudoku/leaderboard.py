# file: leaderboard.py
# author: Christopher Smith
# date: 8 June 2020

import datetime

from django.db import connection


# modifications by Christopher Smith for Sprint 2
# raw SQL queries to determine user, puzzle ID, and completion time of puzzles
def calculate_leaders(difficulty):
    with connection.cursor() as cursor:
        record = [dict()]
        query = cursor.execute(
            "SELECT sudoku_played.user, sudoku_played.puzzle_id_id, sudoku_played.end_time - "
            "sudoku_played.start_time FROM sudoku_played JOIN sudoku_puzzles ON sudoku_played.puzzle_id_id = "
            "sudoku_puzzles.puzzle_id WHERE sudoku_played.hints = 0 AND sudoku_puzzles.difficulty = %s AND "
            "sudoku_played.end_time - sudoku_played.start_time IS NOT NULL ORDER BY sudoku_played.end_time - "
            "sudoku_played.start_time LIMIT 5", [difficulty])
        rownr = 0
        for row in query:
            record.insert(rownr, {'user': row[0], 'puzzle_id': row[1], 'completion_time':
                datetime.timedelta(seconds=row[2])})
            rownr += 1
        return record
