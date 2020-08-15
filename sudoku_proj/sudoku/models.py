from django.db import models


class Puzzles(models.Model):
    puzzle_id = models.AutoField(primary_key=True)
    board = models.CharField(max_length=1863, unique=True)
    solution = models.CharField(max_length=1863)
    difficulty = models.CharField(max_length=1)
    naked_single = models.IntegerField(default=0)
    hidden_single = models.IntegerField(default=0)
    naked_pair = models.IntegerField(default=0)
    omission = models.IntegerField(default=0)
    naked_triplet = models.IntegerField(default=0)
    hidden_pair = models.IntegerField(default=0)
    naked_quad = models.IntegerField(default=0)
    hidden_triplet = models.IntegerField(default=0)
    hidden_quad = models.IntegerField(default=0)
    x_wing = models.IntegerField(default=0)
    swordfish = models.IntegerField(default=0)
    xy_wing = models.IntegerField(default=0)
    unique_rectangle = models.IntegerField(default=0)
