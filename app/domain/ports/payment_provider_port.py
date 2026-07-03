from abc import ABC
from abc import abstractmethod


class PaymentProviderPort(
    ABC
):

    @abstractmethod
    async def charge(
        self,
        amount: float,
        currency: str,
    ) -> dict:
        pass

    @abstractmethod
    async def refund(
        self,
        provider_reference: str,
        amount: float,
    ) -> dict:
        pass