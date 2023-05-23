from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from apps.transactions.models import Transactions
from apps.transactions.serializer import TransactionsSerializer, WithdrawalsSerializer


class TransactionsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet for return list of user financial operations with pagination
    """

    serializer_class = TransactionsSerializer

    def get_queryset(self):
        """
        List of all transactions for request user.
        """
        return Transactions.objects.filter(user=self.request.user).order_by("-date")


class TransactionAPIView(CreateAPIView):
    """
    API view for process transaction request from 3-rd party systems
    """

    permission_classes = (AllowAny,)
    serializer_class = TransactionsSerializer


class WithdrawalsAPIView(CreateAPIView):
    """
    API view for process user withdrawal operations.
    """

    serializer_class = WithdrawalsSerializer
