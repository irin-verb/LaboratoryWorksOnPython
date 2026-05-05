# -*- coding: utf-8 -*-
import math
import random
import matplotlib.pyplot as plt


# ===============================
# ХАРДКОД / НАСТРОЙКИ
# ===============================

M = 8               # число шагов по условию
N_BEES = 1000       # число пчёл в одном эксперименте
BINS = 15           # число интервалов для гистограммы
ALPHA = 0.05        # уровень значимости

random.seed(42)


# ===============================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ===============================

def sample_mean(data):
    return sum(data) / len(data)


def sample_variance(data):
    m = sample_mean(data)
    return sum((x - m) ** 2 for x in data) / (len(data) - 1)


def sample_std(data):
    return math.sqrt(sample_variance(data))


# ===============================
# НОРМАЛЬНОЕ РАСПРЕДЕЛЕНИЕ
# Аппроксимируем выборку нормальным законом
# с параметрами, оценёнными по выборке
# ===============================

def normal_pdf(x, mu, sigma):
    z = (x - mu) / sigma
    return (1.0 / (sigma * math.sqrt(2.0 * math.pi))) * math.exp(-0.5 * z * z)


def normal_cdf(x, mu, sigma):
    z = (x - mu) / (sigma * math.sqrt(2.0))
    return 0.5 * (1.0 + math.erf(z))


# ===============================
# ГЕНЕРАЦИЯ НАЧАЛЬНОЙ ТОЧКИ
# Равномерно внутри единичного круга
# ===============================

def generate_point_in_unit_circle():
    # Чтобы точки были равномерны по площади круга:
    # r = sqrt(U), phi = 2*pi*V
    u1 = random.random()
    u2 = random.random()

    r = math.sqrt(u1)
    phi = 2.0 * math.pi * u2

    x = r * math.cos(phi)
    y = r * math.sin(phi)

    return x, y


# ===============================
# БЛУЖДАНИЕ ОДНОЙ ПЧЕЛЫ
# ===============================

def simulate_one_bee():
    x, y = generate_point_in_unit_circle()

    for _ in range(M):
        r = random.random()

        if r < 0.7:
            y += 1      # север
        elif r < 0.80:
            y -= 1      # юг
        elif r < 0.9:
            x += 1      # восток
        else:
            x -= 1      # запад

    distance = math.sqrt(x * x + y * y)
    return distance


# ===============================
# МОДЕЛИРОВАНИЕ РОЯ ИЗ N ПЧЁЛ
# ===============================

def simulate_swarm(n_bees):
    distances = []

    for _ in range(n_bees):
        d = simulate_one_bee()
        distances.append(d)

    return distances


# ===============================
# КРИТЕРИЙ КОЛМОГОРОВА
# Проверяем гипотезу о нормальной аппроксимации
# ===============================

def ks_test_normal(data, mu, sigma):
    n = len(data)
    xs = sorted(data)

    D = 0.0
    for i, x in enumerate(xs, start=1):
        F = normal_cdf(x, mu, sigma)
        Fn_right = i / n
        Fn_left = (i - 1) / n

        D = max(D, abs(Fn_right - F), abs(F - Fn_left))

    D_crit = 1.36 / math.sqrt(n)
    return D, D_crit


# ===============================
# ЭМПИРИЧЕСКАЯ ФУНКЦИЯ РАСПРЕДЕЛЕНИЯ
# ===============================

def empirical_cdf(data):
    xs = sorted(data)
    ys = []

    n = len(xs)
    for i in range(n):
        ys.append((i + 1) / n)

    return xs, ys


# ===============================
# ВИЗУАЛИЗАЦИЯ
# ===============================

def plot_histogram_with_normal(data, mu, sigma):
    plt.figure()

    plt.hist(data, bins=BINS, density=True)

    xmin = min(data)
    xmax = max(data)

    xs = [xmin + i * (xmax - xmin) / 400 for i in range(401)]
    ys = [normal_pdf(x, mu, sigma) for x in xs]

    plt.plot(xs, ys)

    plt.title("Гистограмма расстояний и нормальная аппроксимация")
    plt.xlabel("r — расстояние пчелы от начала координат после 8 шагов")
    plt.ylabel("f(r) — плотность вероятности")
    plt.grid(True)


def plot_ecdf_with_normal(data, mu, sigma):
    plt.figure()

    xs_emp, ys_emp = empirical_cdf(data)
    plt.step(xs_emp, ys_emp, where="post")

    xmin = min(data)
    xmax = max(data)
    xs = [xmin + i * (xmax - xmin) / 400 for i in range(401)]
    ys = [normal_cdf(x, mu, sigma) for x in xs]

    plt.plot(xs, ys)

    plt.title("Эмпирическая функция распределения и нормальная аппроксимация")
    plt.xlabel("r — расстояние пчелы от начала координат после 8 шагов")
    plt.ylabel("F(r) — функция распределения")
    plt.grid(True)


# ===============================
# MAIN
# ===============================

def main():
    print("ЛАБОРАТОРНАЯ РАБОТА №7")
    print("Моделирование случайных блужданий")
    print("Вариант: Пчёлы на квадратной решётке")
    print()
    print(f"M = {M} шагов")
    print(f"N = {N_BEES} пчёл")
    print(f"k = {BINS} интервалов")
    print(f"alpha = {ALPHA}")
    print()

    data = simulate_swarm(N_BEES)

    mu_hat = sample_mean(data)
    d_hat = sample_variance(data)
    sigma_hat = math.sqrt(d_hat)

    print("РЕЗУЛЬТАТЫ МОДЕЛИРОВАНИЯ:")
    print(f"Среднее расстояние: {mu_hat:.6f}")
    print(f"Выборочная дисперсия: {d_hat:.6f}")
    print(f"Выборочное СКО: {sigma_hat:.6f}")
    print(f"Минимум: {min(data):.6f}")
    print(f"Максимум: {max(data):.6f}")

    D, D_crit = ks_test_normal(data, mu_hat, sigma_hat)

    print()
    print("ПРОВЕРКА НОРМАЛЬНОЙ АППРОКСИМАЦИИ:")
    print(f"KS: D = {D:.6f}, D_crit = {D_crit:.6f}")

    if D <= D_crit:
        print("Гипотеза о нормальной аппроксимации ПРИНИМАЕТСЯ")
    else:
        print("Гипотеза о нормальной аппроксимации ОТВЕРГАЕТСЯ")

    plot_histogram_with_normal(data, mu_hat, sigma_hat)
    plot_ecdf_with_normal(data, mu_hat, sigma_hat)

    plt.show()


if __name__ == "__main__":
    main()