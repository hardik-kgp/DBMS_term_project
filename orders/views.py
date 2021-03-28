from django.shortcuts import render
import time   
from django.shortcuts import render, redirect, HttpResponse 
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import Order

# Create your views here.

def view_orders(request):
	
	return render(request, "orders/view_orders.html")
	
@csrf_exempt
def save_order(request):
	print(request)
	cur_time = time.strftime('%Y-%m-%d %H:%M:%S')

	print(request.session)

	ordered_items = request.session['cart_items']

	print("delivery method: ",request.POST['delivery_method'])
	print("address : ",request.POST['delivery_address'])
	print("payment method : ",request.POST['payment_method'])
	print("total bill: ", request.session['total_bill'])

	o = Order(cur_time, 'Pending', request.POST['delivery_method'], request.user.profile.customer_id, request['addr'],request['payment_method'], request.session['total_bill'],NULL, "" )
	o.insert()

	cursor = connection.cursor()

	for item, count in ordered_items:
		query = """ INSERT INTO order_items values ('{0}','{1}', '{2}') """.format(o.order_id, item.food_id, count)
		cursor.execute(query)

	return HttpResponse('{"status":"1", "redirect_url":"/orders/view_orders"}', content_type="application/json")
	# return redirect("foods:menu")