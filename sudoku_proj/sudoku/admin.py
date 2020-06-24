# Written by Christopher Breen for Sprint 1, last updated June 23, 2020
from django.contrib import admin

from .models import Puzzles, Played

admin.site.register(Puzzles)
admin.site.register(Played)
