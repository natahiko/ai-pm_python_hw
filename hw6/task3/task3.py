import sys
from pathlib import Path

from colorama import Fore, Style, init

# Символи для побудови дерева
BRANCH = "┣ "
LAST_BRANCH = "┗ "
PIPE = "┃ "
SPACE = "  "

# Іконки та кольори для різних типів елементів
ROOT_ICON = "📦"
DIR_ICON = "📂"
FILE_ICON = "📜"
DIR_COLOR = Fore.BLUE + Style.BRIGHT
FILE_COLOR = Fore.GREEN
ROOT_COLOR = Fore.YELLOW + Style.BRIGHT


def sort_entries(directory: Path) -> list[Path]:
    """Повертає вміст директорії: спочатку піддиректорії, потім файли (за алфавітом)."""
    return sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))


def print_tree(directory: Path, prefix: str = "") -> None:
    """Рекурсивно виводить вміст директорії з відступами та кольорами."""
    try:
        entries = sort_entries(directory)
    except PermissionError:
        print(f"{prefix}{LAST_BRANCH}{Fore.RED}[немає доступу]{Style.RESET_ALL}")
        return

    for index, entry in enumerate(entries):
        is_last = index == len(entries) - 1
        connector = LAST_BRANCH if is_last else BRANCH

        if entry.is_dir():
            print(f"{prefix}{connector}{DIR_COLOR}{DIR_ICON}{entry.name}{Style.RESET_ALL}")
            # Для вкладених елементів продовжуємо вертикальну лінію, якщо це не останній елемент
            print_tree(entry, prefix + (SPACE if is_last else PIPE))
        else:
            print(f"{prefix}{connector}{FILE_COLOR}{FILE_ICON}{entry.name}{Style.RESET_ALL}")


def get_directory_path() -> Path:
    """Бере шлях з аргументу командного рядка, а якщо його немає — просить ввести вручну."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])

    print("Програма запускається не на оригінальній машині, тому вкажіть шлях до директорії.")
    print(f"Наприклад: {Fore.CYAN}/Users/natahiko/Pictures")
    # strip() прибирає пробіли та лапки, які додаються при перетягуванні папки в термінал
    user_input = input("Шлях до директорії: ").strip().strip("'\"")
    if not user_input:
        print(f"{Fore.RED}Помилка: шлях не вказано.")
        sys.exit(1)
    return Path(user_input)


def main() -> None:
    init(autoreset=True)  # Ініціалізація colorama (потрібно для коректної роботи у Windows)

    path = get_directory_path()

    # Перевірка, що шлях існує і веде саме до директорії
    if not path.exists():
        print(f"{Fore.RED}Помилка: шлях '{path}' не існує.")
        sys.exit(1)
    if not path.is_dir():
        print(f"{Fore.RED}Помилка: '{path}' не є директорією.")
        sys.exit(1)

    print(f"{ROOT_COLOR}{ROOT_ICON}{path.resolve().name}")
    print_tree(path)


if __name__ == "__main__":
    main()
