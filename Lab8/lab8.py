# -*- coding: utf-8 -*-
import math
import random
from statistics import NormalDist
import matplotlib.pyplot as plt


# ===============================
# ХАРДКОД / НАСТРОЙКИ
# ===============================

M = 8                       # число шагов по условию
PILOT_N = 200               # объем пробного эксперимента
BINS = 15                   # число интервалов гистограммы
ALPHA = 0.05                # уровень значимости => достоверность 0.95
CONFIDENCE = 1.0 - ALPHA

EPS_MEAN = 0.010             # требуемая точность для оценки среднего
EPS_VARIANCE = 0.020         # требуемая точность для оценки дисперсии

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


def central_moment_4(data):
    m = sample_mean(data)
    n = len(data)
    return sum((x - m) ** 4 for x in data) / n


def z_quantile(p):
    return NormalDist().inv_cdf(p)


# ===============================
# НОРМАЛЬНОЕ РАСПРЕДЕЛЕНИЕ
# ===============================

def normal_pdf(x, mu, sigma):
    z = (x - mu) / sigma
    return (1.0 / (sigma * math.sqrt(2.0 * math.pi))) * math.exp(-0.5 * z * z)


def normal_cdf(x, mu, sigma):
    z = (x - mu) / (sigma * math.sqrt(2.0))
    return 0.5 * (1.0 + math.erf(z))


# ===============================
# ПРИБЛИЖЕНИЕ КВАНТИЛЯ ХИ-КВАДРАТ
# Формула Уилсона–Хилферти
# ===============================

def chi_square_quantile(p, df):
    z = z_quantile(p)
    a = 2.0 / (9.0 * df)
    return df * (1.0 - a + z * math.sqrt(a)) ** 3


# ===============================
# ГЕНЕРАЦИЯ НАЧАЛЬНОЙ ТОЧКИ
# Равномерно внутри единичного круга
# ===============================

def generate_point_in_unit_circle():
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

        if r < 0.25:
            y += 1      # север
        elif r < 0.50:
            y -= 1      # юг
        elif r < 0.75:
            x += 1      # восток
        else:
            x -= 1      # запад

    return math.sqrt(x * x + y * y)


# ===============================
# МОДЕЛИРОВАНИЕ ВЫБОРКИ
# ===============================

def simulate_sample(n):
    data = []
    for _ in range(n):
        data.append(simulate_one_bee())
    return data


# ===============================
# КРИТЕРИЙ КОЛМОГОРОВА
# Проверка нормальной аппроксимации
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
    n = len(xs)
    ys = []

    for i in range(n):
        ys.append((i + 1) / n)

    return xs, ys


# ===============================
# ВИЗУАЛИЗАЦИЯ
# ===============================

def plot_histogram_with_normal(data, mu, sigma, title_suffix):
    plt.figure()

    plt.hist(data, bins=BINS, density=True)

    xmin = min(data)
    xmax = max(data)
    xs = [xmin + i * (xmax - xmin) / 400 for i in range(401)]
    ys = [normal_pdf(x, mu, sigma) for x in xs]

    plt.plot(xs, ys)

    plt.title(f"Гистограмма расстояний и нормальная аппроксимация ({title_suffix})")
    plt.xlabel("r — расстояние пчелы от начала координат")
    plt.ylabel("f(r) — плотность вероятности")
    plt.grid(True)


def plot_ecdf_with_normal(data, mu, sigma, title_suffix):
    plt.figure()

    xs_emp, ys_emp = empirical_cdf(data)
    plt.step(xs_emp, ys_emp, where="post")

    xmin = min(data)
    xmax = max(data)
    xs = [xmin + i * (xmax - xmin) / 400 for i in range(401)]
    ys = [normal_cdf(x, mu, sigma) for x in xs]

    plt.plot(xs, ys)

    plt.title(f"Эмпирическая функция распределения ({title_suffix})")
    plt.xlabel("r — расстояние пчелы от начала координат")
    plt.ylabel("F(r) — функция распределения")
    plt.grid(True)


# ===============================
# ПЛАНИРОВАНИЕ ДЛЯ ОЦЕНКИ СРЕДНЕГО
# ===============================

def required_n_for_mean_normal(sigma_hat, eps, confidence):
    z = z_quantile((1.0 + confidence) / 2.0)
    n = (z * sigma_hat / eps) ** 2
    return max(2, math.ceil(n))


