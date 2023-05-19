from rest_framework import serializers

from apps.customer.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.
    """
    class Meta:
        model = Profile
        fields = ["user", "balance"]
