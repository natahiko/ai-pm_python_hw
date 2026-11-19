from collections import UserDict
from datetime import date, timedelta
from typing import Optional

from .fields import DATE_FORMAT
from .record import Record

SATURDAY = 5  # weekday(): пн = 0 ... нд = 6


# 29.02 у невисокосний рік -> 28.02
def _birthday_in_year(birthday: date, year: int) -> date:
    try:
        return birthday.replace(year=year)
    except ValueError:
        return birthday.replace(year=year, day=28)


# Ключ — ім'я малими літерами (john = John), значення — Record
class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value.lower()] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name.lower())

    def delete(self, name: str) -> None:
        self.data.pop(name.lower(), None)

    # Вихідні переносимо на понеділок
    def get_upcoming_birthdays(self, days: int = 7) -> list[dict]:
        today = date.today()
        upcoming = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = _birthday_in_year(record.birthday.value, today.year)
            if birthday < today:  # вже минув
                birthday = _birthday_in_year(record.birthday.value, today.year + 1)

            # Включно з 7-м днем
            if (birthday - today).days <= days:
                if birthday.weekday() >= SATURDAY:
                    birthday += timedelta(days=7 - birthday.weekday())

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": birthday.strftime(DATE_FORMAT),
                })

        return upcoming
