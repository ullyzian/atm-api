from django.urls import path
from api.views import CreditCardDetail, CreditCardAuthToken

urlpatterns = [
    path("cards/<str:num>", CreditCardDetail.as_view(), name="card_detail"),
    path("auth/", CreditCardAuthToken.as_view(), name="auth"),
]
