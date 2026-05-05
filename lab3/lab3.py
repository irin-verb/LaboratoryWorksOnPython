
# -*- coding: utf-8 -*-
import math
import random
from typing import List, Tuple

import matplotlib.pyplot as plt


# ---------- Теоретические F(x) и f(x) для варианта 4 ----------

def F_theoretical(x: float) -> float:
    """Теоретическая функция распределения F(x)."""
    if x < 0.0:
        return 0.0
    if 0.0 <= x < 0.5:
        return x
    if 0.5 <= x < 1.0:
        return 0.5
    if 1.0 <= x < 1.5:
        return 2.0 * (x - 1.0) ** 2 + 0.5
    return 1.0


def f_theoretical(x: float) -> float:
    """Теоретическая плотность f(x) (для наглядного наложения на гистограмму)."""
    if 0.0 <= x < 0.5:
        return 1.0
    if 1.0 <= x < 1.5:
        return 4.0 * (x - 1.0)
    return 0.0


# ---------- Метод обратных функций (инверсия F) ----------

def inv_F(r: float) -> float:
    """
    Обратная функция для заданной F(x).
    r ~ U[0,1).
    """
    if not (0.0 <= r < 1.0):
        # на всякий случай подправим
        r = min(max(r, 0.0), 1.0 - 1e-15)

    if r < 0.5:
        return r
    # r in [0.5, 1): решаем r = 0.5 + 2(x-1)^2, x in [1, 1.5)
    return 1.0 + math.sqrt((r - 0.5) / 2.0)


def sample_inverse_transform(n: int, seed: int | None = 42) -> List[float]:
    """Генерация выборки методом обратных функций."""
    if n < 1000:
        raise ValueError("По условию нужно n >= 1000")

    rng = random.Random(seed)
    xs = [inv_F(rng.random()) for _ in range(n)]
    return xs


# ---------- Оценки матожидания/дисперсии ----------

def mean(xs: List[float]) -> float:
    return sum(xs) / len(xs)


def variance_unbiased(xs: List[float]) -> float:
    """Несмещенная выборочная дисперсия (деление на n-1)."""
    n = len(xs)
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / (n - 1)


# ---------- Эмпирическая CDF и критерий Колмогорова ----------

def ecdf_points(xs: List[float]) -> Tuple[List[float], List[float]]:
    """Точки эмпирической функции распределения F_n(x)."""
    xs_sorted = sorted(xs)
    n = len(xs_sorted)
    ys = [(i + 1) / n for i in range(n)]
    return xs_sorted, ys


def ks_test(xs: List[float], alpha: float = 0.05) -> Tuple[float, float, bool]:
    """
    Одновыборочный KS-тест на соответствие F_theoretical.
    Возвращает: (D, D_crit, accept)
    Где accept=True означает "гипотеза НЕ отвергается".
    """
    xs_sorted = sorted(xs)
    n = len(xs_sorted)

    # D+ = max(i/n - F(x_i)), D- = max(F(x_i) - (i-1)/n)
    d_plus = 0.0
    d_minus = 0.0

    for i, x in enumerate(xs_sorted, start=1):
        Fx = F_theoretical(x)
        d_plus = max(d_plus, i / n - Fx)
        d_minus = max(d_minus, Fx - (i - 1) / n)

    D = max(d_plus, d_minus)

    # Критические константы для KS (асимптотически):
    # alpha: 0.10 -> 1.22; 0.05 -> 1.36; 0.01 -> 1.63
    c_table = {0.10: 1.22, 0.05: 1.36, 0.01: 1.63}
    if alpha not in c_table:
        raise ValueError("alpha должен быть одним из: 0.10, 0.05, 0.01")

    D_crit = c_table[alpha] / math.sqrt(n)
    accept = D <= D_crit
    return D, D_crit, accept


# ---------- Визуализация ----------

def plot_histogram(xs: List[float], k: int = 25) -> None:
    plt.figure()
    plt.hist(xs, bins=k, density=True)
    plt.title(f"Гистограмма (k={k}), наложена теоретическая плотность")

    grid_n = 600
    x_grid = [0.0 + 1.5 * i / (grid_n - 1) for i in range(grid_n)]
    y_grid = [f_theoretical(x) for x in x_grid]
    plt.plot(x_grid, y_grid)

    plt.xlabel("x")
    plt.ylabel("Плотность")
    plt.grid(True)


def plot_cdf(xs: List[float]) -> None:
    plt.figure()
    x_emp, y_emp = ecdf_points(xs)

    plt.step(x_emp, y_emp, where="post", label="Эмпирическая F_n(x)")

    grid_n = 600
    x_grid = [0.0 + 1.5 * i / (grid_n - 1) for i in range(grid_n)]
    y_grid = [F_theoretical(x) for x in x_grid]
    plt.plot(x_grid, y_grid, label="Теоретическая F(x)")

    plt.title("Сравнение эмпирической и теоретической функций распределения")
    plt.xlabel("x")
    plt.ylabel("F(x)")
    plt.grid(True)
    plt.legend()


# ---------- Теоретические значения (для сравнения) ----------
# Можно не выводить, но удобно для отчёта:
# E[X] = 19/24 ≈ 0.7916667
# Var[X] = 179/576 ≈ 0.3107639

def main():
    n = 5000      # >= 1000
    k = 25        # 15 или 25
    alpha = 0.05  # 0.10 / 0.05 / 0.01

    xs = sample_inverse_transform(n=n, seed=42)

    m_hat = mean(xs)
    d_hat = variance_unbiased(xs)

    print("=== Выборочные оценки ===")
    print(f"n = {n}, k = {k}, alpha = {alpha}")
    print(f"Оценка матожидания M̂ = {m_hat:.6f}")
    print(f"Оценка дисперсии D̂ (несмещ.) = {d_hat:.6f}")

    print("\n=== Теоретические значения (для отчёта) ===")
    print(f"M = 19/24 = {19/24:.6f}")
    print(f"D = 179/576 = {179/576:.6f}")

    D, D_crit, accept = ks_test(xs, alpha=alpha)
    print("\n=== Критерий Колмогорова (KS) ===")
    print(f"D = {D:.6f}")
    print(f"D_crit = {D_crit:.6f}")
    print("Гипотеза о соответствии теоретическому распределению:",
          "НЕ отвергается" if accept else "ОТВЕРГАЕТСЯ")

    plot_histogram(xs, k=k)
    plot_cdf(xs)
    plt.show()


if __name__ == "__main__":
    main()