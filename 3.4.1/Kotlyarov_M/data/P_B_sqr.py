import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib as mpl

# Настройка стиля графиков
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['mathtext.fontset'] = 'cm'

# Данные для каждого материала
materials = {
    'Медь': {
        'B2': np.array([0.10125, 0.11601, 0.14640, 0.20743, 0.27612, 
                        0.35796, 0.44666, 0.54516, 0.64895, 0.76668]),
        'sigma_B2': np.array([0.00270, 0.00314, 0.00409, 0.00615, 0.00870,
                              0.01203, 0.01597, 0.02071, 0.02612, 0.03270]),
        'delta_P': np.array([0.00001981, 0.00002972, 0.00003963, 0.00005944, 0.00007925,
                             0.00010897, 0.00012879, 0.00015851, 0.00017832, 0.00020804]),
        'diameter': 0.01,  # м
        'color': 'red'
    },
    'Алюминий': {
        'B2': np.array([0.06021, 0.09948, 0.14855, 0.20743, 0.27612,
                        0.35462, 0.44292, 0.54103, 0.65347, 0.78146]),
        'sigma_B2': np.array([0.00153, 0.00264, 0.00416, 0.00615, 0.00870,
                              0.01189, 0.01579, 0.02051, 0.02636, 0.03356]),
        'delta_P': np.array([0.00003963, 0.00005944, 0.00009907, 0.00013869, 0.00017832,
                             0.00022785, 0.00028729, 0.00034673, 0.00040617, 0.00046561]),
        'diameter': 0.01,  # м
        'color': 'blue'
    },
    'Графит': {
        'B2': np.array([0.04725, 0.09948, 0.14855, 0.20743, 0.27612,
                        0.35129, 0.44292, 0.54103, 0.64895, 0.76668]),
        'sigma_B2': np.array([0.00118, 0.00264, 0.00416, 0.00615, 0.00870,
                              0.01175, 0.01579, 0.02051, 0.02612, 0.03270]),
        'delta_P': np.array([0.00001981, 0.00005944, 0.00008916, 0.00013869, 0.00018823,
                             0.00023776, 0.00030711, 0.00037645, 0.00044580, 0.00050524]),
        'diameter': 0.0056,  # м
        'color': 'green'
    },
    'Вольфрам': {
        'B2': np.array([0.03075, 0.06021, 0.09772, 0.15072, 0.20743,
                        0.27612, 0.35462, 0.44292, 0.54103, 0.64895, 0.76668]),
        'sigma_B2': np.array([0.00075, 0.00153, 0.00259, 0.00423, 0.00615,
                              0.00870, 0.01189, 0.01579, 0.02051, 0.02612, 0.03270]),
        'delta_P': np.array([0.00004953, 0.00011888, 0.00021795, 0.00033683, 0.00047552,
                             0.00065384, 0.00083216, 0.00103029, 0.00122842, 0.00143646, 0.00163460]),
        'diameter': 0.01,  # м
        'color': 'orange'
    }
}

# Погрешность измерения силы
sigma_delta_P = 0.00001  # Н

# Магнитная постоянная
mu_0 = 4 * np.pi * 1e-7  # Гн/м

# Линейная модель (через начало координат)
def linear_model(x, k):
    return k * x

# Создание полотна с 4 субплoтами
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Зависимость силы |ΔP| от квадрата магнитной индукции B² для различных материалов', fontsize=16)

# Создание отдельного графика со всеми материалами
fig_all, ax_all = plt.subplots(figsize=(12, 8))

# Для хранения результатов
results = {}