def required_n_for_mean_chebyshev(sigma_hat, eps, alpha):
    # Из неравенства Чебышёва для среднего:
    # P(|X̄ - m| < eps) >= 1 - Var(X)/(n*eps^2)
    # Для достоверности 1-alpha:
    # n >= Var(X)/(alpha * eps^2)
    variance_hat = sigma_hat ** 2
    n = variance_hat / (alpha * eps * eps)
    return max(2, math.ceil(n))


# ===============================
# ПЛАНИРОВАНИЕ ДЛЯ ОЦЕНКИ ДИСПЕРСИИ
# ===============================

def variance_ci_normal(s2, n, alpha):
    df = n - 1

    chi2_left = chi_square_quantile(alpha / 2.0, df)
    chi2_right = chi_square_quantile(1.0 - alpha / 2.0, df)

    lower = df * s2 / chi2_right
    upper = df * s2 / chi2_left

    return lower, upper


def required_n_for_variance_normal(s2_pilot, eps, alpha):
    n = 2
    while True:
        lower, upper = variance_ci_normal(s2_pilot, n, alpha)
        half_width = max(s2_pilot - lower, upper - s2_pilot)

        if half_width <= eps:
            return n

        n += 1


def variance_half_width_asymptotic(mu4_hat, s2_hat, n, confidence):
    z = z_quantile((1.0 + confidence) / 2.0)

    # Асимптотически:
    # Var(S^2) ≈ (mu4 - sigma^4) / n
    value = mu4_hat - s2_hat * s2_hat
    if value < 0:
        value = 0.0

    return z * math.sqrt(value / n)


def required_n_for_variance_asymptotic(mu4_hat, s2_hat, eps, confidence):
    z = z_quantile((1.0 + confidence) / 2.0)

    value = mu4_hat - s2_hat * s2_hat
    if value <= 0:
        return 2

    n = (z * z * value) / (eps * eps)
    return max(2, math.ceil(n))


# ===============================
# ОЦЕНКА ДОСТИГНУТОЙ ТОЧНОСТИ
# ===============================

def achieved_mean_half_width(sigma_hat, n, confidence):
    z = z_quantile((1.0 + confidence) / 2.0)
    return z * sigma_hat / math.sqrt(n)


# ===============================
# MAIN
# ===============================

