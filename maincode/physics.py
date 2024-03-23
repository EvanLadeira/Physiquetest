from math import *


def calcul_distance(pos1, pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    d = sqrt(dx**2 + dy**2)
    return {"distance":d, "distance_coord":(dx, dy)}


def propulsion(angle):
    x = -cos(angle)*0.15
    y = -sin(angle)*0.15
    return x, y


def force_grav(pos, data_list):
    sum_force_x = 0
    sum_force_y = 0
    for line in data_list:
        data = line.split(';')
        #distance_x = pos[0]-(int(data[2]))
        #distance_y = pos[1]-(int(data[3]))
        #distance = sqrt(distance_x**2 + distance_y**2)
        distance_data = calcul_distance(pos, (int(data[2]), (int(data[3]))))
        distance_x = distance_data["distance_coord"][0]
        distance_y = distance_data["distance_coord"][1]
        distance = distance_data["distance"]
        vec = [distance_x, distance_y]
        vec[0] /= distance
        vec[1] /= distance
        F = (6.67*10E-11) * (int(data[1])*10E10) / distance**2
        sum_force_x += -vec[0]*F
        sum_force_y += -vec[1]*F
    return sum_force_x, sum_force_y


def movement_vector(thrust_vector = (0, 0), initial_vector: tuple = (0, 0), grav_vector: tuple = (0, 0)):
    x = thrust_vector[0] + initial_vector[0] + grav_vector[0]
    y = thrust_vector[1] + initial_vector[1] + grav_vector[1]
    return x, y
