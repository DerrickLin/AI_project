from django.urls import path
from .views import register
# from .views import  main_page, log_out, register, home

from . import views

urlpatterns = [
    path('sign_up/', views.sign_up, name='sign_up'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_user/<int:id>', views.update_user, name='update_user'),
    # path('main_page/', main_page, name='main_page'),
    path('log_out/', views.log_out, name='log_out'),
    path('login/', views.login_view, name='login_view'),
    path('', views.login_view, name='login_view'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('shop/noodles/', views.noodles, name='noodles'),
    path('shop/candy/', views.candy, name='candy'),
    path('shop/biscuits/', views.biscuits, name='biscuits'),
    path('shop/drinks/', views.drinks, name='drinks'),
    path('renew_Picture/', views.renew_Picture, name='renew_Picture'),
    path('check_finished/', views.check_finished, name='check_finished'),
    path('order_list/', views.order_list, name='order_list'),
    path('feedback/', views.feedback, name='feedback'),
]
