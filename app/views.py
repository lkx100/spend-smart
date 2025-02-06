from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

def signup_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # filter the user from User model
        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request, f"{username} already taken!")
            return redirect('login_page')
        else:
            user = User.objects.create(
                first_name = first_name,
                last_name = lastName,
                username = username,
                email = email,
                # password can't be set directly, as it would not encrypt it & remain as raw str!
            )
            # Django's set_password method encrypts the password
            user.set_password(password)
            user.save()  # Save the user to the database
            messages.info(request, f"Account created successfully")

    return render(request, 'signup.html')

def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.all().filter(username=username).exists():
            validUser = authenticate(username=username, password=password)
            if validUser:
                login(request, validUser)   # Add user to a session
                return redirect("home")
            else:
                messages.info(request, f"Invalid Password, Try Again")
        else:
            messages.info(request, f"username \"{username}\" Not found")

    return render(request, 'login.html')


def home(request):
    return render(request, 'index.html')

def chatbot_dashboard(request):
    return render(request, 'chatbot_dashboard.html')


def transactions(request):
    # Dummy Data
    transactions = [
        {'id': 1, 'description': 'Salary', 'amount': 5000, 'date': '2023-10-01'},
        {'id': 2, 'description': 'Groceries', 'amount': -150, 'date': '2023-10-02'},
        {'id': 3, 'description': 'Electricity Bill', 'amount': -100, 'date': '2023-10-03'},
        {'id': 4, 'description': 'Internet Bill', 'amount': -50, 'date': '2023-10-04'},
        {'id': 5, 'description': 'Freelance Work', 'amount': 800, 'date': '2023-10-05'},
    ]

    balance = sum(t['amount'] for t in transactions)
    profit = sum(t['amount'] for t in transactions if t['amount'] > 0)
    expenses = sum(t['amount'] for t in transactions if t['amount'] < 0)

    context = {
        'transactions': transactions,
        'balance': balance,
        'profit': profit,
        'expenses': expenses,
    }
    return render(request, 'transactions.html', context)