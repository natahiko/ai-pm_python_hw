from functools import wraps


# Ловить помилки в командах, щоб бот не падав
def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError):
            return "Enter the argument for the command"
        except KeyError:
            return "Contact not found."

    return inner
