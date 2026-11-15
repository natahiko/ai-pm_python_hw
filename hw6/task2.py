from typing import Dict, List


def get_cats_info(path: str) -> List[Dict[str, str]]:
    cats = []

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if line:
                    try:
                        cat_id, name, age = line.split(",")
                        cats.append({"id": cat_id, "name": name, "age": age})
                    except ValueError:
                        print(f"Рядок {line_number} пошкоджений, пропускаю: {line!r}")
    except (OSError, UnicodeDecodeError) as error:
        print(f"Не вдалося прочитати файл {path}: {error}")
        return []

    return cats


if __name__ == "__main__":
    cats_info = get_cats_info("cats_file.txt")
    print(cats_info)
