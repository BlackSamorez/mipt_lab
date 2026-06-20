import matplotlib.pyplot as plt
import numpy as np

# --- 1. Оценочные данные для графика ---
# Центры столбцов (соответствуют верхней шкале X: 0, 1, 2, ..., 20)
x_centers = np.arange(0, 21)

# Высоты для белых столбцов (10c)
# Значения являются приближением плотности (сумма около 1)
y_white = np.array([
    0.005, 0.015, 0.025, 0.027, 0.052, 0.055, 0.080, 0.083, 0.140, 0.118,
    0.110, 0.112, 0.095, 0.075, 0.045, 0.025, 0.022, 0.015, 0.010, 0.005,
    0.003
])

# Высоты для красных столбцов (40c)
y_red = np.array([
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.010, 0.012, 0.020, 0.045,
    0.080, 0.100, 0.075, 0.055, 0.020, 0.010, 0.0, 0.0, 0.0, 0.0,
    0.0
])

bar_width = 1.0  # Ширина каждого столбца

# --- 2. Настройка графика ---
fig, ax = plt.subplots(figsize=(7, 10))

# Установка размера шрифта для имитации стиля

# --- 3. Построение белых контурных столбцов (10c) ---
ax.bar(
    x_centers,
    y_white,
    width=bar_width,
    color='none',           # Отсутствие заливки
    edgecolor='black',      # Черный контур
    linewidth=1.5,
    label='10c',
    align='center'
)

# --- 4. Построение красных заштрихованных столбцов (40c) ---
ax.bar(
    x_centers,
    y_red,
    width=bar_width,
    color='red',            # Красная заливка
    alpha=0.5,              # Прозрачность для лучшей видимости
    hatch='///',            # Вертикальная штриховка
    edgecolor='red',
    linewidth=0.5,
    label='40c',
    align='center'
)

# --- 5. Настройка осей и меток ---

# Ограничения осей
ax.set_xlim(-0.5, 22.5)
ax.set_ylim(0, 0.15)

# Настройка Y-оси (метка и научное обозначение)
ax.set_ylabel(r'$\omega$', rotation=0, labelpad=15)

# Форматирование меток Y-оси в виде a·10⁻²
y_ticks = np.arange(0, 0.15, 0.02)
y_labels = [
    '0', '2 \\cdot 10^{-2}', '4 \\cdot 10^{-2}', '6 \\cdot 10^{-2}',
    '8 \\cdot 10^{-2}', '0.1', '0.12', '0.14'
]
# Применим форматирование (мат. символы не поддерживаются в нативном коде, используем LaTeX-синтаксис, который matplotlib отобразит корректно)
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_labels, usetex=True)

# Настройка X-оси (двойная шкала)
# Верхняя шкала (основные метки)
major_x_ticks = np.arange(0, 23, 2)
ax.set_xticks(major_x_ticks)
ax.tick_params(axis='x', which='major', pad=10) # Добавляем отступ для меток

# Вторая шкала X (внизу) - используем дополнительный X-тикел
# Создадим пустой вспомогательный график, чтобы разместить вторую шкалу
ax2 = ax.twiny()
ax2.set_xlim(ax.get_xlim()) # Синхронизируем границы
ax2.spines['top'].set_visible(False) # Скрываем верхнюю рамку для ax2
ax2.spines['bottom'].set_position(('outward', 30)) # Смещаем ось вниз

# Метки для второй шкалы (умноженные на 4)
minor_x_ticks = np.arange(0, 89, 8)
ax2.set_xticks(major_x_ticks) # Используем те же позиции, что и для ax, но другие метки
ax2.set_xticklabels([str(i) for i in minor_x_ticks])
ax2.tick_params(axis='x', which='major', pad=10)

# Добавляем легенду (используем bbox_to_anchor для размещения в верхнем правом углу)
legend = ax.legend(
    loc='upper right',
    frameon=True,
    edgecolor='black',
    fancybox=False,
    fontsize=12,
    bbox_to_anchor=(0.95, 0.95)
)

# Настройка стиля легенды для отображения "пустого" прямоугольника
for handle in legend.legend_handles:
    if handle.get_label() == '10c':
        handle.set_facecolor('none')
        handle.set_edgecolor('black')
        handle.set_linewidth(1.0)
        handle.set_hatch(None)
    elif handle.get_label() == '40c':
        handle.set_facecolor('red')
        handle.set_edgecolor('red')
        handle.set_alpha(0.5)
        handle.set_hatch('///')

# Убираем рамки сверху и справа
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Сохранение или отображение
# plt.savefig('histogram_matplotlib.png', dpi=300)
plt.show() # Если вы хотите отобразить график
print("Код для построения графика готов. Вы можете запустить его в Python-среде с установленным Matplotlib.")
