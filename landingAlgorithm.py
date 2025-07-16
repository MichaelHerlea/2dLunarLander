import math

def landing_algorithm(modulus, velocity):
    angle = math.acos(velocity[0]/modulus)

    if modulus < 100:
        throttle = 1
    else:
        throttle = 3
    
    return (angle, throttle)