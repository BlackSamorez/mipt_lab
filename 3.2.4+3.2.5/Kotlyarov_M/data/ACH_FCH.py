# script3_ACH_FCH_final_corrected_v4.py
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d, UnivariateSpline
from scipy.optimize import fsolve
import os

# --- Определение функций форматирования оси Y до их использования ---
def pi_formatter(x, pos):
    from fractions import Fraction
    multiple = x / np.pi
    frac = Fraction(multiple).limit_denominator(10)
    num = frac.numerator
    den = frac.denominator
    if den == 1:
        if num == 0:
            return "0"
        elif num == 1:
            return r"$\pi$"
        elif num == -1:
            return r"$-\pi$"
        else:
            return r"${}\pi$".format(num)
    else:
        if num == 0:
            return "0"
        elif num == 1:
            return r"$\frac{{\pi}}{{{}}}$".format(den)
        elif num == -1:
            return r"$-\frac{{\pi}}{{{}}}$".format(den)
        else:
            return r"$\frac{{{}}}{{{}}}\pi$".format(num, den)

def pi_formatter_orig(x, pos):
    from fractions import Fraction
    multiple = x / np.pi
    frac = Fraction(multiple).limit_denominator(10)
    num = frac.numerator
    den = frac.denominator
    if den == 1:
        if num == 0:
            return "0"
        elif num == 1:
            return r"$\pi$"
        elif num == -1:
            return r"$-\pi$"
        else:
            return r"${}\pi$".format(num)
    else:
        if num == 0:
            return "0"
        elif num == 1:
            return r"$\frac{{\pi}}{{{}}}$".format(den)
        elif num == -1:
            return r"$-\frac{{\pi}}{{{}}}$".format(den)
        else:
            return r"$\frac{{{}}}{{{}}}\pi$".format(num, den)
# --- Конец определения функций ---

# Создаем папку для графиков, если её нет
graphics_folder = "../Graphics"
os.makedirs(graphics_folder, exist_ok=True)

