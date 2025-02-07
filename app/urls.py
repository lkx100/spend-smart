from django.urls import path
from . import views

urlpatterns = [
    path('login_page/', views.login_page, name="login_page"),
    path('signup_page/', views.signup_page, name="signup_page"),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name="home"),
    path('file_upload/', views.load_user_transactions, name="file_upload"),
    path('chatbot/', views.chatbot_dashboard, name="chatbot_dashboard"),
    path('transactions/', views.transactions, name="transactions"),
    path('process-message/', views.process_message, name='process_message'),
    path('budget/', views.budget_dashboard, name='budget_dashboard'),
    path('add-annual-expense/', views.add_annual_expense, name='add_annual_expense'),
    path('add-monthly-expense/', views.add_monthly_expense, name='add_monthly_expense'),
]
