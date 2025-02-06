from django.contrib.auth.models import User
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

class AnnualExpense(models.Model):
    name = models.CharField(max_length=100)
    expense = models.BigIntegerField()
    category = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_annual_expenses')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='annual_expenses')

class MonthlyExpense(models.Model):
    name = models.CharField(max_length=100)
    expense = models.BigIntegerField()
    category = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_monthly_expenses')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='monthly_expenses')

class GeneralExpense(models.Model):
    name = models.CharField(max_length=100)
    expense = models.BigIntegerField()
    category = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_general_expenses')
    date = models.DateField(auto_now_add=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='general_expenses')

