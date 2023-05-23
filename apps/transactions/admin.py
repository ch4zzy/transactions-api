from django.contrib import admin

from apps.transactions.models import Transactions


@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "transaction_id",
        "transaction_type",
        "date",
        "amount",
        "balance",
        "user",
    )
