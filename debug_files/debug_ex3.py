import math


def periodicity(x):
    if 0 <= x <= 360:
        return x
    else:
        return x % 360


def symmetry(x):
    if 0 <= x <= 90:
        return 1, x
    elif 90 < x <= 180:
        return 1, 180 - x
    elif 180 < x <= 270:
        return -1, x - 180
    elif 270 < x <= 360:
        return -1, 360 - x
    else:
        raise ValueError("Should not have reached here")


def cofunction(x):
    if x < 45:
        return sin_poly(x)
    else:
        opp_x = 90 - x
        cos = cos_poly(opp_x)
        return cos


def sin_poly(x):
    x_rad = x * math.pi / 180
    sin = x_rad - (x_rad**3) / 6 + (x_rad**5) / 120
    return sin


def cos_poly(x):
    x_rad = x * math.pi / 180
    cos = 1 - (x_rad**2) / 2 + (x_rad**4) / 24 - (x**6) / 720
    return cos


def calc_sin(x):
    x = periodicity(x)
    sign, x = symmetry(x)
    sin = sign * cofunction(x)
    return sin


if __name__ == '__main__':
    x = 60
    print(math.sin(x * math.pi / 180))
    print(calc_sin(x))

