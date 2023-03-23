import math


def normalised_deviation(shocks1: float, shocks2: float) -> float:
    return math.fabs(shocks1 - shocks2) / (2 * math.sqrt(shocks1 + shocks2))


if __name__ == '__main__':
    print(normalised_deviation(50, 72))
