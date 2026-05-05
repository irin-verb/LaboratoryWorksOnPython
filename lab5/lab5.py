# -*- coding: utf-8 -*-
import math
import random
from typing import List, Callable

import matplotlib.pyplot as plt


# =========================
# НАСТРОЙКИ
# =========================

SAMPLE_SIZE = 1000     # объем выборки
BINS_COUNT = 15        # количество интервалов: 15 или 25
EPS = 1e-12            # защита от log(0)

# Параметры экспоненциального распределения
LAMBDA_EXP = 3.0

# Параметры распределения Вейбулла
B_WEIBULL = 2.0
C_WEIBULL = 3.0


# =========================
# ГЕНЕРАЦИЯ
# =========================

def uniform_0_1() -> float:
    """Равномерная случайная величина на [0, 1), защищенная от 0."""
    r = random.random()
    return max(r, EPS)


def generate_exponential_sample(n: int, lam: float) -> List[float]:
    """
    Экспоненциальное распределение:
    x = -ln(r) / lambda
    """
    sample = []
    for _ in range(n):
        r = uniform_0_1()
        x = -math.log(r) / lam
        sample.append(x)
    return sample


def generate_weibull_sample(n: int, b: float, c: float) -> List[float]:
    """
    Распределение Вейбулла:
    x = b * (-ln(r))^(1/c)
    """
    sample = []
    for _ in range(n):
        r = uniform_0_1()
        x = b * ((-math.log(r)) ** (1.0 / c))
        sample.append(x)
    return sample


# =========================
# ТЕОРЕТИЧЕСКИЕ ФУНКЦИИ
# =========================

def exponential_pdf(x: float, lam: float) -> float:
    if x < 0:
        return 0.0
    return lam * math.exp(-lam * x)


def exponential_cdf(x: float, lam: float) -> float:
    if x < 0:
        return 0.0
    return 1.0 - math.exp(-lam * x)


def weibull_pdf(x: float, b: float, c: float) -> float:
    if x <= 0:
        return 0.0
    return (c / b) * ((x / b) ** (c - 1)) * math.exp(-((x / b) ** c))


def weibull_cdf(x: float, b: float, c: float) -> float:
    if x < 0:
        return 0.0
    return 1.0 - math.exp(-((x / b) ** c))


# =========================
# ХАРАКТЕРИСТИКИ
# =========================

def sample_mean(sample: List[float]) -> float:
    return sum(sample) / len(sample)


def sample_variance(sample: List[float]) -> float:
    mean = sample_mean(sample)
    return sum((x - mean) ** 2 for x in sample) / len(sample)


def exponential_theoretical_mean(lam: float) -> float:
    return 1.0 / lam


def exponential_theoretical_variance(lam: float) -> float:
    return 1.0 / (lam ** 2)


def weibull_theoretical_mean(b: float, c: float) -> float:
    return b * math.gamma(1.0 + 1.0 / c)


def weibull_theoretical_variance(b: float, c: float) -> float:
    g1 = math.gamma(1.0 + 1.0 / c)
    g2 = math.gamma(1.0 + 2.0 / c)
    return (b ** 2) * (g2 - g1 ** 2)


# =========================
# КРИТЕРИЙ КОЛМОГОРОВА
# =========================

def kolmogorov_statistic(sample: List[float], cdf_func: Callable[[float], float]) -> float:
    data = sorted(sample)
    n = len(data)
    d = 0.0

    for i, x in enumerate(data, start=1):
        f_theor = cdf_func(x)
        f_emp_left = (i - 1) / n
        f_emp_right = i / n

        d = max(d, abs(f_emp_left - f_theor), abs(f_emp_right - f_theor))

    return d


def kolmogorov_critical_value(n: int, alpha: float = 0.05) -> float:
    """
    Для alpha = 0.05:
    D_crit ≈ 1.36 / sqrt(n)
    """
    if alpha == 0.05:
        return 1.36 / math.sqrt(n)
    raise ValueError("В программе реализовано только alpha = 0.05")


# =========================
# ВИЗУАЛИЗАЦИЯ
# =========================

def plot_histogram_with_pdf(
    sample: List[float],
    bins_count: int,
    pdf_func: Callable[[float], float],
    title: str
) -> None:
    plt.figure(figsize=(10, 6))

    # Гистограмма
    plt.hist(sample, bins=bins_count, density=True, edgecolor='black', label='Гистограмма')

    # Теоретическая плотность
    x_min = 0.0
    x_max = max(sample) * 1.05
    xs = [x_min + i * (x_max - x_min) / 500 for i in range(501)]
    ys = [pdf_func(x) for x in xs]

    plt.plot(xs, ys, linewidth=2, label='Теоретическая плотность')

    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title(title)
    plt.grid(True)
    plt.legend()


