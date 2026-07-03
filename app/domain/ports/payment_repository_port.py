from abc import ABC, abstractmethod

from app.domain.entities.payment import Payment


class PaymentRepositoryPort(ABC):

    @abstractmethod
    async def save(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    async def get_by_id(
            self,
            payment_id: str,
    ) -> Payment | None:
        pass

    @abstractmethod
    async def get_by_idempotency_key(
        self,
        idempotency_key: str,
    ) -> Payment | None:
        pass

    @abstractmethod
    async def update(
        self,
        payment: Payment,
    ) -> Payment:
        pass