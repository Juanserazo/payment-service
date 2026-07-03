from datetime import datetime

from pydantic import BaseModel, Field


class CreatePaymentRequest(BaseModel):
    amount: float = Field(gt=0)
    currency: str = Field(
        min_length=3,
        max_length=3,
    )


class RefundPaymentRequest(BaseModel):
    amount: float = Field(gt=0)


class PaymentResponse(BaseModel):
    id: str
    amount: float
    currency: str
    status: str
    provider_reference: str | None

    created_at: datetime
    updated_at: datetime