from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from api.models import Customer, BankAccount, CreditCard, Operation
from api.serializers import CreditCardSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class CreditCardAuthToken(APIView):
    def post(self, request, *args, **kwargs):
        card_number = request.data["card"]
        pin = request.data["pin"]
        card = get_object_or_404(CreditCard, number=card_number)
        serializer = CreditCardSerializer(card).data
        if serializer.pin == pin:
            customer = get_object_or_404(Customer, id=serializer.customer)
            user = get_object_or_404(User, pk=customer.user.id)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"message": "Incorrect pin"})


class CreditCardDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, num, format=None):
        card = self.get_object_or_404(num)
        serializer = CreditCardSerializer(card)
        return Response(serializer.data)
