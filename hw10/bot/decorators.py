from functools import wraps


# Ловить помилки, щоб бот не падав
def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError as e:
            if e.args:
                return f"Not enough arguments. Usage: {e}"
            return "Enter the argument for the command"
        except ValueError as e:
            # Помилки валідації полів
            return str(e)
        except KeyError as e:
            if e.args:
                return f"Contact '{e.args[0]}' not found."
            return "Contact not found."

    return inner
