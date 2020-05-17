import datetime
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from api.models import Customer, BankAccount, CreditCard, Operation
from api.serializers import OperationSerializer


class CreditCardAuthToken(APIView):
    def post(self, request, *args, **kwargs):
        # get credentials information from post request
        card_number = request.data["card"]
        pin = request.data["pin"]

        # get card
        card = get_object_or_404(CreditCard, number=card_number)

        # expiration card validation
        if card.expiration < datetime.date.today():
            return Response({"detail": "This card is expired"})

        # pin validation
        if str(card.pin) == pin:
            # get user and create token
            customer = get_object_or_404(Customer, id=card.customer.id)
            user = get_object_or_404(User, pk=customer.user.id)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"detail": "Incorrect pin"})


class AccountList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # get all customers except customer that requested
        customers = Customer.objects.all().exclude(user=request.user.id)
        accounts = []
        # serialize accounts number
        for customer in customers:
            account = BankAccount.objects.get(customer=customer.id).account
            accounts.append(
                {
                    "label": " ".join(
                        account[i : i + 4] for i in range(0, len(account), 4)
                    ),
                    "id": account,
                }
            )
        return Response(accounts)


class Withdraw(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, num, format=None):
        amount = request.data["amount"]
        # amount parsing
        if len(amount) == 0:
            return Response({"detail": "Inccorect amount"})
        amount = float(amount)

        # get and check customer requested info
        card = get_object_or_404(CreditCard, number=num)
        user = get_object_or_404(User, username=request.user)
        account = get_object_or_404(BankAccount, pk=card.account.id, customer=user.id)

        # balance validation
        if account.balance > amount:

            # update balance
            account.balance = account.balance - amount
            account.save()
            Operation.objects.create(
                customer=account.customer, amount=amount, kind="Withdraw",
            )
            return Response({"message": "Operation completed"})
        else:
            return Response({"detail": "Not enough funds on the balance"})


class Transfer(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, num, format=None):
        receiver = request.data["receiver"]
        # amount parsing
        amount = request.data["amount"]
        if len(amount) == 0:
            return Response({"detail": "Inccorect amount"})
        amount = float(amount)

        # get and check customer requested info
        card = get_object_or_404(CreditCard, number=num)
        user = get_object_or_404(User, username=request.user)
        account = get_object_or_404(BankAccount, pk=card.account.id, customer=user.id)

        # get and check reciever account number
        receiver_account = get_object_or_404(BankAccount, account=receiver)

        # balance validation
        if account.balance > amount:

            # update balance for customer and receiver
            account.balance -= amount
            receiver_account.balance += amount
            account.save()
            receiver_account.save()

            # create operation
            Operation.objects.create(
                customer=account.customer,
                receiver=receiver_account,
                amount=amount,
                kind="Transfer",
            )
            return Response({"message": "Operation completed"})
        else:
            return Response({"detail": "Not enough funds on the balance"})


class Balance(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, num, *args, **kwargs):
        # get and check customer requested info
        card = get_object_or_404(CreditCard, number=num)
        user = get_object_or_404(User, username=request.user)
        account = get_object_or_404(BankAccount, pk=card.account.id, customer=user.id)

        return Response({"balance": account.balance})


class History(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, num, *args, **kwargs):
        # get and check customer requested info
        customer = get_object_or_404(Customer, user=request.user.id)
        # get all operations and order by latest
        operations = Operation.objects.filter(customer=customer).order_by(
            "-created_at", "-pk"
        )[0:8]
        serializer = OperationSerializer(operations, many=True)
        return Response(serializer.data)