def plot_empirical_and_theoretical_cdf(
    sample: List[float],
    cdf_func: Callable[[float], float],
    title: str
) -> None:
    data = sorted(sample)
    n = len(data)

    x_emp = [0.0]
    y_emp = [0.0]

    for i, x in enumerate(data, start=1):
        x_emp.append(x)
        y_emp.append((i - 1) / n)
        x_emp.append(x)
        y_emp.append(i / n)

    x_max = max(sample) * 1.05
    xs = [0.0 + i * x_max / 500 for i in range(501)]
    ys = [cdf_func(x) for x in xs]

    plt.figure(figsize=(10, 6))
    plt.plot(x_emp, y_emp, label='Эмпирическая функция распределения')
    plt.plot(xs, ys, linewidth=2, label='Теоретическая функция распределения')

    plt.xlabel("x")
    plt.ylabel("F(x)")
    plt.title(title)
    plt.grid(True)
    plt.legend()


# =========================
# АНАЛИЗ
# =========================

def analyze_distribution(
    name: str,
    sample: List[float],
    theoretical_mean: float,
    theoretical_variance: float,
    cdf_func: Callable[[float], float]
) -> None:
    n = len(sample)

    emp_mean = sample_mean(sample)
    emp_var = sample_variance(sample)

    d_n = kolmogorov_statistic(sample, cdf_func)
    d_crit = kolmogorov_critical_value(n)

    print("=" * 60)
    print(name)
    print("=" * 60)
    print(f"Теоретическое матожидание: {theoretical_mean:.6f}")
    print(f"Выборочное матожидание:    {emp_mean:.6f}")
    print(f"Теоретическая дисперсия:   {theoretical_variance:.6f}")
    print(f"Выборочная дисперсия:      {emp_var:.6f}")
    print(f"Статистика Колмогорова:    {d_n:.6f}")
    print(f"Критическое значение:      {d_crit:.6f}")

    if d_n < d_crit:
        print("Вывод: распределение согласуется с теоретическим.")
    else:
        print("Вывод: распределение не согласуется с теоретическим.")
    print()


# =========================
# MAIN
# =========================

def main() -> None:
    random.seed(42)

    # -------------------------
    # Экспоненциальное
    # -------------------------
    exp_sample = generate_exponential_sample(SAMPLE_SIZE, LAMBDA_EXP)

    analyze_distribution(
        name=f"Экспоненциальное распределение (lambda = {LAMBDA_EXP})",
        sample=exp_sample,
        theoretical_mean=exponential_theoretical_mean(LAMBDA_EXP),
        theoretical_variance=exponential_theoretical_variance(LAMBDA_EXP),
        cdf_func=lambda x: exponential_cdf(x, LAMBDA_EXP)
    )

    # -------------------------
    # Вейбулл
    # -------------------------
    weibull_sample = generate_weibull_sample(SAMPLE_SIZE, B_WEIBULL, C_WEIBULL)

    analyze_distribution(
        name=f"Распределение Вейбулла (b = {B_WEIBULL}, c = {C_WEIBULL})",
        sample=weibull_sample,
        theoretical_mean=weibull_theoretical_mean(B_WEIBULL, C_WEIBULL),
        theoretical_variance=weibull_theoretical_variance(B_WEIBULL, C_WEIBULL),
        cdf_func=lambda x: weibull_cdf(x, B_WEIBULL, C_WEIBULL)
    )

    # -------------------------
    # Графики
    # -------------------------
    plot_histogram_with_pdf(
        sample=exp_sample,
        bins_count=BINS_COUNT,
        pdf_func=lambda x: exponential_pdf(x, LAMBDA_EXP),
        title=f"Экспоненциальное распределение: гистограмма и плотность"
    )

    plot_histogram_with_pdf(
        sample=weibull_sample,
        bins_count=BINS_COUNT,
        pdf_func=lambda x: weibull_pdf(x, B_WEIBULL, C_WEIBULL),
        title=f"Распределение Вейбулла: гистограмма и плотность"
    )

    plot_empirical_and_theoretical_cdf(
        sample=exp_sample,
        cdf_func=lambda x: exponential_cdf(x, LAMBDA_EXP),
        title="Экспоненциальное распределение: эмпирическая и теоретическая F(x)"
    )

    plot_empirical_and_theoretical_cdf(
        sample=weibull_sample,
        cdf_func=lambda x: weibull_cdf(x, B_WEIBULL, C_WEIBULL),
        title="Распределение Вейбулла: эмпирическая и теоретическая F(x)"
    )

    plt.show()


if __name__ == "__main__":
    main()