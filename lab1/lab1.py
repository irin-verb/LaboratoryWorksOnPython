
# -*- coding: utf8 -*-
import math
from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt


@dataclass(frozen=True)
class GeneratorParams:
    a: int
    b: int
    c: int
    d: int


# Константы из методички (для k = 1,2,3)
PARAMS_ALL = [
    GeneratorParams(a=171, b=177, c=2,  d=30269),  # k = 1
    GeneratorParams(a=172, b=176, c=35, d=30307),  # k = 2
    GeneratorParams(a=170, b=178, c=63, d=30323),  # k = 3
]


def next_y(y: int, p: GeneratorParams) -> int:
    """
    Реализация формулы (2.12):
    y_{n+1} = int(abs(a*(y mod b) - c*y/b))
    """
    value = p.a * (y % p.b) - p.c * (y // p.b)
    return abs(value)
                 


def generate_sequence(n: int, y0: int, k: int = 1) -> List[float]:
    """
    Генерация n чисел на [0,1).
    По варианту: k=1 -> используем только первый датчик, x = y/d.
    """
    if k != 1:
        raise ValueError("Для варианта 4 по таблице используем k=1 (один датчик).")

    p = PARAMS_ALL[0]  # k=1
    y = y0
    out: List[float] = []

    for _ in range(n):
        y = next_y(y, p)
        # нормируем на [0,1)
        x = y / p.d
        out.append(x)

    return out


def estimates(xs: List[float]) -> Tuple[float, float, float, float]:
    """
    Возвращает:
    mean = E[X]
    var  = D[X] (несмещённая или смещённая? в учебных часто смещённая 1/n; тут сделаем 1/n)
    m2   = E[X^2]
    m3   = E[X^3]
    """
    n = len(xs)
    mean = sum(xs) / n
    m2 = sum(x * x for x in xs) / n
    m3 = sum(x * x * x for x in xs) / n
    var = sum((x - mean) ** 2 for x in xs) / n  # оценка дисперсии (по 1/n)
    return mean, var, m2, m3


def plot_histogram(xs: List[float], bins: int) -> None:
    plt.figure()
    plt.hist(
        xs,
        bins=bins,
        range=(0.0, 1.0),
        density=False,
        edgecolor='black',  
        linewidth=1.0  
    )
    plt.title(f"Гистограмма частот (n={len(xs)}, bins={bins})")
    plt.xlabel("x")
    plt.ylabel("частота")


def plot_empirical_cdf(xs: List[float]) -> None:
    plt.figure()
    xs_sorted = sorted(xs)
    n = len(xs_sorted)
    ys = [(i + 1) / n for i in range(n)]
    plt.step(xs_sorted, ys, where="post")
    plt.title(f"Эмпирическая функция распределения (n={n})")
    plt.xlabel("x")
    plt.ylabel("F_n(x)")


def main() -> None:
    n = 16000
    bins = 18

    raw = input("Введите начальное целое Y0 (Enter = 12345): ").strip()
    y0 = int(raw) if raw else 12345

    p = PARAMS_ALL[0]
    y0 = y0 % p.d
    if y0 == 0:
        y0 = 1


    xs = generate_sequence(n=n, y0=y0, k=1)
    mean, var, m2, m3 = estimates(xs)

    # Теоретические значения для U[0,1):
    mean_th = 0.5
    var_th = 1.0 / 12.0
    m2_th = 1.0 / 3.0
    m3_th = 1.0 / 4.0

    print("\nОценки по выборке:")
    print(f"E[X]   ≈ {mean:.6f}")
    print(f"D[X]   ≈ {var:.6f}")
    print(f"E[X^2] ≈ {m2:.6f}")
    print(f"E[X^3] ≈ {m3:.6f}")

    print("\nТеория для равномерного U[0,1):")
    print(f"E[X]   = {mean_th:.6f}")
    print(f"D[X]   = {var_th:.6f}")
    print(f"E[X^2] = {m2_th:.6f}")
    print(f"E[X^3] = {m3_th:.6f}")

    print("\nОтклонения (оценка - теория):")
    print(f"ΔE[X]   = {mean - mean_th:+.6f}")
    print(f"ΔD[X]   = {var - var_th:+.6f}")
    print(f"ΔE[X^2] = {m2 - m2_th:+.6f}")
    print(f"ΔE[X^3] = {m3 - m3_th:+.6f}")

    plot_histogram(xs, bins=bins)
    plot_empirical_cdf(xs)
    plt.show()


if __name__ == "__main__":
    main()