# --- 1. Чтение данных из FR_PR.xlsx ---
try:
    df = pd.read_excel('FR_PR.xlsx', sheet_name='Sheet1', header=None)
    if len(df) < 8: # Нужно 8 строк данных (0-7), плюс может быть пустая 8 (индекс 8)
        print("Ошибка: Не хватает данных в FR_PR.xlsx (нужны 8 строк данных).")
        exit()

    # Читаем строки
    # Строка 0: ν/ν₀ (нормированная частота)
    nu_norm_series = df.iloc[0, 1:].dropna()   # ν/ν₀
    dnu_norm_series = df.iloc[1, 1:].dropna()  # σ_{ν/ν₀}
    U_U0_series = df.iloc[2, 1:].dropna() # U/U₀
    dU_U0_series = df.iloc[3, 1:].dropna()# σ_{U/U₀}
    # Строка 4: ν (частота в кГц)
    nu_series = df.iloc[4, 1:].dropna()   # ν, кГц
    dnu_series = df.iloc[5, 1:].dropna()  # σ_ν, кГц
    # Строка 6: Δφ (фазовый сдвиг в рад) - ПРЕДПОЛАГАЕТСЯ, ЧТО РАССЧИТАН КАК 2πνΔx
    Delta_phi_series = df.iloc[6, 1:].dropna() # Δφ, рад
    # Строка 7: σ_{Δx} (погрешность Δx в мкс) - используем как σ_{Δφ}
    dDelta_x_series = df.iloc[7, 1:].dropna() # σ_{Δx} (мкс) -> σ_{Δφ} (рад)

    # Преобразуем в numpy массивы
    nu_norm_data_orig = nu_norm_series.astype(float).to_numpy()
    dnu_norm_data_orig = dnu_norm_series.astype(float).to_numpy()
    U_U0_data_orig = U_U0_series.astype(float).to_numpy()
    dU_U0_data_orig = dU_U0_series.astype(float).to_numpy()
    nu_data_orig = nu_series.astype(float).to_numpy() * 1e3  # переводим ν в Гц
    dnu_data_orig = dnu_series.astype(float).to_numpy() * 1e3 # σ_ν в Гц
    Delta_phi_data_orig = Delta_phi_series.astype(float).to_numpy() # Δφ в рад
    dDelta_phi_data_orig = dDelta_x_series.astype(float).to_numpy() * 1e-6 # σ_{Δx} в мкс -> σ_{Δφ} в рад (приблизительно)

    print("Данные успешно загружены из FR_PR.xlsx:")
    print(f"nu_norm_orig (ν/ν₀): {nu_norm_data_orig}")
    print(f"sigma_nu_norm_orig: {dnu_norm_data_orig}")
    print(f"U_U0_orig: {U_U0_data_orig}")
    print(f"sigma_U_U0_orig: {dU_U0_data_orig}")
    print(f"nu_orig (Гц): {nu_data_orig}")
    print(f"sigma_nu_orig (Гц): {dnu_data_orig}")
    print(f"Delta_phi_orig (рад): {Delta_phi_data_orig}")
    print(f"sigma_Delta_phi_orig (рад): {dDelta_phi_data_orig}")

    # --- 1.1. Сортировка данных по возрастанию nu (или nu_norm, они должны быть связаны) ---
    # Лучше сортировать по nu, так как он используется для ФЧХ
    sort_indices = np.argsort(nu_data_orig)
    nu_norm_data = nu_norm_data_orig[sort_indices]
    dnu_norm_data = dnu_norm_data_orig[sort_indices]
    U_U0_data = U_U0_data_orig[sort_indices]
    dU_U0_data = dU_U0_data_orig[sort_indices]
    nu_data = nu_data_orig[sort_indices]
    dnu_data = dnu_data_orig[sort_indices]
    Delta_phi_data = Delta_phi_data_orig[sort_indices] # Сохраняем оригинальный массив
    dDelta_phi_data = dDelta_phi_data_orig[sort_indices]

    print(f"\nДанные отсортированы по возрастанию частоты nu (Гц): {nu_data}")
    print(f"Соответствующие nu/nu0: {nu_norm_data}")
    print(f"Соответствующие Delta_phi (до инверсии): {Delta_phi_data}")

    # --- 1.2. ИНВЕРСИЯ ФАЗЫ для соответствия рис. 5 (Δφ = φ(U_C) - φ(U_gen)) ---
    # Из анализа выше: данные в файле, вероятно, представляют φ(U_gen) - φ(U_C)
    # Для соответствия рис. 5 и методу из п. 2.7.9, нужно φ(U_C) - φ(U_gen)
    print("Инвертируем знак Delta_phi для соответствия φ(U_C) - φ(U_gen)")
    Delta_phi_data_for_FCH = -Delta_phi_data # Инвертируем знак
    print(f"Delta_phi (после инверсии для ФЧХ): {Delta_phi_data_for_FCH}")

except FileNotFoundError:
    print("Ошибка: Файл 'FR_PR.xlsx' не найден.")
    exit()
except Exception as e:
    print(f"Ошибка при чтении файла FR_PR.xlsx: {e}")
    import traceback
    traceback.print_exc()
    exit()

# --- 2. Определение резонансной частоты nu0 (по АЧХ, из нормированной частоты) ---
# Найдём индекс, где nu_norm_data близко к 1.0 (это nu0)
max_idx_norm = np.argmin(np.abs(nu_norm_data - 1.0))
# Также найдём индекс максимальной амплитуды U_U0_data
max_idx_U = np.argmax(U_U0_data)

# Проверим, совпадают ли они или близки
print(f"Индекс max(U/U0): {max_idx_U}, nu_norm = {nu_norm_data[max_idx_U]:.4f}")
print(f"Индекс min(|nu_norm - 1|): {max_idx_norm}, nu_norm = {nu_norm_data[max_idx_norm]:.4f}")
# Возьмём за основу индекс из nu_norm_data, так как он должен быть точно 1.0 при резонансе
nu0_ACH = nu_data[max_idx_norm] # или nu_data[max_idx_U], если они близки
U0_norm = U_U0_data[max_idx_norm] # или U_U0_data[max_idx_U]
print(f"\nРезонансная частота nu0 (по АЧХ): {nu0_ACH/1e3:.3f} кГц")

# --- 3. Построение АЧХ: U/U0 = f(nu/nu0) ---
# nu_norm уже нормирована
dnu_norm = dnu_norm_data # σ_{nu/nu0} уже есть

