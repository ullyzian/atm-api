from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(blank=True)
    adress = models.CharField(max_length=70, blank=True)

    def __str__(self):
        return self.user.username


class BankAccount(models.Model):
    customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, blank=False, null=False
    )
    account = models.CharField(max_length=24, blank=False, null=False, unique=True)
    balance = models.FloatField(default=0.0, blank=False, null=False)

    def __str__(self):
        return self.account


class CreditCard(models.Model):
    number = models.CharField(max_length=16, blank=False, null=False, unique=True)
    expiration = models.DateField()
    account = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, blank=False, null=False
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=False, null=False
    )
    cvv = models.IntegerField(blank=False, null=False)
    pin = models.IntegerField(blank=False, null=False)
    kind = models.CharField(max_length=30)

    def __str__(self):
        return self.number


class Operation(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, blank=False, null=False
    )
    receiver = models.ForeignKey(
        BankAccount, on_delete=models.CASCADE, blank=False, null=False
    )
    amount = models.FloatField(default=1.0, blank=False, null=False)
    kind = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return self.customer.user.username
