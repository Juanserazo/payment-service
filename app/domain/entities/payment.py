from dataclasses import dataclass
from datetime import datetime

from app.domain.enums.payment_status import PaymentStatus


@dataclass
class Payment:
    id: str
    amount: float
    currency: str
    status: PaymentStatus
    provider_reference: str | None
    idempotency_key: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        payment_id: str,
        amount: float,
        currency: str,
        idempotency_key: str,
        created_at: datetime,
    ) -> "Payment":
        return cls(
            id=payment_id,
            amount=amount,
            currency=currency,
            status=PaymentStatus.PENDING,
            provider_reference=None,
            idempotency_key=idempotency_key,
            created_at=created_at,
            updated_at=created_at,
        )

    def approve(
        self,
        provider_reference: str,
        updated_at: datetime,
    ) -> None:
        self.status = PaymentStatus.APPROVED
        self.provider_reference = provider_reference
        self.updated_at = updated_at

    def decline(
        self,
        updated_at: datetime,
    ) -> None:
        self.status = PaymentStatus.DECLINED
        self.updated_at = updated_at

    def refund(
        self,
        updated_at: datetime,
    ) -> None:
        self.status = PaymentStatus.REFUNDED
        self.updated_at = updated_at