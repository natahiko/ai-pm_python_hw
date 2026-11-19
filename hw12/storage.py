import pickle
from pathlib import Path
from typing import Union

from models import AddressBook

# Поруч з main.py, хоч звідки запускай
DEFAULT_FILE = Path(__file__).parent / "addressbook.pkl"


def save_data(book: AddressBook, filename: Union[Path, str] = DEFAULT_FILE) -> None:
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: Union[Path, str] = DEFAULT_FILE) -> AddressBook:
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        # Перший запуск — файлу ще немає
        return AddressBook()
    except (pickle.UnpicklingError, EOFError, AttributeError, ImportError):
        # Файл битий або порожній — бот все одно стартує
        print(f"Could not read {Path(filename).name}, starting with an empty address book.")
        return AddressBook()
