from django.db import models

# User table with stats
class UserInfo(models.Model):
    uid = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=20)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

# Saved game table
class Board(models.Model):
    bid = models.IntegerField(primary_key=True)
    saved_board = models.CharField(max_length=1863)
