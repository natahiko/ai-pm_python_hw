from datetime import date, datetime

DATE_FORMAT = "%d.%m.%Y"


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str):
        if not (isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            # Відсіює й неіснуючі дати, як 31.02
            birthday = datetime.strptime(value, DATE_FORMAT).date()
        except (ValueError, TypeError):
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from None
        if birthday > date.today():
            raise ValueError("Birthday cannot be in the future.")
        super().__init__(birthday)

    def __str__(self):
        return self.value.strftime(DATE_FORMAT)
