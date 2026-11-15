from .decorators import input_error


def hello(args: list, contacts: dict) -> str:
    return "How can I help you?"


@input_error
def add_contact(args: list, contacts: dict) -> str:
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: list, contacts: dict) -> str:
    name, phone = args
    if name not in contacts:
        raise KeyError(name)
    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args: list, contacts: dict) -> str:
    name = args[0]
    return contacts[name]


@input_error
def show_all(args: list, contacts: dict) -> str:
    if not contacts:
        return "No contacts saved."
    return "\n".join(f"{name}: {phone}" for name, phone in contacts.items())


# Нова команда = нова функція + рядок тут
COMMANDS = {
    "hello": hello,
    "add": add_contact,
    "change": change_contact,
    "phone": show_phone,
    "all": show_all,
}
