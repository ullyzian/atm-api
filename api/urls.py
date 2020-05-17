from django.urls import path
from api.views import (
    CreditCardAuthToken,
    Withdraw,
    Transfer,
    Balance,
    History,
    AccountList,
)

urlpatterns = [
    path("auth/", CreditCardAuthToken.as_view(), name="auth"),
    path("cards/<str:num>/withdraw/", Withdraw.as_view(), name="card_withdraw"),
    path("cards/<str:num>/transfer/", Transfer.as_view(), name="card_transfer"),
    path("cards/<str:num>/balance/", Balance.as_view(), name="card_balance"),
    path("cards/<str:num>/history/", History.as_view(), name="card_history"),
    path("accounts/", AccountList.as_view(), name="accounts"),
]
