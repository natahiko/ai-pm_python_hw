from models import AddressBook, Record

from .decorators import input_error
from .parser import split_phones

# Команда -> (формат, опис). Звідси беруться і usage в помилках, і help
COMMAND_INFO = {
    "hello": ("hello", "greeting"),
    "help": ("help", "show this list"),
    "add": ("add <name> <phone>", "add a contact or one more phone"),
    "change": ("change <name> <old phone> <new phone>", "change a phone"),
    "phone": ("phone <name>", "show contact's phones"),
    "all": ("all", "show all contacts"),
    "add-birthday": ("add-birthday <name> <DD.MM.YYYY>", "add a birthday"),
    "show-birthday": ("show-birthday <name>", "show contact's birthday"),
    "birthdays": ("birthdays", "birthdays in the next 7 days"),
    "exit": ("close / exit", "save and exit"),
}


def _require(args: list[str], count: int, command: str) -> None:
    if len(args) < count:
        raise IndexError(COMMAND_INFO[command][0])


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
    _require(args, 2, "add")
    name, *phone_parts = args
    (phone,) = split_phones(phone_parts, 1)
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
    _require(args, 3, "change")
    name, *phone_parts = args
    phones = split_phones(phone_parts, 2)
    _require(phones, 2, "change")
    old_phone, new_phone = phones
    _get_record(book, name).edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    _require(args, 1, "phone")
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
    _require(args, 2, "add-birthday")
    name, birthday, *_ = args
    _get_record(book, name).add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    _require(args, 1, "show-birthday")
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


_USAGE_WIDTH = max(len(usage) for usage, _ in COMMAND_INFO.values()) + 2
HELP_TEXT = "Available commands:\n" + "\n".join(
    f"  {usage:<{_USAGE_WIDTH}}- {description}" for usage, description in COMMAND_INFO.values()
)


def show_help(args: list[str], book: AddressBook) -> str:
    return HELP_TEXT


# Команда -> обробник
COMMANDS = {
    "hello": hello,
    "help": show_help,
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": show_all,
    "add-birthday": add_birthday,
    "show-birthday": show_birthday,
    "birthdays": birthdays,
}
