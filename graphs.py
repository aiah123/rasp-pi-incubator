import math

import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

TEMP_INDEX = 0
DATE_INDEX = 1
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

start_time = '2018-08-08 22:00:01.696912'
end_time = '2018-08-09 07:38:01.696912'

fname = 'temp.log'


def graph_temperatures():
    dates, temps = get_data()
    temps = [np.float(x) for x in temps]
    dates_to_floats = [np.float(x) for x in range(len(dates))]
    fitted_polynom, derivative = lousy_derivative(dates_to_floats, temps)

    plt.plot(dates_to_floats, temps, '.-', c='b')
    #plt.plot(dates_to_floats,fitted_polynom, c='xkcd:sky blue')
    # plt.plot(derivative, c='y')
    # plt.axhline(36.1)
    # plt.axhline(35.9, c="r")
    plt.show()


def get_data():
    with open(fname) as file:
        lines = [line.strip() for line in file]
    # create an array with <temperature, date> columns.
    data = np.array([[float(x.split(maxsplit=1)[TEMP_INDEX][:-1]), x.split(maxsplit=1)[1]] for x in lines])
    temps = data[:, 0]
    dates = np.array([datetime.strptime(x, TIMESTAMP_FORMAT) for x in data[:, 1]])
    formatted_start_date = datetime.strptime(end_time, TIMESTAMP_FORMAT)
    formatter_end_date = datetime.strptime(start_time, TIMESTAMP_FORMAT)
    dates_in_range = (dates < formatted_start_date) & (dates >= formatter_end_date)
    temps = temps[dates_in_range]
    dates = dates[dates_in_range]
    return dates, temps


def calc_polynom_value(coefficients, x):
    out = []
    for index, coefficient in enumerate(coefficients):
        val = coefficient * math.pow(x, index)
        out.append(val)
    return sum(out)
    #return sum([coefficient * math.pow(x, index) for index, coefficient in enumerate(coefficients)])


def calc_polynom_derivative_value(coefficients, x):
    return sum([index * coefficient * math.pow(x, max(0,index-1)) for index, coefficient in enumerate(coefficients)])


def lousy_derivative(x, y):
    coefficients = np.polyfit(x, y, 3)
    fitted_polynom = [calc_polynom_value(coefficients, x_val) for x_val in x]
    derivatives = [calc_polynom_derivative_value(coefficients, x_val) for x_val in x]
    return fitted_polynom, derivatives


graph_temperatures()
