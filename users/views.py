from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import datetime
import itertools
from .models import Customer, Employee, Address
from orders.models import Order
from .forms import UserRegisterForm
from django.contrib import messages
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from foods.models import food_item


def home(request):
    return render(request, 'resauto/home.html')


def customer_login(request):
    if request.user.is_authenticated:
        messages.info(request, "You're already logged in")
        if request.user.profile.type == "E":
            return redirect('users:dashboard')
        else:
            return redirect('foods:menu')
    return render(request, 'users/customer_login.html')


def employee_login(request):
    if request.user.is_authenticated:
        messages.info(request, "You're already logged in")
        if request.user.profile.type == "E":
            return redirect('users:dashboard')
        else:
            return redirect('foods:menu')
    return render(request, 'users/employee_login.html')


def view_profile_customer(request):
    return render(request, 'users/view_profile_customer.html')


def verifycustomerlogin(request):
    if request.method == 'POST':
        temp = request.POST.dict()
        temp['username'] = temp['phone']
        form = AuthenticationForm(data=temp)
        if form.is_valid():
            user = form.get_user()

            if user.profile.type == "E":
                messages.warning(request, f'Invalid Credentials')
                return render(request, 'users/customer_login.html')

            if 'cart_items' in request.session.keys():
                old_cart = request.session['cart_items']
            login(request, user)
            if 'cart_items' in request.session.keys():
                request.session['cart_items'] = old_cart

            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('foods:menu')
    else:
        form = AuthenticationForm()
    return render(request, 'users/customer_login.html')


def verifyemployeelogin(request):
    if request.method == 'POST':
        temp = request.POST.dict()
        temp['username'] = temp['phone']
        form = AuthenticationForm(data=temp)
        if form.is_valid():
            user = form.get_user()

            if user.profile.type == "C":
                messages.warning(request, f'Invalid Credentials')
                return render(request, 'users/employee_login.html')

            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('users:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/employee_login.html')


def customer_signup(request):
    if request.method == 'POST':

        print("post request")
        temp = request.POST.dict()
        temp['username'] = request.POST['phone']

        print("username: ", temp['username'], "password: ",
              temp['password1'], "email: ", temp['email'])
        user_form = UserRegisterForm(temp)

        print(user_form)

        if user_form.is_valid():
            cur_user = user_form.save()
            customer = Customer(
                request.POST['name'], request.POST['email'], request.POST['phone'], 0, 0)
            customer.insert()

            profile = Profile()
            profile.user = cur_user
            profile.customer_id = customer.customer_id
            profile.type = "C"
            profile.save()

            if 'cart_items' in request.session.keys():
                old_cart = request.session['cart_items']
            login(request, cur_user)
            if 'cart_items' in request.session.keys():
                request.session['cart_items'] = old_cart

            print("Customer created successfully")

            messages.success(request, f'Your Account Has been Created')
            return redirect('foods:menu')
        else:
            print("Enter Valid Details")
            messages.warning(request, f'Please Enter Valid details')
            return render(request, 'users/customer_signup.html')

    else:
        return render(request, 'users/customer_signup.html')


def employee_signup(request):

    if request.method == 'POST':

        print("post request")
        temp = request.POST.dict()
        temp['username'] = temp['phone']

        # print("username: ", request.POST['username'], "password: ", request.POST['password1'], "email: ", request.POST['email'])
        user_form = UserRegisterForm(temp)

        print(user_form)

        if user_form.is_valid():
            cur_user = user_form.save()
            employee = Employee(
                request.POST['name'], request.POST['position'], request.POST['salary'])
            employee.insert()

            profile = Profile()
            profile.user = cur_user
            profile.customer_id = employee.employee_id

            profile.type = "E"
            profile.save()

            login(request, cur_user)

            print("Employee created successfully")

            messages.success(request, f'Your Account Has been Created')
            return redirect('users:dashboard')
        else:
            print("Enter Valid Details")
            messages.warning(request, f'Please Enter Valid details')
            return render(request, 'users/employee_signup.html')
    else:
        return render(request, 'users/employee_signup.html')


