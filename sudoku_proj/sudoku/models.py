from django.db import models


# User table with stats
class UserBoard(models.Model):
    uid = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=20)
    start_time = models.IntegerField(default=0)
    end_time = models.IntegerField(default=0)
    saved_board = models.CharField(max_length=1863)
    status = models.CharField(max_length=1)
    hints = models.IntegerField(default=0)
