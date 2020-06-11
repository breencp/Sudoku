# file: models.py
# author: Christopher Smith
# date: May 24, 2020

from django.db import models


# Puzzle table for storing pre-generated puzzles
class Puzzles(models.Model):
    puzzle_id = models.AutoField(primary_key=True)
    board = models.CharField(max_length=1863, unique=True)
    solution = models.CharField(max_length=1863)
    difficulty = models.CharField(max_length=1)
    naked_single = models.BooleanField(default=False)
    hidden_single = models.BooleanField(default=False)
    naked_pair = models.BooleanField(default=False)
    omission = models.BooleanField(default=False)
    naked_triplet = models.BooleanField(default=False)
    hidden_pair = models.BooleanField(default=False)
    naked_quad = models.BooleanField(default=False)
    hidden_triplet = models.BooleanField(default=False)
    hidden_quad = models.BooleanField(default=False)
    x_wing = models.BooleanField(default=False)
    swordfish = models.BooleanField(default=False)
    xy_wing = models.BooleanField(default=False)
    unique_rectangle = models.BooleanField(default=False)


# User table with stats for leaderboard determination
class Played(models.Model):
    played_id = models.AutoField(primary_key=True)
    puzzle_id = models.ForeignKey(Puzzles, on_delete=models.CASCADE)
    user = models.CharField(max_length=20)
    start_time = models.IntegerField(default=0)
    end_time = models.IntegerField(default=0)
    saved_board = models.CharField(max_length=1863)
    status = models.CharField(max_length=1)
    hints = models.IntegerField(default=0)
