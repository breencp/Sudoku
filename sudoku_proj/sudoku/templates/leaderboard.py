# file: leaderboard.py
# author: Christopher Smith
# date: 8 June 2020

import sqlite3


def add():
    try:
        conn = sqlite3.connect('sudoku.db')
        cur = conn.cursor()
        insert = """ INSERT INTO sudoku_userboard
        (uid, user, start_time, end_time, saved_board, status, hints)
        VALUES (?,?,?,?,?,?,?) """
        cur.execute(insert)
        conn.close()
    except sqlite3.Error as e:
        print(e)
