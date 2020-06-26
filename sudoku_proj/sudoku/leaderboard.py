# file: leaderboard.py
# author: Christopher Smith
# date: 8 June 2020

import datetime
from django.db import connection


# raw SQL queries to determine user, puzzle ID, and completion time of puzzles
def calculate_leaders(difficulty):
    with connection.cursor() as cursor:
        if difficulty == 1:
            record = dict()
            query = cursor.execute(
                "SELECT sudoku_played.user, sudoku_played.puzzle_id_id, sudoku_played.end_time - "
                "sudoku_played.start_time FROM sudoku_played JOIN sudoku_puzzles ON sudoku_played.puzzle_id_id = "
                "sudoku_puzzles.puzzle_id WHERE sudoku_puzzles.difficulty = 1 AND sudoku_played.end_time - "
                "sudoku_played.start_time IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time "
                "LIMIT 5")
            for row in query:
                record.update(
                    {'user': row[0], 'puzzle_id': row[1], 'completion_time': datetime.timedelta(seconds=row[2])})
            return record

        if difficulty == 2:
            record = dict()
            query = cursor.execute(
                "SELECT sudoku_played.user, sudoku_played.puzzle_id_id, sudoku_played.end_time - "
                "sudoku_played.start_time FROM sudoku_played JOIN sudoku_puzzles ON sudoku_played.puzzle_id_id = "
                "sudoku_puzzles.puzzle_id WHERE sudoku_puzzles.difficulty = 2 AND sudoku_played.end_time - "
                "sudoku_played.start_time IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time "
                "LIMIT 5")
            for row in query:
                record.update(
                    {'user': row[0], 'puzzle_id': row[1], 'completion_time': datetime.timedelta(seconds=row[2])})
            return record

        if difficulty == 3:
            record = dict()
            query = cursor.execute(
                "SELECT sudoku_played.user, sudoku_played.puzzle_id_id, sudoku_played.end_time - "
                "sudoku_played.start_time FROM sudoku_played JOIN sudoku_puzzles ON sudoku_played.puzzle_id_id = "
                "sudoku_puzzles.puzzle_id WHERE sudoku_puzzles.difficulty = 3 AND sudoku_played.end_time - "
                "sudoku_played.start_time IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time "
                "LIMIT 5")
            for row in query:
                record.update(
                    {'user': row[0], 'puzzle_id': row[1], 'completion_time': datetime.timedelta(seconds=row[2])})
            return record

        if difficulty == 4:
            record = dict()
            query = cursor.execute(
                "SELECT sudoku_played.user, sudoku_played.puzzle_id_id, sudoku_played.end_time - "
                "sudoku_played.start_time FROM sudoku_played JOIN sudoku_puzzles ON sudoku_played.puzzle_id_id = "
                "sudoku_puzzles.puzzle_id WHERE sudoku_puzzles.difficulty = 4 AND sudoku_played.end_time - "
                "sudoku_played.start_time IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time "
                "LIMIT 5")
            for row in query:
                record.update(
                    {'user': row[0], 'puzzle_id': row[1], 'completion_time': datetime.timedelta(seconds=row[2])})
            return record

        if difficulty == 5:
            record = dict()
            query = cursor.execute(
                "SELECT sudoku_played.user, sudoku_played.puzzle_id_id, sudoku_played.end_time - "
                "sudoku_played.start_time FROM sudoku_played JOIN sudoku_puzzles ON sudoku_played.puzzle_id_id = "
                "sudoku_puzzles.puzzle_id WHERE sudoku_puzzles.difficulty = 5 AND sudoku_played.end_time - "
                "sudoku_played.start_time IS NOT NULL ORDER BY sudoku_played.end_time - sudoku_played.start_time "
                "LIMIT 5")
            for row in query:
                record.update(
                    {'user': row[0], 'puzzle_id': row[1], 'completion_time': datetime.timedelta(seconds=row[2])})
            return record
