import asyncio
import uuid

from app.domain.exceptions.payment_exceptions import (
    CardDeclinedException,
    InsufficientFundsException,
    ProviderTimeoutException,
)
from app.domain.ports.payment_provider_port import (
    PaymentProviderPort,
)


class MockPaymentProvider(
    PaymentProviderPort
):

    async def charge(
        self,
        amount: float,
        currency: str,
    ) -> dict:

        await asyncio.sleep(0.2)

        if amount == 400:
            raise CardDeclinedException(
                "Card declined"
            )

        if amount == 500:
            raise ProviderTimeoutException(
                "Provider timeout"
            )

        if amount == 600:
            raise InsufficientFundsException(
                "Insufficient funds"
            )

        return {
            "status": "approved",
            "provider_reference": str(
                uuid.uuid4()
            ),
        }

    async def refund(
        self,
        provider_reference: str,
        amount: float,
    ) -> dict:

        await asyncio.sleep(0.2)

        return {
            "status": "refunded",
            "provider_reference": provider_reference,
        }