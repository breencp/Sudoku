from django.shortcuts import render


def index(request):
    return render(request, 'sudoku/index.html')


def how_to_play(request):
    return render(request, 'sudoku/howtoplay.html')


def new_game(request):
    return render(request, 'sudoku/newgame.html')


def leaderboard(request):
    return render(request, 'sudoku/leaderboard.html')


def sudoku(request):
    return render(request, 'sudoku/sudoku.html')
