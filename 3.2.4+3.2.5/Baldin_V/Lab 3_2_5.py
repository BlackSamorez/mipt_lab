# ПЕРЕД ЗАПУСКОМ ПРОГРАММЫ ПРИВЕДИТЕ ВАШИ ДАННЫЕ К ТАКОМУ ЖЕ ВИДУ, ЧТО И МОИ, РАСПОЛОЖЕНИЕ ТАБЛИЦ РОЛИ НЕ ИГРАЕТ,
# ГЛАВНОЕ НЕ ЛЕПИТЕ ИХ ДРУГ К ДРУГУ, ДАННАЯ ПРОГРАММА ПРОИЗВЕДЁТ ЗА ВАС ПОЛНУЮ (почти) ОБРАБОТКУ ДАННЫХ.

from lab_cheat import *
from lab_cheat.advanced_functions import curve_fit
# Библиотеку можно найти по ссылке: https://github.com/Vistog/lab_cheat
c, tables = shredder(read_data("C:/Users/McTuT/OneDrive/Рабочий стол/Lab 3.2.5 ProgramLikeEdition.xlsx"))

tab = []
for i in tables:
    tab.append(get_into_groupvar_col_last_err(i))
for i in range(len(tab)):
    quick_use_form(tab[i], 'tab', i)
quick_use_form(c, 'c')

# Генерируется автоматически
# если при компиляции есть ошибки, удалите эти строки, скомпилируйте программу, она выдаст в консоль, чем их заменить
N2, C2, T21, T22, T23 = tab[0]['N2'], tab[0]['C2'], tab[0]['T21'], tab[0]['T22'], tab[0]['T23']
L7, R7, Frec7 = tab[1]['L7'], tab[1]['R7'], tab[1]['Frec7']
nu5_140, Uc5_140, dX5_140 = tab[2]['nu5_140'], tab[2]['Uc5_140'], tab[2]['dX5_140']
nu5_280, Uc5_280, dX5_280 = tab[3]['nu5_280'], tab[3]['Uc5_280'], tab[3]['dX5_280']
n6_140, Uk6_140, Ukn6_140 = tab[4]['n6_140'], tab[4]['Uk6_140'], tab[4]['Ukn6_140']
n6_280, Uk6_280, Ukn6_280 = tab[5]['n6_280'], tab[5]['Uk6_280'], tab[5]['Ukn6_280']
n3_140, Um3_140, Umn3_140 = tab[6]['n3_140'], tab[6]['Um3_140'], tab[6]['Umn3_140']
n3_560, Um3_560, Umn3_560 = tab[7]['n3_560'], tab[7]['Um3_560'], tab[7]['Umn3_560']
n4_140, Um4_140, Umn4_140 = tab[8]['n4_140'], tab[8]['Um4_140'], tab[8]['Umn4_140']
n4_560, Um4_560, Umn4_560 = tab[9]['n4_560'], tab[9]['Um4_560'], tab[9]['Umn4_560']
n6_140u, Uk6_140u, Ukn6_140u = tab[10]['n6_140u'], tab[10]['Uk6_140u'], tab[10]['Ukn6_140u']
n6_280u, Uk6_280u, Ukn6_280u = tab[11]['n6_280u'], tab[11]['Uk6_280u'], tab[11]['Ukn6_280u']
n3_280, Um3_280, Umn3_280 = tab[12]['n3_280'], tab[12]['Um3_280'], tab[12]['Umn3_280']
n3_700, Um3_700, Umn3_700 = tab[13]['n3_700'], tab[13]['Um3_700'], tab[13]['Umn3_700']
n4_280, Um4_280, Umn4_280 = tab[14]['n4_280'], tab[14]['Um4_280'], tab[14]['Umn4_280']
n4_700, Um4_700, Umn4_700 = tab[15]['n4_700'], tab[15]['Um4_700'], tab[15]['Umn4_700']
n3_420, Um3_420, Umn3_420 = tab[16]['n3_420'], tab[16]['Um3_420'], tab[16]['Umn3_420']
n3_350, Um3_350, Umn3_350 = tab[17]['n3_350'], tab[17]['Um3_350'], tab[17]['Umn3_350']
n4_420, Um4_420, Umn4_420 = tab[18]['n4_420'], tab[18]['Um4_420'], tab[18]['Umn4_420']
n4_350, Um4_350, Umn4_350 = tab[19]['n4_350'], tab[19]['Um4_350'], tab[19]['Umn4_350']
n3_490, Um3_490, Umn3_490 = tab[20]['n3_490'], tab[20]['Um3_490'], tab[20]['Umn3_490']
n3_630, Um3_630, Umn3_630 = tab[21]['n3_630'], tab[21]['Um3_630'], tab[21]['Umn3_630']
n4_490, Um4_490, Umn4_490 = tab[22]['n4_490'], tab[22]['Um4_490'], tab[22]['Umn4_490']
n4_630, Um4_630, Umn4_630 = tab[23]['n4_630'], tab[23]['Um4_630'], tab[23]['Umn4_630']
RkrTh, RkrPr, Ct, U0_140, U0_280 = c['RkrTh'], c['RkrPr'], c['Ct'], c['U0_140'], c['U0_280']


