class Expense:
    def __init__(self, title, amount, category, date, user_email):
        self.title = title
        self.amount = float(amount)
        self.category = category
        self.date = date
        self.user_email = user_email.lower()

    def to_dict(self):
        return {
            "title": self.title,
            "amount": self.amount,
            "category": self.category,
            "date": self.date,
            "user_email": self.user_email
        }

    @staticmethod
    def validate(data):
        required_fields = ["title", "amount", "category", "date", "user_email"]

        for field in required_fields:
            if field not in data:
                return False

        return True
