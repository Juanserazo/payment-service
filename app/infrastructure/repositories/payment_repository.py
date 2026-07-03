from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.payment import Payment
from app.domain.ports.payment_repository_port import (
    PaymentRepositoryPort,
)
from app.infrastructure.database.models.payment_model import (
    PaymentModel,
)
from app.infrastructure.repositories.payment_mapper import (
    to_entity,
    to_model,
)


class SqlAlchemyPaymentRepository(
    PaymentRepositoryPort
):
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

    async def save(
        self,
        payment: Payment,
    ) -> Payment:
        model = to_model(payment)

        self.session.add(model)

        await self.session.commit()
        await self.session.refresh(model)

        return to_entity(model)

    async def get_by_id(
        self,
        payment_id: str,
    ) -> Payment | None:
        model = await self.session.get(
            PaymentModel,
            payment_id,
        )

        return (
            to_entity(model)
            if model
            else None
        )

    async def get_by_idempotency_key(
        self,
        idempotency_key: str,
    ) -> Payment | None:
        stmt = select(
            PaymentModel
        ).where(
            PaymentModel.idempotency_key
            == idempotency_key
        )

        result = await self.session.execute(
            stmt
        )

        model = result.scalar_one_or_none()

        return (
            to_entity(model)
            if model
            else None
        )

    async def update(
        self,
        payment: Payment,
    ) -> Payment:
        stmt = select(
            PaymentModel
        ).where(
            PaymentModel.id == payment.id
        )

        result = await self.session.execute(
            stmt
        )

        model = result.scalar_one()

        model.status = payment.status.value
        model.provider_reference = (
            payment.provider_reference
        )
        model.updated_at = payment.updated_at

        await self.session.commit()
        await self.session.refresh(model)

        return to_entity(model)