# Некоторые характеристики установки, которые я выставлял, нужны в дальнейших расчётах
L = L7[3]   # мГн
# Ct - в лабораторной называется C*, нФ

# Пункт 2 об измерении периодов
print("\n<<<<<<<< Пункт 2 >>>>>>>>")
# Расчёт точек для теоретической зависимости T(C)
Tth = GroupVar([2*3.1415 * (0.0001*i/1000000)**0.5 for i in range(1, len(C2))], [0 for i in range(1, len(C2))])*1000000
# Усредняем значения периода
T2 = (T21 + T22 + T23) / 3
# отбрасываем 1ую точку ибо там якобы 0 индуктивность
C2r = C2[1::]
T2r = T2[1::]

fig2 = Figure("T($\sqrt{C}$)", "\sqrt{C}, мФ", "T, мкс", zero_in_corner=False, x_label_coords=[1.01 + 0.01 * 7 * 0.8, 0.06])
fig2.plot(C2r**0.5, T2r, colour="RED")
fig2.plot(C2r**0.5, Tth, colour="BLUE")

mnk(C2r**0.5, Tth, colour="BLUE", figure=fig2, show_coefficients=False, label="Теоретическая")
mnk(C2r**0.5, T2r, colour="RED", figure=fig2, show_coefficients=False, label="Практическая")

#fig2.show()

# Пункт 3 о свободных затухающих колебаниях
print("\n<<<<<<<< Пункт 3 >>>>>>>>")
# Рассчитываем логарифмические коэфф затухания
Th3_140 = 1/n3_140 * ln(Um3_140/Umn3_140)
Th3_280 = 1/n3_280 * ln(Um3_280/Umn3_280)
Th3_420 = 1/n3_420 * ln(Um3_420/Umn3_420)
Th3_490 = 1/n3_490 * ln(Um3_490/Umn3_490)
Th3_560 = 1/n3_560 * ln(Um3_560/Umn3_560)
Th3_700 = 1/n3_700 * ln(Um3_700/Umn3_700)
Th3_350 = 1/n3_350 * ln(Um3_350/Umn3_350)
Th3_630 = 1/n3_630 * ln(Um3_630/Umn3_630)

# И собираем их в список
Th3 = GroupVar([Th3_140.mean(), Th3_280.mean(), Th3_420.mean(), Th3_490.mean(), Th3_560.mean(), Th3_700.mean(), Th3_350.mean(), Th3_630.mean()])
R3 = GroupVar([140, 280, 420, 490, 560, 700, 350, 630], [1, 1, 1, 1, 1, 1, 1, 1])
print(Th3)
# Это сопротивления магазина, сопротивление катушки ещё не учтено
R3 += R7[3]     # Учли сопротивление катушки
fig3 = Figure("$\\frac{1}{\Theta^2}(\\frac{1}{R^2})$", "\\frac{1}{R^2}", "\\frac{1}{\Theta^2}", x_label_coords=[1.01 + 0.01 * 7 * 0.8, 0.06])
fig3.plot(1/R3**2, 1/Th3**2)
k3, b3 = mnk(1/R3**2, 1/Th3**2, fig3)
#fig3.show()

