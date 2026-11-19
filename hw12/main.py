from bot.handlers import COMMANDS
from bot.parser import parse_input
from storage import load_data, save_data

EXIT_COMMANDS = {"close", "exit"}


def main() -> None:
    book = load_data()
    print("Welcome to the assistant bot! Type 'help' to see all commands.")
    # finally — щоб зберегти книгу навіть якщо бот впаде
    try:
        while True:
            try:
                command, args = parse_input(input("Enter a command: "))
            except (EOFError, KeyboardInterrupt):
                # Ctrl+C / Ctrl+D
                print("\nGood bye!")
                break

            if not command:
                continue

            if command in EXIT_COMMANDS:
                print("Good bye!")
                break

            handler = COMMANDS.get(command)
            if handler is None:
                print(f"Unknown command '{command}'. Type 'help' to see all commands.")
                continue

            print(handler(args, book))
    finally:
        save_data(book)


if __name__ == "__main__":
    main()
