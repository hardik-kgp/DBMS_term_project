from . import views
from django.urls import path,include

app_name = 'users'

urlpatterns = [
    path('customer_signup',views.customer_signup,name="customer_signup"),
    path('employee_signup', views.employee_signup, name = "employee_signup"),
    path('customer_login',views.customer_login,name="customer_login"),
    path('employee_login',views.employee_login,name="employee_login"),
    path('view_profile_customer', views.view_profile_customer, name = "view_profile_customer"),
    path('loginresultcustomer', views.verifycustomerlogin, name='verifycustomerlogin'),
    path('loginresultemployee', views.verifyemployeelogin, name='verifyemployeelogin'),
    path('signup',views.signup, name = 'signup'),
    path('profile',views.profile, name = 'profile'),
    path('employee_profile',views.employee_profile, name = 'employee_profile'),
    path('add_balance', views.add_balance, name="add_balance"),
    path('edit_details', views.edit_details, name="edit_details"),
    path('edit_details_employee', views.edit_details_employee, name="edit_details_employee"),
    path('address_book', views.address_book, name="address_book"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('view_ratings', views.view_ratings, name="view_ratings"),
    path('edit_food', views.edit_food, name = 'edit_food'),
    path('add_food', views.add_food, name = 'add_food'),
    # path('add_combo', views.add_combo, name = 'add_combo'),
    path('my_orders', views.my_orders, name = 'my_orders'),
]