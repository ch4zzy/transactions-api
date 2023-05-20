from django.db.models import TextChoices

class Type(TextChoices):
    PURCHASE = "PURCHASE", "Transaction:Purchase"
    REFUND = "REFUND", "Transaction:Refund"
    WITHDRAWAL = "WITHDRAWAL", "Withdrawal"
