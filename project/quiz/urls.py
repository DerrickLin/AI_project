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
    path('',views.home, name='home'),
    path('home/', views.home, name='home'),
    path('about/',views.about, name='about'),

]