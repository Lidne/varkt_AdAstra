import math
import matplotlib.pyplot as plt
import csv

T = 300  #

rocket_mass = [0] * T
velocity_x = [0] * T
velocity_y = [0] * T
delta_vx_arr = [0] * T
delta_vy_arr = [0] * T
velocity = [0] * T
pos_x = [0] * T
pos_y = [0] * T
Fc_list = [0] * T
altitude_arr = [0] * T

time_arr = list(range(1, T + 1))  # массив времени, сек
pi = math.pi  # число пи
s = pi * (1.5 ** 2)  # площадь
p0 = 1.2754  # плотность воздуха
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
FLOW_RATE_1 = (49758 - 21677) / 40
FLOW_RATE_2 = (7458 - 4114) / 91

STAGE1_THRUST = 1350000  # сила тяги первой ступени
STAGE2_THRUST = 200000  # сила тяги второй ступени


def open_file():
    with open("C:\\Users\\george\\Projects\\python_projects\\varkt\\data_mass.txt", encoding='utf-8') as f:
        table = csv.reader(f, delimiter=';', quotechar='"')
        ksp_alt, ksp_speed, ksp_mass, ksp_dv = [], [], [], []
        for row in list(table)[1:]:
            ksp_alt.append(float(row[3]))
            ksp_speed.append(float(row[1]))
            ksp_mass.append(float(row[4]))
        tmp = ksp_speed[0]
        for v in ksp_speed:
            ksp_dv.append(v - tmp)
            tmp = v
    return ksp_alt, ksp_speed, ksp_mass, ksp_dv


def main():
    cos_alpha = 1
    sin_alpha = 0
    stage = 1
    current_vx = 0
    current_vy = 0
    V = 0
    V_sq = 0
    current_x = 600000
    current_y = 0
    pos_x[0] = current_x
    pos_y[0] = current_y
    velocity_x[0] = current_vx
    velocity_y[0] = current_vy
    delta_vx_arr[0] = 0
    delta_vy_arr[0] = 0
    velocity[0] = V
    current_mass = STAGE1_MASS
    rocket_mass[0] = current_mass
    current_thrust = STAGE1_THRUST

    

    for t in range(1, T):
        d_sq = current_x ** 2 + current_y ** 2
        d = math.sqrt(d_sq)
        h = round(d - R, 6)
        print(f"x: {current_x}, y: {current_y}, vx: {current_vx}, vy: {current_vy}, d: {current_x / d}, m: {current_mass}, alt: {h}, t: {t}")
        altitude_arr[t] = h
        # stage: 1 - первая ступень, 2 - вторая ступень, 3 - двигатели не работают
        if h >= 350000.0:
            stage = 2
            cos_alpha = 0
            sin_alpha = 1
            print("stage 2")
        
        if stage == 1:
            if t < 40:
                current_mass = round(current_mass - FLOW_RATE_1, 6)
            else:
                stage = 0
                current_mass = STAGE2_MASS
                current_thrust = 0
        elif stage == 2:
            if V_sq >= g * d:
                stage = 3
            current_mass = round(current_mass - FLOW_RATE_2, 6)
            current_thrust = STAGE2_THRUST
        elif stage == 3:
            current_mass = STAGE3_MASS
            current_thrust = 0

        rocket_mass[t] = current_mass       
        
        if h < 100000:
            Fc = round(0.5 * s * 1.2754 * (V_sq) / 2, 6)
        else: 
            Fc = 0
        Fc_list[t] = Fc

        Ft = round(G * ((M * current_mass) / d_sq), 6)

        delta_vx = round((current_thrust * cos_alpha - Fc * cos_alpha * 0 - Ft * (
                current_x / d)) / current_mass, 6)
        delta_vy = round((current_thrust * sin_alpha - Fc * sin_alpha * 0 - Ft * (
                current_y / d)) / current_mass, 6)
        
        delta_vx_arr[t] = delta_vx
        delta_vy_arr[t] = delta_vy

        current_vx = round(current_vx + delta_vx, 6)
        current_vy = round(current_vy + delta_vy, 6)

        velocity_x[t] = current_vx
        velocity_y[t] = current_vy
        V_sq = current_vx ** 2 + current_vy ** 2
        V = math.sqrt(V_sq)
        velocity[t] = V
        current_x = round(current_x + current_vx + (delta_vx / 2), 6)
        current_y = round(current_y + current_vy + (delta_vy / 2), 6)
        pos_x[t] = current_x
        pos_y[t] = current_y

    # velocity_arr = [math.sqrt(vx ** 2 + vy ** 2) for vx, vy in zip(velocity_x, velocity_y)]
    # print(velocity_arr)

    ksp_alt, ksp_speed, ksp_mass, ksp_dv = open_file()

    fig, mass_total = plt.subplots()
    mass_total.set_title('Изменение массы ракеты')
    mass_total.set_xlabel('Время, секунды')
    mass_total.set_ylabel('Масса, килограммы')
    mass_total.plot(time_arr, rocket_mass)
    mass_total.plot(time_arr, ksp_mass[:T])
    mass_total.grid()

    # fig, friction = plt.subplots()
    # friction.set_title('Изменение силы сопротивления воздуха')
    # friction.set_xlabel('Время, секунды')
    # friction.set_ylabel('Сопротивление, ньютоны')
    # friction.plot(time_arr, Fc_list)
    # friction.grid()

    fig, velocity_cur = plt.subplots()
    velocity_cur.set_title('Изменение скорости')
    velocity_cur.set_ylabel('Скорость, метры в секунду')
    velocity_cur.set_xlabel('Время в секунды')
    velocity_cur.plot(time_arr, velocity)
    velocity_cur.plot(time_arr, ksp_speed[:T])
    velocity_cur.grid()

    fig, velocity_cur = plt.subplots()
    velocity_cur.set_title('Изменение dV')
    velocity_cur.set_ylabel('Скорость, метры в секунду')
    velocity_cur.set_xlabel('Время в секунды')
    velocity_cur.plot(time_arr, delta_vx_arr)
    velocity_cur.plot(time_arr, ksp_dv[:T])
    velocity_cur.grid()

    fig, velocity_cur = plt.subplots()
    velocity_cur.set_title('Изменение высоты')
    velocity_cur.set_ylabel('Высота, метры')
    velocity_cur.set_xlabel('Время в секундах')
    velocity_cur.plot(time_arr, altitude_arr)
    velocity_cur.plot(time_arr, ksp_alt[:T])
    velocity_cur.grid()


if __name__ == '__main__':
    main()
    plt.show()
