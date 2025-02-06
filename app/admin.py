from django.contrib import admin
from .models import Tag, AnnualExpense, MonthlyExpense, GeneralExpense

admin.site.register(Tag)
admin.site.register(AnnualExpense)
admin.site.register(MonthlyExpense)
admin.site.register(GeneralExpense)
