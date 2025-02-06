from django.shortcuts import render, redirect
from .load_user_transactions import LoadTransactions
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .chat_agent import run_flow

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

def logout_view(request):
    logout(request)
    return redirect('home')

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

def logout_page(request):
    logout(request)
    return render(request, 'login.html')

def load_user_transactions(request):
    if request.method == "POST" and request.FILES['file']:
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        file_path = fs.save(uploaded_file.name, uploaded_file)

        load_user_transactions = LoadTransactions()
        transactions_json = load_user_transactions.filter_extract(file_path)

        print(transactions_json)

        return render(request, 'success.html')
    return render(request, 'upload.html')
        
def process_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = run_flow(message)
        # Create a dictionary wrapper for the response
        # responseText = response['outputs'][0]['outputs'][0]['results']['message']['data']['text']
        # print("Response Text:", responseText)
        response_data = {
            'response': response
        }
        print(response_data)
        return JsonResponse(response_data)