from bot.handlers import COMMANDS
from bot.parser import parse_input
from models import AddressBook

EXIT_COMMANDS = {"close", "exit"}


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        try:
            command, args = parse_input(input("Enter a command: "))
        except (EOFError, KeyboardInterrupt):
            # Ctrl+C / Ctrl+D
            print("\nGood bye!")
            break

        if command in EXIT_COMMANDS:
            print("Good bye!")
            break

        handler = COMMANDS.get(command)
        print(handler(args, book) if handler else "Invalid command.")


if __name__ == "__main__":
    main()
