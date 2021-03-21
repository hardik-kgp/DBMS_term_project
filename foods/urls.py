from . import views
from django.urls import path,include

app_name = 'foods'

urlpatterns = [
    path('menu',views.menu,name="menu"),
    path('checkout',views.menu,name="checkout"),
]