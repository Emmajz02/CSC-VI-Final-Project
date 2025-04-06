from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, BudgetForm, ExpenseForm
from django.contrib.auth.decorators import login_required
from .models import Budget, Expense


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
def budget_view(request):
    budget, created = Budget.objects.get_or_create(user=request.user, defaults={'amount': 0.00})
    form = BudgetForm(instance=budget)
    expense_form = ExpenseForm()

    if request.method == 'POST':
        if 'update_budget' in request.POST:
            form = BudgetForm(request.POST, instance=budget)
            if form.is_valid():
                form.save()
            return redirect('home')

        elif 'add_expense' in request.POST:
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                expense = expense_form.save(commit=False)
                expense.budget = budget
                expense.save()
                
                # Update the budget amount after adding an expense
                budget.amount -= expense.amount
                budget.save()
            return redirect('home')

    else:
        form = BudgetForm(instance=budget)
        expense_form = ExpenseForm()

    expenses = Expense.objects.filter(budget=budget)
    return render(request, 'budget_app/home.html', {
        'expense_form': expense_form,
        'expenses': expenses,
        'form': form,
        'budget': budget
    })


    

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    budget = expense.budget
    expense.delete()
    budget.amount += expense.amount
    budget.save()
    return redirect('home')