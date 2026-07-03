from fastapi import APIRouter
from fastapi import Header
from fastapi import HTTPException
from fastapi import status

from app.config.dependencies import (
    CreatePaymentUseCaseDep,
    GetPaymentUseCaseDep,
    RefundPaymentUseCaseDep,
)
from app.domain.exceptions.payment_exceptions import (
    CardDeclinedException,
    InsufficientFundsException,
    InvalidRefundException,
    PaymentNotFoundException,
    ProviderTimeoutException,
)
from app.schemas.payment import (
    CreatePaymentRequest,
    PaymentResponse,
    RefundPaymentRequest,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)

@router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    request: CreatePaymentRequest,
    use_case: CreatePaymentUseCaseDep,
    idempotency_key: str = Header(
        ...,
        alias="Idempotency-Key",
    ),
):

    try:

        payment = await use_case.execute(
            amount=request.amount,
            currency=request.currency,
            idempotency_key=idempotency_key,
        )

        return PaymentResponse(
            **payment.__dict__
        )

    except CardDeclinedException:
        raise HTTPException(
            status_code=402,
            detail="Card declined",
        )

    except InsufficientFundsException:
        raise HTTPException(
            status_code=402,
            detail="Insufficient funds",
        )

    except ProviderTimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Provider timeout",
        )

@router.get(
    "/{payment_id}",
    response_model=PaymentResponse,
)
async def get_payment(
    payment_id: str,
    use_case: GetPaymentUseCaseDep,
):

    try:

        payment = await use_case.execute(
            payment_id
        )

        return PaymentResponse(
            **payment.__dict__
        )

    except PaymentNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )

@router.post(
    "/{payment_id}/refund",
    response_model=PaymentResponse,
)
async def refund_payment(
    payment_id: str,
    request: RefundPaymentRequest,
    use_case: RefundPaymentUseCaseDep,
):

    try:

        payment = await use_case.execute(
            payment_id=payment_id,
            amount=request.amount,
        )

        return PaymentResponse(
            **payment.__dict__
        )

    except PaymentNotFoundException:
        raise HTTPException(
            status_code=404,
            detail="Payment not found",
        )

    except InvalidRefundException:
        raise HTTPException(
            status_code=400,
            detail="Invalid refund",
        )