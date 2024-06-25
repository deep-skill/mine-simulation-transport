import random

class TimeFunction():
    def __init__(self, points):
        self.points = points

    def get_time_by_x(self, x):
        if x == self.points[-1][0]: return self.points[-1][1]

        interval = 0
        for i in range(len(self.points)):
            if self.points[i][0] <= x:
                interval = i

        range_interval_x = self.points[interval + 1][0] - self.points[interval][0]
        range_current_x = x - self.points[interval][0]

        range_interval_y = self.points[interval + 1][1] - self.points[interval][1]

        base = self.points[interval][1]

        return base + range_interval_y * (range_current_x / range_interval_x)

    def get_random_time(self):
        x = random.uniform(self.points[0][0], self.points[-1][0])
        return self.get_time_by_x(x)


def obtain_dict_of_time_functions(fname):
    time_functions_dict = {}

    with open(fname, 'r') as ftiempos:
        lines = ftiempos.readlines()

        # Eliminar espacios al inicio y al final de cada linea
        for i, line in enumerate(lines):
            lines[i] = line.strip()

        # Lineas vacias al final
        while not lines[-1]: lines.pop(-1)

        for line in lines:
            id_function, points = line.split(' ')

            points = points.split('/')

            lst_points = []

            for point in points:
                x, y = point.split(',')
                x = float(x)
                y = float(y)

                lst_points.append((x, y))

            time_functions_dict[id_function] = TimeFunction(lst_points)

    return time_functions_dict

