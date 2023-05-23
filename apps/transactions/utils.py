from apps.transactions.models import Transactions


def create_operation_and_update_balance(operation_data):
    """
    Method for create financial operation and update customer current balance.
    """
    user = operation_data["user"]
    amount = operation_data["amount"]
    financial_operation = Transactions.objects.create(**operation_data)
    user.profile.update_balance(amount)
    return financial_operation
