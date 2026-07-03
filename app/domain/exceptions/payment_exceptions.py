class PaymentException(Exception):
    pass


class PaymentNotFoundException(PaymentException):
    pass


class CardDeclinedException(PaymentException):
    pass


class InsufficientFundsException(PaymentException):
    pass


class ProviderTimeoutException(PaymentException):
    pass


class InvalidRefundException(PaymentException):
    pass