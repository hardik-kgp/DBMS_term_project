from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import datetime
from .models import Customer, Employee
from .forms import UserRegisterForm
from django.contrib import messages
from .models import Profile
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required

def home(request):
	return render(request, 'resauto/home.html')

def customer_login(request):
	return render(request, 'users/customer_login.html')

def employee_login(request):
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
			old_cart = request.session['cart_items']
			login(request,user)
			request.session['cart_items'] = old_cart
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				return redirect('foods:menu')
	else:
		form = AuthenticationForm()
	return render(request,'users/customer_login.html')


def verifyemployeelogin(request):
	if request.method == 'POST':
		temp = request.POST.dict()
		temp['username'] = temp['phone']
		form = AuthenticationForm(data=temp)
		if form.is_valid():
			user = form.get_user()
			login(request,user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				return redirect('users:dashboard')
	else:
		form = AuthenticationForm()
	return render(request,'users/employee_login.html')

def customer_signup(request):
	if request.method == 'POST':

		print("post request")
		temp = request.POST.dict()
		temp['username'] = request.POST['phone']
		
		print("username: ", temp['username'], "password: ", temp['password1'], "email: ", temp['email'])
		user_form = UserRegisterForm(temp)
		
		print(user_form)

		if user_form.is_valid():
			cur_user = user_form.save()
			customer = Customer(request.POST['name'],request.POST['email'],request.POST['phone'],0, 20000)
			customer.insert()

			profile = Profile()
			profile.user = cur_user
			profile.customer_id = customer.customer_id

			profile.save()

			old_cart = request.session['cart_items']
			login(request, cur_user)
			request.session['cart_items'] = old_cart

			print("Customer created successfully")

			messages.success(request, f'Your Account Has been Created')
			return redirect('foods:menu')
		else:
			print("Enter Valid Details")
			messages.error(request, f'Please Enter Valid details')
			return render(request,'users/customer_signup.html')

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
			employee = Employee(request.POST['name'],request.POST['position'],request.POST['salary'])
			employee.insert()

			profile = Profile()
			profile.user = cur_user
			profile.customer_id = employee.employee_id

			profile.save()

			login(request, cur_user)

			print("Employee created successfully")

			messages.success(request, f'Your Account Has been Created')
			return redirect('users:dashboard')
		else:
			print("Enter Valid Details")
			messages.error(request, f'Please Enter Valid details')
			return render(request,'users/employee_signup.html')
	else:
		return render(request, 'users/employee_signup.html')




def signup(request):
	return render(request, 'users/signup.html')

@login_required(login_url="/users/customer_login")
def profile(request):
	customer_id = request.user.profile.customer_id
	
	print("customer id: ",customer_id)
	cus = Customer.find(customer_id)

	return render(request, 'users/customer_profile.html', {'customer':cus})


@login_required(login_url="/users/employee_login")
def employee_profile(request):
	employee_id = request.user.profile.customer_id
	
	print("employee id: ",employee_id)
	emp = Employee.find(employee_id)

	return render(request, 'users/employee_profile.html', {'employee':emp})


# @login_required(login_url="/users/employee_login")
def dashboard(request):
    return render(request, 'users/dashboard.html')
    

@login_required(login_url="/users/customer_login")
def add_balance(request):

	if 'Amount' in request.GET:
		amount = request.GET['Amount']
		
		cus = Customer.find(request.user.profile.customer_id)
		cus.balance = cus.balance+int(amount)
		cus.update()
		messages.success(request, 'Amount {0} has been added successfully'.format(int(amount)))
		return redirect('users:profile') 

	# get current balance
	cursor = connection.cursor()
	cursor.execute("""SELECT balance FROM Customer WHERE customer_id = {0} """.format(request.user.profile.customer_id))

	row = cursor.fetchall()
	row = row[0][0]

	return render(request, "users/add_balance.html", {'balance': row})


@login_required(login_url="/users/customer_login")
def edit_details(request):
	if request.method == 'POST':
		cus = Customer.find(request.user.profile.customer_id)
		cus.name = request.POST['name']
		cus.email = request.POST['email']
		cus.phone = request.POST['phone']
		cus.update()
		messages.success(request, 'Details Updated Sucessfully')
		return redirect('users:profile')

	cus = Customer.find(request.user.profile.customer_id)

	return render(request, "users/edit_details.html",{'customer':cus})

def address_book(request):	
	if 'address' in request.GET:
		Customer.add_address(request.user.profile.customer_id, request.GET['address'])
		messages.success(request, 'Address Added Successfully')
		return redirect("users:address_book")

	addresses = Customer.get_addresses(request.user.profile.customer_id)
	return render(request, "users/address_book.html", {'addresses': addresses})



@login_required(login_url="/users/employee_login")
def edit_details_employee(request):
	if request.method == 'POST':
		emp = Employee.find(request.user.profile.customer_id)
		emp.name = request.POST['name']
		emp.update()
		messages.success(request, 'Details Updated Sucessfully')
		return redirect('users:employeeprofile')

	emp = Employee.find(request.user.profile.customer_id)

	return render(request, "users/edit_details_employee.html",{'employee':emp})