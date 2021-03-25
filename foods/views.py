from django.shortcuts import render
from .models import food_item
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import itertools

# Create your views here.
@csrf_exempt
def menu(request):
    # send menu to front-end
    if request.method == 'POST': #send to checkout page from here
        print(request.POST)

    non_combos = food_item.find_all_non_combos()
    combos = food_item.find_all_combos()
    # print(non_combos[-2].is_veg)

    foods = sorted([(item, item.type) for item in non_combos],key=lambda x: x[1])
    foods = {i:[j[0] for j in grp] for i,grp in itertools.groupby(foods, lambda x:x[1])}

    combos_list = []
    for combo in combos:
        temp = {}
        temp['head'] = combo
        temp['children'] = food_item.find_combo_internals(combo.food_id)
        combos_list.append(temp)
    # print(foods['Pizza'][2].is_veg)
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