# Получаем Rкр с графика
Rkr3 = 2 * pi * sqrt(k3)
print("Критическое сопротивление, определённое с помощью зависимости логарифмического декремента затухания от сопротивления контура: $R_\\text{кр декр} =", Rkr3/1000, "\\text{кОм}.$")
print("Критическое сопротивление, рассчитанное с помощью теории: $R_\\text{кр теор} =", 2 * sqrt(L/1000/Ct*10**9)/1000, "\\text{кОм}.$")

# Рассчитываем максимальную и минимальную добротность по декрементам затухания
QMax3 = pi / min(Th3)
QMin3 = pi / max(Th3)
print("\nНаибольшая добротность, рассчитанная с помощью логарифмического декремента затухания равна: $\Omega_\\text{max} = " + str(QMax3) + ".$")
print("Наименьшая добротность, рассчитанная с помощью логарифмического декремента затухания равна: $\Omega_\\text{min} = " + str(QMin3) + ".$")
for i in range(len(Th3)):
    print("$", R3[i], "$	$", pi/Th3[i], "$	$", 1/R3[i] * sqrt(L/Ct*1000000), "$")


# Пункт 4 о спиралях на фазовых плоскостях
print("\n<<<<<<<< Пункт 4 >>>>>>>>")
# Рассчитываем логарифмические коэфф затухания
Th4_140 = 1/n4_140 * ln(Um4_140/Umn4_140)
Th4_280 = 1/n4_280 * ln(Um4_280/Umn4_280)
Th4_420 = 1/n4_420 * ln(Um4_420/Umn4_420)
Th4_490 = 1/n4_490 * ln(Um4_490/Umn4_490)
Th4_560 = 1/n4_560 * ln(Um4_560/Umn4_560)
Th4_700 = 1/n4_700 * ln(Um4_700/Umn4_700)
Th4_450 = 1/n4_350 * ln(Um4_350/Umn4_350)
Th4_640 = 1/n4_630 * ln(Um4_630/Umn4_630)

# И собираем их в список
Th4 = GroupVar([Th4_140.mean(), Th4_280.mean(), Th4_420.mean(), Th4_490.mean(), Th4_560.mean(), Th4_700.mean(), Th4_450.mean(), Th4_640.mean()])
R4 = GroupVar([140, 280, 420, 490, 560, 700, 450, 640], [1, 1, 1, 1, 1, 1, 1, 1])
# Это сопротивления магазина, сопротивление катушки ещё не учтено
R4 += R7[3]     # Учли сопротивление катушки

fig4 = Figure("$\\frac{1}{\Theta^2}(\\frac{1}{R^2})$", "\\frac{1}{R^2}", "\\frac{1}{\Theta^2}", x_label_coords=[1.01 + 0.01 * 7 * 0.8, 0.06])
fig4.plot(1/R4**2, 1/Th4**2)
k4, b4 = mnk(1/R4**2, 1/Th4**2, fig4)
#fig4.show()

# Рассчитываем максимальную и минимальную добротность по декрементам затухания
QMax4 = pi / min(Th4)
QMin4 = pi / max(Th4)

for i in range(len(Th4)):
    print("$", R3[i], "$	$", pi/Th4[i], "$	$", 1/R3[i] * sqrt(L/Ct*1000000), "$")
