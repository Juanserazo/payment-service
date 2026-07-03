from datetime import UTC, datetime
from uuid import uuid4

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.domain.entities.payment import Payment
from app.domain.exceptions.payment_exceptions import (
    CardDeclinedException,
    InsufficientFundsException,
    ProviderTimeoutException,
)
from app.domain.ports.payment_provider_port import (
    PaymentProviderPort,
)
from app.domain.ports.payment_repository_port import (
    PaymentRepositoryPort,
)


class CreatePaymentUseCase:

    def __init__(
        self,
        repository: PaymentRepositoryPort,
        provider: PaymentProviderPort,
    ):
        self.repository = repository
        self.provider = provider

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(
            multiplier=1,
            min=1,
            max=8,
        ),
        retry=retry_if_exception_type(
            ProviderTimeoutException,
        ),
        reraise=True,
    )
    async def _charge_provider(
        self,
        amount: float,
        currency: str,
    ) -> dict:
        return await self.provider.charge(
            amount=amount,
            currency=currency,
        )

    async def execute(
        self,
        amount: float,
        currency: str,
        idempotency_key: str,
    ) -> Payment:

        existing_payment = (
            await self.repository.get_by_idempotency_key(
                idempotency_key
            )
        )

        if existing_payment:
            return existing_payment

        now = datetime.now(UTC)

        payment = Payment.create(
            payment_id=str(uuid4()),
            amount=amount,
            currency=currency,
            idempotency_key=idempotency_key,
            created_at=now,
        )

        await self.repository.save(payment)

        try:

            provider_response = (
                await self._charge_provider(
                    amount=amount,
                    currency=currency,
                )
            )

            payment.approve(
                provider_reference=provider_response[
                    "provider_reference"
                ],
                updated_at=datetime.now(UTC),
            )

        except (
            CardDeclinedException,
            InsufficientFundsException,
        ):

            payment.decline(
                updated_at=datetime.now(UTC),
            )

            await self.repository.update(
                payment
            )

            raise

        await self.repository.update(
            payment
        )

        return payment