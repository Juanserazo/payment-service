from app.domain.entities.payment import Payment
from app.domain.enums.payment_status import PaymentStatus
from app.infrastructure.database.models.payment_model import (
    PaymentModel,
)


def to_entity(
    model: PaymentModel,
) -> Payment:
    return Payment(
        id=model.id,
        amount=model.amount,
        currency=model.currency,
        status=PaymentStatus(model.status),
        provider_reference=model.provider_reference,
        idempotency_key=model.idempotency_key,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def to_model(
    entity: Payment,
) -> PaymentModel:
    return PaymentModel(
        id=entity.id,
        amount=entity.amount,
        currency=entity.currency,
        status=entity.status.value,
        provider_reference=entity.provider_reference,
        idempotency_key=entity.idempotency_key,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )