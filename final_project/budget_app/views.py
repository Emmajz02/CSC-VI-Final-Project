from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, BudgetForm, ExpenseForm, ProfilePictureForm
from django.contrib.auth.decorators import login_required
from .models import Budget, Expense

#Allows users to register and create their account
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

#Allows previous users to login to their account
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password') #error handling

    return render(request, 'budget_app/login.html')

def logout_view(request): #logs users out
    logout(request)
    return redirect('login')


@login_required(login_url='login') #requires users to be logged in to use the app
def budget_view(request): #Creates the budget, expenses, and the profile pic
    budget, created = Budget.objects.get_or_create(user=request.user, defaults={'amount': 0.00})
    form = BudgetForm(instance=budget)
    expense_form = ExpenseForm()
    profile_form = ProfilePictureForm(instance=budget)

    if request.method == 'POST':
        if 'update_budget' in request.POST:
            form = BudgetForm(request.POST, instance=budget)
            if form.is_valid():
                form.save()
            else:
                 messages.error(request, "Failed to update budget.") #error handling
            return redirect('home')

        elif 'add_expense' in request.POST:
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                expense = expense_form.save(commit=False)
                expense.budget = budget
                expense.save() 
                budget.amount -= expense.amount #subtracts the expense from the budget
                budget.save()
            else:
                messages.error(request, "Failed to add expense.") #error handling
            return redirect('home')
        
        elif 'update_profile_pic' in request.POST:
            profile_form = ProfilePictureForm(request.POST, instance=budget)
            if profile_form.is_valid():
                profile_form.save()
            else:
                messages.error(request, "Failed to update profile picture.") #error handling
            return redirect('home')

    else:
        form = BudgetForm(instance=budget)
        expense_form = ExpenseForm()
        profile_form = ProfilePictureForm(instance=budget)

    expenses = Expense.objects.filter(budget=budget)
    return render(request, 'budget_app/home.html', {
        'expense_form': expense_form,
        'expenses': expenses,
        'form': form,
        'budget': budget,
        'profile_form': profile_form
    })


    

@login_required #makes sure only users are autorized to delete their expenses
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    budget = expense.budget
    expense.delete()
    budget.amount += expense.amount #adds the expense amount back to the budget
    budget.save()
    return redirect('home')