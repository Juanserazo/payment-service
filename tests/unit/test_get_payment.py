from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from app.application.use_cases.get_payment import (
    GetPaymentUseCase,
)
from app.domain.entities.payment import Payment
from app.domain.enums.payment_status import (
    PaymentStatus,
)
from app.domain.exceptions.payment_exceptions import (
    PaymentNotFoundException,
)


@pytest.mark.asyncio
async def test_get_payment_success():

    repository = AsyncMock()

    repository.get_by_id.return_value = (
        Payment(
            id="payment-1",
            amount=100,
            currency="USD",
            status=PaymentStatus.APPROVED,
            provider_reference="ref-1",
            idempotency_key="key-1",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
    )

    use_case = GetPaymentUseCase(
        repository=repository,
    )

    payment = await use_case.execute(
        "payment-1"
    )

    assert payment.id == "payment-1"


@pytest.mark.asyncio
async def test_get_payment_not_found():

    repository = AsyncMock()

    repository.get_by_id.return_value = None

    use_case = GetPaymentUseCase(
        repository=repository,
    )

    with pytest.raises(
        PaymentNotFoundException
    ):
        await use_case.execute(
            "invalid-id"
        )