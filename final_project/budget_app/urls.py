from django.urls import path
from . import views
from django.shortcuts import redirect
from .views import register_view, login_view, logout_view, budget_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', lambda request: redirect('login')), 
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('budget/', budget_view, name='home'),
    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
]