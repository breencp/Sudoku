# file: models.py
# author: Christopher Smith
# date: May 24, 2020

from django.db import models


# Puzzle table for storing pre-generated puzzles
class Puzzles(models.Model):
    puzz_id = models.CharField(primary_key=True)
    puzzle = models.CharField(max_length=1863)
    difficulty = models.CharField(max_length=1)


# User table with stats for leaderboard
class Played(models.Model):
    puzz_id = models.ForeignKey(Puzzles, on_delete=models.CASCADE)
    user = models.CharField(max_length=20)
    start_time = models.FloatField(default=0)
    end_time = models.FloatField(default=0)
    saved_board = models.CharField(max_length=1863)
    status = models.CharField(max_length=1)
    hints = models.IntegerField(default=0)
    difference = models.FloatField
