from django.shortcuts import render, redirect, HttpResponse
from .models import food_item
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import itertools

# Create your views here.
@csrf_exempt
def menu(request):
    # send menu to front-end
    if request.method == 'POST': #send to checkout page from here
        order_items = request.POST
        checkout_items = {}
        for fid,count in order_items.items():
            if int(count):
                checkout_items[fid] = int(count)
        print("checkout: ", checkout_items)
        request.session['cart_items'] = checkout_items
        return HttpResponse('{"status":"1", "redirect_url":"/foods/checkout"}', content_type="application/json")

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
    cart = request.session['cart_items']
    cart_items = []
    bill_tot = 0
    for key,count in cart.items():
        f = food_item.find(key)
        if f.is_combo:
            f.combo_internals = f.find_combo_internals(f.food_id)
        cart_items.append((f, count));
        bill_tot += count * f.price
    return render(request, 'foods/checkout.html', {'cart':cart_items, 'total_bill':bill_tot})

# @csrf_exempt
# def addfood(request):

#     if(request.method == 'POST'):
#         print(request.POST['name'],request.POST['item_type'],request.POST['price'],bool(request.POST['is_veg']),bool(request.POST['avail']),bool(request.POST['is_combo']))
#         nf = food_item(request.POST['name'],request.POST['item_type'],request.POST['price'],bool(request.POST['is_veg']),bool(request.POST['avail']),bool(request.POST['is_combo']))
#         nf.insert()
#         return render(request, 'foods/checkout.html')
#     else:
#         return render(request, 'foods/error.html')