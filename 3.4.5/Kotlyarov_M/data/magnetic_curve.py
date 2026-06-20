import numpy as np
import matplotlib.pyplot as plt
import os

# Константа
mu_0 = 4 * np.pi * 1e-7  # Гн/м

# Данные
materials = {
    "Пермаллой": {
        "H": [50.0, 33.3, 30.6, 27.8, 27.8, 25.0, 22.2],
        "B": [0.337, 0.295, 0.232, 0.189, 0.126, 0.074, 0.021]
    },
    "Феррит": {
        "H": [37.3, 28.0, 13.1, 11.2],
        "B": [0.200, 0.160, 0.027, 0.013]
    },
    "Кремнистое железо": {
        "H": [400.0, 293.3, 240.0, 186.7, 120.0, 80.0, 40.0],
        "B": [0.833, 0.708, 0.667, 0.583, 0.417, 0.333, 0.167]
    }
}

# Создаём папку для графиков
output_dir = "../Graphics"
os.makedirs(output_dir, exist_ok=True)

print("=" * 60)
print("Расчёт начальной и максимальной дифференциальной проницаемости")
print("=" * 60)

results = {}

for name, data in materials.items():
    H = np.array(data["H"])
    B = np.array(data["B"])
    
    # Убираем дубликаты H, оставляя максимальное B
    unique_H = []
    unique_B = []
    seen = {}
    for h, b in zip(H, B):
        if h not in seen or b > seen[h]:
            seen[h] = b
            if h not in unique_H:
                unique_H.append(h)
                unique_B.append(b)
            else:
                idx = unique_H.index(h)
                unique_B[idx] = b

    # Сортируем по H
    sorted_indices = np.argsort(unique_H)
    H_sorted = np.array(unique_H)[sorted_indices]
    B_sorted = np.array(unique_B)[sorted_indices]
    
    # Численная производная dB/dH
    dB_dH = np.gradient(B_sorted, H_sorted)  # численная производная
    
    # Дифференциальная проницаемость
    mu_diff = dB_dH / mu_0
    
    # Начальная проницаемость — в первой точке (минимальное H)
    mu_initial = mu_diff[0]
    
    # Максимальная проницаемость — максимум по всем точкам
    mu_max = np.max(mu_diff)
    
    # Сохраняем результаты
    results[name] = {
        "mu_initial": mu_initial,
        "mu_max": mu_max,
        "H_sorted": H_sorted,
        "mu_diff": mu_diff
    }
    
    print(f"\n{name}:")
    print(f"  Начальная μ_диф = {mu_initial:.1f}")
    print(f"  Максимальная μ_диф = {mu_max:.1f}")

    # --- Построение графика μ_диф(H) ---
    plt.figure(figsize=(10, 6))
    plt.plot(H_sorted, mu_diff, marker='o', linestyle='-', color='purple', linewidth=2, markersize=6)
    plt.title(f"Дифференциальная проницаемость: {name}", fontsize=16)
    plt.xlabel("H, А/м", fontsize=12)
    plt.ylabel("μ_диф", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    filename = f"{name.replace(' ', '_')}_mu_diff.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    print(f"  График сохранён: {filepath}")
    
    plt.close()

print("\n" + "=" * 60)