print("\nНаибольшая добротность, рассчитанная с помощью логарифмического декремента затухания равна: $\Omega_\\text{max} = " + str(QMax4) + ".$")
print("Наименьшая добротность, рассчитанная с помощью логарифмического декремента затухания равна: $\Omega_\\text{min} = " + str(QMin4) + ".$")
print("\nНаибольшая теоретически рассчитанная добротность контура с учётом активного сопротивления индуктивности равна: $\Omega_\\text{теорMax} = " + str(1/min(R3) * sqrt(L/Ct*1000000)) + ".$")
print("Наименьшая теоретически рассчитанная добротность контура с учётом активного сопротивления индуктивности равна: $\Omega_\\text{теорMin} = " + str(1/max(R3) * sqrt(L/Ct*1000000)) + ".$")


# Пункт 5 о ФЧХ и АЧХ
print("\n<<<<<<<< Пункт 5 >>>>>>>>")
# АЧХ
fig5 = Figure("АЧХ", "\\frac{\\nu}{\\nu_0}", "\\frac{U}{U_0}", x_label_coords=[1.01 + 0.01 * 7 * 0.8, 0.06], zero_in_corner=False)
fig5.plot(nu5_140/nu5_140[10], Uc5_140/Uc5_140[10], colour="RED")
fig5.plot(nu5_280/nu5_280[10], Uc5_280/Uc5_280[10], colour="BLUE")
# Аппроксимируем колокола
params140 = curve_fit(lambda x, a, s, shift, ampl: ampl/sqrt(1+((x-a)/s)**2) + shift, x=nu5_140/nu5_140[10], y=Uc5_140/Uc5_140[10], p0=(0, 1, 0, 0.6))
fig5.func_graph(
    lambda x: (lambda x, a, s, shift, ampl: ampl/sqrt(1+((x-a)/s)**2) + shift)(x, *params140.val()),
    x_min=min(nu5_140/nu5_140[10]), x_max=max(nu5_140/nu5_140[10]), colour="RED", label="При $R$ = 140 Ом")

params280 = curve_fit(lambda x, a, s, shift, ampl: ampl/sqrt(1+((x-a)/s)**2) + shift, x=nu5_280/nu5_280[10], y=Uc5_280/Uc5_280[10], p0=(0, 1, 0, 0.6))
fig5.func_graph(
    lambda x: (lambda x, a, s, shift, ampl: ampl/sqrt(1+((x-a)/s)**2) + shift)(x, *params280.val()),
    x_min=min(nu5_280/nu5_280[10]), x_max=max(nu5_280/nu5_280[10]), colour="BLUE", label="При $R$ = 140 Ом")
fig5.h_line(1/sqrt(2))

# Вычисляем координаты точки пересечения (для определения "дисперсии")
"""a, s, d, A = params140
disp = 2*sqrt(a**2 * (1/2 - d**2)**2 - (1/2 - d**2)*(1/2*s**2 - A*A*s*s - d*d*s*s + a*a*d*d + 1/2 * a*a))/(1/2 - d**2)
print(disp)"""
# fig5.show()
disp140 = Var(0.0548, 0.005)
disp280 = Var(0.0917, 0.005)

print("Ширина резонансной кривой, измеренная на уровне $\\frac{A}{\\sqrt{2}}$ при сопротивлении магазина 140 Ом равна: $\\Delta \\Omega_\\text{140} = " + str(disp140) + ".$")
print("Ширина резонансной кривой, измеренная на уровне $\\frac{A}{\\sqrt{2}}$ при сопротивлении магазина 280 Ом равна: $\\Delta \\Omega_\\text{280} = " + str(disp280) + ".$")

print("\nДобротность, рассчитанная с помощью АЧХ, при сопротивлении магазина 140 Ом равна: $\Omega_\\text{140} = " + str(1/sqrt(L * Ct / 100000) / 2 / disp140 / 2 / pi) + ".$")
print("Добротность, рассчитанная с помощью АЧХ, при сопротивлении магазина 280 Ом равна: $\Omega_\\text{280} = " + str(1/sqrt(L * Ct / 100000) / 2 / disp280 / 2 / pi) + ".$")

