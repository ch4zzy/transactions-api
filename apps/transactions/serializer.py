from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import ValidationError

from apps.transactions.constants import Type
from apps.transactions.models import Transactions
from apps.transactions.utils import create_operation_and_update_balance


class BaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for common validation methods.
    """

    def validate_user(self, value):
        """
        Validate the user associated with the transaction.
        """
        if not User.objects.filter(id=value).exists():
            if settings.DEBUG:
                raise ValidationError("User does not exist")
        return value


class TransactionsListSerializer(serializers.ModelSerializer):
    transaction_type = serializers.SerializerMethodField()

    class Meta:
        model = Transactions
        fields = (
            "id",
            "transaction_id",
            "date",
            "amount",
            "balance",
            "transaction_type",
        )

    @staticmethod
    def get_transaction_type(obj):
        return obj.get_kind_display()


class TransactionsSerializer(BaseSerializer):
    user_id = serializers.IntegerField()
    transaction_id = serializers.IntegerField()
    date = serializers.DateTimeField(default=datetime.now)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Transactions
        fields = ("user_id", "transaction_id", "date", "amount")

    def create(self, validated_data):
        user = User.objects.get(id=validated_data["user_id"])

        if validated_data["amount"] > 0:
            transaction_type = Type.PURCHASE
        else:
            transaction_type = Type.REFUND

        operation = Transactions.objects.filter(transaction_id=validated_data["transaction_id"]).last()

        if operation:
            return operation

        with transaction.atomic():
            balance_after_transaction = user.profile.balance + validated_data["amount"]
            if settings.DEBUG:
                if transaction_type == Type.REFUND and balance_after_transaction < 0:
                    raise ValidationError("Balance cannot be negative")

            operation = create_operation_and_update_balance(
                {
                    "amount": validated_data["amount"],
                    "date": validated_data["date"],
                    "transaction_id": validated_data["transaction_id"],
                    "user": user,
                    "transaction_type": transaction_type,
                    "balance": balance_after_transaction,
                }
            )
        return operation


class WithdrawalsSerializer(BaseSerializer):
    """ """

    user_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateTimeField(default=datetime.now)

    class Meta:
        model = Transactions
        fields = ("user_id", "amount", "date")

    def create(self, validated_data):
        user = User.objects.get(id=validated_data["user_id"])
        transaction_type = Type.WITHDRAWAL
        amount = validated_data["amount"]

        with transaction.atomic():
            balance_after_withdrawal = user.profile.balance - amount
            if settings.DEBUG:
                if transaction_type == Type.WITHDRAWAL and balance_after_withdrawal < 0:
                    raise ValidationError("Balance cannot be negative")

            operation = create_operation_and_update_balance(
                {
                    "amount": -amount,
                    "date": validated_data["date"],
                    "user": user,
                    "transaction_type": transaction_type,
                    "balance": balance_after_withdrawal,
                }
            )

        return operation