def signup(request):
    return render(request, 'users/signup.html')


@login_required(login_url="/users/customer_login")
def profile(request):
    if request.user.is_authenticated and request.user.profile.type == "E":
        messages.warning(request, "You can't access customer profiles")
        return redirect('users:employee_profile')
    customer_id = request.user.profile.customer_id

    print("customer id: ", customer_id)
    cus = Customer.find(customer_id)

    return render(request, 'users/customer_profile.html', {'customer': cus})


@login_required(login_url="/users/employee_login")
def employee_profile(request):
    if(request.user.profile.type != 'E'):
        messages.warning(request,"You can't access employee profiles")
        return redirect('foods:menu')
    employee_id = request.user.profile.customer_id

    print("employee id: ", employee_id)
    emp = Employee.find(employee_id)

    return render(request, 'users/employee_profile.html', {'employee': emp})


@login_required(login_url="/users/employee_login")
def dashboard(request):

    if(request.user.profile.type != 'E'):
        messages.warning(request,"You're not an employee!")
        return redirect('foods:menu')
    non_combos = food_item.find_all_non_combos()
    combos = food_item.find_all_combos()
    # print(non_combos[-2].is_veg)

    foods = sorted([(item, item.type)
                    for item in non_combos], key=lambda x: x[1])
    foods = {i: [j[0] for j in grp]
             for i, grp in itertools.groupby(foods, lambda x: x[1])}

    combos_list = []

    best_employee = Employee.get_best_employee()
    for combo in combos:
        temp = {}
        temp['head'] = combo
        temp['children'] = food_item.find_combo_internals(combo.food_id)
        combos_list.append(temp)
    # print(foods['Pizza'][2].is_veg)
    return render(request, 'users/dashboard.html', {'non_combos': foods, 'combos': combos_list, 'best_employee': best_employee})


@login_required(login_url="/users/employee_login")
def view_ratings(request):
    if(request.user.profile.type != 'E'):
        messages.warning(request,"You're not an employee!")
        return redirect('foods:menu')
    employee_id = request.user.profile.customer_id

    rating = Employee.get_average_rating(employee_id)

    orders = Order.find_orders_by_employee(employee_id)
    orders_box = []
    for order in orders:
        orders_box.append((order, Order.find_order_items(order.order_id)))

    return render(request, 'users/view_ratings.html', {'rating': rating if rating else 0, 'orders': orders_box})


@login_required(login_url="/users/customer_login")
def add_balance(request):
    if request.user.is_authenticated and request.user.profile.type == "E":
        messages.warning(request, "You don't have any balance as employee")
        return redirect('users:dashboard')

    if 'Amount' in request.GET:
        amount = request.GET['Amount']

        cus = Customer.find(request.user.profile.customer_id)
        cus.balance = cus.balance+int(amount)
        cus.update()
        messages.success(
            request, 'Amount {0} has been added successfully'.format(int(amount)))
        return redirect('users:profile')

    # get current balance
    cursor = connection.cursor()
    cursor.execute("""SELECT balance FROM Customer WHERE customer_id = {0} """.format(
        request.user.profile.customer_id))

    row = cursor.fetchall()
    row = row[0][0]

    return render(request, "users/add_balance.html", {'balance': row})


@login_required(login_url="/users/customer_login")
def edit_details(request):
    if request.user.is_authenticated and request.user.profile.type == "E":
        messages.warning(request, "You can't access customer profiles")
        return redirect('users:employee_profile')
    if request.method == 'POST':
        cus = Customer.find(request.user.profile.customer_id)
        cus.name = request.POST['name']
        cus.email = request.POST['email']
        # cus.phone = request.POST['phone']
        cus.update()
        messages.success(request, 'Details Updated Sucessfully')
        return redirect('users:profile')

    cus = Customer.find(request.user.profile.customer_id)

    return render(request, "users/edit_details.html", {'customer': cus})