def main():
    print("ЛАБОРАТОРНАЯ РАБОТА №8")
    print("Тактическое планирование эксперимента")
    print("Вариант: Пчёлы на квадратной решётке")
    print()
    print(f"M = {M} шагов")
    print(f"N0 = {PILOT_N} — объём пробного эксперимента")
    print(f"k = {BINS} интервалов")
    print(f"alpha = {ALPHA}")
    print(f"confidence = {CONFIDENCE}")
    print(f"eps_mean = {EPS_MEAN}")
    print(f"eps_variance = {EPS_VARIANCE}")
    print()

    # ==========================================
    # 1. ПРОБНЫЙ ЭКСПЕРИМЕНТ
    # ==========================================
    pilot_data = simulate_sample(PILOT_N)

    mu0 = sample_mean(pilot_data)
    s20 = sample_variance(pilot_data)
    sigma0 = math.sqrt(s20)
    mu4_0 = central_moment_4(pilot_data)

    print("1) ПРОБНЫЙ ЭКСПЕРИМЕНТ")
    print(f"Среднее: {mu0:.6f}")
    print(f"Выборочная дисперсия: {s20:.6f}")
    print(f"Выборочное СКО: {sigma0:.6f}")
    print(f"Минимум: {min(pilot_data):.6f}")
    print(f"Максимум: {max(pilot_data):.6f}")

    D, D_crit = ks_test_normal(pilot_data, mu0, sigma0)

    print()
    print("ПРОВЕРКА НОРМАЛЬНОЙ АППРОКСИМАЦИИ ПО ПРОБНОЙ ВЫБОРКЕ:")
    print(f"KS: D = {D:.6f}, D_crit = {D_crit:.6f}")

    normal_ok = D <= D_crit

    if normal_ok:
        print("Гипотеза о нормальной аппроксимации ПРИНИМАЕТСЯ")
    else:
        print("Гипотеза о нормальной аппроксимации ОТВЕРГАЕТСЯ")

    plot_histogram_with_normal(pilot_data, mu0, sigma0, "пробный эксперимент")
    plot_ecdf_with_normal(pilot_data, mu0, sigma0, "пробный эксперимент")

    # ==========================================
    # 2. ПЛАНИРОВАНИЕ ОБЪЕМА ДЛЯ СРЕДНЕГО
    # ==========================================
    print()
    print("2) ПЛАНИРОВАНИЕ ОБЪЁМА ЭКСПЕРИМЕНТА ДЛЯ ОЦЕНКИ СРЕДНЕГО")

    if normal_ok:
        n_mean = required_n_for_mean_normal(sigma0, EPS_MEAN, CONFIDENCE)
        print("Используется нормальный подход:")
        print("n >= (z * sigma / eps)^2")
    else:
        n_mean = required_n_for_mean_chebyshev(sigma0, EPS_MEAN, ALPHA)
        print("Используется неравенство Чебышёва:")
        print("n >= D / (alpha * eps^2)")

    print(f"Требуемый объём для оценки среднего: n_mean = {n_mean}")

    # ==========================================
    # 3. ПЛАНИРОВАНИЕ ОБЪЕМА ДЛЯ ДИСПЕРСИИ
    # ==========================================
    print()
    print("3) ПЛАНИРОВАНИЕ ОБЪЁМА ЭКСПЕРИМЕНТА ДЛЯ ОЦЕНКИ ДИСПЕРСИИ")

    if normal_ok:
        n_var = required_n_for_variance_normal(s20, EPS_VARIANCE, ALPHA)
        print("Используется доверительный интервал для дисперсии")
        print("на основе распределения хи-квадрат")
    else:
        n_var = required_n_for_variance_asymptotic(mu4_0, s20, EPS_VARIANCE, CONFIDENCE)
        print("Используется асимптотический подход")
        print("Var(S^2) ≈ (mu4 - sigma^4) / n")

    print(f"Требуемый объём для оценки дисперсии: n_var = {n_var}")

    # ==========================================
    # 4. ИТОГОВЫЙ ЭКСПЕРИМЕНТ
    # Берём объем, достаточный для обеих задач
    # ==========================================
    n_final = max(n_mean, n_var)

    print()
    print("4) ИТОГОВЫЙ ЭКСПЕРИМЕНТ")
    print(f"Итоговый объём эксперимента: n_final = {n_final}")

    final_data = simulate_sample(n_final)

    mu_final = sample_mean(final_data)
    s2_final = sample_variance(final_data)
    sigma_final = math.sqrt(s2_final)
    mu4_final = central_moment_4(final_data)

    print(f"Оценка среднего: {mu_final:.6f}")
    print(f"Оценка дисперсии: {s2_final:.6f}")
    print(f"Оценка СКО: {sigma_final:.6f}")

    mean_half_width = achieved_mean_half_width(sigma_final, n_final, CONFIDENCE)

    print()
    print("ПРОВЕРКА ДОСТИГНУТОЙ ТОЧНОСТИ ДЛЯ СРЕДНЕГО:")
    print(f"Фактическая полуширина доверительного интервала: {mean_half_width:.6f}")
    print(f"Требуемая точность: {EPS_MEAN:.6f}")

    if normal_ok:
        lower_var, upper_var = variance_ci_normal(s2_final, n_final, ALPHA)
        var_half_width = max(s2_final - lower_var, upper_var - s2_final)

        print()
        print("ПРОВЕРКА ДОСТИГНУТОЙ ТОЧНОСТИ ДЛЯ ДИСПЕРСИИ:")
        print(f"Доверительный интервал для дисперсии: [{lower_var:.6f}; {upper_var:.6f}]")
        print(f"Фактическая полуширина интервала: {var_half_width:.6f}")
        print(f"Требуемая точность: {EPS_VARIANCE:.6f}")
    else:
        var_half_width = variance_half_width_asymptotic(mu4_final, s2_final, n_final, CONFIDENCE)

        print()
        print("ПРОВЕРКА ДОСТИГНУТОЙ ТОЧНОСТИ ДЛЯ ДИСПЕРСИИ:")
        print(f"Фактическая полуширина интервала (асимптотически): {var_half_width:.6f}")
        print(f"Требуемая точность: {EPS_VARIANCE:.6f}")

    plot_histogram_with_normal(final_data, mu_final, sigma_final, "итоговый эксперимент")
    plot_ecdf_with_normal(final_data, mu_final, sigma_final, "итоговый эксперимент")

    plt.show()


if __name__ == "__main__":
    main()