from django.urls import path
from .views import order_create
# from eshop_order.views import add_user_order, user_open_order
app_name = 'orders'
urlpatterns = [
    # path('add-user-order', add_user_order),
    # path('open-order', user_open_order),
    path('create/', order_create, name='order_create'),
]
