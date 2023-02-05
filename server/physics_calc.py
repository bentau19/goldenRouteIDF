# const variables
AIR_PLAIN_MASS = 35000
TAKE_OFF_SPEED = 140
ENGINE_FORCE = 100000
MAX_TIME_FOR_MISSION = 60
MAX_MASS = (MAX_TIME_FOR_MISSION * ENGINE_FORCE) / TAKE_OFF_SPEED


def general_calc(load_mass):
    try:
        if load_mass >= 0:
            total_mass = load_mass + AIR_PLAIN_MASS
            acceleration = ENGINE_FORCE / total_mass
            time = take_off_time(acceleration)
            distance = take_off_distance(acceleration, time)
            overweight = overweight_reduce(time, total_mass)
            print(
                f'acceleration: {str(acceleration)}m/sec**2 ,time: {str(time)}sec, distance: {str(distance)}m, need to be reduce in {str(overweight)}KG')
            return time, distance, overweight
        return -9
    except:
        return -9


def take_off_time(acceleration):
    time = TAKE_OFF_SPEED / acceleration
    return time


def take_off_distance(acceleration, time):
    distance = (acceleration * (time ** 2)) / 2
    return distance
    # the distance that the plan pass to takeoff


def overweight_reduce(time, imass):
    if time > 60:
        return imass - MAX_MASS
    return 0
