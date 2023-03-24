import math


def normalised_deviation(count1: float, count2: float) -> float:
    """Returns the normalized difference between two counts (in number of shocks)"""

    return math.fabs(count1 - count2) / (2 * math.sqrt(count1 + count2))


if __name__ == '__main__':
    print(normalised_deviation(50, 72))
