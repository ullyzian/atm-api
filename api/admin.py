from django.contrib import admin
from api.models import Customer, BankAccount, CreditCard, Operation

# Register your models here.
admin.site.register(Customer)
admin.site.register(BankAccount)
admin.site.register(CreditCard)
admin.site.register(Operation)
