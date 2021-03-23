from django.shortcuts import render
from .models import food_item
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def menu(request):
    # send menu to front-end

    non_combos = food_item.find_all_non_combos()
    combos = food_item.find_all_combos()

    return render(request, 'foods/menu.html',{'non_combos':non_combos, 'combos':combos})

def checkout(request):

    return render(request, 'foods/checkout.html')

@csrf_exempt
def addfood(request):

    if(request.method == 'POST'):
        nf = food_item(request.POST['name'],request.POST['item_type'],request.POST['price'],bool(request.POST['is_veg']),bool(request.POST['avail']),bool(request.POST['is_combo']))
        nf.insert()
        return render(request, 'foods/checkout.html')
    else:
        return render(request, 'foods/error.html')