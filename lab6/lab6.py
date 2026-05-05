import random
import math


def simulate_battle(p1, p2, p3):
    """
    Возвращает исход одного боя:
    A = 1, если сбит бомбардировщик, иначе 0
    B = 1, если сбит истребитель, иначе 0
    C = 1, если сбит хотя бы один, иначе 0
    """

    # Первый выстрел истребителя
    r = random.random()
    if r < p1:
        return 1, 0, 1

    # Если бомбардировщик не сбит, он стреляет по истребителю
    r = random.random()
    if r < p2:
        return 0, 1, 1

    # Если истребитель не сбит, он стреляет второй раз
    r = random.random()
    if r < p3:
        return 1, 0, 1

    # Никто не сбит
    return 0, 0, 0


def monte_carlo_estimation(p1, p2, p3, n):
    count_a = 0
    count_b = 0
    count_c = 0

    for _ in range(n):
        a, b, c = simulate_battle(p1, p2, p3)
        count_a += a
        count_b += b
        count_c += c

    p_a_hat = count_a / n
    p_b_hat = count_b / n
    p_c_hat = count_c / n

    return p_a_hat, p_b_hat, p_c_hat


def analytical_probabilities(p1, p2, p3):
    p_a = p1 + (1 - p1) * (1 - p2) * p3
    p_b = (1 - p1) * p2
    p_c = 1 - (1 - p1) * (1 - p2) * (1 - p3)
    return p_a, p_b, p_c


def confidence_interval(phat, n, z=1.96):
    """
    Доверительный интервал для вероятности по нормальной аппроксимации:
    phat ± z * sqrt(phat * (1 - phat) / n)
    Для beta = 0.95 берется z = 1.96
    """
    margin = z * math.sqrt(phat * (1 - phat) / n)
    left = max(0.0, phat - margin)
    right = min(1.0, phat + margin)
    return left, right


def print_result(name, estimate, exact, interval):
    inside = "ДА" if interval[0] <= exact <= interval[1] else "НЕТ"
    print(f"{name}:")
    print(f"  Оценка Монте-Карло       = {estimate:.6f}")
    print(f"  Точное значение          = {exact:.6f}")
    print(f"  95% доверительный интервал = [{interval[0]:.6f}; {interval[1]:.6f}]")
    print(f"  Точное значение внутри интервала: {inside}")
    print()


def main():
    print("МОДЕЛИРОВАНИЕ ВОЗДУШНОГО БОЯ (метод Монте-Карло)")
    print()

    p1 = float(input("Введите p1 (вероятность, что истребитель первым выстрелом собьет бомбардировщик): "))
    p2 = float(input("Введите p2 (вероятность, что бомбардировщик собьет истребитель): "))
    p3 = float(input("Введите p3 (вероятность, что истребитель вторым выстрелом собьет бомбардировщик): "))
    n = int(input("Введите число экспериментов N: "))

    if not (0 <= p1 <= 1 and 0 <= p2 <= 1 and 0 <= p3 <= 1):
        print("Ошибка: вероятности должны быть в диапазоне [0, 1].")
        return

    if n <= 0:
        print("Ошибка: число экспериментов должно быть положительным.")
        return

    # Моделирование
    p_a_hat, p_b_hat, p_c_hat = monte_carlo_estimation(p1, p2, p3, n)

    # Аналитическое решение
    p_a_exact, p_b_exact, p_c_exact = analytical_probabilities(p1, p2, p3)

    # Доверительные интервалы
    ci_a = confidence_interval(p_a_hat, n)
    ci_b = confidence_interval(p_b_hat, n)
    ci_c = confidence_interval(p_c_hat, n)

    print()
    print("АНАЛИТИЧЕСКОЕ РЕШЕНИЕ:")
    print(f"P(A) = p1 + (1 - p1)(1 - p2)p3 = {p_a_exact:.6f}")
    print(f"P(B) = (1 - p1)p2               = {p_b_exact:.6f}")
    print(f"P(C) = 1 - (1 - p1)(1 - p2)(1 - p3) = {p_c_exact:.6f}")
    print()

    print("РЕЗУЛЬТАТЫ МОДЕЛИРОВАНИЯ:")
    print_result("Событие A (сбит бомбардировщик)", p_a_hat, p_a_exact, ci_a)
    print_result("Событие B (сбит истребитель)", p_b_hat, p_b_exact, ci_b)
    print_result("Событие C (сбит хотя бы один)", p_c_hat, p_c_exact, ci_c)


if __name__ == "__main__":
    main()
