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
    path('signup',views.signup, name = 'signup')
]