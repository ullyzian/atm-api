from rest_framework import serializers
from api.models import Customer, BankAccount, CreditCard, Operation


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "user", "phone", "adress"]


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ["id", "customer", "account", "balance"]


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = [
            "id",
            "number",
            "expiration",
            "account",
            "customer",
            "cvv",
            "pin",
            "kind",
        ]


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ["id", "customer", "reciever", "amount", "kind"]
