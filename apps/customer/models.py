from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F


class Profile(models.Model):
    """
    Model representing a user profile with associated balance.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def update_balance(self, balance):
        """
        Update the balance of the profile by adding the specified amount.
        """
        Profile.objects.select_for_update().filter(pk=self.pk).update(balance=F("balance") + balance)
