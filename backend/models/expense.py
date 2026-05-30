class Expense:
    def __init__(self, title, amount, category, date):
        self.title = title
        self.amount = float(amount)
        self.category = category
        self.date = date

    def to_dict(self):
        return {
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "date": self.date
        }

    @staticmethod
    def validate(data):
        required_fields = ["title", "amount", "category", "date"]

        for field in required_fields:
            if field not in data:
                return False

        return True