# --- 3.1. Интерполяция АЧХ ---
try:
    # Используем сплайн для более плавной интерполяции
    # Убедимся, что nu_norm_data строго возрастает (должно быть после сортировки)
    spline_ACH = UnivariateSpline(nu_norm_data, U_U0_data, s=0, k=3) # k=3
    # Создаём плотную сетку для плавной кривой
    nu_norm_smooth = np.linspace(min(nu_norm_data), max(nu_norm_data), 500)
    U_U0_smooth = spline_ACH(nu_norm_smooth)
    print("Сплайн для АЧХ успешно создан.")
except Exception as e:
    print(f"Ошибка при создании сплайна для АЧХ: {e}")
    # Если сплайн не получается, используем линейную интерполяцию
    try:
        f_interp_ACH = interp1d(nu_norm_data, U_U0_data, kind='linear', fill_value="extrapolate")
        nu_norm_smooth = np.linspace(min(nu_norm_data), max(nu_norm_data), 500)
        U_U0_smooth = f_interp_ACH(nu_norm_smooth)
        print("Линейная интерполяция для АЧХ успешно создана.")
    except Exception as e2:
        print(f"Ошибка при создании линейной интерполяции для АЧХ: {e2}")
        # Если и линейная не работает, используем просто точки
        nu_norm_smooth = nu_norm_data
        U_U0_smooth = U_U0_data
        print("Используем исходные точки для АЧХ.")

# --- 3.2. Расчёт Q по АЧХ (ширина на уровне 1/√2) ---
U_half = U0_norm / np.sqrt(2)  # уровень 1/√2
print(f"\nУровень 1/√2: {U_half:.4f}")

# Ищем пересечения с U_half с использованием ЭКСПЕРИМЕНТАЛЬНЫХ данных
Q_ACH = np.nan
try:
    # Найдём индекс максимума U_U0_data (это резонанс)
    max_idx_U = np.argmax(U_U0_data)

    # Найдём точки слева и справа от максимума, где U_U0_data близка к U_half

    # --- Левая граница ---
    # Рассмотрим данные слева от максимума
    U_left_part = U_U0_data[:max_idx_U]
    nu_left_part = nu_norm_data[:max_idx_U]

    # Найдём индекс, где разница с U_half минимальна в левой части
    if len(U_left_part) > 0:
        idx_left_min_diff = np.argmin(np.abs(U_left_part - U_half))
        nu_norm_left = nu_left_part[idx_left_min_diff]
        print(f"Найдена приближённая левая граница: nu_norm_left = {nu_norm_left:.4f}")
    else:
        print("Нет данных слева от максимума для поиска левой границы.")
        nu_norm_left = np.nan

    # --- Правая граница ---
    # Рассмотрим данные справа от максимума (включая максимум)
    U_right_part = U_U0_data[max_idx_U:]
    nu_right_part = nu_norm_data[max_idx_U:]

    # Найдём индекс, где разница с U_half минимальна в правой части
    if len(U_right_part) > 0:
        idx_right_min_diff = np.argmin(np.abs(U_right_part - U_half))
        # Индекс в глобальном массиве
        global_idx_right = max_idx_U + idx_right_min_diff
        nu_norm_right = nu_norm_data[global_idx_right]
        print(f"Найдена приближённая правая граница: nu_norm_right = {nu_norm_right:.4f}")
    else:
        print("Нет данных справа от максимума для поиска правой границы.")
        nu_norm_right = np.nan

    # Проверим, что обе границы найдены и левая меньше правой (относительно nu0)
    # и что они не на индексах самого максимума
    if not (np.isnan(nu_norm_left) or np.isnan(nu_norm_right)):
        if max_idx_U < len(nu_norm_data) and abs(nu_norm_left - nu_norm_data[max_idx_U]) < 1e-6:
             print("Предупреждение: Левая граница совпадает с резонансной точкой.")
        if max_idx_U < len(nu_norm_data) and abs(nu_norm_right - nu_norm_data[max_idx_U]) < 1e-6:
             print("Предупреждение: Правая граница совпадает с резонансной точкой.")

        if nu_norm_left < nu_norm_data[max_idx_U] and nu_norm_right > nu_norm_data[max_idx_U]:
            delta_nu_norm = nu_norm_right - nu_norm_left
            if delta_nu_norm <= 0:
                print(f"Предупреждение: Ширина АЧХ delta_nu_norm = {delta_nu_norm:.4f} не положительна. Q не будет рассчитан.")
            else:
                # Q = nu0 / Delta_nu
                # Delta_nu = delta_nu_norm * nu0_ACH
                # Q_ACH = nu0_ACH / (delta_nu_norm * nu0_ACH) = 1 / delta_nu_norm
                Q_ACH = 1 / delta_nu_norm
                print(f"Ширина АЧХ на уровне 1/√2 (по эксп. точкам): Δ(nu/nu0) = {delta_nu_norm:.4f}")
                print(f"Добротность по АЧХ: Q_ACH = {Q_ACH:.2f}")
        else:
            print("Не удалось определить корректные границы для расчёта Q по АЧХ (левая граница >= правой или одна из них на резонансе).")
            print(f"  nu_norm_left: {nu_norm_left}")
            print(f"  nu_norm_right: {nu_norm_right}")
            print(f"  nu_norm (резонанс): {nu_norm_data[max_idx_U]:.4f}")
    else:
        print("Не удалось определить границы для расчёта Q по АЧХ (одна или обе равны NaN).")
        print(f"  nu_norm_left: {nu_norm_left if 'nu_norm_left' in locals() else 'not defined'}")
        print(f"  nu_norm_right: {nu_norm_right if 'nu_norm_right' in locals() else 'not defined'}")