# ФЧХ
fig5_FCHH = Figure("ФЧХ", "\\omega, Гц", "\\Delta \\varphi", zero_in_corner=False, x_label_coords=[1.01 + 0.01 * 7 * 0.8, 0.06])
fig5_FCHH.plot(nu5_140, 1/sqrt(L * Ct / 1000000000000) * dX5_140/1000000 / pi, colour="RED")
fig5_FCHH.plot(nu5_280, -1/sqrt(L * Ct / 1000000000000) * dX5_280/1000000 / pi + 2.2, colour="BLUE")

params140F = curve_fit(lambda x, shift, compress, rais: arctg(-compress*(x-shift))/pi + rais, x=nu5_140, y=1/sqrt(L * Ct / 1000000000000) * dX5_140/1000000 / pi, p0=(6000, 1, 1))
fig5_FCHH.func_graph(
    lambda x: (lambda x, shift, compress, rais: arctg(-compress*(x-shift))/pi + rais)(x, *params140F.val()),
    x_min=min(nu5_140), x_max=max(nu5_140), colour="RED", label="При $R$ = 140 Ом")

"""params280F = curve_fit(lambda x, shift, compress, rais: arctg(-compress*(x-shift))/pi + rais, x=nu5_280, y=1/sqrt(L * Ct / 1000000000000) * dX5_280/1000000 / pi, p0=(6000, 0.5, 1))
fig5_FCHH.func_graph(
    lambda x: (lambda x, shift, compress, rais: arctg(-compress*(x-shift))/pi + rais)(x, *params280F.val()),
    x_min=min(nu5_280), x_max=max(nu5_280), colour="BLUE")"""
fig5_FCHH.h_line(0.25, line_style="dotted", colour="BLACK")
fig5_FCHH.h_line(0.75, line_style="dotted", colour="BLACK")

dO = 151 # Гц
Q5_FCHH = 1/2 / pi / dO / sqrt(L*Ct*10**(-12))
print("Добротность, рассчитанная с помощью ФЧХ, при сопротивлении магазина 140 Ом равна: $\Omega_\\text{ФЧХ} = " + str(Q5_FCHH) + ".$")

#fig5_FCHH.show()


# Пункт 6 о процессах установления и затухания
print("\n<<<<<<<< Пункт 6 >>>>>>>>")

# Рассчитываем логарифмические коэфф затухания
Th6_140u = 1/n6_140u * ln(Uk6_140u/Ukn6_140u)
Th6_280u = 1/n6_280u * ln(Uk6_280u/Ukn6_280u)
Th6_140 = 1/n6_140 * ln((U0_140 - Uk6_140)/(U0_140 - Ukn6_140))
Th6_280 = 1/n6_280 * ln((U0_280 - Uk6_280)/(U0_280 - Ukn6_280))

print(Th6_140u.mean(), Th6_280u.mean(), Th6_140.mean(), Th6_280.mean())
print("Добротность, рассчитанная с помощью логарифмического декремента затухания, при затухании колебаний и сопротивлении магазина 140 Ом равна: $\Omega_\\text{140u} = " + str(pi/Th6_140u.mean()) + ".$")
print("Добротность, рассчитанная с помощью логарифмического декремента затухания, при затухании колебаний и сопротивлении магазина 280 Ом равна: $\Omega_\\text{140u} = " + str(pi/Th6_280u.mean()) + ".$")

print("\nДобротность, рассчитанная с помощью логарифмического декремента затухания, при установлении колебаний и сопротивлении магазина 140 Ом равна: $\Omega_\\text{140u} = " + str(pi/Th6_140.mean()) + ".$")
print("Добротность, рассчитанная с помощью логарифмического декремента затухания, при установлении колебаний и сопротивлении магазина 280 Ом равна: $\Omega_\\text{140u} = " + str(pi/Th6_280.mean()) + ".$")

fig2.show()
fig3.show()
fig4.show()
fig5.show()
fig5_FCHH.show()
