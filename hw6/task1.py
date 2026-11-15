from typing import Tuple, Union

Number = Union[int, float]

def total_salary(path: str) -> Tuple[Number, Number]:
    total = 0
    count = 0

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if line:
                    try:
                        _name, salary = line.split(",")
                        total += int(salary)
                        count += 1
                    except ValueError:
                        print(f"Рядок {line_number} пошкоджений, пропускаю: {line!r}")
    except (OSError, UnicodeDecodeError) as error:
        print(f"Не вдалося прочитати файл {path}: {error}")
        return 0, 0

    try:
        average = total / count
    except ZeroDivisionError:
        average = 0.0

    if average.is_integer():
        average = int(average)
    return total, average


if __name__ == "__main__":
    total, average = total_salary("salary_file.txt")
    print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")