from rest_framework import serializers
from api.models import Customer, BankAccount, Operation


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "user"]


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ["id", "customer", "account"]


class OperationSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    receiver = BankAccountSerializer()

    class Meta:
        model = Operation
        fields = ["id", "customer", "receiver", "amount", "kind"]
