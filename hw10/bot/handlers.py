from models import AddressBook, Record

from .decorators import input_error


def _require(args: list[str], count: int, usage: str) -> None:
    if len(args) < count:
        raise IndexError(usage)


def _get_record(book: AddressBook, name: str) -> Record:
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    return record


def hello(args: list[str], book: AddressBook) -> str:
    return "How can I help you?"


# Новий контакт або ще телефон до існуючого
@input_error
def add_contact(args: list[str], book: AddressBook) -> str:
    _require(args, 2, "add <name> <phone>")
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        message = "Contact added."
    record.add_phone(phone)
    book.add_record(record)
    return message


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    _require(args, 3, "change <name> <old phone> <new phone>")
    name, old_phone, new_phone, *_ = args
    _get_record(book, name).edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    _require(args, 1, "phone <name>")
    record = _get_record(book, args[0])
    if not record.phones:
        return f"{record.name.value} has no phones."
    return "; ".join(p.value for p in record.phones)


@input_error
def show_all(args: list[str], book: AddressBook) -> str:
    if not book:
        return "No contacts saved."
    return "\n".join(str(record) for record in book.values())


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    _require(args, 2, "add-birthday <name> <DD.MM.YYYY>")
    name, birthday, *_ = args
    _get_record(book, name).add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    _require(args, 1, "show-birthday <name>")
    record = _get_record(book, args[0])
    if record.birthday is None:
        return f"{record.name.value} has no birthday set."
    return str(record.birthday)


@input_error
def birthdays(args: list[str], book: AddressBook) -> str:
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next week."
    return "\n".join(f"{u['name']}: {u['congratulation_date']}" for u in upcoming)


# Команда -> обробник
COMMANDS = {
    "hello": hello,
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": show_all,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
}
