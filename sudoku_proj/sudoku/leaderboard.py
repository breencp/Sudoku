# file: leaderboard.py
# author: Christopher Smith
# date: 8 June 2020

from .models import Played


# raw SQL queries to determine user, puzzle ID, and completion time of puzzles
def calculate_leaders():
    diff1 = Played.objects.raw('SELECT user, puzzle_id_id, end_time - start_time FROM sudoku_played JOIN sudoku_puzzles'
                               'ON puzzle_id_id = puzzle_id WHERE difficulty = 1 AND'
                               'end_time - start_time IS NOT NULL ORDER BY end_time - start_time LIMIT 5')
    diff2 = Played.objects.raw('SELECT user, puzzle_id_id, end_time - start_time FROM sudoku_played JOIN sudoku_puzzles'
                               'ON puzzle_id_id = puzzle_id WHERE difficulty = 2 AND'
                               ' end_time - start_time IS NOT NULL ORDER BY end_time - start_time LIMIT 5')
    diff3 = Played.objects.raw('SELECT user, puzzle_id_id, end_time - start_time FROM sudoku_played JOIN sudoku_puzzles'
                               'ON puzzle_id_id = puzzle_id WHERE difficulty = 3 AND'
                               'end_time - start_time IS NOT NULL ORDER BY end_time - start_time LIMIT 5')
    diff4 = Played.objects.raw('SELECT user, puzzle_id_id, end_time - start_time FROM sudoku_played JOIN sudoku_puzzles'
                               'ON puzzle_id_id = puzzle_id WHERE difficulty = 4 AND'
                               'end_time - start_time IS NOT NULL ORDER BY end_time - start_time LIMIT 5')
    diff5 = Played.objects.raw('SELECT user, puzzle_id_id, end_time - start_time FROM sudoku_played JOIN sudoku_puzzles'
                               'ON puzzle_id_id = puzzle_id WHERE difficulty = 5 AND'
                               'end_time - start_time IS NOT NULL ORDER BY end_time - start_time LIMIT 5')
    return diff1, diff2, diff3, diff4, diff5
