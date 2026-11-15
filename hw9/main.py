from bot.handlers import COMMANDS
from bot.parser import parse_input

EXIT_COMMANDS = {"close", "exit"}


def main():
    # Поки що звичайний словник, у наступному ДЗ замінимо на AddressBook
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        command, args = parse_input(input("Enter a command: "))

        if command in EXIT_COMMANDS:
            print("Good bye!")
            break

        handler = COMMANDS.get(command)
        print(handler(args, contacts) if handler else "Invalid command.")


if __name__ == "__main__":
    main()
