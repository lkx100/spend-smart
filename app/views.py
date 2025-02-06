from django.shortcuts import render, redirect
from .models import AnnualExpense, MonthlyExpense
from .load_user_transactions import LoadTransactions
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .chat_agent import run_flow
from .models import Tag, GeneralExpense, MonthlyExpense, AnnualExpense
from django.contrib.auth.decorators import login_required
import random

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

@login_required(login_url='/login_page/')
def chatbot_dashboard(request):
    return render(request, 'chatbot_dashboard.html')
    
@login_required(login_url='/login_page/')
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
                tag_name = transaction.get('tag') or 'default'
                tag_obj, created = Tag.objects.get_or_create(name=tag_name.lower())
                # Create the GeneralExpense object
                GeneralExpense.objects.create(
                    date=transaction['date'],
                    name=transaction['name'],
                    expense=transaction['expense'],
                    category=transaction['category'] if transaction['category'] else 'None',
                    user=request.user,  # associate with the logged-in user
                    tag=tag_obj
                )
                print(type(transaction), transaction)

            if transactions and isinstance(transactions, list):
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


@login_required(login_url='/login_page/')
def transactions(request):
    all_transactions = GeneralExpense.objects.filter(user=request.user).order_by('-date')

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
                tag_name = transaction.get('tag') or 'default'
                tag_obj, created = Tag.objects.get_or_create(name=tag_name.lower())
                # Create the GeneralExpense object
                GeneralExpense.objects.create(
                    date=transaction['date'],
                    name=transaction['name'],
                    expense=transaction['expense'],
                    category=transaction['category'] if transaction['category'] else 'None',
                    user=request.user,  # associate with the logged-in user
                    tag=tag_obj
                )
                print(type(transaction), transaction)

            if transactions and isinstance(transactions, list):
                # Clean up the file
                fs.delete(file_path)

                transaction_list = []
                for exp in all_transactions:
                    transaction_list.append({
                        'amount': exp.expense,           
                        'date': str(exp.date),           
                        'category': exp.category,
                        'tag': exp.tag.name if exp.tag else ""
                    })

                balance = sum(t['amount'] for t in transaction_list)
                profit = sum(t['amount'] for t in transaction_list if t['amount'] > 0)
                expenses = sum(t['amount'] for t in transaction_list if t['amount'] < 0)

                context = {
                    'transactions': all_transactions,
                    'balance': balance,
                    'profit': profit,
                    'expenses': expenses,
                }
                return render(request, 'transactions.html', context)

                # return render(request, 'transactions.html', {
                #     'transactions': transactions,
                #     'transaction_count': len(transactions)
                # })
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
        
    return render(request, 'transactions.html')


def budget_dashboard(request):
    annual_expenses = AnnualExpense.objects.all()
    monthly_expenses = MonthlyExpense.objects.all()

    annual_expenses_values = [expense.expense for expense in annual_expenses]
    annual_expenses_labels = [expense.name for expense in annual_expenses]

    monthly_expenses_values = [expense.expense for expense in monthly_expenses]
    monthly_expenses_labels = [expense.name for expense in monthly_expenses]

    context = {
        'annual_expenses': annual_expenses,
        'monthly_expenses': monthly_expenses,
        'annual_expenses_values': annual_expenses_values,
        'annual_expenses_labels': annual_expenses_labels,
        'monthly_expenses_values': monthly_expenses_values,
        'monthly_expenses_labels': monthly_expenses_labels,
    }
    # print(annual_expenses_values)

    return render(request, 'budget_dashboard.html', context)