from . import views
from django.urls import path,include

app_name = 'orders'

urlpatterns = [
    path('view_orders',views.view_orders,name="view_orders"),
    path('save_order', views.save_order, name="save_order"),
]