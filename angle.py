"""Calculating vector's angle w.r.t. given axis"""

import argparse
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument('-c', '--coordinate', nargs='*', default=[-2.978715e-01, 9.506773e-01,8.641501e-02])
parser.add_argument('-a', '--axis', type=int,
                    help="axis index of the angle you want to calculate, beginning at `0`",
                    default=2)

parse = parser.parse_args()


def main(coordinate=parse.coordinate, axis=parse.axis, module=False):
    """Calculating vector's angle w.r.t. given axis

    :param coordinate:
    :param axis: Axis index of the angle you want to calculate, beginning at `0`
    :param module: `True` if using for other program
    :return: Angle (Union: degree)
    """

    if len(coordinate) != 3:
        return None

    sum = 0

    for coor in coordinate:
       sum += float(coor) ** 2

    angle = np.arccos(float(coordinate[axis]) / (sum ** 0.5))

    if not module:
        print(angle * 180 / np.pi)
    else:
        return angle * 180 / np.pi


if __name__ == '__main__':
    main()