except Exception as e:
    print(f"Ошибка при расчёте ширины АЧХ (по эксп. точкам): {e}")
    print(f"Детали ошибки: {e}")

# --- 3.3. Построение АЧХ ---
plt.figure(figsize=(8, 5))
plt.errorbar(nu_norm_data, U_U0_data,
             xerr=dnu_norm_data, yerr=dU_U0_data,
             fmt='o', ecolor='red', markersize=6,
             capsize=5, capthick=1,
             label='Экспериментальные данные')
if len(nu_norm_smooth) == len(U_U0_smooth) and len(nu_norm_smooth) > 1:
    plt.plot(nu_norm_smooth, U_U0_smooth, 'b-', label='Интерполированная кривая', linewidth=1)
plt.axhline(y=U_half, color='g', linestyle='--', label=f'Уровень 1/√2 = {U_half:.3f}')
plt.xlabel(r'$\nu / \nu_0$')
plt.ylabel(r'$U / U_0$')
plt.title('АЧХ колебательного контура')
plt.grid(True, alpha=0.5)
plt.legend()
output_filename_ACH = 'ACH_plot_final_corrected.png'
full_output_path_ACH = os.path.join(graphics_folder, output_filename_ACH)
plt.savefig(full_output_path_ACH)
print(f"АЧХ график сохранен в файл: {full_output_path_ACH}")
try:
    plt.show()
except:
    pass
plt.close() # Закрываем первый график

# --- 4. Интерполяция ФЧХ (с инвертированной фазой) ---
try:
    # Используем сплайн для более плавной интерполяции
    # Убедимся, что nu_data строго возрастает (должно быть после сортировки)
    spline_FCH = UnivariateSpline(nu_data, Delta_phi_data_for_FCH, s=0, k=3) # Используем инвертированную фазу
    # Создаём плотную сетку для плавной кривой
    nu_smooth = np.linspace(min(nu_data), max(nu_data), 500)
    Delta_phi_smooth = spline_FCH(nu_smooth) # Это теперь инвертированная фаза
    print("Сплайн для ФЧХ (инвертированной) успешно создан.")
except Exception as e:
    print(f"Ошибка при создании сплайна для ФЧХ (инвертированной): {e}")
    # Если сплайн не получается, используем линейную интерполяцию
    try:
        f_interp_FCH = interp1d(nu_data, Delta_phi_data_for_FCH, kind='linear', fill_value="extrapolate") # Используем инвертированную фазу
        nu_smooth = np.linspace(min(nu_data), max(nu_data), 500)
        Delta_phi_smooth = f_interp_FCH(nu_smooth) # Это теперь инвертированная фаза
        print("Линейная интерполяция для ФЧХ (инвертированной) успешно создана.")
    except Exception as e2:
        print(f"Ошибка при создании линейной интерполяции для ФЧХ (инвертированной): {e2}")
        # Если и линейная не работает, используем просто точки
        nu_smooth = nu_data
        Delta_phi_smooth = Delta_phi_data_for_FCH # Это теперь инвертированная фаза
        print("Используем исходные точки для ФЧХ (инвертированной).")

