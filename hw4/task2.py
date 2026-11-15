import random
from typing import List


def get_numbers_ticket(min: int, max: int, quantity: int) -> List[int]:

    # Перевірка типів і обмежень
    if not all(isinstance(x, int) for x in (min, max, quantity)):
        return []
    if min < 1 or max > 1000 or min > max:
        return []
    if not 1 <= quantity <= max - min + 1:
        return []

    numbers = set()  # множина гарантує унікальність
    while len(numbers) < quantity:
        numbers.add(random.randint(min, max))

    return sorted(numbers)


if __name__ == "__main__":
    lottery_numbers = get_numbers_ticket(1, 49, 6)
    print("Ваші лотерейні числа:", lottery_numbers)
    print(get_numbers_ticket(0, 49, 6))     # [] - min < 1
    print(get_numbers_ticket(1, 1001, 6))   # [] - max > 1000
    print(get_numbers_ticket(1, 5, 10))     # [] - забагато чисел
