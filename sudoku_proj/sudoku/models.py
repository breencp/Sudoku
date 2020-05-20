from django.db import models

class ID(models.Model):
    id = models.IntegerField(primary_key=True)

class User(models.Model):
    id = models.ForeignKey(ID, primary_key=True, on_delete=models.CASCADE)
    user = models.CharField(max_length=20)

class Wins(models.Model):
    id = models.ForeignKey(ID, primary_key=True, on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)

class Losses(models.Model):
    id = models.ForeignKey(ID, primary_key=True, on_delete=models.CASCADE)
    losses = models.IntegerField(default=0)