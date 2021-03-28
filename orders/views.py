from django.shortcuts import render
import time   
from django.shortcuts import render, redirect, HttpResponse 
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import Order
from foods.models import food_item 
from users.models import Address

# Create your views here.

def view_orders(request):
	orders = Order.find_orders_of_customer(request.user.profile.customer_id)
	orders_with_addresses = []
	for order in orders:
		dict_cur = {}
		dict_cur['order'] = order
		dict_cur['address'] = Address.get_address_from_id(order.address_id)
		orders_with_addresses.append(dict_cur)
	return render(request, "orders/view_orders.html", {'orders':orders_with_addresses})
	
@csrf_exempt
def save_order(request):
	print(request)
	cur_time = time.strftime('%Y-%m-%d %H:%M:%S')

	print(request.POST)

	ordered_items = request.session['cart_items']

	print(ordered_items)

	bill_tot=0
	for key,count in ordered_items.items():
		f = food_item.find(key)
		bill_tot += count * f.price

	print("delivery method: ",request.POST['delivery_method'])
	print("address : ",request.POST['delivery_address'])
	print("payment method : ",request.POST['payment_method'])
	print("total bill: ", bill_tot)

	o = Order(cur_time, 'Pending', request.POST['delivery_method'], request.user.profile.customer_id, request.POST['delivery_address'],request.POST['payment_method'], bill_tot ,'NULL', "" )
	o.insert()

	cursor = connection.cursor()

	for item, count in ordered_items.items():
		f = food_item.find(key)
		query = """ INSERT INTO order_items values ('{0}','{1}', '{2}') """.format(o.order_id, f.food_id, count)
		cursor.execute(query)

	return HttpResponse('{"status":"1", "redirect_url":"/orders/view_orders"}', content_type="application/json")
	# return redirect("foods:menu")