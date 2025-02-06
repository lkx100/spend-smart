from django.contrib.auth.models import User
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=100)

class AnnualExpense(models.Model):
    name = models.CharField(max_length=100)
    expense = models.BigIntegerField()
    category = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_annual_expenses')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='annual_expenses')

class MonthlyExpense(models.Model):
    name = models.CharField(max_length=100)
    expense = models.BigIntegerField()
    category = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_monthly_expenses')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='monthly_expenses')

class GeneralExpense(models.Model):
    name = models.CharField(max_length=100)
    expense = models.BigIntegerField()
    category = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_general_expenses')
    date = models.DateField(auto_now_add=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='general_expenses')

class Transaction(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.description} - {self.amount}"