# --- 4.2. Проверка, достигает ли ФЧХ уровня -π/2 ---
target_phi_FCH = -np.pi / 2
min_phi_smooth = np.min(Delta_phi_smooth)
max_phi_smooth = np.max(Delta_phi_smooth)
print(f"Минимальное значение Delta_phi (инвертированное, интерполированное): {min_phi_smooth:.3f} рад (-π/2 = {target_phi_FCH:.3f})")
print(f"Максимальное значение Delta_phi (инвертированное, интерполированное): {max_phi_smooth:.3f} рад")
if min_phi_smooth > target_phi_FCH:
    print("Предупреждение: Интерполированная ФЧХ (инвертированная) не достигает уровня -π/2.")
    print("Расчёт Q по ФЧХ будет невозможен.")
    Q_FCH = np.nan
    Q_FCH_method9 = np.nan
else:
    # --- 4.3. Расчёт Q по ФЧХ (по методу п. 2.7.9) ---
    Q_FCH_method9 = np.nan
    try:
        # Найдём приближённый индекс, где Delta_phi близка к -pi/2 в интерполированной кривой
        target_idx_approx = np.argmin(np.abs(Delta_phi_smooth - target_phi_FCH))
        nu0_FCH_approx = nu_smooth[target_idx_approx]

        # Уточним с помощью интерполяции
        # Найдём ближайшие точки к -pi/2 в интерполированной кривой
        region_indices = np.argsort(np.abs(Delta_phi_smooth - target_phi_FCH))[:5] # 5 ближайших точек
        region_nu = nu_smooth[region_indices]
        region_phi = Delta_phi_smooth[region_indices]

        # Построим интерполяцию в этой области
        # Используем линейную интерполяцию: f(phi) = nu
        f_phi_interp_local = interp1d(region_phi, region_nu, kind='linear', fill_value="extrapolate")
        nu0_FCH = f_phi_interp_local(target_phi_FCH)

        print(f"Резонансная частота по ФЧХ (уточнённая): {nu0_FCH/1e3:.3f} кГц")

        # --- 4.4. Реализация метода из п. 2.7.9 ---
        # 1. Построить φ(ω) (уже сделано, Delta_phi_smooth)
        # 2. Отметить уровень -π/2 (target_phi_FCH)
        # 3. Зеркально отразить нижнюю часть относительно -π/2
        #    Нижняя часть - это где φ < -π/2
        #    Отражённая часть: φ_refl = -π/2 + (-π/2 - φ) = -π - φ
        phi_reflected_smooth = np.where(Delta_phi_smooth < target_phi_FCH, -np.pi - Delta_phi_smooth, Delta_phi_smooth)

        # 4. Измерить Δω на уровне -π/4 (относительно отражённой кривой)
        #    Нужно найти частоты, где phi_reflected_smooth = -π/4
        target_phi_refl = -np.pi / 4
        print(f"Целевой уровень для Δω: {target_phi_refl:.3f} рад")

        # Найдём приближённые индексы для пересечений с -π/4 на отражённой кривой
        # Ищем слева и справа от nu0_FCH
        idx_0_FCH = np.argmin(np.abs(nu_smooth - nu0_FCH))
        left_part_refl = phi_reflected_smooth[:idx_0_FCH]
        right_part_refl = phi_reflected_smooth[idx_0_FCH:]

        # Ищем пересечение слева от резонанса
        left_cross_indices = np.where(np.diff(np.sign(left_part_refl - target_phi_refl)))[0]
        if len(left_cross_indices) > 0:
            i_left = left_cross_indices[-1] # Берём последнее пересечение до резонанса
            # Линейная интерполяция между двумя точками
            x1_l, x2_l = nu_smooth[i_left], nu_smooth[i_left+1]
            y1_l, y2_l = phi_reflected_smooth[i_left], phi_reflected_smooth[i_left+1]
            omega_left = x1_l + (target_phi_refl - y1_l) * (x2_l - x1_l) / (y2_l - y1_l)
            print(f"Найдена левая граница Δω: ω_left = {omega_left/1e3:.3f} кГц")
        else:
            print("Не найдена левая граница Δω на отражённой кривой.")
            omega_left = np.nan

        # Ищем пересечение справа от резонанса
        right_cross_indices = np.where(np.diff(np.sign(right_part_refl - target_phi_refl)))[0]
        if len(right_cross_indices) > 0:
            i_right = right_cross_indices[0] + idx_0_FCH # Индекс в глобальном массиве
            # Линейная интерполяция между двумя точками
            x1_r, x2_r = nu_smooth[i_right], nu_smooth[i_right+1]
            y1_r, y2_r = phi_reflected_smooth[i_right], phi_reflected_smooth[i_right+1]
            omega_right = x1_r + (target_phi_refl - y1_r) * (x2_r - x1_r) / (y2_r - y1_r)
            print(f"Найдена правая граница Δω: ω_right = {omega_right/1e3:.3f} кГц")
        else:
            print("Не найдена правая граница Δω на отражённой кривой.")
            omega_right = np.nan

        if not (np.isnan(omega_left) or np.isnan(omega_right)):
            delta_omega = omega_right - omega_left
            if delta_omega <= 0:
                print(f"Предупреждение: Δω = {delta_omega:.2f} не положительна. Q не будет рассчитан.")
            else:
                Q_FCH_method9 = nu0_FCH / delta_omega
                print(f"Ширина отражённой ФЧХ на уровне -π/4: Δω = {delta_omega/1e3:.3f} кГц")
                print(f"Добротность по ФЧХ (метод 9): Q_FCH_method9 = {Q_FCH_method9:.2f}")
        else:
            print("Не удалось определить границы для расчёта Q по ФЧХ (метод 9): одна или обе равны NaN.")
            print(f"  omega_left: {omega_left}")
            print(f"  omega_right: {omega_right}")


    except Exception as e:
        print(f"Ошибка при расчёте Q по ФЧХ (метод 9): {e}")
        print(f"Детали ошибки: {e}")
        Q_FCH_method9 = np.nan

    # Сохраняем Q_FCH_method9 в Q_FCH для совместимости
    Q_FCH = Q_FCH_method9


