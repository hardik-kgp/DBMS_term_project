from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import datetime
from .models import Customer
from .forms import UserRegisterForm
def home(request):
	return render(request, 'resauto/home.html')

def customer_login(request):
	return render(request, 'users/customer_login.html')

def employee_login(request):
	return render(request, 'users/employee_login.html')

def view_profile_customer(request):
	return render(request, 'users/view_profile_customer.html')

def verifycustomerlogin(request):
	print(request.POST['username'], request.POST['password'])
	with connection.cursor() as cursor:
		cursor.execute('SELECT * FROM Customer WHERE customer_id = %s and password = %s;', [request.POST['username'],request.POST['password']])        
		row = cursor.fetchall()
	row1 = [y for x in row for y in x]
	print(row1)
	if(len(row1)>=1):
		user_form = UserRegisterForm(request.POST)
		user = user_form.save()
		# user = authenticate(username=request.POST['username'], password=request.POST['password'])
		customer = Customer.find(int(request.POST['username']))
		login(request, user)
		return render(request, 'foods/menu.html', {'customer',customer})
	else:
		return render(request, 'users/customer_login.html', {'data':"Enter correct details"})

def customer_signup(request):
	# if not request.user.is_authenticated:
	#     return render(request, 'users/adminlogin.html', {'data':"Login again"})
	return render(request, 'users/customer_signup.html')


def employeesignup(request):
	if not request.user.is_authenticated:
		return render(request, 'resauto/adminlogin.html', {'data':"Login again"})
	return render(request, 'resauto/addemployee.html')


def userlogout(request):
	logout(request)
	return render(request, 'resauto/home.html', {'data':"Logged out"})


def createemployeeusers(request):
	if not request.user.is_authenticated:
		return render(request, 'resauto/adminlogin.html', {'data':"Login again"})
	username = request.POST['username']
	password = request.POST['password']
	with connection.cursor() as cursor:
		cursor.execute("select count(*) from auth_user where username = %s", [username])
		row = cursor.fetchall()
	row1 = [y for x in row for y in x]
	if(row1[0]==0):
		User.objects.create_user(username, '', password)
	else:
		render(request, 'resauto/addemployee.html', {'data':"Username already taken."})
	with connection.cursor() as cursor:
		cursor.execute('select count(*) from guide where id=%s;', [username])
		r = cursor.fetchall()
	if(r[0][0]!=0):
		return render(request, 'resauto/addemployee.html', {'data':"Username already taken."})
	with connection.cursor() as cursor:
		cursor.execute('insert into guide values(%s, "Anonymous New User", 4,aes_encrypt(%s, "cryptography"), "Computer Science and Engineering")', [username, password])
	return render(request, 'resauto/admin.html', {'data':"User Created"})

def createcustomerusers(request):
	if not request.user.is_authenticated:
		return render(request, 'resauto/adminlogin.html', {'data':"Login again"})
	begin = request.POST['start']
	end = request.POST['end']
	for i in range(int(begin), int(end)+1):
		with connection.cursor() as cursor:
			cursor.execute("select count(*) from auth_user where username = %s", [i])
			row = cursor.fetchall()
		row1 = [y for x in row for y in x]
		if(row1[0]==0):
			User.objects.create_user(i, '', str(i)+"123xyz")
		else:
			return render(request, 'resauto/addcustomer.html', {'data':"Username already taken."})
		with connection.cursor() as cursor:
			cursor.execute('select count(*) from customer where rollno=%s;', [i])
			r = cursor.fetchall()
		if(r[0][0]!=0):
			return render(request, 'resauto/addcustomer.html', {'data':"Username already taken."})
		with connection.cursor() as cursor:
			cursor.execute('insert into customer values(%s, "Anonymous New User", 0.0, NULL, 0, aes_encrypt(%s, "cryptography"), "Computer Science and Engineering", NULL, 0, 40, NULL)', [i, str(i)+"123xyz"])
	return render(request, 'resauto/admin.html', {'data':"Users Created"})
	
def adminlogin(request):
	return render(request, 'resauto/adminlogin.html')

def adminverify(request):
	with connection.cursor() as cursor:
		cursor.execute('SELECT * FROM admin WHERE username = %s and password = %s;', [request.POST['username'], request.POST['password']])
		row = cursor.fetchall()
	row1 = [y for x in row for y in x]
	if(len(row1)>=1):
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		login(request, user)
		return render(request, 'resauto/admin.html')
	else:
		return render(request, 'resauto/home.html', {'data':"Enter correct credentials"})