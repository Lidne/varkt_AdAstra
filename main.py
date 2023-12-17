import math
import matplotlib.pyplot as plt

T = 200  #

rocket_mass = [0] * T
velocity_x = [0] * T
velocity_y = [0] * T
pos_x = [0] * T
pos_y = [0] * T

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

MASS = 37607
STAGE1_MASS = 31660
STAGE2_MASS = 5747
STAGE1_FUEL = 37600 - 15200
STAGE2_FUEL = 5900 - 3100
FLOW_RATE_1 = (48807 - 16400) / 70.9
FLOW_RATE_2 = (7100 - 3100) / 50.66

STAGE1_THRUST = 1283607  # сила тяги первой ступени
STAGE2_THRUST = 240000  # сила тяги второй ступени

def main():
    alpha = 0
    stage = 1
    current_vx = 0
    current_vy = 0
    current_x = 600000
    current_y = 0
    pos_x[0] = current_x
    pos_y[0] = current_y
    velocity_x[0] = current_vx
    velocity_y[0] = current_vy
    current_mass = MASS
    rocket_mass[0] = current_mass
    current_thrust = STAGE1_THRUST
    for t in range(1, T):
        h = round(math.sqrt(current_x ** 2 + current_y ** 2) - R, 6)
        print(f"x: {current_x}, y: {current_y}, vx: {current_vx}, vy: {current_vy}, m: {current_mass}, t: {t}")
        # stage: 1 - первая ступень, 2 - вторая ступень, 3 - двигатели не работают
        if h >= 350000:
            stage = 2
            current_mass = MASS - STAGE1_MASS - STAGE2_MASS
            alpha = pi / 2
        
        if stage == 1:
            if current_mass - FLOW_RATE_1 >= MASS - STAGE1_FUEL:
                current_mass -= FLOW_RATE_1
            else:
                stage = 3
                current_mass = MASS - STAGE1_MASS
                current_thrust = 0
        elif stage == 2:
            if current_mass - FLOW_RATE_2 < MASS - STAGE1_MASS - STAGE2_FUEL:
                current_mass -= FLOW_RATE_2
            if current_vx ** 2 + current_vy ** 2 == g * math.sqrt(current_x ** 2 + current_y ** 2):
                stage = 3
                current_thrust = 0

        rocket_mass[t] = current_mass       
        # TODO исправить ошибку при отрицательном давлении
        p = max(0, p0 * (1 + (L * h / t0)) ** ((-g * m) / (r0 * L)))
        temp = max(t0 + L * h, 0)
        density = (p * m) / (r0 * temp)
        Fc = 0.5 * s * density * (current_vx ** 2 + current_vy ** 2) / 2
        
        Ft = G * ((M * current_mass) / (current_x ** 2 + current_y ** 2))

        delta_vx = round((current_thrust * math.cos(alpha) - Fc * math.cos(alpha) - Ft * (
                current_x / math.sqrt(current_x ** 2 + current_y ** 2))) / current_mass, 6)
        delta_vy = round((current_thrust * math.sin(alpha) - Fc * math.sin(alpha) - Ft * (
                current_y / math.sqrt(current_x ** 2 + current_y ** 2))) / current_mass, 6)

        current_vx = round(current_vx + delta_vx, 6)
        current_vy = round(current_vy + delta_vy, 6)

        velocity_x[t] = current_vx
        velocity_y[t] = current_vy
        current_x = round(current_x + current_vx + (delta_vx / 2), 6)
        current_y = round(current_y + current_vy + (delta_vy / 2), 6)
        pos_x[t] = current_x
        pos_y[t] = current_y

    velocity_arr = [math.sqrt(vx ** 2 + vy ** 2) for vx, vy in zip(velocity_x, velocity_y)]
    # print(velocity_arr)

    fig, mass_total = plt.subplots()
    mass_total.set_title('Изменение массы ракеты')
    mass_total.set_xlabel('Время, секунды')
    mass_total.set_ylabel('Масса, килограммы')
    mass_total.plot(time_arr, rocket_mass)
    mass_total.grid()

    fig, velocity_cur = plt.subplots()
    velocity_cur.set_title('Изменение скорости')
    velocity_cur.set_ylabel('Скорость, метры в секунду')
    velocity_cur.set_xlabel('Время в секунды')
    velocity_cur.plot(time_arr, velocity_arr)
    velocity_cur.grid()


if __name__ == '__main__':
    main()
    plt.show()