# --- 4.6. Построение ФЧХ (единый график) ---
import matplotlib.ticker as ticker # Добавляем импорт

plt.figure(figsize=(10, 6)) # Увеличим размер для отражённой кривой

# Оригинальная инвертированная кривая
plt.plot(nu_smooth/nu0_ACH, Delta_phi_smooth, 'c-', label='Интерполированная ФЧХ', linewidth=1)

# Экспериментальные данные с крестами и погрешностями
# Экспериментальные данные с крестами и погрешностями
plt.errorbar(nu_data/nu0_ACH, Delta_phi_data_for_FCH, 
             yerr=dDelta_phi_data, 
             fmt='+', ecolor='red', markersize=10, markeredgewidth=2, 
             capsize=0, elinewidth=1,
             label='Экспериментальные данные')
# Отражённая кривая
plt.plot(nu_smooth/nu0_ACH, phi_reflected_smooth, 'm--', label='Отражённая кривая', linewidth=1)

# Уровень -π/2
plt.axhline(y=target_phi_FCH, color='gray', linestyle='--', label=r'$-\pi/2$')
# Уровень -π/4
plt.axhline(y=target_phi_refl, color='red', linestyle=':', label=r'$-\pi/4$ (уровень для $\Delta\omega$)')
# Вертикальная линия резонанса (по ФЧХ)
if 'nu0_FCH' in locals() and not np.isnan(nu0_FCH):
    plt.axvline(x=nu0_FCH/nu0_ACH, color='orange', linestyle='-.', label=f'$\\nu_0$ (ФЧХ) = {nu0_FCH/1e3:.3f} кГц')

# Отметим найденные точки omega_left и omega_right, если они есть
if 'omega_left' in locals() and not np.isnan(omega_left):
    plt.plot(omega_left/nu0_ACH, target_phi_refl, 'go', markersize=8, label=f'$\\nu_{{left}}$ ({omega_left/1e3:.3f} кГц)')
if 'omega_right' in locals() and not np.isnan(omega_right):
    plt.plot(omega_right/nu0_ACH, target_phi_refl, 'ro', markersize=8, label=f'$\\nu_{{right}}$ ({omega_right/1e3:.3f} кГц)')

plt.xlabel(r'$\nu / \nu_0$')
plt.ylabel(r'$\Delta \phi$')
plt.title('ФЧХ колебательного контура')
plt.grid(True, alpha=0.5)
plt.legend()

