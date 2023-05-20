import uuid

from django.contrib.auth.models import User
from django.db import models

from apps.transactions.constants import Type


class Transactions(models.Model):
    """
    Model representing a transaction
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    transaction_type = models.CharField(choices=Type.choices, max_length=10)
    transaction_id = models.IntegerField(null=True)
    date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "transactions"
