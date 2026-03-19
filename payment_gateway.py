"""
payment_gateway.py

A simple payment gateway integration module.
Supports basic payment processing, refund handling,
and transaction status checks.

NOTE: This is a mock implementation for testing/demo purposes.
"""

import uuid
import time
from enum import Enum


class PaymentStatus(Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"
    REFUNDED = "refunded"


class PaymentGatewayError(Exception):
    """Custom exception for payment gateway errors."""
    pass


class PaymentGateway:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API key is required")
        self.api_key = api_key

    def _simulate_network_delay(self):
        time.sleep(0.5)

    def _generate_transaction_id(self) -> str:
        return str(uuid.uuid4())

    def process_payment(self, amount: float, currency: str, source: str) -> dict:
        """
        Process a payment.

        :param amount: Payment amount
        :param currency: Currency code (e.g., USD)
        :param source: Payment source (e.g., card token)
        :return: Transaction details
        """
        if amount <= 0:
            raise PaymentGatewayError("Invalid payment amount")

        if not source:
            raise PaymentGatewayError("Payment source is required")

        self._simulate_network_delay()

        transaction_id = self._generate_transaction_id()

        # Mock logic: approve payments under 1000, fail otherwise
        if amount < 1000:
            status = PaymentStatus.SUCCESS
        else:
            status = PaymentStatus.FAILED

        return {
            "transaction_id": transaction_id,
            "amount": amount,
            "currency": currency,
            "status": status.value,
            "timestamp": int(time.time())
        }

    def refund_payment(self, transaction_id: str, amount: float) -> dict:
        """
        Refund a payment.

        :param transaction_id: Original transaction ID
        :param amount: Refund amount
        :return: Refund details
        """
        if not transaction_id:
            raise PaymentGatewayError("Transaction ID is required")

        if amount <= 0:
            raise PaymentGatewayError("Invalid refund amount")

        self._simulate_network_delay()

        return {
            "transaction_id": transaction_id,
            "refund_id": self._generate_transaction_id(),
            "amount": amount,
            "status": PaymentStatus.REFUNDED.value,
            "timestamp": int(time.time())
        }

    def get_transaction_status(self, transaction_id: str) -> dict:
        """
        Retrieve transaction status.

        :param transaction_id: Transaction ID
        :return: Status details
        """
        if not transaction_id:
            raise PaymentGatewayError("Transaction ID is required")

        self._simulate_network_delay()

        # Mock random status behavior
        statuses = [
            PaymentStatus.SUCCESS,
            PaymentStatus.PENDING,
            PaymentStatus.FAILED
        ]

        status = statuses[hash(transaction_id) % len(statuses)]

        return {
            "transaction_id": transaction_id,
            "status": status.value,
            "checked_at": int(time.time())
        }


# Example usage (for testing)
if __name__ == "__main__":
    gateway = PaymentGateway(api_key="test_api_key_123")

    payment = gateway.process_payment(
        amount=150.0,
        currency="USD",
        source="card_visa_123"
    )
    print("Payment:", payment)

    status = gateway.get_transaction_status(payment["transaction_id"])
    print("Status:", status)

    refund = gateway.refund_payment(
        transaction_id=payment["transaction_id"],
        amount=150.0
    )
    print("Refund:", refund)
