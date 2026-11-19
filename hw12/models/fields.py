import re
from datetime import date, datetime
from typing import Any

DATE_FORMAT = "%d.%m.%Y"
PHONE_LENGTH = 10
COUNTRY_CODE = "38"


# Пробіли, дефіси й дужки: "(066) 377-85-32" -> "0663778532"
def _strip_separators(value: str) -> str:
    return re.sub(r"[\s()-]", "", value)


# +380661234567 / 380661234567 -> 0661234567
def normalize_phone(value: str) -> str:
    if not isinstance(value, str):
        return value
    value = _strip_separators(value)
    if value.startswith("+" + COUNTRY_CODE):
        value = value[1:]
    if value.startswith(COUNTRY_CODE) and len(value) == len(COUNTRY_CODE) + PHONE_LENGTH:
        value = value[len(COUNTRY_CODE):]
    return value


# Чи вже набрано повний номер: 10 цифр або 12 з кодом країни
def is_full_phone(value: str) -> bool:
    digits = _strip_separators(value).lstrip("+")
    if not digits.isdigit():
        return False
    if digits.startswith(COUNTRY_CODE):
        return len(digits) == len(COUNTRY_CODE) + PHONE_LENGTH
    return len(digits) == PHONE_LENGTH


class Field:
    def __init__(self, value: Any) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value: str) -> None:
        value = normalize_phone(value)
        if not (isinstance(value, str) and value.isdigit() and len(value) == PHONE_LENGTH):
            raise ValueError(
                f"Phone number must contain exactly {PHONE_LENGTH} digits "
                "(e.g. 0661234567 or +380661234567)."
            )
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str) -> None:
        try:
            # Відсіює й неіснуючі дати, як 31.02
            birthday = datetime.strptime(value, DATE_FORMAT).date()
        except (ValueError, TypeError):
            raise ValueError("Invalid date format. Use DD.MM.YYYY") from None
        if birthday > date.today():
            raise ValueError("Birthday cannot be in the future.")
        super().__init__(birthday)

    def __str__(self) -> str:
        return self.value.strftime(DATE_FORMAT)
