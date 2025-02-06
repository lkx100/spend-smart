from django.shortcuts import render, redirect
from .load_user_transactions import LoadTransactions
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Tag, GeneralExpense, MonthlyExpense, AnnualExpense

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

def logout_page(request):
    logout(request)
    return render(request, 'login.html')

def load_user_transactions(request):
    if request.method == "POST" and request.FILES['file']:
        try:
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            file_path = fs.save(uploaded_file.name, uploaded_file)

            full_path = fs.path(file_path)

            load_user_transactions = LoadTransactions()
            transactions = load_user_transactions.filter_extract(full_path)
            # Debug prints
            # print("Extracted transactions:", transactions)
            # print("Type:", type(transactions))

            for transaction in transactions:
                # Clean and validate the transaction data
                # cleaned = load_user_transactions.clean_transaction(transaction)
                
                # Get or create the tag object from the Tag model
                # tag_obj, created = Tag.objects.get_or_create(name=cleaned.get('tag').lower())
                
                # Create the GeneralExpense object
                GeneralExpense.objects.create(
                    date=transaction['date'],
                    name=transaction['name'],
                    expense=transaction['expense'],
                    category=transaction['category'],
                    user=request.user,  # associate with the logged-in user
                    tag=transaction
                )
                print(type(transaction), transaction)

            if transactions and isinstance(transactions, list):
                # Here you can save to your database
                
                # Clean up the file
                fs.delete(file_path)
                return render(request, 'success.html', {
                    'transactions': transactions,
                    'transaction_count': len(transactions)
                })
            else:
                messages.error(request, "Failed to extract valid transactions from the file")
                return render(request, 'upload.html')
        
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return render(request, 'upload.html')
        
        finally:
            # Ensure file cleanup happens even if there's an error
            if 'file_path' in locals():
                fs.delete(file_path)
        
    return render(request, 'upload.html')
        
