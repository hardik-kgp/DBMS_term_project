from django.shortcuts import render
from .models import food_item
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import itertools

# Create your views here.
def menu(request):
    # send menu to front-end

    non_combos = food_item.find_all_non_combos()
    combos = food_item.find_all_combos()

    foods = [(item, item.type) for item in non_combos]
    foods = {i:[j[0] for j in grp] for i,grp in itertools.groupby(foods, lambda x:x[1])}

    combos_list = []
    for combo in combos:
        temp = {}
        temp['head'] = combo
        temp['children'] = food_item.find_combo_internals(combo.food_id)
        combos_list.append(temp)

    return render(request, 'foods/menu.html',{'non_combos':foods, 'combos':combos_list})

def checkout(request):

    return render(request, 'foods/checkout.html')

# @csrf_exempt
# def addfood(request):

#     if(request.method == 'POST'):
#         print(request.POST['name'],request.POST['item_type'],request.POST['price'],bool(request.POST['is_veg']),bool(request.POST['avail']),bool(request.POST['is_combo']))
#         nf = food_item(request.POST['name'],request.POST['item_type'],request.POST['price'],bool(request.POST['is_veg']),bool(request.POST['avail']),bool(request.POST['is_combo']))
#         nf.insert()
#         return render(request, 'foods/checkout.html')
#     else:
#         return render(request, 'foods/error.html')