from django.shortcuts import render, redirect, HttpResponse
from .models import food_item
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import itertools
from django.contrib.auth.decorators import login_required
from users.models import Customer, Address
import json
from django.contrib import messages


# Create your views here.
@csrf_exempt
def menu(request):
    # print(request.user)
    if request.user.is_authenticated and request.user.profile.type == "E":
        messages.warning(request, "You can't order with an employee profile")
        return redirect('users:dashboard')
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
    
    best_foods = {}
    best_foods['till_now'] = food_item.find_max_selling_till_now()
    best_foods['day'] = food_item.find_max_occuring_food_today()
    best_foods['month'] = food_item.find_max_occuring_food_this_month()
    best_foods['year'] = food_item.find_max_occuring_food_this_year()

    return render(request, 'foods/menu.html',{'non_combos':foods, 'combos':combos_list, 'best_foods':best_foods })

@login_required(login_url="/users/customer_login")
def checkout(request):
    if request.user.is_authenticated and request.user.profile.type == "E":
        messages.warning(request, "You can't order with an employee profile")
        return redirect('users:dashboard')
    cart = request.session['cart_items']
    cart_items = []
    bill_tot = 0
    for key,count in cart.items():
        f = food_item.find(key)
        if f.is_combo:
            f.combo_internals = f.find_combo_internals(f.food_id)
        cart_items.append((f, count));
        bill_tot += count * f.price
    addresses = Address.get_addresses(request.user.profile.customer_id)

    return render(request, 'foods/checkout.html', {'cart':cart_items, 'total_bill':bill_tot, 'addresses':addresses, 'cart_str':json.dumps(cart)})

@login_required(login_url="/users/customer_login")
def get_cart(request):
    cart = request.session['cart_items']
    return HttpResponse(json.dumps({'status':1,'cart':json.dumps(cart)}))

# @csrf_exempt
# def addfood(request):

#     if(request.method == 'POST'):
#         print(request.POST['name'],request.POST['item_type'],request.POST['price'],bool(request.POST['is_veg']),bool(request.POST['avail']),bool(request.POST['is_combo']))
#         nf = food_item(request.POST['name'],request.POST['item_type'],request.POST['price'],bool(request.POST['is_veg']),bool(request.POST['avail']),bool(request.POST['is_combo']))
#         nf.insert()
#         return render(request, 'foods/checkout.html')
#     else:
#         return render(request, 'foods/error.html')