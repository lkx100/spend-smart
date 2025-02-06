from django.urls import path
from . import views
from . import views

urlpatterns = [
    path('login_page/', views.login_page, name="login_page"),
    path('signup_page/', views.signup_page, name="signup_page"),
    path('logout_page/', views.login_page, name="login_page"),
    path('', views.home, name="home"),
    path('file_upload/', views.load_user_transactions, name="file_upload"),
    path('chatbot/', views.chatbot_dashboard, name="chatbot_dashboard"),
    path('logout/', views.logout_view, name='logout'),
]
