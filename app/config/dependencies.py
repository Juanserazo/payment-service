from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.create_payment import (
    CreatePaymentUseCase,
)
from app.application.use_cases.get_payment import (
    GetPaymentUseCase,
)
from app.application.use_cases.refund_payment import (
    RefundPaymentUseCase,
)
from app.domain.ports.payment_provider_port import (
    PaymentProviderPort,
)
from app.domain.ports.payment_repository_port import (
    PaymentRepositoryPort,
)
from app.infrastructure.database.session import (
    get_session,
)
from app.infrastructure.providers.mock_payment_provider import (
    MockPaymentProvider,
)
from app.infrastructure.repositories.payment_repository import (
    SqlAlchemyPaymentRepository,
)


def get_payment_repository(
    session: AsyncSession = Depends(
        get_session,
    ),
) -> PaymentRepositoryPort:
    return SqlAlchemyPaymentRepository(
        session=session,
    )


def get_payment_provider(
) -> PaymentProviderPort:
    return MockPaymentProvider()


def get_create_payment_use_case(
    repository: PaymentRepositoryPort = Depends(
        get_payment_repository,
    ),
    provider: PaymentProviderPort = Depends(
        get_payment_provider,
    ),
) -> CreatePaymentUseCase:
    return CreatePaymentUseCase(
        repository=repository,
        provider=provider,
    )


def get_get_payment_use_case(
    repository: PaymentRepositoryPort = Depends(
        get_payment_repository,
    ),
) -> GetPaymentUseCase:
    return GetPaymentUseCase(
        repository=repository,
    )


def get_refund_payment_use_case(
    repository: PaymentRepositoryPort = Depends(
        get_payment_repository,
    ),
    provider: PaymentProviderPort = Depends(
        get_payment_provider,
    ),
) -> RefundPaymentUseCase:
    return RefundPaymentUseCase(
        repository=repository,
        provider=provider,
    )


CreatePaymentUseCaseDep = Annotated[
    CreatePaymentUseCase,
    Depends(get_create_payment_use_case),
]

GetPaymentUseCaseDep = Annotated[
    GetPaymentUseCase,
    Depends(get_get_payment_use_case),
]

RefundPaymentUseCaseDep = Annotated[
    RefundPaymentUseCase,
    Depends(get_refund_payment_use_case),
]