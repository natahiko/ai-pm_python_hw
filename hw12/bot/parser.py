from models.fields import is_full_phone


# "add John 123" -> ("add", ["John", "123"])
def parse_input(user_input: str) -> tuple[str, list[str]]:
    parts = user_input.split()
    if not parts:
        return "", []
    cmd, *args = parts
    return cmd.strip().lower(), args


# Номер з пробілами приходить шматками: ["+38", "066", "377", "8532"].
# Склеюємо шматки, доки не набереться повний номер; останньому — все, що лишилось
def split_phones(parts: list[str], count: int) -> list[str]:
    if len(parts) == count:
        return parts
    phones: list[str] = []
    current = ""
    for part in parts:
        current += part
        if len(phones) < count - 1 and is_full_phone(current):
            phones.append(current)
            current = ""
    if current:
        phones.append(current)
    return phones
