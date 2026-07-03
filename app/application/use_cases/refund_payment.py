from datetime import UTC, datetime

from app.domain.exceptions.payment_exceptions import (
    InvalidRefundException,
    PaymentNotFoundException,
)
from app.domain.ports.payment_provider_port import (
    PaymentProviderPort,
)
from app.domain.ports.payment_repository_port import (
    PaymentRepositoryPort,
)
from app.domain.entities.payment import Payment


class RefundPaymentUseCase:

    def __init__(
        self,
        repository: PaymentRepositoryPort,
        provider: PaymentProviderPort,
    ):
        self.repository = repository
        self.provider = provider

    async def execute(
        self,
        payment_id: str,
        amount: float,
    ) -> Payment:

        payment = await self.repository.get_by_id(
            payment_id
        )

        if not payment:
            raise PaymentNotFoundException(
                f"Payment {payment_id} not found"
            )

        if amount > payment.amount:
            raise InvalidRefundException(
                "Refund amount cannot exceed original payment amount"
            )

        await self.provider.refund(
            provider_reference=payment.provider_reference,
            amount=amount,
        )

        payment.refund(
            updated_at=datetime.now(
                UTC
            )
        )

        await self.repository.update(
            payment
        )

        return payment