from django.urls import path
from . import views

app_name = 'api-order'

urlpatterns = [
    path('create_order/', views.CreateOrderView.as_view(), name='create-order'),
    path('get-orders/', views.GetUsersOrders.as_view(), name='orders'),
]
