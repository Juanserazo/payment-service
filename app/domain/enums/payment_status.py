from enum import Enum


class PaymentStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DECLINED = "declined"
    REFUNDED = "refunded"