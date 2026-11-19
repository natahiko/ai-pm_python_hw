from typing import Optional

from .fields import Birthday, Name, Phone, normalize_phone


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Optional[Birthday] = None

    def _ensure_new_phone(self, phone: str) -> None:
        if self.find_phone(phone):
            raise ValueError(f"Phone {phone} already exists for {self.name.value}.")

    def add_phone(self, phone: str) -> None:
        new_phone = Phone(phone)
        self._ensure_new_phone(new_phone.value)
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
        replacement = Phone(new_phone)
        if replacement.value == found.value:
            raise ValueError("New phone is the same as the old one, nothing changed.")
        self._ensure_new_phone(replacement.value)
        # Зберігаємо порядок
        self.phones[self.phones.index(found)] = replacement

    # Приймає будь-який формат: 066..., 38066..., +38066...
    def find_phone(self, phone: str) -> Optional[Phone]:
        phone = normalize_phone(phone)
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self) -> str:
        phones = "; ".join(p.value for p in self.phones)
        result = f"Contact name: {self.name.value}, phones: {phones}"
        if self.birthday is not None:
            result += f", birthday: {self.birthday}"
        return result