# --- Настройка оси Y ---
# Объединим данные для определения лимитов
all_phi_data = np.concatenate([Delta_phi_data_for_FCH, Delta_phi_smooth, phi_reflected_smooth])
y_min = min(np.min(all_phi_data), target_phi_FCH, target_phi_refl) # Включаем целевые уровни
y_max = max(np.max(all_phi_data), target_phi_FCH, target_phi_refl)
y_margin = (y_max - y_min) * 0.1 # 10% отступа
plt.ylim(y_min - y_margin, y_max + y_margin)
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(base=np.pi/4))
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(pi_formatter))

output_filename_FCH_detailed = 'FCH_plot_detailed_method9.png'
full_output_path_FCH_detailed = os.path.join(graphics_folder, output_filename_FCH_detailed)
plt.savefig(full_output_path_FCH_detailed)
print(f"Детальный ФЧХ график (метод 9) сохранен в файл: {full_output_path_FCH_detailed}")
try:
    plt.show()
except:
    pass
plt.close() # Закрываем второй график (единый ФЧХ)

# --- 4.7. Построение стандартной ФЧХ (оригинальная версия, для сравнения) ---
plt.figure(figsize=(8, 5))
plt.errorbar(nu_data/nu0_ACH, Delta_phi_data,  # nu / nu0 (без перевода в кГц), оригинальная фаза
             yerr=dDelta_phi_data,
             fmt='x', ecolor='blue', markersize=8, markeredgewidth=2,
             capsize=5, capthick=1, elinewidth=1,
             label='Экспериментальные данные (оригинальные)')
# Построим интерполированную кривую для оригинальных данных (неинвертированных)
try:
    spline_FCH_orig = UnivariateSpline(nu_data, Delta_phi_data, s=0, k=3)
    Delta_phi_smooth_orig = spline_FCH_orig(nu_smooth)
    plt.plot(nu_smooth/nu0_ACH, Delta_phi_smooth_orig, 'm-', label='Интерполированная кривая (оригинальная)', linewidth=1)
except:
    plt.plot(nu_data/nu0_ACH, Delta_phi_data, 'mx-', label='Оригинальные данные', linewidth=1)

plt.xlabel(r'$\nu / \nu_0$')
plt.ylabel(r'$\Delta \phi$ (оригинальная)')
plt.title('ФЧХ колебательного контура (оригинальная)')
plt.grid(True, alpha=0.5)
plt.legend()

# Настройка оси Y
y_min_orig = min(np.min(Delta_phi_data - dDelta_phi_data), np.min(Delta_phi_smooth_orig)) if len(Delta_phi_smooth_orig) > 1 else np.min(Delta_phi_data - dDelta_phi_data)
y_max_orig = max(np.max(Delta_phi_data + dDelta_phi_data), np.max(Delta_phi_smooth_orig)) if len(Delta_phi_smooth_orig) > 1 else np.max(Delta_phi_data + dDelta_phi_data)
y_margin_orig = (y_max_orig - y_min_orig) * 0.05
plt.ylim(y_min_orig - y_margin_orig, y_max_orig + y_margin_orig)
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(base=np.pi/4))
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(pi_formatter_orig))

output_filename_FCH_orig = 'FCH_plot_original.png'
full_output_path_FCH_orig = os.path.join(graphics_folder, output_filename_FCH_orig)
plt.savefig(full_output_path_FCH_orig)
print(f"Оригинальный ФЧХ график сохранен в файл: {full_output_path_FCH_orig}")
try:
    plt.show()
except:
    pass
plt.close() # Закрываем третий график (оригинальный)

# --- 5. Вывод результатов ---
print(f"\n=== Результаты ===")
print(f"Резонансная частота nu0 (по АЧХ): {nu0_ACH/1e3:.3f} кГц")
if 'Q_FCH' in locals() and not np.isnan(Q_FCH):
    print(f"Резонансная частота nu0 (по ФЧХ): {nu0_FCH/1e3:.3f} кГц")
else:
    print("Резонансная частота nu0 (по ФЧХ): не определена")
print(f"Добротность по АЧХ (Q_ACH): {Q_ACH:.2f}")
print(f"Добротность по ФЧХ (Q_FCH_method9): {Q_FCH_method9:.2f}")
print(f"Добротность по ФЧХ (Q_FCH - совместимость): {Q_FCH:.2f}")
