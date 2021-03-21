from django.shortcuts import render
from . import models
from django.db import connection

# Create your views here.
def menu(request):
    # send menu to front-end

    # cursor = connection.cursor()

    # non_combos = food_item.find_all_non_combos()
    # combos = food_item.find_all_combos()

    # return render(request, 'menu.html',{'non_combos':non_combos, 'combos':combos})

    return render(request, 'foods/menu.html')