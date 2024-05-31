from django.urls import path
from . import views
# from .views import  main_page, log_out, register, home

urlpatterns = [
    path('add/', views.cart_add, name="cart_add"),
    path('', views.cart_summary, name="cart_summary"),
    path('delete/', views.cart_delete, name="cart_delete"),
    path('update/', views.cart_update, name="cart_update"),
    path('cart_clear/', views.cart_clear, name='cart_clear'),
    path('checkout/', views.checkout, name="checkout"),
    path('get_cart_quantity/', views.get_cart_quantity, name='get_cart_quantity'),
]