@login_required(login_url="/users/customer_login")
def address_book(request):
    if request.user.is_authenticated and request.user.profile.type == "E":
        messages.warning(request, "You don't have addresses as employees")
        return redirect('users:dashboard')

    if 'address' in request.GET:
        Address.add_address(request.user.profile.customer_id, request.GET['address'])
        messages.success(request, 'Address Added Successfully')
        return redirect("users:address_book")

    addresses = Address.get_addresses(request.user.profile.customer_id)
    return render(request, "users/address_book.html", {'addresses': addresses})

    # addresses = Customer.get_addresses(request.user.profile.customer_id)
    # return render(request, "users/address_book.html", {'addresses': addresses})


@login_required(login_url="/users/employee_login")
def edit_details_employee(request):
    if(request.user.profile.type != 'E'):
        messages.warning(request,"You're not an employee!")
        return redirect('foods:menu')
    if request.method == 'POST':
        emp = Employee.find(request.user.profile.customer_id)
        emp.name = request.POST['name']
        emp.update()
        messages.success(request, 'Details Updated Sucessfully')
        return redirect('users:employee_profile')

    emp = Employee.find(request.user.profile.customer_id)
    
    return render(request, "users/edit_details_employee.html", {'employee': emp})


@login_required(login_url="/users/employee_login")
def edit_food(request):

    if(request.user.profile.type != 'E'):
        messages.warning(request,"You're not an employee!")
        return redirect('foods:menu')
    available_foods = [int(x) for x in request.POST.getlist('availability')]
    non_combos = food_item.find_all_non_combos()
    combos = food_item.find_all_combos()

    print(available_foods)
    for combo in combos:
        if(combo.food_id in available_foods):
            combo.availability = True
        else:
            combo.availability = False
        combo.update()

    for food in non_combos:
        if(food.food_id in available_foods):
            food.availability = True
            print(food.name)
        else:
            food.availability = False
        food.update()

    return redirect('users:dashboard')


@login_required(login_url="/users/employee_login")
def add_food(request):
    if(request.user.profile.type != 'E'):
        messages.warning(request,"You're not an employee!")
        return redirect('foods:menu')
    if(request.method == 'POST'):
        print(request.POST)
        food = food_item(request.POST['name'], request.POST['item_type'], int(
            request.POST['price']), (request.POST['is_veg'] == 'veg'), (request.POST['availability'] == 'available'), 0)
        food.insert()
        return redirect('users:dashboard')
    else:
        return render(request, 'users/add_food.html')

@login_required(login_url="/users/employee_login")
def add_combo(request):
    if(request.user.profile.type != 'E'):
        messages.warning(request,"you are not an employee!")
        return redirect('foods:menu')
    if(request.method == 'POST'):
        print(request.POST)
        food = food_item(request.POST['name'], request.POST['item_type'], int(
            request.POST['price']), (request.POST['is_veg'] == 'veg'), (request.POST['availability'] == 'available'), 0)
        food.insert()
        return redirect('users:dashboard')
    else:
        non_combos = food_item.find_all_non_combos()
        foods = sorted([(item, item.type)
                    for item in non_combos], key=lambda x: x[1])
        foods = {i: [j[0] for j in grp]
                for i, grp in itertools.groupby(foods, lambda x: x[1])}
        return render(request, 'users/create_combo.html',{'food_items':foods})

@login_required(login_url="/users/customer_login")
def my_orders(request):
    if request.user.is_authenticated and request.user.profile.type == "E":
        messages.warning(request, "You can't order as employees")
        return redirect('users:dashboard')
    orders = Order.find_orders_of_customer(request.user.profile.customer_id)
    orders_box = []
    for order in orders:
        orders_box.append((order, Order.find_order_items(order.order_id)))
    return render(request, 'users/my_orders.html', {'orders': orders_box})

@login_required(login_url="/users/customer_login")
def add_review(request):
    if request.user.is_authenticated and request.user.profile.type == "E":
        messages.warning(request, "You can't order as employees")
        return redirect('users:dashboard')
    order = Order.find(request.POST['order_id'])
    if order.customer_id != request.user.profile.customer_id:
        messages.warning(request, 'Invalid Request')
        return my_orders(request)
    order.rating = request.POST['rating']
    order.feedback = request.POST['feedback']
    order.update()
    return my_orders(request)