# Обработка каждого материала
for i, (material, data) in enumerate(materials.items()):
    # Определяем субплoт
    row, col = i // 2, i % 2
    ax = axes[row, col]
    
    B2 = data['B2']
    sigma_B2 = data['sigma_B2']
    delta_P = data['delta_P']
    color = data['color']
    diameter = data['diameter']
    
    # Вычисляем площадь сечения
    S = np.pi * (diameter / 2) ** 2
    
    # Аппроксимация данных
    popt, pcov = curve_fit(linear_model, B2, delta_P, p0=[0.0003], 
                          sigma=sigma_delta_P*np.ones_like(B2), absolute_sigma=True)
    k = popt[0]
    dk = np.sqrt(pcov[0][0])
    
    # Коэффициент детерминации R²
    delta_P_pred = linear_model(B2, k)
    ss_res = np.sum((delta_P - delta_P_pred)**2)
    ss_tot = np.sum((delta_P - np.mean(delta_P))**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    # Создание гладкой кривой для графика
    B2_smooth = np.linspace(min(B2)*0.9, max(B2)*1.1, 100)
    delta_P_smooth = linear_model(B2_smooth, k)
    
    # Построение на субплoте
    ax.errorbar(B2, delta_P, xerr=sigma_B2, yerr=sigma_delta_P, 
                fmt='o', color=color, markersize=5, capsize=3, capthick=1,
                label=f'Экспериментальные точки', zorder=5)
    ax.plot(B2_smooth, delta_P_smooth, '-', color=color, linewidth=2, 
            label=f'Аппроксимация: k = {k:.2e} ± {dk:.2e} Н/Тл²')
    
    ax.set_xlabel('B², Тл²', fontsize=12)
    ax.set_ylabel('|ΔP|, Н', fontsize=12)
    ax.set_title(f'{material}', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=10)
    
    # Добавление на общий график
    ax_all.errorbar(B2, delta_P, xerr=sigma_B2, yerr=sigma_delta_P, 
                   fmt='o', color=color, markersize=5, capsize=3, capthick=1,
                   label=f'{material}', zorder=5)
    ax_all.plot(B2_smooth, delta_P_smooth, '-', color=color, linewidth=2)
    
    # Расчет магнитной восприимчивости
    # Из формулы: F = χ * (B²/(2μ₀)) * S => χ = (2μ₀ * k) / S
    chi = (2 * mu_0 * k) / S
    dchi = (2 * mu_0 * dk) / S  # погрешность χ
    
    # Сохранение результатов
    results[material] = {
        'k': k,
        'dk': dk,
        'chi': chi,
        'dchi': dchi,
        'r_squared': r_squared,
        'S': S
    }

# Настройка общего графика
ax_all.set_xlabel('B², Тл²', fontsize=14)
ax_all.set_ylabel('|ΔP|, Н', fontsize=14)
ax_all.set_title('Зависимость силы |ΔP| от квадрата магнитной индукции B²', fontsize=16)
ax_all.grid(True, linestyle='--', alpha=0.7)
ax_all.legend(fontsize=12)

# Сохранение графиков
plt.figure(fig.number)
plt.tight_layout()
plt.savefig('all_materials_separate.png', dpi=300, bbox_inches='tight')
plt.savefig('all_materials_separate.pdf', bbox_inches='tight')

plt.figure(fig_all.number)
plt.tight_layout()
plt.savefig('all_materials_together.png', dpi=300, bbox_inches='tight')
plt.savefig('all_materials_together.pdf', bbox_inches='tight')

# Вывод результатов
print("РЕЗУЛЬТАТЫ РАСЧЕТА МАГНИТНОЙ ВОСПРИИМЧИВОСТИ")
print("=" * 70)
print(f"{'Материал':<12} {'χ (эксп)':<15} {'σ_χ':<15} {'χ (табл)':<15} {'Отклонение':<15}")
print("-" * 70)

# Табличные значения (справочные данные)
table_chi = {
    'Медь': -9.6e-6,
    'Алюминий': 2.2e-5,
    'Графит': -1.6e-5,  # приблизительное значение для графита
    'Вольфрам': 7.8e-5   # приблизительное значение для вольфрама
}

for material, res in results.items():
    table_value = table_chi.get(material, 0)
    deviation = abs((res['chi'] - table_value) / table_value * 100) if table_value != 0 else 0
    
    print(f"{material:<12} {res['chi']:+.2e}    {res['dchi']:.2e}    {table_value:+.2e}    {deviation:>6.1f}%")

print("\nДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:")
print("=" * 70)
for material, res in results.items():
    print(f"\n{material}:")
    print(f"  Коэффициент наклона k = {res['k']:.2e} ± {res['dk']:.2e} Н/Тл²")
    print(f"  Площадь сечения S = {res['S']:.2e} м²")
    print(f"  Коэффициент детерминации R² = {res['r_squared']:.4f}")

# Показ графиков
plt.show()
