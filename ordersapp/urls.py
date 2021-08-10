from django.urls import path
from ordersapp import views
import ordersapp as ordersapp
from ordersapp.apps import OrdersappConfig

app_name = 'ordersapp'  # 4

urlpatterns = [
    path('', views.OrderList.as_view(), name="orders_list"),
    path('/read/<pk>/', views.OrderRead.as_view(), name="order_read"),
    path('/update/<pk>/', views.OrderItemsUpdate.as_view(), name="order_update"),
    path('/delete/<pk>/', views.OrderDelete.as_view(), name="order_delete"),
    path('create/', views.OrderItemsCreate.as_view(), name="order_create"),
    path('forming/complete\<pk>/', views.order_forming_complete, name="order_forming_complete"),
]
