from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.customer.models import Profile
from apps.customer.serializer import ProfileSerializer


class ProfileBalanceView(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for retrieving the current balance of a user profile.
    """

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @action(detail=True, methods=["get"], url_path="balance")
    def get_balance(self, request, pk=None):
        """
        Retrieves the current balance of the user profile.
        """
        try:
            profile = self.get_object()
            balance = profile.balance
            return Response({"balance": balance})
        except Profile.DoesNotExist:
            return Response({"error": "Profile does not exist"})
