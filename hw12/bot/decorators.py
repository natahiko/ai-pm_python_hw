from functools import wraps
from typing import Any, Callable


# Ловить помилки, щоб бот не падав
def input_error(func: Callable[..., str]) -> Callable[..., str]:
    @wraps(func)
    def inner(*args: Any, **kwargs: Any) -> str:
        try:
            return func(*args, **kwargs)
        except IndexError as e:
            if e.args:
                return f"Not enough arguments. Usage: {e}"
            return "Not enough arguments for this command."
        except ValueError as e:
            # Помилки валідації полів
            return str(e)
        except KeyError as e:
            if e.args:
                return f"Contact '{e.args[0]}' not found."
            return "Contact not found."

    return inner
