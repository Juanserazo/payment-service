from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from app.application.use_cases.create_payment import (
    CreatePaymentUseCase,
)
from app.domain.entities.payment import Payment
from app.domain.enums.payment_status import (
    PaymentStatus,
)


@pytest.mark.asyncio
async def test_create_payment_success():

    repository = AsyncMock()
    provider = AsyncMock()

    provider.charge.return_value = {
        "provider_reference": "provider-ref-123"
    }

    repository.get_by_idempotency_key.return_value = None

    repository.save.side_effect = (
        lambda payment: payment
    )

    use_case = CreatePaymentUseCase(
        repository=repository,
        provider=provider,
    )

    payment = await use_case.execute(
        amount=100,
        currency="USD",
        idempotency_key="key-123",
    )

    assert payment.amount == 100
    assert payment.currency == "USD"
    assert payment.status == PaymentStatus.APPROVED
    assert payment.provider_reference == (
        "provider-ref-123"
    )

    repository.save.assert_called_once()