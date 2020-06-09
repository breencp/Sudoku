# file: models.py
# author: Christopher Smith
# date: May 24, 2020

from django.db import models


# Puzzle table for storing pre-generated puzzles
class Puzzles(models.Model):
    id = models.AutoField(primary_key=True)
    board = models.CharField(max_length=1863)
    difficulty = models.CharField(max_length=1)
    techniques = models.CharField


# User table with stats for leaderboard
class Played(models.Model):
    p_id = models.AutoField(primary_key=True)
    id = models.ForeignKey(Puzzles, on_delete=models.CASCADE)
    user = models.CharField(max_length=20)
    start_time = models.IntegerField(default=0)
    end_time = models.IntegerField(default=0)
    saved_board = models.CharField(max_length=1863)
    status = models.CharField(max_length=1)
    hints = models.IntegerField(default=0)
