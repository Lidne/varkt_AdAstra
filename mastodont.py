import math
import matplotlib.pyplot as plt
import csv

T = 310  #

rocket_mass = [0] * T
velocity_x = [0] * T
velocity_y = [0] * T
delta_v_arr = [0] * T
delta_vy_arr = [0] * T
velocity = [0] * T
pos_x = [0] * T
pos_y = [0] * T
Fc_list = [0] * T
altitude_arr = [0] * T

time_arr = list(range(1, T + 1))  # массив времени, сек
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

cf = 0.5 * (3.7 / 7.2)

# MASS = 49758
STAGE1_MASS = 49758
STAGE2_MASS = 7458
STAGE3_MASS = 551
FLOW_RATE_1 = (49758 - 21677) / 59
FLOW_RATE_2 = (7458 - 4114) / 91

# STAGE1_THRUST = 1350000  # сила тяги первой ступени
# STAGE2_THRUST = 200000  # сила тяги второй ступени


def open_file():
    with open("/Users/bebebe/Desktop/varkt_AdAstra/data/Mastodont_real.txt", encoding='utf-8') as f:
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


def main():
    cos_alpha = 1
    sin_alpha = 0
    ksp_alt, ksp_speed, ksp_mass, ksp_dv, ksp_thrust, ksp_friction = open_file()
    current_vx = 0
    current_vy = 0
    V = 0
    stage = 1
    V_sq = 0
    current_x = 600000
    current_y = 0
    pos_x[0] = current_x
    pos_y[0] = current_y
    velocity_x[0] = current_vx
    velocity_y[0] = current_vy
    delta_v_arr[0] = 0
    delta_vy_arr[0] = 0
    velocity[0] = V
    current_mass = STAGE1_MASS
    rocket_mass[0] = current_mass
    current_thrust = ksp_thrust[0]

    for t in range(1, T):
        d_sq = current_x ** 2 + current_y ** 2
        d = math.sqrt(d_sq)
        h = round(d - R, 6)
        altitude_arr[t] = h
        # stage: 1 - первая ступень, 2 - вторая ступень, 3 - двигатели не работают
        # по времени подгоняй
        if t < 59:
            current_mass = round(current_mass - FLOW_RATE_1, 6)
        elif stage != 2:
            stage = 2
            current_mass = STAGE2_MASS

        if t >= 238 and stage == 2:
            current_mass = round(current_mass - FLOW_RATE_2, 6)
            cos_alpha = 0
            sin_alpha = -1
            # print("stage 2")
            # current_thrust = STAGE2_THRUST

        current_thrust = ksp_thrust[t]
        rocket_mass[t] = current_mass       

        # рассчет сопротивления воздуха (игнорируй)
        # if h <= 11000:
        #     # temp = max(t0 + L * h, 0)
        #     p = p0 * math.exp((-g * m * h) / (r0 * t0))
        #     density = (p * m) / (r0 * t0)
        #     Fc = density * V_sq * cf * s / 2
        # else:
        #     Fc = 0

        # Fc_list[t] = Fc

        Ft = round(G * ((M * current_mass) / d_sq), 6)

        # рассчет изменения скорости за секунду
        delta_vx = round((current_thrust * cos_alpha - ksp_friction[t] * cos_alpha - Ft * (
                current_x / d)) / current_mass, 6)
        delta_vy = round((current_thrust * sin_alpha - ksp_friction[t] * sin_alpha - Ft * (
                current_y / d)) / current_mass, 6)
        
        sign_vx = 1 if delta_vx >= 0 else -1
        sign_vy = 1 if delta_vy >= 0 else -1
        delta_v_arr[t] = sign_vx * sign_vy * math.sqrt(((delta_vx ** 2 + delta_vy ** 2)))  # запись в массив ускорения

        # обновление скорости
        current_vx = round(current_vx + delta_vx, 6) 
        current_vy = round(current_vy + delta_vy, 6)

        # запись в массив скоростей по х и у
        velocity_x[t] = current_vx
        velocity_y[t] = current_vy
        # общая скорость
        V_sq = current_vx ** 2 + current_vy ** 2
        V = math.sqrt(V_sq)
        velocity[t] = V

        # координаты
        current_x = round(current_x + current_vx + (delta_vx / 2), 6)
        current_y = round(current_y + current_vy + (delta_vy / 2), 6)
        pos_x[t] = current_x
        pos_y[t] = current_y

        print(f"x: {current_x}, y: {current_y}, vx: {current_vx}, vy: {current_vy}, d: {current_x / d}, m: {current_mass}, alt: {h}, Fc_ksp: {ksp_friction[t]}, t: {t}")

    # ksp - red
    # model - blue

    # масса (в отчет)
    fig, mass_total = plt.subplots()
    mass_total.set_title('Изменение массы ракеты')
    mass_total.set_xlabel('Время, секунды')
    mass_total.set_ylabel('Масса, килограммы')
    mass_total.plot(time_arr, rocket_mass, color="blue")
    mass_total.plot(time_arr, ksp_mass[:T], color="red")
    mass_total.grid()

    # сопротивление (для дебага)
    fig, friction = plt.subplots()
    friction.set_title('Изменение силы сопротивления воздуха')
    friction.set_xlabel('Время, секунды')
    friction.set_ylabel('Сопротивление, ньютоны')
    friction.plot(time_arr, Fc_list, color="blue")
    friction.plot(time_arr, ksp_friction[:T], color="red")
    friction.grid()

    # скорость (в отчет)
    fig, velocity_cur = plt.subplots()
    velocity_cur.set_title('Изменение скорости')
    velocity_cur.set_ylabel('Скорость, метры в секунду')
    velocity_cur.set_xlabel('Время в секунды')
    velocity_cur.plot(time_arr, velocity, color="blue")
    velocity_cur.plot(time_arr, ksp_speed[:T], color="red")
    velocity_cur.grid()

    # ускорение (для дебага)
    fig, velocity_cur = plt.subplots()
    velocity_cur.set_title('Изменение ускорения')
    velocity_cur.set_ylabel('Ускорение, метры в секунду')
    velocity_cur.set_xlabel('Время в секунды')
    velocity_cur.plot(time_arr, delta_v_arr, color="blue")
    velocity_cur.plot(time_arr, ksp_dv[:T], color="red")
    velocity_cur.grid()

    # силя тяги (для дебага)
    fig, thrust = plt.subplots()
    thrust.set_title('Изменение силы тяги')
    thrust.set_ylabel('Сила тяги, Кн')
    thrust.set_xlabel('Время, с')
    thrust.plot(time_arr, ksp_thrust[:T], color="red")
    thrust.grid()

    # высота (в отчет)
    fig, velocity_cur = plt.subplots()
    velocity_cur.set_title('Изменение высоты')
    velocity_cur.set_ylabel('Высота, метры')
    velocity_cur.set_xlabel('Время в секундах')
    velocity_cur.plot(time_arr, altitude_arr, color="blue")
    velocity_cur.plot(time_arr, ksp_alt[:T], color="red")
    velocity_cur.grid()


if __name__ == '__main__':
    main()
    plt.show()
