from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, BudgetForm
from django.contrib.auth.decorators import login_required
from .models import Budget


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login') 
    else:
        form = RegisterForm()

    return render(request, 'budget_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'budget_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')  # Redirect users to login if they are not authenticated
def home_view(request):
    budget, created = Budget.objects.get_or_create(user=request.user, defaults={'amount': 0.00})

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BudgetForm(instance=budget)

    return render(request, 'budget_app/home.html', {'form': form, 'budget': budget})


#for later
#@login_required
#def home_view(request):
    #return render(request, 'budget_app/templates/budget_app/home.html')