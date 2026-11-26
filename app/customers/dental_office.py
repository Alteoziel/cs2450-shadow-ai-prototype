from app.customers.customer import Customer
from app.subscriptions.subscription import Subscription


class DentalOffice(Customer):
    def __init__(self, name: str, dentalId: str, allowed: bool = True):
        super().__init__(name, allowed)
        self.dentalId = dentalId
        self.subscription = Subscription(0, 365)
