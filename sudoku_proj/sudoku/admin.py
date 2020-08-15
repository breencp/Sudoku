from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Puzzles

admin.site.register(Puzzles)
AdminSite.site_url = '/sudoku'
