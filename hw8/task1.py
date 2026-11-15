def caching_fibonacci():
    # кеш для вже обчислених чисел n: F(n)
    cache = {}

    def fibonacci(n):
        if n <= 0:
            return 0
        if n == 1:
            return 1

        # якщо знайдено - вертаємо з кешу
        if n in cache:
            return cache[n]

        # рахуємо рекурсивно
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


if __name__ == "__main__":
    fib = caching_fibonacci()

    print(fib(10))  # Виведе 55
    print(fib(15))  # Виведе 610
