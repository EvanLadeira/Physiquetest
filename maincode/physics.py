from math import *


def thrust_vector(angle):
    x = -cos(angle)*0.15
    y = -sin(angle)*0.15
    return x, y

def grav_vector(distance: tuple, M_planet: int) -> tuple:
    d = sqrt(distance[0]**2+distance[1]**2)
    if d != 0:
        G = -6.67*10E-11
        F_grav = -G*(M_planet*1)/(d**2)
        angle = asin(distance[1]/d)
        print(angle)
        x = cos(angle)*F_grav
        y = sin(angle)*F_grav
        return x, y
    else:
        return(0, 0)

def force_grav(pos_spacecraft, data_list):
    sum_force_x = 0
    sum_force_y = 0
    for line in data_list:
        data = line.split(';')
        distance_x = pos_spacecraft[0]-int(data[2])
        distance_y = pos_spacecraft[1]-int(data[3])
        distance = sqrt(distance_x**2 + distance_y**2)
        vec = [distance_x, distance_y]
        vec[0]/=distance
        vec[1]/=distance
        F= (6.67*10E-11) * (int(data[1])*10E10) / distance**2
        sum_force_x += -vec[0]*F
        sum_force_y += -vec[1]*F
    print(sum_force_x, sum_force_y)
    return sum_force_x, sum_force_y


def movement_vector(thrust_vector: tuple, initial_vector: tuple, grav_vector: tuple = (0, 0)):
    x = thrust_vector[0] + initial_vector[0] + grav_vector[0]
    y = thrust_vector[1] + initial_vector[1] + grav_vector[1]
    return x, y

initial_vector = (0, 0)
vector1 = movement_vector(thrust_vector(3.14), initial_vector)
print("vector1 : ", vector1)


