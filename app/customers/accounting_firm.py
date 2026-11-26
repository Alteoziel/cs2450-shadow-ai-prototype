from app.customers.customer import Customer


class AccountingFirm(Customer):
    """Present so the class diagram has this subclass. The firm path is not built."""

    def __init__(self, name: str, firmId: str, allowed: bool = True):
        super().__init__(name, allowed)
        self.firmId = firmId
