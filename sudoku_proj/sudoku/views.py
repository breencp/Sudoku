from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, World")


def how_to_play(request):
    return HttpResponse("How to Play")


def new_game(request):
    return HttpResponse("New Game")


def leaderboard(request):
    return HttpResponse("Leader Board")


def sudoku(request):
    return HttpResponse("Game Board")
