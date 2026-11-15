from collections import UserDict
from typing import Optional

from .record import Record


# Книга контактів: ключ — ім'я, значення — Record
class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    # Повертає запис або None, якщо контакту немає
    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        self.data.pop(name, None)
