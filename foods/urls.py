from . import views
from django.urls import path,include

app_name = 'foods'

urlpatterns = [
    path('menu',views.menu,name="menu"),
    path('checkout',views.checkout,name="checkout"),
    path('addfood',views.addfood,name="addfood"),
]