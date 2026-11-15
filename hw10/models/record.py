from typing import Optional

from .fields import Birthday, Name, Phone


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Optional[Birthday] = None

    def add_phone(self, phone: str) -> None:
        new_phone = Phone(phone)
        if self.find_phone(new_phone.value):
            raise ValueError(f"Phone {phone} already exists for {self.name.value}.")
        self.phones.append(new_phone)

    # Повторний виклик перезаписує
    def add_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone: str) -> None:
        found = self.find_phone(phone)
        if found is None:
            raise ValueError(f"Phone {phone} not found.")
        self.phones.remove(found)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        found = self.find_phone(old_phone)
        if found is None:
            raise ValueError(f"Phone {old_phone} not found.")
        if new_phone != old_phone and self.find_phone(new_phone):
            raise ValueError(f"Phone {new_phone} already exists for {self.name.value}.")
        # Зберігаємо порядок
        self.phones[self.phones.index(found)] = Phone(new_phone)

    def find_phone(self, phone: str) -> Optional[Phone]:
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        result = f"Contact name: {self.name.value}, phones: {phones}"
        if self.birthday is not None:
            result += f", birthday: {self.birthday}"
        return result
