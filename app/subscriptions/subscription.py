class Subscription:
    def __init__(self, startDate: int, endDate: int):
        self.startDate = startDate
        self.endDate = endDate

    def length(self) -> int:
        return self.endDate - self.startDate
