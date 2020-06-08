# file: leaderboard.py
# author: Christopher Smith
# date: 8 June 2020

import sqlite3


def add():
    try:
        conn = sqlite3.connect('sudoku.sqlite3')
        cur = conn.cursor()
        insert = """ INSERT INTO sudoku_userboard
        (uid, user, start_time, end_time, saved_board, status, hints)
        VALUES (?,?,?,?,?,?,?) """
        cur.execute(insert)
        cur.close()
        conn.close()
    except sqlite3.Error as e:
        print(e)


def calculate_leaders():
    try:
        conn = sqlite3.connect('sudoku.sqlite3')
        cur = conn.cursor()
        diff1 = ''' SELECT user FROM sudoku_userboard
        WHERE difficulty = 1 ORDER BY difference LIMIT 5 '''
        diff2 = ''' SELECT user FROM sudoku_userboard
        WHERE difficulty = 2 ORDER BY difference LIMIT 5 '''
        diff3 = ''' SELECT user FROM sudoku_userboard
        WHERE difficulty = 3 ORDER BY difference LIMIT 5 '''
        diff4 = ''' SELECT user FROM sudoku_userboard
        WHERE difficulty = 4 ORDER BY difference LIMIT 5 '''
        diff5 = ''' SELECT user FROM sudoku_userboard
        WHERE difficulty = 5 ORDER BY difference LIMIT 5 '''
        cur.execute(diff1)
        cur.execute(diff2)
        cur.execute(diff3)
        cur.execute(diff4)
        cur.execute(diff5)
        cur.close()
        conn.close()
        return diff1, diff2, diff3, diff4, diff5
    except sqlite3.Error as e:
        print(e)
