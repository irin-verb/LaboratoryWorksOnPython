# -*- coding: utf-8 -*-
import math
import random
import matplotlib.pyplot as plt


# ===============================
# ХАРДКОД ПАРАМЕТРОВ ВАРИАНТА
# ===============================

MU = -2.0
SIGMA2 = 0.81
SIGMA = math.sqrt(SIGMA2)

N = 1000          # объем выборки
BINS = 15         # число интервалов
ALPHA = 0.05      # уровень значимости

# Для воспроизводимости (можешь убрать)
random.seed(42)


# ===============================
# Теоретические функции
# ===============================

def normal_pdf(x):
    z = (x - MU) / SIGMA
    return (1.0 / (SIGMA * math.sqrt(2.0 * math.pi))) * math.exp(-0.5 * z * z)


def normal_cdf(x):
    z = (x - MU) / (SIGMA * math.sqrt(2.0))
    return 0.5 * (1.0 + math.erf(z))


# ===============================
# 1) Метод ЦПТ
# ===============================

def generate_normal_clt():
    data = []
    for _ in range(N):
        s = 0.0
        for _ in range(12):
            s += random.random()
        x0 = s - 6.0  # sum(U) - 6
        x = MU + SIGMA * x0
        data.append(x)
    return data


# ===============================
# 2) Метод аппроксимации
# ===============================

def generate_normal_approx():
    data = []
    k = math.sqrt(8.0 / math.pi)

    for _ in range(N):
        r = random.random()
        r = max(min(r, 1 - 1e-12), 1e-12)

        x0 = (1.0 / k) * math.log((1.0 + r) / (1.0 - r))

        if random.random() < 0.5:
            x0 = -x0

        x = MU + SIGMA * x0
        data.append(x)

    return data


# ===============================
# Оценки
# ===============================

def sample_mean(data):
    return sum(data) / len(data)


def sample_variance(data):
    m = sample_mean(data)
    return sum((x - m) ** 2 for x in data) / (len(data) - 1)


# ===============================
# Критерий Колмогорова
# ===============================

def ks_test(data):
    n = len(data)
    xs = sorted(data)

    D = 0.0
    for i, x in enumerate(xs, start=1):
        F = normal_cdf(x)
        Fn_right = i / n
        Fn_left = (i - 1) / n
        D = max(D, abs(Fn_right - F), abs(F - Fn_left))

    # критическое значение при alpha=0.05
    D_crit = 1.36 / math.sqrt(n)

    return D, D_crit


# ===============================
# Визуализация
# =============================== 

def plot_results(data, title):
    # ===============================
    # Гистограмма + теоретическая PDF
    # ===============================
    plt.figure()
    plt.hist(data, bins=BINS, density=True)

    xmin = min(data)
    xmax = max(data)

    xs = [xmin + i * (xmax - xmin) / 400 for i in range(401)]
    ys = [normal_pdf(x) for x in xs]

    plt.plot(xs, ys)

    plt.title(title + " — Гистограмма плотности")
    plt.xlabel("x — случайная величина")
    plt.ylabel("f(x) — плотность вероятности")
    plt.grid(True)


    # ===============================
    # ECDF + теоретическая CDF
    # ===============================
    plt.figure()
    xs_sorted = sorted(data)
    ys_ecdf = [(i + 1) / N for i in range(N)]

    plt.step(xs_sorted, ys_ecdf, where="post")

    ys_cdf = [normal_cdf(x) for x in xs]
    plt.plot(xs, ys_cdf)

    plt.title(title + " — Функция распределения")
    plt.xlabel("x — случайная величина")
    plt.ylabel("F(x) — функция распределения")
    plt.grid(True)


# ===============================
# MAIN
# ===============================

def run_method(name, generator):
    print("\n==============================")
    print("Метод:", name)

    data = generator()

    m_hat = sample_mean(data)
    d_hat = sample_variance(data)

    print(f"Оценка матожидания: {m_hat:.6f} (теор. {MU})")
    print(f"Оценка дисперсии:   {d_hat:.6f} (теор. {SIGMA2})")

    D, D_crit = ks_test(data)

    print(f"KS: D = {D:.6f}, D_crit = {D_crit:.6f}")

    if D <= D_crit:
        print("Гипотеза о нормальном распределении ПРИНИМАЕТСЯ")
    else:
        print("Гипотеза ОТВЕРГАЕТСЯ")

    plot_results(data, name)


if __name__ == "__main__":

    print("Нормальное распределение N(-2, 0.81)")
    print(f"n = {N}, k = {BINS}, alpha = {ALPHA}")

    run_method("ЦПТ (12 сумм)", generate_normal_clt)
    run_method("Метод аппроксимации", generate_normal_approx)

    plt.show()
