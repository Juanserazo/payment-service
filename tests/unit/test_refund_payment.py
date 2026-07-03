from datetime import datetime, timezone
from unittest.mock import AsyncMock

import pytest

from app.application.use_cases.refund_payment import (
    RefundPaymentUseCase,
)
from app.domain.entities.payment import Payment
from app.domain.enums.payment_status import (
    PaymentStatus,
)
from app.domain.exceptions.payment_exceptions import (
    PaymentNotFoundException,
)


@pytest.mark.asyncio
async def test_refund_payment_success():

    repository = AsyncMock()
    provider = AsyncMock()

    payment = Payment(
        id="payment-1",
        amount=100,
        currency="USD",
        status=PaymentStatus.APPROVED,
        provider_reference="provider-ref",
        idempotency_key="key-1",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    repository.get_by_id.return_value = payment
    repository.update.side_effect = (
        lambda payment: payment
    )

    use_case = RefundPaymentUseCase(
        repository=repository,
        provider=provider,
    )

    result = await use_case.execute(
        payment_id="payment-1",
        amount=100,
    )

    assert (
        result.status
        == PaymentStatus.REFUNDED
    )

    repository.update.assert_called_once()


@pytest.mark.asyncio
async def test_refund_payment_not_found():

    repository = AsyncMock()
    provider = AsyncMock()

    repository.get_by_id.return_value = None

    use_case = RefundPaymentUseCase(
        repository=repository,
        provider=provider,
    )

    with pytest.raises(
        PaymentNotFoundException
    ):
        await use_case.execute(
            payment_id="invalid-id",
            amount=100,
        )