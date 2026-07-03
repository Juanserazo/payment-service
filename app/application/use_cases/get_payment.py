from app.domain.exceptions.payment_exceptions import (
    PaymentNotFoundException,
)
from app.domain.ports.payment_repository_port import (
    PaymentRepositoryPort,
)


class GetPaymentUseCase:

    def __init__(
        self,
        repository: PaymentRepositoryPort,
    ):
        self.repository = repository

    async def execute(
        self,
        payment_id: str,
    ):
        payment = await self.repository.get_by_id(
            payment_id
        )

        if not payment:
            raise PaymentNotFoundException()

        return payment