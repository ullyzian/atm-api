from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import Http404
from api.models import Customer, BankAccount, CreditCard, Operation


class CreditCardDetail(APIView):
    def get_object(self, pk):
        try:
            return CreditCard.objects.get(pk=pk)
        except CreditCard.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        card = self.get_object(pk)
