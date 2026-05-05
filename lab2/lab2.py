# -*- coding: utf8 -*-
import math
from dataclasses import dataclass
from typing import List, Tuple


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
    Формула (2.12):
    y_{n+1} = abs( a*(y mod b) - c*(y div b) )
    """
    value = p.a * (y % p.b) - p.c * (y // p.b)
    return abs(value)


def generate_sequence(n: int, y0: int, k: int = 1) -> List[float]:
    """
    Генерация n чисел на [0,1).
    Для варианта: k=1 -> x = y/d.
    """
    if k != 1:
        raise ValueError("В этом варианте используется k=1 (один датчик).")

    p = PARAMS_ALL[0]
    y = y0
    out: List[float] = []

    for _ in range(n):
        y = next_y(y, p)
        x = y / p.d
        out.append(x)

    return out


# ---------------------------
# 1) Критерий Пирсона (χ²)
# ---------------------------

def chi2_pearson_uniform(xs: List[float], k_bins: int) -> Tuple[float, int]:
    """
    Проверка равномерности на [0,1) критерием χ² Пирсона.
    Возвращает: (chi2_value, df)
    df = k_bins - 1
    """
    n = len(xs)
    expected = n / k_bins

    counts = [0] * k_bins
    for x in xs:
        # x in [0,1), интервал: [0, 1/k), ... [ (k-1)/k, 1 )
        idx = int(x * k_bins)
        if idx == k_bins:  # на всякий случай, если из-за округлений получилось ровно 1
            idx = k_bins - 1
        counts[idx] += 1

    chi2 = 0.0
    for mj in counts:
        chi2 += (mj - expected) ** 2 / expected

    df = k_bins - 1
    return chi2, df


def chi2_critical_wilson_hilferty(df: int, conf: float) -> float:
    """
    Приближённый квантиль χ² через аппроксимацию Уилсона–Хилферти.
    conf = 1 - alpha (например 0.95)
    """
    # z для нормального распределения: используем простую аппроксимацию
    # чтобы не тянуть scipy.
    z = normal_quantile(conf)
    return df * (1 - 2 / (9 * df) + z * math.sqrt(2 / (9 * df))) ** 3


def normal_quantile(p: float) -> float:
    """
    Аппроксимация квантиля N(0,1) (inverse CDF).
    """
    # Алгоритм Питера Дж. Акерса (приближённо), реализация через рациональные аппроксимации.
    # p в (0,1)
    if not (0.0 < p < 1.0):
        raise ValueError("p must be in (0,1)")

    # коэффициенты
    a = [-3.969683028665376e+01,  2.209460984245205e+02,
         -2.759285104469687e+02,  1.383577518672690e+02,
         -3.066479806614716e+01,  2.506628277459239e+00]

    b = [-5.447609879822406e+01,  1.615858368580409e+02,
         -1.556989798598866e+02,  6.680131188771972e+01,
         -1.328068155288572e+01]

    c = [-7.784894002430293e-03, -3.223964580411365e-01,
         -2.400758277161838e+00, -2.549732539343734e+00,
          4.374664141464968e+00,  2.938163982698783e+00]

    d = [ 7.784695709041462e-03,  3.224671290700398e-01,
          2.445134137142996e+00,  3.754408661907416e+00]

    plow = 0.02425
    phigh = 1 - plow

    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
               ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)
    elif p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5]) / \
                ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)
    else:
        q = p - 0.5
        r = q * q
        return (((((a[0]*r + a[1])*r + a[2])*r + a[3])*r + a[4])*r + a[5]) * q / \
               (((((b[0]*r + b[1])*r + b[2])*r + b[3])*r + b[4])*r + 1)


# ---------------------------
# 2) Критерий Колмогорова
# ---------------------------

def kolmogorov_test_uniform(xs: List[float], alpha: float = 0.05) -> Tuple[float, float]:
    """
    Возвращает (D, p_value) для проверки U[0,1).
    p_value вычисляем по асимптотической формуле Колмогорова.
    """
    n = len(xs)
    xs_sorted = sorted(xs)

    d_plus = 0.0
    d_minus = 0.0

    for i, x in enumerate(xs_sorted, start=1):
        fn = i / n
        fn_prev = (i - 1) / n
        f_theory = x  # F(x) = x для U[0,1)

        d_plus = max(d_plus, fn - f_theory)
        d_minus = max(d_minus, f_theory - fn_prev)

    d = max(d_plus, d_minus)
    lam = d * math.sqrt(n)

    p_value = kolmogorov_p_value(lam)
    return d, p_value


def kolmogorov_p_value(lam: float) -> float:
    """
    p-value для статистики λ = D*sqrt(n).
    Используем стандартную асимптотическую формулу:
    P(D_n <= d) ≈ 1 - 2 * Σ_{k>=1} (-1)^{k-1} exp(-2 k^2 λ^2)
    Тогда p-value = 1 - P(D_n <= d)
    """
    if lam <= 0:
        return 1.0

    s = 0.0
    # 20 членов ряда обычно достаточно
    for k in range(1, 21):
        term = (-1) ** (k - 1) * math.exp(-2 * (k * k) * (lam * lam))
        s += term

    cdf = 1 - 2 * s
    # численные погрешности
    cdf = min(1.0, max(0.0, cdf))

    return 1.0 - cdf


# ---------------------------------------------
# 3) Тест длины серий единиц (p_split = 0.4)
# ---------------------------------------------

def ones_runs_length_test(xs: List[float], p_split: float = 0.4, beta: float = 0.95) -> Tuple[int, int, float, float, float, bool]:
    """
    Тест длины серий единиц.
    y_i = 1, если x_i >= p_split, иначе 0.
    Возвращает:
    N1, K1, Mz_hat, lower, upper, accept
    """
    ys = [1 if x >= p_split else 0 for x in xs]

    n1 = sum(ys)

    # K1: число серий единиц
    k1 = 0
    in_run = False
    for y in ys:
        if y == 1 and not in_run:
            k1 += 1
            in_run = True
        elif y == 0:
            in_run = False

    if k1 == 0:
        # нет серий единиц => тест формально не применим
        return n1, k1, float('nan'), float('nan'), float('nan'), False

    mz_hat = n1 / k1

    # Теоретические формулы (как в методичке для "серий единиц"):
    # p = P(0) = p_split, q = P(1) = 1 - p_split
    p0 = p_split
    q1 = 1.0 - p0

    # Для серий единиц:
    # M(Z) = 1/p0
    # D(Z) = (1 - p0) / p0^2
    m_theory = 1.0 / p0
    d_theory = (1.0 - p0) / (p0 * p0)

    # t_beta из таблицы стандартного нормального распределения
    t_beta = normal_quantile(0.5 + beta / 2)  # двусторонний интервал

    half = t_beta * math.sqrt(d_theory / k1)
    lower = m_theory - half
    upper = m_theory + half

    accept = (lower <= mz_hat <= upper)
    return n1, k1, mz_hat, lower, upper, accept


def main() -> None:
    # Параметры лабораторной
    n = 1600

    # Для χ² обычно берут 20..50 (в методичке).
    # Можно оставить 20 по умолчанию.
    k_bins = 20

    alpha = 0.1      # уровень значимости для χ² и Колмогорова
    beta = 0.95       # надёжность для теста серий (t_beta)
    p_split = 0.4     # разделительный элемент

    raw = input("Введите начальное целое Y0 (Enter = 12345): ").strip()
    y0 = int(raw) if raw else 12345

    p = PARAMS_ALL[0]
    y0 = y0 % p.d
    if y0 == 0:
        y0 = 1

    xs = generate_sequence(n=n, y0=y0, k=1)
    print(f"\nСгенерировано N = {len(xs)} чисел на [0,1).")

    # --- 1) Пирсон χ² ---
    chi2, df = chi2_pearson_uniform(xs, k_bins=k_bins)
    chi2_crit = chi2_critical_wilson_hilferty(df=df, conf=1 - alpha)
    pearson_ok = chi2 <= chi2_crit

    print("\n[Критерий Пирсона χ²]")
    print(f"k (интервалов) = {k_bins}, df = {df}, alpha = {alpha}")
    print(f"χ² наблюд. = {chi2:.4f}")
    print(f"χ² критич. (≈) = {chi2_crit:.4f}")
    print("Результат:", "ГИПОТЕЗА ПРИНИМАЕТСЯ (равномерно)" if pearson_ok else "ГИПОТЕЗА ОТКЛОНЯЕТСЯ")

    # --- 2) Колмогоров ---
    d_stat, p_value = kolmogorov_test_uniform(xs, alpha=alpha)
    kolmog_ok = p_value >= alpha

    print("\n[Критерий Колмогорова]")
    print(f"alpha = {alpha}")
    print(f"D = {d_stat:.6f}")
    print(f"p-value ≈ {p_value:.6f}")
    print("Результат:", "ГИПОТЕЗА ПРИНИМАЕТСЯ (равномерно)" if kolmog_ok else "ГИПОТЕЗА ОТКЛОНЯЕТСЯ")

    # --- 3) Серии единиц (p=0.4) ---
    n1, k1, mz_hat, lower, upper, runs_ok = ones_runs_length_test(xs, p_split=p_split, beta=beta)

    print("\n[Тест длины серий единиц]")
    print(f"p (разделитель) = {p_split}, beta = {beta}")
    print(f"N1 (число единиц) = {n1}")
    print(f"K1 (число серий единиц) = {k1}")

    if k1 == 0:
        print("Серий единиц нет -> тест неприменим (плохой признак для случайности).")
    else:
        print(f"M̂z = N1/K1 = {mz_hat:.6f}")
        print(f"Доверительный интервал: [{lower:.6f}; {upper:.6f}]")
        print("Результат:", "ГИПОТЕЗА ПРИНИМАЕТСЯ" if runs_ok else "ГИПОТЕЗА ОТКЛОНЯЕТСЯ")

    # Итог
    print("\n[ИТОГ]")
    ok_all = pearson_ok and kolmog_ok and runs_ok
    print("Последовательность считается качественной по всем тестам."
          if ok_all else
          "Последовательность НЕ прошла хотя бы один из тестов (качество сомнительно).")


if __name__ == "__main__":
    main()
