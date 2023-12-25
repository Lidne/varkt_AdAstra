import csv
import math
import matplotlib.pyplot as plt


# time_arr = list(range(1, T + 1))  # массив времени, сек
pi = math.pi  # число пи
s = (pi * (1.5 ** 2) * 23.3) ** (2/3)

p0 = 101325  # давление воздуха
c = 1004.685  # удельная теплоёмкость при постоянном давлении
t0 = 288.15  # стандартная температура на уровне моря
m = 0.029  # молярная масса сухого воздуха
r0 = 8.31  # универсальная газовая постоянная
g = 9.81  # коэффициент ускорения свободного падения
R = 600000  # радиус планеты
G = 6.67 * 10 ** -11
M = 5.292 * (10 ** 22)
L = -0.0065 # среднее значение вертикальной компоненты градиента температуры в тропосфере

cf = 0.5

# MASS = 49758
STAGE1_MASS = 49758
STAGE2_MASS = 7458
STAGE3_MASS = 551
FLOW_RATE_1 = (49758 - 21677) / 59
FLOW_RATE_2 = (7458 - 4114) / 91

# STAGE1_THRUST = 1350000  # сила тяги первой ступени
# STAGE2_THRUST = 200000  # сила тяги второй ступени


def open_file():
    with open("C:\\Users\\george\\Projects\\python_projects\\varkt\\data_sopr.txt", encoding='utf-8') as f:
        table = csv.reader(f, delimiter=';', quotechar='"')
        ksp_alt, ksp_speed, ksp_mass, ksp_dv, ksp_thrust, ksp_friction = [], [], [], [], [], []
        for row in list(table)[1:]:
            ksp_alt.append(float(row[3]))
            ksp_speed.append(float(row[1]))
            ksp_mass.append(float(row[4]))
            ksp_thrust.append(float(row[5]))
            ksp_friction.append(float(row[8]))
        tmp = ksp_speed[0]
        for v in ksp_speed:
            ksp_dv.append(v - tmp)
            tmp = v
    return ksp_alt, ksp_speed, ksp_mass, ksp_dv, ksp_thrust, ksp_friction


ksp_alt, ksp_speed, ksp_mass, ksp_dv, ksp_thrust, ksp_friction = open_file()
cf = 0
c = 0

for i in zip(ksp_friction, ksp_speed, ksp_alt):
    # print(i)
    Fc, v, h = i
    p = p0 * math.exp((-g * m * h) / (r0 * t0))
    density = (p * m) / (r0 * t0)
    cf1 = (2 * Fc) / (density * (v ** 2) * s)
    print(cf1)
    cf += cf1
    c += 1


print(cf / c)