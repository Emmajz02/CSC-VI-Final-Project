from django.urls import path
from . import views
from django.shortcuts import redirect
from .views import register_view, login_view, logout_view, home_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('', lambda request: redirect('login')), 
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
]